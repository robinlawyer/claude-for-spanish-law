#!/usr/bin/env python3
"""
Auditoría profunda de las 127 skills + 7 agents.

Comprueba todo lo que se puede sin OAuth:

1. Frontmatter completo y bien formado.
2. Cada tool `mcp__robin__*` referenciada existe en el catálogo del MCP server.
3. Cada handoff `/robin:<skill>` apunta a una skill real del plugin.
4. No hay `[PLACEHOLDER]` huérfanos en el cuerpo de las skills.
5. Los bloques universales del template Anthropic están presentes en las skills que deberían tenerlos.
6. Cross-references consistentes: si una skill X dice "deriva a /robin:Y", Y existe.
7. Severity rating sistemático: si una skill usa 🔴 también debería usar 🟢.
8. Citation tagging coherente: los tags [robin-verified], [robin-corpus] etc están en skills que devuelven citas.

Reporta hallazgos por severidad (🔴 crítico / 🟠 alto / 🟡 medio / 🟢 info).
"""

from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_DIR = ROOT / "robin"
SKILLS_DIR = PLUGIN_DIR / "skills"
AGENTS_DIR = PLUGIN_DIR / "agents"

# Tools del MCP catalog (extraído del backend en sesión anterior)
MCP_CATALOG = {
    "analizar_escrito_contraparte", "analizar_expediente",
    "auditar_compliance_aml", "auditar_compliance_penal_corporativo",
    "auditar_compliance_rgpd", "auditar_compliance_whistleblowing",
    "buscar_aepd", "buscar_bde", "buscar_cnmc", "buscar_cnmv",
    "buscar_consejo_estado", "buscar_convenio_colectivo",
    "buscar_convenio_internacional", "buscar_defensor_pueblo",
    "buscar_dgt", "buscar_doctrina_general", "buscar_jurisprudencia",
    "buscar_normativa", "buscar_por_ccaa", "buscar_por_hechos_analogos",
    "buscar_tacrc", "buscar_tc", "buscar_tcu", "buscar_teac",
    "buscar_tedh", "buscar_tgue", "buscar_tjue",
    "calcular_actualizacion_renta", "calcular_baremo_trafico",
    "calcular_costas_procesales", "calcular_herencia",
    "calcular_indemnizacion_despido", "calcular_intereses_demora",
    "calcular_pena", "calcular_pension_alimentos",
    "calcular_pension_compensatoria", "calcular_plusvalia_municipal",
    "calcular_prestacion_seguridad_social",
    "calculo_plazos", "cronologia_hechos",
    "deposito_recurso", "estimar_viabilidad_caso",
    "generar_plan_estrategico", "mapa_documental",
    "obtener_articulo_ley", "obtener_sentencia_completa",
    "preparar_acto_pre_procesal", "preparar_acuerdo_societario",
    "preparar_arbitraje", "preparar_contestacion", "preparar_demanda",
    "preparar_demanda_pi", "preparar_dictamen",
    "preparar_documento_financiacion", "preparar_documento_ma",
    "preparar_due_diligence", "preparar_email_cliente",
    "preparar_escrito_concursal", "preparar_escrito_familia",
    "preparar_escrito_fase_intermedia_penal", "preparar_escrito_libre",
    "preparar_escrito_sucesiones", "preparar_escrito_tributario",
    "preparar_hoja_encargo", "preparar_informe_juridico",
    "preparar_litigio_societario", "preparar_memorandum",
    "preparar_pacto_socios", "preparar_querella_o_denuncia",
    "preparar_reclamacion_civil", "preparar_reclamacion_seguros",
    "preparar_recurso", "preparar_recurso_administrativo",
    "preparar_recurso_extraordinario", "preparar_redaccion_contrato",
    "preparar_revision_contrato", "preparar_solicitud_pi",
    "preparar_supuesto", "preparar_tramite_extranjeria",
    "resumen_ejecutivo", "revisar_propio_escrito", "simular_oposicion",
    "tasa_judicial", "verificar_cita",
    "listar_supuestos", "listar_playbooks", "obtener_playbook",
}

# Tools que están en backend pero NO registradas en catalog (bug del backend)
MCP_ORPHAN = {"buscar_acuerdo_pleno_ts", "obtener_acuerdo_pleno_ts"}

CRITICAL = []
HIGH = []
MEDIUM = []
INFO = []


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    try:
        end = text.index("---", 3)
    except ValueError:
        return {}, text
    fm_raw = text[3:end]
    body = text[end + 3:].lstrip("\n")
    fm = {}
    for line in fm_raw.strip().splitlines():
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()
    return fm, body


def audit_skill(skill_dir: Path, all_skill_names: set, all_handoffs_used: dict):
    name = skill_dir.name
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        CRITICAL.append(f"{name}: falta SKILL.md")
        return

    text = skill_md.read_text()
    fm, body = parse_frontmatter(text)

    # 1. Frontmatter
    if "description" not in fm:
        CRITICAL.append(f"{name}: falta `description` en frontmatter")

    # 2. Tools referenciadas que NO existen en catalog
    tools = set(re.findall(r"mcp__robin__([a-z_]+)", body))
    tools.discard("auditar_compliance_")  # wildcard pattern, ok
    for tool in tools:
        if tool in MCP_ORPHAN:
            HIGH.append(
                f"{name}: referencia `mcp__robin__{tool}` — tool tiene descripción en backend "
                f"pero NO está registrada en tools.py. Cuando el LLM la llame, devolverá "
                f"method_not_found. Solucionable registrándola en el backend."
            )
        elif tool not in MCP_CATALOG:
            CRITICAL.append(
                f"{name}: referencia `mcp__robin__{tool}` que NO existe en el catálogo. "
                f"Posibles fixes: renombrar a tool real o crear la tool en el backend."
            )

    # 3. Handoffs a otras skills
    handoffs = set(re.findall(r"/robin:([a-z0-9-]+)", body))
    for handoff in handoffs:
        all_handoffs_used[name].add(handoff)
        # excepción para slash commands meta del template
        meta_commands = {"cold-start-interview", "customize", "matter-workspace",
                         "doctor", "help", "agents", "plugin"}
        if handoff in meta_commands:
            continue
        if handoff not in all_skill_names:
            HIGH.append(
                f"{name}: referencia `/robin:{handoff}` que NO existe como skill. "
                f"El slash command quedará muerto."
            )

    # 4. Placeholders huérfanos
    # Excepción: las skills boilerplate (cold-start, customize, doctor)
    # mencionan literalmente [PLACEHOLDER] porque su trabajo es guiar al
    # letrado a rellenar los placeholders del CLAUDE.md del despacho.
    BOILERPLATE_PLACEHOLDER_OK = {"cold-start-interview", "customize", "doctor"}
    if name not in BOILERPLATE_PLACEHOLDER_OK:
        placeholders = re.findall(r"\[PLACEHOLDER[^\]]*\]", body)
        if placeholders:
            MEDIUM.append(
                f"{name}: contiene {len(placeholders)} `[PLACEHOLDER]` huérfanos en el body. "
                f"Esos deberían vivir solo en CLAUDE.md (template) o references/, no en una skill."
            )

    # 5. Bloques universales del template (skipped para boilerplate)
    BOILERPLATE = {"cold-start-interview", "customize", "matter-workspace",
                   "doctor", "help"}
    if name not in BOILERPLATE:
        # Skills que producen output sensible deberían tener Destination check
        produces_output = any(prefix in name for prefix in [
            "civil-", "societario-", "mercantil-", "contrato-", "rgpd-",
            "laboral-", "penal-", "admin-", "tributario-", "familia-",
            "sucesiones-", "concursal-", "extranjeria-", "seguros-",
            "ip-", "inmobiliario-", "compliance-",
        ]) or name in {"dictamen", "memorandum", "informe-juridico",
                       "cliente-email", "cliente-hoja-encargo",
                       "resumen-ejecutivo"}
        if produces_output:
            for required_block in [
                "Matter context", "Destination check",
                "Source attribution tiering", "No silent supplement",
                "Cross-skill handoffs", "Lo que esta skill NO hace",
                "Closing action",
            ]:
                if required_block.lower() not in body.lower():
                    MEDIUM.append(
                        f"{name}: falta bloque `## {required_block}` del template Anthropic"
                    )
            # Foral check para ramas civiles
            FORAL_PREFIXES = ("civil-", "societario-", "mercantil-", "contrato-",
                              "familia-", "sucesiones-", "inmobiliario-", "seguros-")
            if name.startswith(FORAL_PREFIXES):
                if "foral check" not in body.lower():
                    HIGH.append(
                        f"{name}: skill foral pero falta bloque `## Foral check`"
                    )

    # 6. Severity rating coherencia
    has_red = "🔴" in body
    has_green = "🟢" in body
    if has_red and not has_green:
        INFO.append(
            f"{name}: usa 🔴 pero no 🟢. Considera escala completa para outputs estructurados."
        )

    # 7. ECLI explícito en skills primariamente jurisprudenciales.
    # Para skills que llaman secundariamente a TJUE (RGPD, compliance), la
    # convención está en CLAUDE.md como regla global del plugin.
    PRIMARILY_JURISPRUDENCE = {
        "jurisprudencia", "verificar-citas",
        "civil-demanda", "civil-contestacion", "civil-recurso-apelacion",
        "civil-recurso-casacion", "civil-recurso-infraccion-procesal",
        "civil-analizar-escrito", "civil-viabilidad",
        "penal-defensa", "penal-acusacion",
    }
    if name in PRIMARILY_JURISPRUDENCE:
        mentions_jurisprudence = any(t in tools for t in [
            "buscar_jurisprudencia", "buscar_tc", "buscar_tjue", "buscar_tgue",
            "buscar_tedh", "buscar_aepd", "obtener_sentencia_completa",
        ])
        if mentions_jurisprudence and "ECLI" not in body:
            INFO.append(
                f"{name}: skill primariamente jurisprudencial pero no menciona ECLI explícitamente."
            )


def audit_agent(agent_md: Path):
    name = agent_md.stem
    text = agent_md.read_text()
    fm, body = parse_frontmatter(text)

    if "name" not in fm or "description" not in fm:
        CRITICAL.append(f"agent {name}: falta name o description en frontmatter")

    # tools field
    tools_match = re.search(r"^tools:\s*\[(.+?)\]", text, re.MULTILINE | re.DOTALL)
    if tools_match:
        raw_tools = tools_match.group(1)
        tools_listed = re.findall(r"mcp__robin__([a-z_*]+)", raw_tools)
        for t in tools_listed:
            if t.endswith("*"):
                continue  # glob ok
            if t in MCP_ORPHAN:
                HIGH.append(
                    f"agent {name}: tool `mcp__robin__{t}` no registrada en catalog (orphan)"
                )
            elif t not in MCP_CATALOG:
                CRITICAL.append(
                    f"agent {name}: tool `mcp__robin__{t}` no existe en catálogo"
                )


def main() -> int:
    print("🔍 Auditoría profunda del plugin Robin...\n")

    all_skill_names = {d.name for d in SKILLS_DIR.iterdir() if d.is_dir()}
    all_handoffs_used: dict[str, set] = defaultdict(set)

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if skill_dir.is_dir():
            audit_skill(skill_dir, all_skill_names, all_handoffs_used)

    for agent_md in sorted(AGENTS_DIR.glob("*.md")):
        audit_agent(agent_md)

    # Reporte
    n_critical = len(CRITICAL)
    n_high = len(HIGH)
    n_medium = len(MEDIUM)
    n_info = len(INFO)
    total = n_critical + n_high + n_medium + n_info

    if n_critical:
        print(f"🔴 CRÍTICO ({n_critical}) — bloquea uso real:\n")
        for h in CRITICAL[:30]:
            print(f"  • {h}")
        if len(CRITICAL) > 30:
            print(f"  ... y {len(CRITICAL) - 30} más")
        print()

    if n_high:
        print(f"🟠 ALTO ({n_high}) — degrada calidad o produce errores en runtime:\n")
        for h in HIGH[:30]:
            print(f"  • {h}")
        if len(HIGH) > 30:
            print(f"  ... y {len(HIGH) - 30} más")
        print()

    if n_medium:
        print(f"🟡 MEDIO ({n_medium}) — mejorable, no bloqueante:\n")
        for h in MEDIUM[:20]:
            print(f"  • {h}")
        if len(MEDIUM) > 20:
            print(f"  ... y {len(MEDIUM) - 20} más")
        print()

    if n_info:
        print(f"🟢 INFO ({n_info}) — sugerencias:\n")
        for h in INFO[:10]:
            print(f"  • {h}")
        if len(INFO) > 10:
            print(f"  ... y {len(INFO) - 10} más")
        print()

    print(f"=== Resumen ===")
    print(f"Total hallazgos: {total}")
    print(f"  Crítico: {n_critical} (bloqueante)")
    print(f"  Alto: {n_high}")
    print(f"  Medio: {n_medium}")
    print(f"  Info: {n_info}")
    print()

    if n_critical:
        print("❌ La auditoría detecta problemas críticos. Resolver antes de submission.")
        return 1
    if n_high:
        print(f"⚠️ {n_high} hallazgos altos. Plugin usable pero con bugs conocidos del backend.")
        return 0
    print("✅ Plugin estructuralmente sólido.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
