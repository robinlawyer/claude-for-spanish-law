# Contribuir a Claude for Spanish Law

Gracias por considerar contribuir. Este repo es la capa pública sobre el MCP de Robin: editamos prompts, no código de aplicación.

## Antes de contribuir

1. Lee [CLAUDE.md](./CLAUDE.md). Las convenciones de verificación, foral y jerarquía jurisprudencial son no-negociables.
2. Si tu cambio requiere una tool nueva del MCP de Robin, abre primero un issue describiendo el caso de uso. Las tools del MCP se mantienen en el backend privado de Robin; necesitan despliegue antes de poder ser referenciadas desde una skill.
3. Si tu cambio toca derecho foral, etiqueta el PR con `foral:<comunidad>` (catalunya, galicia, aragon, navarra, pais-vasco, baleares, valencia).

## Tipos de aportación que aceptamos

### Skills

- Añadir una skill a un plugin existente: PR con nueva carpeta `skills/<nombre>/SKILL.md`.
- Mejorar el pipeline de una skill existente: PR con diff sobre el `SKILL.md` y, si procede, un ejemplo real (anonimizado) en `references/examples/`.

Requisitos de toda skill que produzca un escrito:

- Pipeline explícito numerado con las tools del MCP en orden.
- Verificación obligatoria al cierre (`mcp__robin__verificar_cita` sobre todas las citas).
- Detector foral si toca rama civil / mercantil / sucesoria.
- Salida estructurada con bloque "Citas verificadas" + "Avisos al letrado".

### Agents

- Un agent por archivo en `agents/<nombre>.md`.
- Frontmatter con `name`, `description`, `model` (sonnet por defecto, opus solo si lo justifica el tipo de razonamiento), `tools` con globs explícitos.
- **Nunca declarar `tools: "*"`.** El lint rechaza ese patrón.

### Playbooks (CLAUDE.md del plugin)

- Editar la TEMPLATE no cambia el playbook de ningún despacho instalado (es solo el template inicial). Documenta los cambios en el PR para que despachos existentes sepan si quieren re-correr `cold-start-interview --redo`.

## Tests

```bash
# Schema del marketplace
claude plugin validate .claude-plugin/marketplace.json

# Schema de cada plugin
for d in robin-*/; do claude plugin validate "$d"; done

# JSON sanity
python3 -c "import json,glob; [json.load(open(f)) for f in glob.glob('**/*.json', recursive=True)]"

# Lint de scope de tools en agents
python3 scripts/lint-tool-scope.py
```

## Política sobre datos confidenciales

- No commits con expedientes, nombres de cliente o datos identificativos. Si necesitas ejemplos, anonimízalos completamente (cambia nombres, NIFs, fechas, importes).
- No conectar el repo a sistemas que reciban datos del despacho. El playbook editable vive en local del usuario (`~/.claude/plugins/config/...`) y nunca debe acabar en el repo.

## Política sobre citas

- Toda referencia a sentencia debe llevar ECLI explícito en el ejemplo o el test.
- Toda referencia a norma debe llevar BOE-A o equivalente.
- Si una cita no pasa `verificar_cita` en el momento del PR, fuera.

## Estilo

- Español neutro, registro profesional. Sin coloquialismos.
- Términos técnicos de Anthropic en inglés (skill, agent, hook, plugin, MCP). Resto en español.
- Markdown en líneas de hasta 100 columnas en código y prosa flexible.

## Code of Conduct

Trato profesional. Discusiones técnicas, no personales. Las disputas se resuelven citando fuente (BOE, jurisprudencia, doctrina vinculante).
