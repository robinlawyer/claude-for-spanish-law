#!/usr/bin/env python3
"""Cambia la versión del plugin en TODOS los sitios a la vez (Juan, 13-nov-2026, «Re: Plugin Robin
en Claude…»: mandar la versión desde las skills, sin que se desfase).

    python3 scripts/version.py 2.5.6

- robin/.claude-plugin/plugin.json → "version".
- Cada disparador robin/skills/*/SKILL.md → `version_plugin: "X.Y.Z"` en la llamada a
  `obtener_skill`. El servidor la apunta (sabe quién va atrasado) y, si va atrasada, devuelve el
  aviso como dato. NO toca robin/.mcp.json: una cabecera o una dirección que cambien con la
  versión obligan a cada cliente a volver a conectar Robin (prueba en Cowork, 26-oct-2026).

scripts/validate.py falla si alguna skill lleva otra versión que plugin.json.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PLUGIN = RAIZ / "robin" / ".claude-plugin" / "plugin.json"
SKILLS = RAIZ / "robin" / "skills"
RE_VERSION = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}$")
# `nombre: "slug"`  [y `version_plugin: "X.Y.Z"`]
RE_LLAMADA = re.compile(r'(con `nombre: "[a-z0-9-]+"`)(?: y `version_plugin: "[^"]*"`)?')


def poner(version: str) -> int:
    """Con el BLOQUEO tomado desde antes de leer nada hasta terminar de escribir (revisión de
    Codex, 4.ª vuelta): dos ejecuciones a la vez no pueden mezclarse."""
    import fcntl

    with open(RAIZ / "scripts" / ".version.lock", "w") as cerrojo:
        try:
            fcntl.flock(cerrojo, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise SystemExit("Hay otra ejecución de version.py en marcha: no se ha cambiado nada.")
        return _poner(version)


def _poner(version: str) -> int:
    """Calcula TODOS los cambios y los comprueba antes de escribir nada: o se cambia todo o
    no se cambia nada (revisión de Codex, 16-nov-2026)."""
    if not RE_VERSION.match(version):
        raise SystemExit(f"versión no válida: {version!r} (X.Y.Z)")
    cambios: dict[Path, str] = {}
    texto = PLUGIN.read_text(encoding="utf-8")
    nuevo, n = re.subn(r'("version"\s*:\s*")[^"]*(")', rf"\g<1>{version}\g<2>", texto, count=1)
    if n != 1:
        raise SystemExit("plugin.json sin campo version")
    json.loads(nuevo)
    cambios[PLUGIN] = nuevo
    errores = []
    for md in sorted(SKILLS.glob("*/SKILL.md")):
        t = md.read_text(encoding="utf-8")
        t2, k = RE_LLAMADA.subn(rf'\g<1> y `version_plugin: "{version}"`', t)
        if k != 1:
            errores.append(f"{md.relative_to(RAIZ)}: {k} llamadas a obtener_skill reconocidas (tiene que haber una)")
            continue
        # Ni restos de una versión anterior con otra redacción ni el parámetro duplicado.
        if t2.count("version_plugin") != 1 or t2.count(f'`version_plugin: "{version}"`') != 1:
            errores.append(f"{md.relative_to(RAIZ)}: version_plugin aparece fuera de la llamada reconocida")
            continue
        cambios[md] = t2
    if errores:
        raise SystemExit("No se ha cambiado nada:\n  " + "\n  ".join(errores))
    pendientes = {r: t for r, t in cambios.items() if r.read_text(encoding="utf-8") != t}
    escribir_todo(pendientes)
    print(f"plugin {version}: {len(pendientes)} ficheros cambiados ({len(cambios) - 1} disparadores revisados)")
    return 0


def escribir_todo(pendientes: dict[Path, str]) -> None:
    """Todo o nada (revisión de Codex, 3 vueltas):
    - el BLOQUEO exclusivo (scripts/.version.lock) lo toma poner() antes de leer nada;
    - temporales de nombre ÚNICO junto a cada fichero; si falla uno, no se ha tocado nada;
    - COPIA EN DISCO de cada original (en .version-copia/) antes de sustituir nada;
    - cada sustitución es atómica (os.replace); si una falla, se restauran TODOS los ya
      sustituidos, aunque falle alguno, y se dice cuáles quedan pendientes. Las copias solo se
      borran si todo ha ido bien: con ellas se recupera a mano si el proceso muere a mitad
      (validate.py lo detecta)."""
    import os
    import shutil
    import uuid

    if not pendientes:
        return
    marca = uuid.uuid4().hex[:12]
    copia_dir = RAIZ / ".version-copia" / marca
    if True:  # el bloqueo lo tiene poner() desde antes de leer
        for r in pendientes:
            if not r.exists():
                raise SystemExit(f"No se ha cambiado nada: {r.relative_to(RAIZ)} ha desaparecido.")
        copias: dict[Path, Path] = {}
        temporales: dict[Path, Path] = {}
        try:
            for r, t in pendientes.items():
                c = copia_dir / r.relative_to(RAIZ)
                c.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(r, c)
                copias[r] = c
                tmp = r.with_name(f"{r.name}.{marca}.tmp")
                tmp.write_text(t, encoding="utf-8")
                temporales[r] = tmp
        except Exception:
            for tmp in temporales.values():
                tmp.unlink(missing_ok=True)
            shutil.rmtree(copia_dir, ignore_errors=True)
            raise
        hechos: list[Path] = []
        try:
            for r, tmp in temporales.items():
                os.replace(tmp, r)
                hechos.append(r)
        except Exception as e:
            sin_restaurar = []
            for r in hechos:
                try:
                    vuelta = r.with_name(f"{r.name}.{marca}.vuelta")
                    shutil.copy2(copias[r], vuelta)
                    os.replace(vuelta, r)
                except Exception:  # noqa: BLE001
                    sin_restaurar.append(str(r.relative_to(RAIZ)))
                    try:
                        vuelta.unlink(missing_ok=True)
                    except Exception:  # noqa: BLE001
                        sin_restaurar.append(f"(quedó {vuelta.relative_to(RAIZ)})")
            for tmp in temporales.values():
                try:
                    tmp.unlink(missing_ok=True)
                except Exception:  # noqa: BLE001
                    pass
            if sin_restaurar:
                raise SystemExit(
                    f"Falló una escritura ({e}) y NO se han podido restaurar: {', '.join(sin_restaurar)}. "
                    f"Los originales están en {copia_dir.relative_to(RAIZ)}/.")
            shutil.rmtree(copia_dir, ignore_errors=True)
            raise SystemExit(f"No se ha cambiado nada: falló una escritura ({e}) y se han restaurado los originales.")
        shutil.rmtree(copia_dir, ignore_errors=True)
        try:
            (RAIZ / ".version-copia").rmdir()
        except OSError:
            pass


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    sys.exit(poner(sys.argv[1]))
