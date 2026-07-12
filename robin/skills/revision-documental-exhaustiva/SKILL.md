---
name: revision-documental-exhaustiva
description: >
  Revisión exhaustiva documento a documento de un data room o expediente
  completo con Robin Search (búsqueda documental local): recorre TODOS los
  ficheros —no el top-K semántico—, extrae hallazgos con traza fichero+página,
  lleva un ledger de cobertura, y entrega un informe con garantía de que no se
  ha saltado ningún documento. Habilita due diligence documental, revisión de
  contratos en masa y doc review de litigios. Delega el análisis jurídico
  especializado en la skill de materia (M&A → societario-due-diligence).
argument-hint: "[objetivo de la revisión + carpeta/caso + materia si se conoce]"
---

# /robin:revision-documental-exhaustiva

Skill de **cobertura total**. Donde `buscar_documentos` trae lo más relevante
(búsqueda dirigida), esta skill garantiza que **cada documento del expediente se
lee de principio a fin**. Es la capa de workflow que convierte "responde
preguntas sobre tus documentos" en "revisa todo el expediente y dime qué hay".

## Requisito previo

El expediente debe estar indexado en **Robin Search** (el conector de búsqueda
documental local; los documentos nunca salen del equipo). Si el letrado no lo
tiene conectado, o la carpeta del caso no está indexada, dilo y para: sin índice
local no hay data room que recorrer. Herramientas del conector Robin Search que
usa esta skill (el prefijo MCP exacto lo resuelve el cliente):
`listar_documentos_indexados`, `obtener_documento`, `buscar_documentos`.

## Pipeline

### Fase 1 — Inventario del data room

1. `listar_documentos_indexados` (con `carpeta_filtro` si el letrado acota a un
   caso o subcarpeta concreta). Obtienes el total `N` de documentos, su
   `ruta_relativa`, `paginas`, `fragmentos` y la marca `sin_ocr`.
2. Construye el **registro de cobertura**: una fila por documento con estado
   inicial `pendiente`. Los documentos `sin_ocr = true` son PDFs escaneados aún
   sin capa de texto — márcalos `sin_ocr_pendiente` y trátalos como **hueco de
   cobertura**, no como revisados (avisa al letrado de que reindexe con OCR o
   los aporte en texto).
3. Anuncia el alcance al letrado antes de empezar: "He localizado N documentos
   (M sin OCR). Voy a revisarlos uno a uno; te aviso al terminar con el mapa de
   cobertura." Si `N` es grande, procesa por tandas y persiste el ledger (ver
   § *Ledger y escala*).

### Fase 2 — Barrido exhaustivo, documento a documento (map)

Por CADA documento con estado `pendiente`:

1. `obtener_documento` con su `doc_id`. Si `siguiente_fragmento` no es `null`,
   **vuelve a llamar** con `desde_fragmento = siguiente_fragmento` hasta agotar
   el documento. No te quedes con la primera ventana: la exhaustividad depende
   de leerlo entero.
2. Extrae un **registro estructurado** del documento:
   - Tipo/naturaleza (contrato, escritura, sentencia, nómina, cuentas, correo…).
   - Partes intervinientes.
   - Fechas clave (firma, vencimiento, efectos, prescripción).
   - Importes y magnitudes relevantes.
   - Cláusulas o hitos sensibles (cambio de control, no competencia, garantías,
     resolución, exclusividad, penalizaciones, avales).
   - **Hallazgos / red flags**, cada uno con su cita `fichero + pág.`.
3. Vuelca el registro al ledger y marca el documento `revisado`.

Cita siempre con la traza que devuelve Robin Search: `[fichero, pág. X]`. Nunca
atribuyas un hallazgo sin el documento y la página de los que sale.

### Fase 3 — Clasificación y handoff al análisis de materia

Con el data room ya leído, clasifica el conjunto por materia y **delega el
análisis jurídico especializado** en la skill que corresponda, pasándole los
hallazgos ya extraídos (no la hagas empezar de cero):

- **Compraventa de sociedad / M&A** → `/robin:societario-due-diligence`
  (cruza con TEAC/AEPD/BORME, R&W, deal breakers).
- **Cartera de contratos** → `/robin:contrato-revisar` por cada contrato
  material (cláusulas abusivas, riesgos, cobertura normativa).
- **Litigio / expediente contencioso** → análisis del escrito de contraparte,
  cronología procesal y mapa documental.
- **Compliance** → `auditar_compliance_penal_corporativo` / `_aml` /
  `_whistleblowing` / `_rgpd` según lo que aflore.

Si no encaja en una materia clara, sigue tú con el análisis genérico y señálalo.

### Fase 4 — Cruce con fuentes oficiales (verificación)

Contrasta los hallazgos con las fuentes públicas de Robin: `mcp__robin__buscar_aepd`
/ `_teac` / `_jurisprudencia` por la entidad o el objeto, y `mcp__robin__verificar_cita`
sobre toda cita jurídica del informe. Inconsistencias entre el data room y los
registros públicos (BORME, AEPD, RPM) son **red flag automático**.

### Fase 5 — Informe con garantía de cobertura (reduce)

Reduce el ledger a un informe único (formato abajo). **Obligatorio**: cerrar con
el bloque de cobertura — es el antídoto contra el "se me escapó algo".

## Garantía de cobertura (no opcional)

El informe SIEMPRE termina con un recuento explícito:

```
📊 Cobertura de la revisión
Documentos en el expediente: N
Revisados íntegramente:       N  (100%)   ← debe cuadrar
Sin OCR (pendientes):         M  → [lista]
No revisados:                 0            ← si ≠ 0, EXPLICA por qué y para
Ítems de checklist sin soporte documental en el data room: [lista]
```

Si `revisados ≠ N − M`, **no cierres el informe**: reanuda el barrido de los
documentos que falten. Un informe de cobertura que no cuadra es un informe que
miente. Si un documento no se puede leer (corrupto, formato no soportado),
decláralo como hueco, nunca lo des por revisado en silencio.

## Ledger y escala

Un data room grande no cabe en contexto ni leyéndolo documento a documento. Por
eso el barrido es map-reduce:

- Procesa en **tandas** (p. ej. 10-15 documentos) y **persiste el ledger** en el
  matter workspace activo (`ledger-cobertura.md`) tras cada tanda, para poder
  reanudar sin perder lo revisado.
- El ledger es la fuente de verdad de la cobertura; el informe final se compone
  del ledger, no de lo que quede en contexto.
- No cargues documentos enteros en contexto más allá de lo necesario para
  extraer su registro: extrae, vuelca al ledger, libera.

## Formato del informe

```
🔍 Revisión documental exhaustiva — [objeto]

Resumen ejecutivo
[5-7 líneas: qué es el expediente, hallazgos más graves, recomendación]

Hallazgos por severidad
🔴 CRÍTICO
  1. […] [fichero, pág. X]
🟠 ALTO
  1. […] [fichero, pág. X]
🟡 MEDIO
🟢 BAJO / constatación

Inventario documental (qué hay)
[tabla: documento · tipo · partes · fechas clave · estado]

Análisis por materia
[▶ por cada materia detectada — el output de la skill especializada]

Documentación pendiente / huecos
[docs sin OCR, docs esperables que no están en el data room]

📊 Cobertura de la revisión
[el bloque obligatorio de arriba]
```

## Matter context

**Matter context.** Lee `## Matter workspaces` en
`~/.claude/plugins/config/claude-for-spanish-law/robin/CLAUDE.md`. Si la sección
dice `Habilitado: ✗` (default para asesoría jurídica interna), salta este bloque
— la skill opera a nivel practice. Si está habilitado y no hay matter activo,
pregunta: "¿En qué asunto va esto? Ejecuta `/robin:matter-workspace switch <slug>`
o di `practice-level`." Carga `matter.md` del matter activo para contexto y
overrides, y guarda el ledger y el informe en
`~/.claude/plugins/config/claude-for-spanish-law/robin/matters/<slug>/`. Nunca
leas archivos de otro matter salvo que `Cross-matter context` esté explícitamente
`on`.

## Destination check

Antes de devolver el output, comprueba el destino. Si el letrado ha nombrado
canal, lista de distribución, contraparte o "todo el equipo", verifica si está
dentro del círculo de secreto profesional (art. 542.3 LOPJ + art. 5 EGAE). Un
informe de revisión de un data room es work product altamente confidencial:
canales corporativos abiertos, listas amplias, contraparte/letrado adverso,
proveedores y clientes rompen el secreto. Si el destino parece fuera del círculo,
señálalo y ofrece: (a) versión confidencial para uso interno del despacho,
(b) versión sanitizada para el canal amplio, (c) ambas. No metas silenciosamente
cabecera de secreto profesional en un texto que va a publicarse — ese header
pierde protección al salir del círculo.

## Source attribution tiering — Robin es la única fuente

Toda cita jurídica del output procede de Robin (o del propio letrado); todo
hallazgo documental procede de un documento leído con Robin Search, con su
`fichero + pág.`. Si una afirmación no encaja en uno de estos tags, **se elimina**
— no se sustituye por conocimiento del modelo ni por búsqueda web:

| Tag | Cuándo usar |
|---|---|
| `[robin-search]` | Hallazgo extraído de un documento del data room leído con `obtener_documento`. Cita `fichero + pág.` |
| `[robin-verified]` | Cita jurídica que pasó `mcp__robin__verificar_cita`. |
| `[robin-verbatim]` | Pinpoint literal leído en `mcp__robin__obtener_sentencia_completa` / `obtener_articulo_ley`. |
| `[robin-corpus]` | Devuelta por una tool `buscar_*` de Robin, no re-verificada. |
| `[user-provided]` | Aportada por el letrado. Verifícala en Robin como cortesía. |

**Prohibido** `[model-knowledge]`, `[web-search]` o cualquier tag que admita la
memoria del modelo como sustituto. Nunca colapses los tags.

## No silent supplement — Robin va a misa

1. **Si un documento o una tool de Robin devuelve dato → ese dato es la verdad
   operativa.** No lo contrastes contra tu memoria; si crees que Robin se
   equivoca, repórtalo al letrado y que él decida.
2. **Si Robin devuelve `hits=[]` / `existe=false`, o el documento no dice algo →
   NO HAY DATO.** No rellenes con conocimiento general. Declara la ausencia y
   para.
3. **No inventes.** No inventes cláusulas que no están en el documento, ni
   fechas, ni importes, ni jurisprudencia, ni ECLIs. Un hueco es honesto; la
   fabricación es mala praxis y responsabilidad profesional del letrado.

El letrado decide qué hacer ante el hueco. Tú nunca decides en silencio.

## Foral check

Si de la revisión sale materia civil, mercantil, contratación, familia,
sucesiones o inmobiliario con punto de conexión foral (vecindad civil o sito del
inmueble en Cataluña, Galicia, Aragón, Navarra, País Vasco, Baleares o Comunidad
Valenciana), lanza `/robin:foral-check` y aplica la Compilación foral PRIMERO; el
CC estatal es supletorio (art. 13.2 CC).

## Lo que esta skill NO hace

- **No firma** ni **presenta**: el letrado firma y el despacho presenta
  (art. 542 LOPJ).
- **No sustituye al letrado**: propone hallazgos y riesgos con su traza; el
  letrado valora y decide.
- **No accede a nada que no esté indexado en Robin Search**: solo ve el data room
  que el letrado ha puesto en la carpeta local. Lo que no está indexado, no
  existe para la revisión — dilo.
- **No fabrica**: si un documento no lo dice, la skill no lo inventa.

## Closing action

Toda salida termina con:

> "Esta revisión es un apoyo al análisis del letrado; requiere su validación y,
> en su caso, firma antes de emplearse frente al cliente, la contraparte o en
> sede judicial o administrativa."

Y con el árbol de próximos pasos (default — el despacho puede sobrescribir en
`## Política de cierre` del playbook):

> ¿Qué hacemos ahora?
> 1. **Profundizar** en un hallazgo o documento concreto (dime cuál).
> 2. **Análisis de materia** completo (M&A, contratos, litigio) sobre lo hallado.
> 3. **Resolver huecos**: reindexar con OCR o pedir los documentos que faltan.
> 4. **Escalar a socio** para revisión.
> 5. **Standby** — guardo el ledger en el matter y retomamos cuando decidas.
