---
name: normativa
description: >
  Búsqueda asistida en BOE y los 17 boletines autonómicos, con detector de
  vigencia, modificaciones, disposiciones DA/DT/DF/DD, y normativa UE (DOUE).
  Úsala para localizar el texto consolidado de una norma, identificar la
  versión aplicable a una fecha, o explorar normativa autonómica concreta.
argument-hint: "[referencia o tema | --vigencia <fecha> | --ccaa <comunidad> | --europea]"
---

# /robin:normativa

Búsqueda y consulta de normas. Usa `mcp__robin__obtener_articulo_ley`
y `mcp__robin__buscar_normativa` con reranker estructural + Gemini
Flash; cada hit lleva `relevancia_robin = {nivel, motivo}`.

## Procedimiento

### 1. Identificar qué busca el usuario

Tres modos:

**Modo A — artículo concreto** ("art. 1124 CC", "art. 56 LJCA",
"DA 7ª LGT")
→ `mcp__robin__obtener_articulo_ley`. Devuelve texto literal,
versión vigente, historial de modificaciones, disposiciones de
desarrollo.

**Modo B — referencia a norma completa** ("Ley 39/2015",
"RD 2065/1974")
→ `mcp__robin__obtener_articulo_ley` con sólo identificación de norma
para devolver índice estructurado (libros / títulos / capítulos /
artículos / disposiciones).

**Modo C — búsqueda temática** ("normativa sobre intimidad genética",
"protección al consumidor en hipotecas") → `mcp__robin__buscar_normativa`
con reranker.

**Modo D — Resolución BOE íntegra** (Resoluciones DGSJFP/DGRN, DGT,
AEPD, Órdenes ministeriales, Circulares, Instrucciones — identificadas
por `BOE-A-AAAA-NNNNN`) → `mcp__robin__obtener_resolucion_boe`. Las
resoluciones no se chunkean por artículos como las leyes: una Resolución
DGSJFP típica es un solo FD doctrinal. **Llama a esta tool SIEMPRE**
cuando `buscar_normativa` devuelva un hit con `tipo='Resolución'`,
`'Orden'`, `'Circular'` o `'Instrucción'` y necesites el texto literal
para citar — los extractos de búsqueda son fragmentarios.

### 2. Filtros disponibles

- `--vigencia <fecha YYYY-MM-DD>` — versión consolidada aplicable en
  esa fecha. Útil para conflictos pre/post reforma.
- `--ccaa <slug>` — restringe a normativa autonómica de la CCAA:
  `andalucia`, `aragon`, `asturias`, `baleares`, `canarias`,
  `cantabria`, `castilla-la-mancha`, `castilla-leon`, `cataluna`,
  `comunidad-valenciana`, `extremadura`, `galicia`, `madrid`,
  `murcia`, `navarra`, `pais-vasco`, `la-rioja`, `ceuta`, `melilla`.
  Si el playbook indica TSJ/territorio, Robin sugiere el más probable.
- `--europea` — busca en DOUE (17 reglamentos UE indexados: RGPD,
  AI Act, MiCA, DSA, DMA, DORA, Roma I-II, Bruselas Ibis, etc.).
- `--ambito <estatal|autonomico|local|europeo>` — combinable con
  filtro CCAA.
- `--rango <ley|rd|orden|circular|resolucion>` — limita por rango
  normativo.
- `--solo-vigentes` (default: true) — excluye normas derogadas.
  `--incluir-derogadas` las muestra con marca explícita.

### 3. Resultado

Para artículo o norma concreta:

```
art. 1124 Código Civil
Versión vigente desde 1889 (sin modificaciones)

Texto:
"La facultad de resolver las obligaciones se entiende implícita en las recíprocas, para el caso de que uno de los obligados no cumpliere lo que le incumbe. […]"

Disposiciones de desarrollo: ninguna directamente conectada.
Jurisprudencia clave (TS):
- STS 678/2024, Sala 1ª, sobre resolución por incumplimiento esencial — ECLI:ES:TS:2024:3214
- STS 234/2023, Sala 1ª, sobre cláusula resolutoria expresa — ECLI:ES:TS:2023:1102

Concordancias:
- art. 1101 CC (responsabilidad contractual)
- art. 1281 CC (interpretación de contratos)
- art. 1255 CC (autonomía de la voluntad)
```

Para búsqueda temática:

```
3 hits ordenados por relevancia:

1. Real Decreto 1015/2009, regulación del consentimiento informado en biobancos
   Relevancia: ALTA. Aplica directamente al supuesto descrito.
   BOE-A-2009-10843. Vigente con modificaciones (última: RD 9/2014).

2. Ley 14/2007 de investigación biomédica (texto consolidado)
   Relevancia: ALTA. Marco legal de las pruebas genéticas.
   BOE-A-2007-12945.

3. RD 1090/2015, ensayos clínicos con medicamentos
   Relevancia: MEDIA. Aplicable si el supuesto implica medicamentos.
   BOE-A-2015-14082.
```

### 4. Detector foral autónomo

Si el usuario busca con `--ccaa cataluna|galicia|aragon|navarra|
pais-vasco|baleares|comunidad-valenciana` y la materia es civil
(propiedad, sucesiones, familia, contratos), Robin recuerda al
letrado que la Compilación foral aplica con prioridad y le ofrece
saltar a `/robin:foral-check` para confirmar la aplicabilidad
concreta.

### 5. Verificación

Como toda salida que cita normas, antes de cerrar:
`mcp__robin__verificar_cita` sobre cada BOE-A devuelto. Si una norma
está derogada y el usuario no usó `--incluir-derogadas`, no aparece
en el resultado.

### 6. Sugerencias contextuales

Si el usuario consultó un artículo concreto, ofrece:

> "¿Quieres que busque jurisprudencia que aplica este artículo?
> (`/robin:jurisprudencia --norma <referencia>`)
> ¿O las consultas vinculantes DGT/TEAC si es tributaria?"

## Ejemplos

```
/robin:normativa art. 1124 CC
```

```
/robin:normativa "ampliación de capital con prima de emisión" --rango ley
```

```
/robin:normativa --ccaa cataluna --vigencia 2024-01-15
"derechos de tanteo y retracto en arrendamientos rústicos"
```

```
/robin:normativa --europea
"Reglamento UE sobre inteligencia artificial — sistemas de alto riesgo"
```

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


## Source attribution tiering — Robin es la única fuente

Toda cita en el output procede de Robin (o del propio letrado). Si no
encaja en uno de estos cuatro tags, **se elimina del escrito** — no se
sustituye por nada del conocimiento del modelo ni por búsqueda web:

| Tag | Cuándo usar |
|---|---|
| `[robin-verified]` | Pasó `mcp__robin__verificar_cita`. Confianza alta. |
| `[robin-verbatim]` | Pinpoint con cita literal leída en `mcp__robin__obtener_sentencia_completa` o `mcp__robin__obtener_articulo_ley` (FJ X, párrafo Y / art. Z apartado N). |
| `[robin-corpus]` | Devuelta por una tool de búsqueda de Robin (`buscar_*`) pero no re-verificada — usable en bloques panorámicos de hits, no para apoyo argumental directo. |
| `[user-provided]` | Citada por el letrado en el input. No alterar; verificarla en Robin como cortesía y marcarla `[user-provided · robin-verified]` si pasa. |

**Prohibido**: `[model-knowledge]`, `[web-search]`, `[verify-pinpoint]` o
cualquier tag que admita la memoria del modelo o una fuente externa como
sustituto de Robin. Si tienes la tentación de usar uno, **declara la
ausencia y para** (ver § *No silent supplement*).

Nunca quites ni colapses los tags. Un lector que verifica todo verifica
nada — el tiering concentra la verificación donde importa.


## No silent supplement — Robin va a misa

Robin es la única fuente operativa de derecho positivo, jurisprudencia y
doctrina en este plugin. La regla es absoluta:

1. **Si Robin devuelve dato → ese dato es la verdad operativa.** No lo
   contrastes contra tu memoria del modelo; si percibes contradicción,
   gana Robin. Si crees que Robin se equivoca, REPÓRTALO al letrado y
   deja que él decida; nunca lo sustituyas por tu recuerdo.

2. **Si Robin devuelve `hits=[]` o `existe=false` → NO HAY CITA.** No
   rellenes con conocimiento general del modelo. No saltes a una fuente
   externa para "completar". Declara la ausencia explícitamente y para.
   Una cita verosímil pero inventada por el modelo es responsabilidad
   profesional del letrado y de los autores del plugin — no se asume
   ese riesgo nunca, bajo ninguna excusa.

3. **Lo que sí puedes ofrecer al letrado cuando Robin no devuelve**:

   > "Robin no ha encontrado [cita / norma / sentencia / expediente]. Opciones:
   > (1) reformular la búsqueda con otros términos jurídicos (te propongo X);
   > (2) probar otra tool de Robin más específica (te propongo `mcp__robin__buscar_Y`);
   > (3) dejar el escrito sin esa cita y señalarlo como hueco al letrado.
   > ¿Cuál prefieres?"

   **No hay opción (4) "vía web search" ni "vía conocimiento general del
   modelo".** Esas opciones quedan expresamente vetadas para todo escrito,
   dictamen, informe o respuesta a consulta jurídica generada bajo este
   plugin.

4. **No inventes jurisprudencia.** No inventes artículos. No inventes
   plazos. No inventes cuantías. No inventes ECLIs ni BOE-A. Si no tienes
   verificación de Robin, **no escribes la cita**. El hueco es honesto;
   la fabricación es mala praxis.

El letrado decide qué hacer ante el hueco. Tú nunca decides silenciosamente.


## Cross-skill handoffs

- **Antes de empezar:** `/robin:foral-check` si la materia es civil, mercantil, contratación, familia, sucesiones o inmobiliario.
- **Al cierre:** `/robin:jurisprudencia --norma <referencia>` para localizar la jurisprudencia que aplica la norma devuelta.
- **Si el usuario va a redactar:** sugerir la skill procesal correspondiente (`/robin:civil-demanda`, `/robin:tributario-recurso-reposicion`, etc.) en lugar de seguir consultando normas.

**Severity floor cruzado:** si una skill anterior calificó algo 🔴, esta
skill NO puede bajarlo a 🟢 sin justificar el cambio en una frase. Los
ratings de upstream son el suelo, no el techo.


## Lo que esta skill NO hace

- **No interpreta la norma ni la aplica al caso:** devuelve el texto literal vigente.
- **No sustituye al letrado en la decisión sobre qué norma aplicar.:** No sustituye al letrado en la decisión sobre qué norma aplicar.
- **No incluye normativa derogada salvo que se pida explícitamente con `--incluir-derogadas`.:** No incluye normativa derogada salvo que se pida explícitamente con `--incluir-derogadas`.
- **No fija criterios de despacho** (tono, costas, política de provisión):
  vienen del playbook editable en
  `~/.claude/plugins/config/claude-for-spanish-law/robin/CLAUDE.md`.
- **No decide estrategia**: la propone con razonamiento; el letrado decide.
- **No fabrica**: si Robin no devuelve un dato, esta skill no lo inventa.


## Closing action

Toda salida termina con:

> "Este resultado requiere revisión y validación de letrado colegiado
> antes de integrarse en un escrito, contrato o dictamen firmable."

Y con el árbol de próximos pasos (default — el despacho puede sobrescribir
en `## Política de cierre` del playbook):

> ¿Qué hacemos ahora?
> 1. **Profundizar** en uno de los hits/resultados (dime cuál).
> 2. **Encadenar** con otra skill (ver Cross-skill handoffs arriba).
> 3. **Volcar** el resultado al expediente del matter activo.
> 4. **Standby** — guardo y volvemos cuando decidas.
> 5. **Otra** — dime.

