# CLAUDE.md

Guía para contribuir a este repositorio. `claude-for-spanish-law` es un marketplace de plugins de Claude — dieciséis plugins de primer nivel sobre las grandes ramas del derecho español, un único MCP central (Robin), y un motor común de verificación.

La mayor parte del trabajo es contenido de prompts (skills, agents, hooks), metadatos de plugin y el manifest del marketplace. Muy poco código de aplicación.

## Layout

```
.claude-plugin/marketplace.json     # manifest del marketplace — una entrada por plugin
<plugin>/                           # 16 plugins de primer nivel
  .claude-plugin/plugin.json        # manifest del plugin (name, version, description, author)
  .mcp.json                         # MCP servers que el plugin consume (Robin + opcionales)
  CLAUDE.md                         # TEMPLATE del playbook del despacho
  README.md                         # docs del plugin
  skills/<name>/SKILL.md            # una skill por carpeta
  agents/<name>.md                  # sub-agentes
  hooks/hooks.json                  # stub vacío salvo plugins con vigilancia activa
references/                         # plantillas compartidas (company-profile, foral matrix)
scripts/                            # validate.py, lint-tool-scope.py
```

## Validación antes de abrir PR

```bash
# 1. Schema del marketplace y de cada plugin
claude plugin validate .claude-plugin/marketplace.json
for d in robin-*/; do claude plugin validate "$d"; done

# 2. JSON/YAML sanity
python3 -c "import json,glob; [json.load(open(f)) for f in glob.glob('**/*.json', recursive=True)]"

# 3. Lint de scope de tools (un agent solo declara las MCP tools que usa)
python3 scripts/lint-tool-scope.py
```

### Invariantes del marketplace

- Cada `plugin.json` `name` matchea `^[a-z0-9][a-z0-9-]{1,63}$` (en este repo, prefijo `robin-`).
- `description` entre 10 y 2000 caracteres, sin whitespace leading/trailing.
- No duplicar nombres en `marketplace.json` ni en `plugin.json`.
- `marketplace.json` y `plugin.json` deben mantener `name`, `description` y `author` sincronizados field-by-field.
- Nombres de skills en prosa deben coincidir con el directorio (`skills/<name>/`). Si una skill dice "ejecuta `/foo`", `foo` debe existir como carpeta — los alias no resuelven.

### Frontmatter

- `agents/*.md`: `name` y `description` obligatorios. `tools` con globs `mcp__<server>__<tool>`. `model` opcional.
- `skills/<name>/SKILL.md`: `description` obligatorio. `user-invocable: false` para skills cargadas por otra skill (no slash command propio). `argument-hint` opcional.
- Descripciones multilínea con `>` block scalar son válidas.

## Convenciones específicas de Robin

### El CLAUDE.md de cada plugin es un TEMPLATE, no contexto del proyecto

Cada `<plugin>/CLAUDE.md` es el template del playbook del despacho. Se copia a:

```
~/.claude/plugins/config/claude-for-spanish-law/<plugin>/CLAUDE.md
```

la primera vez que el usuario corre `cold-start-interview`. Toda skill, agent y hook **lee** desde esa ruta de configuración, **no** desde el repo. Si no existe o aún tiene `[PLACEHOLDER]`, la skill debe parar y pedir cold-start.

`claude plugin validate` avisa de esto y el aviso es esperado. No "lo arregles" moviendo el contenido a otra skill.

### company-profile.md compartido

Datos de despacho que valen para los 16 plugins (denominación, NIF, dirección, ICAM/colegio, especialidades, política de costas) viven en:

```
~/.claude/plugins/config/claude-for-spanish-law/company-profile.md
```

— un nivel arriba de los configs por plugin. El primer `cold-start-interview` que se ejecute lo crea; los siguientes lo respetan.

### Verificación obligatoria

Toda skill que genere un escrito o dictamen termina con `mcp__robin__verificar_cita` sobre cada ECLI, BOE-A, expediente AEPD/CNMC/CNMV/TEAC y artículo de ley citado. Citas no verificadas se eliminan o se sustituyen. **Nunca devuelves al usuario un escrito con cita no verificada.**

### Detector de derecho foral

Toda skill civil, mercantil o sucesoria pasa por el patrón de robin-core:

```
mcp__robin__buscar_por_ccaa con los hechos
→ si el conflicto tiene punto de conexión foral (vecindad civil de las partes, sito del inmueble, lugar de celebración, etc.)
→ aplicar Compilación foral correspondiente; CC estatal solo supletorio (art. 13.2 CC)
```

Esto es no-negociable para Cataluña (CCCat), Galicia (LDCG), Aragón (CDFA), Navarra (Fuero Nuevo), País Vasco (LDCV), Baleares (Compilación) y Valencia (en lo recuperable).

### Jurisprudencia jerarquizada

Cuando una skill cite sentencias, prioridad TS > AN > TSJ > AP > Juzgado, salvo que el supuesto requiera específicamente jurisprudencia menor (criterio territorial reiterado por la AP del lugar). **ECLI explícito siempre**, junto a la referencia corta (STS 123/2025, Sala 1ª, ECLI:ES:TS:2025:123).

## Cambios al MCP de Robin

El servidor MCP en `https://api.robinlawyer.ai/mcp` se mantiene como servicio privado de Robin. Cambios coordinados:

1. Si una skill necesita una tool nueva, primero hay que añadirla al backend de Robin y desplegar.
2. Verificar que `tools/list` la devuelve en producción.
3. Solo entonces referenciarla desde una skill aquí.

## Sincronización con `marketplace.json`

Para plugins de primer nivel, `marketplace.json` debe replicar exactamente `name`, `description` y `author` del `plugin.json` del plugin. Si cambias uno, cambia el otro. El test de validación los compara.

## Formato

- Indent 2 spaces en JSON y `.mcp.json`.
- Newline final en todo archivo de texto.
- Sin trailing whitespace.
- Markdown en español. Términos técnicos de Claude/Anthropic en inglés (skill, agent, hook, MCP, prompt).
