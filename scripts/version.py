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
    """Todo o nada (revisión de Codex): primero se escriben TODOS los temporales (si falla uno,
    no se ha tocado ningún fichero); luego cada uno sustituye a su original de forma atómica
    (os.replace) y, si una sustitución falla, se restauran los originales ya sustituidos. Si el
    proceso muere a mitad, validate.py lo detecta y volver a lanzar este script lo completa."""
    import os

    originales = {r: r.read_bytes() for r in pendientes}
    temporales: dict[Path, Path] = {}
    try:
        for r, t in pendientes.items():
            tmp = r.with_name(r.name + ".version-tmp")
            tmp.write_text(t, encoding="utf-8")
            temporales[r] = tmp
    except Exception:
        for tmp in temporales.values():
            tmp.unlink(missing_ok=True)
        raise
    hechos: list[Path] = []
    try:
        for r, tmp in temporales.items():
            os.replace(tmp, r)
            hechos.append(r)
    except Exception:
        for r in hechos:
            vuelta = r.with_name(r.name + ".version-tmp")
            vuelta.write_bytes(originales[r])
            os.replace(vuelta, r)
        for tmp in temporales.values():
            tmp.unlink(missing_ok=True)
        raise SystemExit("No se ha cambiado nada: falló una escritura y se han restaurado los originales.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    sys.exit(poner(sys.argv[1]))
