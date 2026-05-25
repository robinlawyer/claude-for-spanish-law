#!/usr/bin/env python3
"""
Aplica los bloques estructurales del template Anthropic a las 127 skills.

Para cada SKILL.md:
1. Detecta qué bloques estándar faltan.
2. Añade los que faltan al final, sin pisar contenido existente.
3. Reporta cada cambio.

Bloques universales que se añaden:
- ## Matter context (si la skill produce output)
- ## Destination check (si la skill produce escrito o dictamen)
- ## Source attribution tiering (siempre)
- ## No silent supplement (siempre)
- ## Foral check (en ramas civiles)
- ## Closing action (siempre)
- ## Lo que esta skill NO hace (siempre)

NO modifica los bloques existentes. Solo añade lo que falta.
"""

from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_DIR = ROOT / "robin"
SKILLS_DIR = PLUGIN_DIR / "skills"

# Skills civiles/mercantiles/forales que necesitan foral-check
FORAL_PREFIXES = ("civil-", "societario-", "mercantil-", "contrato-", "familia-",
                  "sucesiones-", "inmobiliario-", "seguros-")

# Skills que producen escrito/dictamen y necesitan destination check
WRITES_OUTPUT_PREFIXES = ("civil-", "societario-", "mercantil-", "contrato-",
                          "rgpd-", "laboral-", "penal-", "admin-",
                          "tributario-", "familia-", "sucesiones-", "concursal-",
                          "extranjeria-", "seguros-", "ip-", "inmobiliario-",
                          "compliance-")
WRITES_OUTPUT_EXTRA = ("dictamen", "memorandum", "informe-juridico",
                       "cliente-email", "cliente-hoja-encargo",
                       "resumen-ejecutivo")

MATTER_CONTEXT_BLOCK = """
## Matter context

**Matter context.** Lee `## Matter workspaces` en
`~/.claude/plugins/config/claude-for-spanish-law/robin/CLAUDE.md`. Si la
sección dice `Habilitado: ✗` (default para asesoría jurídica interna),
salta este bloque — la skill opera a nivel practice. Si está habilitado y
no hay matter activo, pregunta: "¿En qué asunto va esto? Ejecuta
`/robin:matter-workspace switch <slug>` o di `practice-level`." Carga
`matter.md` del matter activo para contexto y overrides. Guarda outputs en
`~/.claude/plugins/config/claude-for-spanish-law/robin/matters/<slug>/`.
Nunca leas archivos de otro matter salvo que `Cross-matter context` esté
explícitamente `on`.
"""

DESTINATION_CHECK_BLOCK = """
## Destination check

Antes de devolver el output, comprueba el destino. Si el letrado ha
nombrado canal, lista de distribución, contraparte o "todo el equipo",
verifica si está dentro del círculo de secreto profesional (art. 542.3
LOPJ + art. 5 EGAE). Canales corporativos abiertos, listas amplias,
contraparte/letrado adverso, proveedores y clientes (para work product)
rompen el secreto. Si el destino parece fuera del círculo, señálalo y
ofrece: (a) versión confidencial para uso interno del despacho,
(b) versión sanitizada para el canal amplio, (c) ambas. No metas
silenciosamente cabecera de secreto profesional en un texto que va a
publicarse — ese header pierde protección al salir del círculo.
"""

CITATION_TAGGING_BLOCK = """
## Source attribution tiering

Toda cita en el output lleva tag de origen, para que el letrado vea de un
vistazo qué grado de verificación tiene cada referencia:

| Tag | Cuándo usar |
|---|---|
| `[robin-verified]` | Pasó `mcp__robin__verificar_cita`. Confianza alta. |
| `[robin-corpus]` | Devuelta por una tool de búsqueda de Robin pero no re-verificada (típico en bloques de hits). |
| `[verify-pinpoint]` | Pinpoint cite (subapartado, ordinal) recordado del modelo — verifica contra fuente primaria SIEMPRE antes de meter en escrito. |
| `[user-provided]` | Citada por el letrado en el input. No alterar. |
| `[web-search — verify]` | Vía búsqueda externa (CENDOJ, BOE, AEPD). Verificar contra fuente antes de meter en escrito. |
| `[model-knowledge — verify]` | Recordada del modelo sin búsqueda. Verificar SIEMPRE. Alto riesgo de fabricación. |

Nunca quites ni colapses los tags. Un lector que verifica todo verifica
nada — el tiering hace que el trabajo de verificación se concentre donde
de verdad importa.
"""

NO_SILENT_SUPPLEMENT_BLOCK = """
## No silent supplement (regla anti-fabricación)

Si una tool de Robin devuelve `hits=[]` o `existe=false` para una cita o
norma que esta skill necesita, REPORTA la ausencia y PARA. No la rellenes
con conocimiento general del modelo sin avisar explícitamente. Di:

> "Robin no ha encontrado [cita / norma / sentencia / expediente]. Opciones:
> (1) reformular la búsqueda con otros términos jurídicos,
> (2) probar otra tool de Robin más específica,
> (3) ir a fuente externa (CENDOJ, BOE, AEPD, etc.) — el resultado irá
>     marcado `[web-search — verify]` y deberá comprobarse antes de meter
>     en escrito,
> (4) dejarlo señalado en el output y seguir sin esa cita.
> ¿Cuál prefieres?"

El letrado decide. Nunca decidas tú silenciosamente: una cita verosímil
pero inventada es peor que un hueco honesto.
"""

FORAL_CHECK_BLOCK = """
## Foral check (no opcional)

ANTES de aplicar Código Civil estatal, comprueba si hay punto de conexión
foral. Si la vecindad civil de las partes o el sito de los inmuebles cae
en Cataluña, Galicia, Aragón, Navarra, País Vasco, Baleares o Comunidad
Valenciana, lanza `/robin:foral-check` y aplica la Compilación foral
PRIMERO. El CC estatal solo opera como derecho supletorio (art. 13.2 CC).

Matriz de leyes forales aplicables: ver `references/foral-matrix.md`.

Si la aplicabilidad foral es discutible (vecindad civil mixta, inmueble
en territorio distinto al del causante, etc.), márcalo en el output como
🟠 y deja que el letrado decida.
"""

CROSS_SKILL_HANDOFFS_BLOCK_TEMPLATE = """
## Cross-skill handoffs

- **Antes de empezar:** `/robin:foral-check` si la materia es civil,
  mercantil, contratación, familia, sucesiones o inmobiliario.
- **En medio del flujo:** `/robin:jurisprudencia --norma <referencia>`
  para apoyo doctrinal puntual; `/robin:plazos` para cualquier plazo
  procesal o de prescripción que aparezca.
- **Al cierre:** `/robin:verificar-citas` sobre el escrito final para
  confirmar todas las citas.
- **Antes de presentar:** `/robin:revisar-propio-escrito` para
  simulación de oposición y blindaje.

**Severity floor cruzado:** si una skill anterior calificó algo 🔴, esta
skill NO puede bajarlo a 🟢 sin justificar el cambio en una frase. Los
ratings de upstream son el suelo, no el techo.
"""

WHAT_NOT_DO_BLOCK_TEMPLATE = """
## Lo que esta skill NO hace

- **No firma**: el letrado firma todo escrito tras revisión, conforme art. 542
  LOPJ.
- **No presenta**: el despacho presenta en Lexnet, sede judicial o
  administrativa. La skill prepara, no presenta.
- **No sustituye al letrado**: en juicio, vista o comparecencia el letrado
  comparece personalmente.
- **No fija criterios de despacho** (tono, costas, política de provisión):
  vienen del playbook editable en
  `~/.claude/plugins/config/claude-for-spanish-law/robin/CLAUDE.md`.
- **No decide estrategia**: la propone con razonamiento; el letrado decide.
- **No fabrica**: si Robin no devuelve un dato, esta skill no lo inventa.
"""

CLOSING_ACTION_BLOCK = """
## Closing action

Toda salida termina con:

> "Este borrador requiere revisión y firma de letrado colegiado antes de
> presentarse en sede judicial, administrativa o ante el cliente."

Y con el árbol de próximos pasos (default — el despacho puede sobrescribir
en `## Política de cierre` del playbook):

> ¿Qué hacemos ahora?
> 1. **Refinar** este borrador con un cambio concreto (dime cuál).
> 2. **Escalar a socio** del despacho para revisión.
> 3. **Pedir más hechos** al cliente o expediente (te digo cuáles).
> 4. **Standby** — guardo en el matter y volvemos cuando decidas.
> 5. **Otra** — dime.
"""


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.index("---", 3)
    fm_raw = text[3:end]
    body = text[end + 3 :].lstrip("\n")
    fm = {}
    for line in fm_raw.strip().splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()
    return fm, body


def needs_block(body: str, marker: str) -> bool:
    """Si el cuerpo ya contiene el marcador (heading o frase clave), no añadir."""
    return marker.lower() not in body.lower()


def apply_template(skill_md: Path) -> dict:
    """Aplica los bloques al SKILL.md. Devuelve dict con cambios hechos."""
    skill_name = skill_md.parent.name
    text = skill_md.read_text()
    fm, body = parse_frontmatter(text)

    is_foral = skill_name.startswith(FORAL_PREFIXES)
    writes_output = (skill_name.startswith(WRITES_OUTPUT_PREFIXES)
                     or skill_name in WRITES_OUTPUT_EXTRA)

    additions = []

    # 1. Matter context — toda skill (excepto matter-workspace que ES el sistema)
    if skill_name not in {"matter-workspace", "cold-start-interview",
                          "customize", "doctor", "help"}:
        if needs_block(body, "## Matter context"):
            additions.append(MATTER_CONTEXT_BLOCK)

    # 2. Destination check — skills que producen output sensible
    if writes_output and needs_block(body, "## Destination check"):
        additions.append(DESTINATION_CHECK_BLOCK)

    # 3. Source attribution tiering — toda skill que devuelve citas
    if writes_output and needs_block(body, "## Source attribution"):
        additions.append(CITATION_TAGGING_BLOCK)

    # 4. No silent supplement — toda skill que llama a tools
    if writes_output and needs_block(body, "## No silent supplement"):
        additions.append(NO_SILENT_SUPPLEMENT_BLOCK)

    # 5. Foral check — civil/mercantil/familia/sucesiones/inmobiliario/contrato
    if is_foral and needs_block(body, "## Foral check"):
        additions.append(FORAL_CHECK_BLOCK)

    # 6. Cross-skill handoffs — skills verticales
    if writes_output and needs_block(body, "## Cross-skill handoffs"):
        additions.append(CROSS_SKILL_HANDOFFS_BLOCK_TEMPLATE)

    # 7. Lo que NO hace — skills verticales
    if writes_output and needs_block(body, "## Lo que esta skill NO hace"):
        additions.append(WHAT_NOT_DO_BLOCK_TEMPLATE)

    # 8. Closing action — skills que devuelven output al letrado
    if writes_output and needs_block(body, "## Closing action"):
        additions.append(CLOSING_ACTION_BLOCK)

    if not additions:
        return {"skill": skill_name, "blocks_added": 0, "changed": False}

    # Insertar los bloques al final
    new_text = text.rstrip() + "\n" + "\n".join(additions) + "\n"
    skill_md.write_text(new_text)

    return {
        "skill": skill_name,
        "blocks_added": len(additions),
        "is_foral": is_foral,
        "writes_output": writes_output,
        "changed": True,
    }


def main() -> int:
    skills = sorted(SKILLS_DIR.iterdir())
    print(f"Procesando {len(skills)} skills...")
    print()
    total_blocks = 0
    changed_skills = 0
    by_block_count = {}
    for skill_dir in skills:
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        result = apply_template(skill_md)
        if result["changed"]:
            changed_skills += 1
            total_blocks += result["blocks_added"]
            by_block_count[result["blocks_added"]] = by_block_count.get(
                result["blocks_added"], 0) + 1
            tag = " (foral)" if result.get("is_foral") else ""
            print(f"  +{result['blocks_added']} bloques → {result['skill']}{tag}")

    print()
    print(f"=== Resumen ===")
    print(f"Skills modificadas: {changed_skills} / {len(skills)}")
    print(f"Bloques añadidos en total: {total_blocks}")
    print(f"Distribución por bloques añadidos:")
    for n in sorted(by_block_count.keys()):
        print(f"  {n} bloques: {by_block_count[n]} skills")
    return 0


if __name__ == "__main__":
    sys.exit(main())
