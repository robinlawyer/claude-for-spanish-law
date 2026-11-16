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
    if not RE_VERSION.match(version):
        raise SystemExit(f"versión no válida: {version!r} (X.Y.Z)")
    texto = PLUGIN.read_text(encoding="utf-8")
    nuevo, n = re.subn(r'("version"\s*:\s*")[^"]*(")', rf"\g<1>{version}\g<2>", texto, count=1)
    if n != 1:
        raise SystemExit("plugin.json sin campo version")
    PLUGIN.write_text(nuevo, encoding="utf-8")
    cambiadas = 0
    for md in sorted(SKILLS.glob("*/SKILL.md")):
        t = md.read_text(encoding="utf-8")
        t2, k = RE_LLAMADA.subn(rf'\g<1> y `version_plugin: "{version}"`', t)
        if k != 1:
            raise SystemExit(f"{md.relative_to(RAIZ)}: {k} llamadas a obtener_skill reconocidas (tiene que haber una)")
        if t2 != t:
            md.write_text(t2, encoding="utf-8")
            cambiadas += 1
    json.loads(PLUGIN.read_text(encoding="utf-8"))
    print(f"plugin {version}: plugin.json y {cambiadas} disparadores")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    sys.exit(poner(sys.argv[1]))
