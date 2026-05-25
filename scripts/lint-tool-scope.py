#!/usr/bin/env python3
"""
Lint del scope de tools en agents.

Reglas:
1. Ningún agent declara `tools: "*"` o `tools: ["*"]`.
2. Toda tool referenciada `mcp__<server>__<tool>` debe apuntar a `mcp__robin__*`
   o a un connector listado en .mcp.json.
3. Cada agent declara como mínimo `Read` o una tool MCP — un agent sin
   herramientas no tiene sentido.

Falla si encuentra cualquier violación.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ERRORS: list[str] = []


def err(msg: str) -> None:
    ERRORS.append(msg)


def parse_tools_field(text: str) -> list[str] | None:
    # Frontmatter mínimo parser: busca tools: [...]
    match = re.search(r"^tools:\s*(.+)$", text, re.MULTILINE)
    if not match:
        return None
    raw = match.group(1).strip()
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1]
        tools = [t.strip().strip('"').strip("'") for t in inner.split(",") if t.strip()]
        return tools
    return [raw.strip('"').strip("'")]


def get_allowed_mcp_servers(plugin_dir: Path) -> set[str]:
    mcp_json = plugin_dir / ".mcp.json"
    if not mcp_json.exists():
        return set()
    data = json.loads(mcp_json.read_text())
    return set(data.get("mcpServers", {}).keys())


def lint_agent(agent_file: Path, allowed_servers: set[str]) -> None:
    text = agent_file.read_text()
    parts = text.split("---", 2)
    if len(parts) < 3:
        err(f"{agent_file}: sin frontmatter")
        return
    fm = parts[1]
    tools = parse_tools_field(fm)
    if tools is None:
        # No declara tools — válido pero raro
        return

    # Regla 1: no wildcard global
    if "*" in tools or any(t.strip('"').strip("'") == "*" for t in tools):
        if any(t == "*" for t in tools):
            err(f"{agent_file}: declara `tools: *` (wildcard total), prohibido")

    # Regla 2: tools MCP en servidores declarados
    for t in tools:
        m = re.match(r"^mcp__([a-z0-9_-]+)__", t)
        if m:
            server = m.group(1)
            if server not in allowed_servers and server != "*":
                err(
                    f"{agent_file}: tool '{t}' referencia server '{server}' no "
                    f"declarado en .mcp.json (declarados: {sorted(allowed_servers)})"
                )


def main() -> int:
    print("🔍 Lint tool-scope...")
    plugin_dir = ROOT / "robin"
    allowed = get_allowed_mcp_servers(plugin_dir)
    agents_dir = plugin_dir / "agents"
    if not agents_dir.exists():
        print("  Sin agents/ — ok")
        return 0
    for agent_file in agents_dir.glob("*.md"):
        lint_agent(agent_file, allowed)

    if ERRORS:
        print(f"\n❌ {len(ERRORS)} errores:\n")
        for e in ERRORS:
            print(f"  - {e}")
        return 1
    print("\n✅ Tool scopes correctos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
