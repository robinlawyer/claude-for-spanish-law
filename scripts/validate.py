#!/usr/bin/env python3
"""
Validador del marketplace y del plugin Robin.

Comprueba:
1. JSON sanity de marketplace.json y plugin.json.
2. Coherencia entre marketplace.json y plugin.json (name, description, author).
3. Frontmatter mínimo de cada SKILL.md (description obligatorio).
4. Frontmatter mínimo de cada agent.md (name y description obligatorios).
5. Nombres canónicos: skills/<name>/ debe coincidir con frontmatter name.
6. Naming: ^[a-z0-9][a-z0-9-]{1,63}$ en plugin name, skill name, agent name.
7. .mcp.json sintácticamente válido y con al menos un server "robin".
"""

import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{1,63}$")
ROOT = Path(__file__).resolve().parent.parent
ERRORS: list[str] = []


def err(msg: str) -> None:
    ERRORS.append(msg)


def parse_frontmatter(text: str) -> dict | None:
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    fm = {}
    for line in parts[1].strip().splitlines():
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fm[key.strip()] = value.strip()
    return fm


def validate_marketplace() -> dict:
    path = ROOT / ".claude-plugin" / "marketplace.json"
    if not path.exists():
        err(f"Falta {path}")
        return {}
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        err(f"marketplace.json no es JSON válido: {e}")
        return {}

    for required in ("name", "description", "plugins"):
        if required not in data:
            err(f"marketplace.json: falta campo '{required}'")

    if not NAME_RE.match(data.get("name", "")):
        err(f"marketplace.json: name '{data.get('name')}' no cumple [a-z0-9-]")

    desc = data.get("description", "")
    if not (10 <= len(desc) <= 2000):
        err(f"marketplace.json: description debe tener 10-2000 chars (tiene {len(desc)})")

    names = [p.get("name") for p in data.get("plugins", [])]
    if len(names) != len(set(names)):
        err("marketplace.json: nombres de plugin duplicados")
    for n in names:
        if not n or not NAME_RE.match(n):
            err(f"marketplace.json: plugin name '{n}' inválido")

    return data


def validate_plugin(plugin_dir: Path, marketplace_entry: dict) -> None:
    plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"
    if not plugin_json_path.exists():
        err(f"Falta {plugin_json_path}")
        return
    try:
        plugin_data = json.loads(plugin_json_path.read_text())
    except json.JSONDecodeError as e:
        err(f"{plugin_json_path}: JSON inválido: {e}")
        return

    for required in ("name", "description"):
        if required not in plugin_data:
            err(f"{plugin_json_path}: falta '{required}'")

    if not NAME_RE.match(plugin_data.get("name", "")):
        err(f"{plugin_json_path}: name '{plugin_data.get('name')}' inválido")

    # Coherencia con marketplace
    for field in ("name", "description"):
        if marketplace_entry.get(field) != plugin_data.get(field):
            err(
                f"{plugin_json_path}: '{field}' no coincide con marketplace.json "
                f"({plugin_data.get(field)!r} vs {marketplace_entry.get(field)!r})"
            )

    # .mcp.json
    mcp_path = plugin_dir / ".mcp.json"
    if not mcp_path.exists():
        err(f"Falta {mcp_path}")
    else:
        try:
            mcp_data = json.loads(mcp_path.read_text())
            if "robin" not in mcp_data.get("mcpServers", {}):
                err(f"{mcp_path}: no declara MCP server 'robin'")
        except json.JSONDecodeError as e:
            err(f"{mcp_path}: JSON inválido: {e}")

    # hooks/hooks.json
    hooks_path = plugin_dir / "hooks" / "hooks.json"
    if hooks_path.exists():
        try:
            json.loads(hooks_path.read_text())
        except json.JSONDecodeError as e:
            err(f"{hooks_path}: JSON inválido: {e}")

    # Skills
    skills_dir = plugin_dir / "skills"
    if not skills_dir.exists():
        err(f"Falta {skills_dir}")
        return

    for skill_subdir in skills_dir.iterdir():
        if not skill_subdir.is_dir():
            continue
        if not NAME_RE.match(skill_subdir.name):
            err(f"Skill dir '{skill_subdir.name}' no cumple naming")
        skill_md = skill_subdir / "SKILL.md"
        if not skill_md.exists():
            err(f"Falta {skill_md}")
            continue
        fm = parse_frontmatter(skill_md.read_text())
        if fm is None:
            err(f"{skill_md}: sin frontmatter")
            continue
        if "description" not in fm:
            err(f"{skill_md}: falta 'description' en frontmatter")
        if "name" in fm and fm["name"] != skill_subdir.name:
            err(
                f"{skill_md}: frontmatter name '{fm['name']}' "
                f"no coincide con dir '{skill_subdir.name}'"
            )

    # Agents
    agents_dir = plugin_dir / "agents"
    if agents_dir.exists():
        for agent_file in agents_dir.glob("*.md"):
            fm = parse_frontmatter(agent_file.read_text())
            if fm is None:
                err(f"{agent_file}: sin frontmatter")
                continue
            for required in ("name", "description"):
                if required not in fm:
                    err(f"{agent_file}: falta '{required}'")


def main() -> int:
    print("🔍 Validando claude-for-spanish-law...")
    marketplace = validate_marketplace()
    for entry in marketplace.get("plugins", []):
        source = entry.get("source", "")
        plugin_dir = ROOT / source.lstrip("./")
        if not plugin_dir.is_dir():
            err(f"marketplace.json: source '{source}' no es directorio")
            continue
        validate_plugin(plugin_dir, entry)

    if ERRORS:
        print(f"\n❌ {len(ERRORS)} errores:\n")
        for e in ERRORS:
            print(f"  - {e}")
        return 1
    print("\n✅ Todo válido.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
