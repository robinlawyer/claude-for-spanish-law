# Skill template — estándar Anthropic adaptado al derecho español

Plantilla universal extraída de las 150 skills de `anthropics/claude-for-legal`,
aplicable a las 127 skills de Robin. Toda nueva skill o rework debe seguir
estos bloques en este orden.

## Frontmatter

```yaml
---
name: nombre-skill
description: >
  Frase corta del propósito. Use when el letrado diga "X", "Y", o "Z".
  Cargada por /robin:OTRA-SKILL cuando se detecte SUPUESTO.
argument-hint: "[forma libre — escribe el hint que verá el usuario]"
---
```

- `description` arranca con propósito en 1 frase, después "Use when..." con los
  disparadores en boca del letrado, y referencia a skills que la cargan.
- `argument-hint` se muestra al usuario; sin él, slash command queda mudo.

## Cabecera operativa (justo tras el frontmatter, antes del `# Título`)

5-6 bullets numerados que resumen el flujo. El abogado los lee en 10 segundos
y sabe lo que va a pasar.

```markdown
1. Cargar `~/.claude/plugins/config/claude-for-spanish-law/robin/CLAUDE.md` →
   sección X que parametriza la skill.
2. Determinar [variable clave: lado, jurisdicción, modo].
3. Aplicar el workflow completo.
4. Verificar TODAS las citas con `mcp__robin__verificar_cita`.
5. Devolver con severity rating + cláusulas faltantes + plazos críticos +
   handoff al siguiente skill si procede.

---
```

## Bloque `## Matter context` (estándar copia-pegable)

```markdown
## Matter context

**Matter context.** Lee `## Matter workspaces` en el CLAUDE.md del plugin. Si
`Habilitado` es `✗` (default para asesoría interna), salta el resto de este
párrafo — la skill opera a nivel practice. Si está habilitado y no hay matter
activo, pregunta: "¿En qué asunto va esto? Ejecuta
`/robin:matter-workspace switch <slug>` o di `practice-level`." Carga
`matter.md` del matter activo para contexto y overrides. Guarda outputs en
`~/.claude/plugins/config/claude-for-spanish-law/robin/matters/<slug>/`.
Nunca leas archivos de otro matter salvo que `Cross-matter context` esté `on`.
```

## Bloque `## Destination check` (en skills que producen escrito o dictamen)

```markdown
## Destination check

Antes de devolver el output, comprueba el destino. Si el letrado ha nombrado
canal, lista de distribución, contraparte o "todo el equipo", pregunta si
está dentro del círculo de secreto profesional. Canales abiertos, listas
corporativas amplias, contraparte/letrado adverso, proveedores y clientes
(para work product) lo rompen. Si el destino parece fuera del círculo,
señálalo y ofrece (a) versión confidencial para uso interno, (b) versión
sanitizada para el canal amplio, (c) ambas. No metas silenciosamente cabecera
de secreto profesional en un texto que va a publicarse.
```

## Bloque `## Purpose`

2-3 frases. Honesto, sin marketing. Qué hace, qué NO hace.

## Bloque `## Load the playbook first` (o `## Load context`)

Qué secciones del CLAUDE.md leer ANTES de actuar. Si está vacío o tiene
`[PLACEHOLDER]`, parar y enviar al cold-start.

Ejemplo:
```markdown
## Load the playbook first

Antes de cualquier análisis, lee `~/.claude/plugins/config/claude-for-spanish-law/robin/CLAUDE.md`:

- `## Tono y registro de escritos` → cómo escribe el despacho
- `## Jurisdicción y territorio` → AP y TSJ de referencia
- `## Derecho foral` → vecindad civil habitual
- `## Política de costas` → cómo trata costas el despacho

Si alguna de estas secciones sigue con `[PLACEHOLDER]`, **para** y di:
"Para hacer este escrito necesito que termines la configuración. Ejecuta
`/robin:cold-start-interview --area civil` (2 minutos)."
```

## Bloque `## Jurisdiction assumption`

Qué supone la skill. Si el caso cae fuera, marcarlo en el output.

```markdown
## Jurisdiction assumption

Esta skill asume jurisdicción española y, salvo que la sección
`## Derecho foral` del playbook diga otra cosa, derecho común. Si los hechos
tienen punto de conexión foral, lanza `/robin:foral-check` ANTES de redactar.
Para casos transfronterizos UE, usa Reglamento Bruselas Ibis (competencia) y
Roma I/II (ley aplicable). Para casos extra-UE, ley elegida o foro del lugar
del demandado.
```

## Bloque `## Workflow` con steps numerados

Step 1, Step 2, Step 3, … con propósito claro de cada paso. Cada paso
nombra la tool MCP que llama.

```markdown
## Workflow

### Step 1: Hechos básicos

- Identificación del cliente y la contraparte.
- Cauce procesal aplicable (LEC, LRJS, LJCA, LECrim).
- Cuantía (si litigioso).
- Vecindad civil de las partes (relevante para foral).
- Partido judicial competente.

### Step 2: Verificación de la situación procesal

`mcp__robin__calculo_plazos` con [fecha inicio] + [tipo]. Si el plazo está
agotado, parar.

### Step 3: Construcción del esqueleto

`mcp__robin__preparar_[demanda|contestacion|recurso]` con los hechos.

### Step 4: Refuerzo jurisprudencial

`/robin:jurisprudencia` con la tesis principal. Aplica jerarquía TS > AN >
TSJ > AP del despacho. ECLI obligatorio.

### Step 5: Verificación obligatoria

`mcp__robin__verificar_cita` sobre cada ECLI, BOE-A y artículo. Citas no
verificadas: eliminadas o sustituidas.
```

## Bloque de modos / triage (si aplica)

Skills tipo review/triage tienen modos. Una sola skill con modos > varias
skills separadas.

```markdown
## Modos

Esta skill carga el modo según el tipo del documento o la petición:

### Modo A — [descripción]

Cuándo: [criterio].

Output:
[estructura específica del modo A].

### Modo B — [descripción]
...
```

## Severity rating sistemático

Toda salida que clasifique riesgos usa la misma escala:

| Icono | Nivel | Significado |
|---|---|---|
| 🔴 | Crítico | Bloqueador. Hay que resolver antes de continuar. |
| 🟠 | Alto | Importante. Decisión del letrado antes de firmar/presentar. |
| 🟡 | Medio | Mejorable. El letrado decide si lo arregla. |
| 🟢 | Informativo | Bien. Constatación. |

Para business friction añadir paralelo:

| Icono | Significado |
|---|---|
| 🔴 | Bloquea la operación |
| 🟠 | La ralentiza |
| 🟡 | Confunde al cliente |
| 🟢 | Invisible al cliente |

## Source attribution tiering (obligatorio en toda salida con citas)

Cada cita lleva tag de origen:

| Tag | Cuándo usar |
|---|---|
| `[robin-verified]` | Verificado contra `mcp__robin__verificar_cita`. Confianza alta. |
| `[robin-corpus]` | Devuelto por una tool de búsqueda de Robin pero no re-verificado. |
| `[verify-pinpoint]` | Pinpoint cite (apartado, subapartado) recordado del modelo — verificar contra fuente primaria SIEMPRE antes de usar. |
| `[user-provided]` | Citado por el letrado en el input. No alterar. |
| `[web-search — verify]` | Vía web search externa. Verificar antes de meter en escrito. |
| `[model-knowledge — verify]` | Recordado del modelo sin búsqueda. Verificar SIEMPRE. |

## "No silent supplement" (regla anti-fabricación)

```markdown
**No silent supplement.** Si la tool de Robin devuelve `hits=[]` o
`existe=false` para una cita que la skill necesita, REPORTA la ausencia y
PARA. NO la rellenes con conocimiento general del modelo sin avisar
explícitamente. Di:

> "Robin no encontró [cita / norma / sentencia / expediente]. Opciones:
> (1) reformular la búsqueda con otros términos, (2) probar otra tool de
> Robin, (3) ir a fuente externa (CENDOJ, BOE) — el resultado irá marcado
> `[web-search — verify]` y deberá verificarse antes de meter en escrito,
> (4) dejarlo señalado y seguir sin esa cita. ¿Cuál prefieres?"

El letrado decide. Nunca decidas tú silenciosamente.
```

## Foral check (en toda skill civil, mercantil, contratación, familia,
   sucesiones, inmobiliario)

```markdown
## Foral check

ANTES de aplicar Código Civil estatal, si la materia es civil / mercantil /
contratación / familia / sucesiones / inmobiliario, comprueba punto de
conexión foral. Si la vecindad civil de las partes o el sito de los
inmuebles cae en Cataluña / Galicia / Aragón / Navarra / País Vasco /
Baleares / Valencia, lanza `/robin:foral-check` y aplica la Compilación
foral PRIMERO. CC estatal solo supletorio (art. 13.2 CC).

Lista de leyes forales: ver `references/foral-matrix.md`.
```

## Cross-skill handoffs

Skills que se llaman entre sí lo declaran explícitamente:

```markdown
## Cross-skill handoffs

- Antes de empezar: `/robin:foral-check` si aplica
- En medio: `/robin:jurisprudencia --norma <referencia>` para apoyo doctrinal
- Al cierre: `/robin:verificar-citas` para confirmar todas las citas
- Después: `/robin:revisar-propio-escrito` antes de presentar el escrito

Si una skill anterior calificó algo 🔴, esta skill NO puede bajarlo a 🟢 sin
justificar el cambio en una frase. Severity floor cruzado.
```

## "What this skill does NOT do"

Anti-scope explícito. Evita que la skill se vaya por las ramas.

```markdown
## Lo que esta skill NO hace

- No firma escritos. El letrado los firma tras revisión.
- No presenta en Lexnet. El despacho lo presenta.
- No sustituye al letrado en juicio o vista.
- No decide estrategia: la propone; el letrado decide.
- No fija criterios de costas (vienen del playbook del despacho).
```

## Output rules (longitud)

```markdown
## Output rules

**Filtro de complejidad:** si la corrección requiere redactar nueva
cláusula, restructurar bloque procesal o introducir motivo nuevo, NO lo
hagas en el bloque ejecutivo. Marca: "Sección X — derivar a letrado para
revisión". Solo acciones mecánicas (cambiar palabra, eliminar frase,
sustituir cita) en el resumen.

**Regla "escrito limpio":** si el documento pasa todos los checks sin
flags, el bloque ejecutivo dice solo: "Sin red flags. Listo para
revisión final y firma." NO escribas un informe extenso para algo limpio.
```

## Closing action

```markdown
## Closing action

Lee `~/.claude/plugins/config/claude-for-spanish-law/robin/CLAUDE.md` →
`## Política de cierre`. Si está configurada, añade su `closing_action`
verbatim al final del output. Si no, añade:

> "Este borrador requiere revisión y firma de letrado colegiado antes de
> presentarse en sede judicial."

Y termina con el árbol de decisión de próximos pasos del playbook
(default: cinco opciones — refinar el escrito, escalar a socio, pedir más
hechos al cliente, dejar en standby, otra).
```

---

## Convenciones de tono

- **Segunda persona, voz de partner** ("Lee X", "Aplica Y", "Si pasa Z").
- **Frases cortas, instrucciones operativas**.
- **Markdown ">"** para texto literal que la skill dice al usuario.
- **Inglés** solo en términos técnicos de Anthropic (skill, agent, hook,
  MCP, plugin). Resto en español neutro profesional.
- **Imperativo**, no condicional. No "podrías", sino "lee", "verifica",
  "para".

## Convenciones de longitud

- **Skills foundational** (boilerplate + core + las más usadas): 1.500-2.500
  palabras. Profundidad Anthropic plena.
- **Skills verticales** (las 110+ de rama): 600-1.200 palabras. Bloques
  obligatorios completos pero sin extensión por extensión.
- **Skills `user-invocable: false`** (cargadas por otras): pueden ser más
  cortas si solo orquestan.

## Convenciones de Robin específicas (sobre el template Anthropic)

1. **Robin-First** (Regla 0): toda cita o cálculo viene de una tool de
   Robin, nunca del conocimiento general. Esto está en el CLAUDE.md del
   plugin como invariante.
2. **Verificación obligatoria al cierre**: toda salida con citas pasa por
   `mcp__robin__verificar_cita` antes de devolver.
3. **Foral checker no opcional** en ramas civil/mercantil/contratación/
   familia/sucesiones/inmobiliario.
4. **Jerarquía jurisprudencial**: TS > AN > TSJ > AP del despacho > resto
   AAPP. ECLI explícito siempre.
5. **Calculadoras** con auto-update IPC/IRAV/baremo (las 14 del MCP).
