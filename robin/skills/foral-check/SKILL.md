---
name: foral-check
description: >
  Detecta si un caso cae bajo derecho civil foral y qué norma aplica con
  prioridad sobre el CC estatal. Cubre Cataluña, Galicia, Aragón, Navarra,
  País Vasco, Baleares y lo recuperable de Valencia. Cualquier skill civil,
  mercantil, contratación, familia, sucesiones o inmobiliario que reciba
  hechos pasa por aquí antes de redactar.
argument-hint: "[descripción del caso con vecindad civil de las partes y sito de los bienes]"
---

# /robin:foral-check

Aplica la matriz foral de `references/foral-matrix.md` y devuelve la
norma aplicable con justificación de los puntos de conexión.

## Procedimiento

### 1. Recoger puntos de conexión

Del input del usuario, identifica:

- **Vecindad civil de las partes** (común / catalana / gallega /
  aragonesa / navarra / vasca / balear / valenciana / desconocida).
- **Lugar de celebración del negocio o residencia habitual** (CCAA).
- **Sito de los inmuebles** afectados (CCAA por inmueble).
- **Ley elegida** (si el contrato la tiene).
- **Lugar de cumplimiento** de las obligaciones.

Si falta dato relevante, **pregunta una vez por los datos críticos**
para resolver el conflicto. Si el usuario dice "no lo sé", asume
"vecindad común" como default seguro y márcalo en la respuesta como
"asumido, confirmar".

### 2. Aplicar reglas de conflicto

Aplica `references/foral-matrix.md` en este orden:

1. **Personalidad de la ley civil (art. 14 CC)**: vecindad civil
   determina ley personal. Aplica a sucesiones, capacidad, régimen
   económico matrimonial.

2. **Lex rei sitae**: inmuebles se rigen por la ley del lugar donde
   estén sitos.

3. **Ley elegida**: en contratos, lex voluntatis. En defecto, ley
   del lugar de cumplimiento (art. 10.5 CC).

4. **Conflicto entre forales**: vecindad civil del causante en
   sucesiones, del titular en derechos reales, de la parte cuyo
   estatuto personal sea relevante en otros casos.

### 3. Búsqueda específica

Para confirmar la norma foral aplicable:

- `mcp__robin__buscar_por_ccaa` con la materia (sucesiones, régimen
  matrimonial, derechos reales, contratos, etc.) y la CCAA cuya
  norma sospechas aplicable.
- Esto trae los artículos exactos de la Compilación foral con BOE-A
  o referencia oficial autonómica.

### 4. Output

```
🏛️ Análisis foral

Materia: sucesión testamentaria con bienes en Cataluña y Madrid.

Puntos de conexión detectados:
- Vecindad civil del causante: catalana (residencia 30 años en Barcelona).
- Inmuebles: piso en Barcelona + piso en Madrid.

Norma aplicable:
✅ Codi Civil de Catalunya, Llibre quart (Successions) — Llei 10/2008.
   - Materia personal del causante (vecindad civil catalana, art. 14 CC).
   - Aplica con prioridad sobre el CC estatal (art. 13.2 CC).

Aspectos sometidos al CCCat:
- Capacidad para testar (art. 421-3 CCCat).
- Cuantía y atribución de la legítima (arts. 451-1 ss CCCat) — legítima
  global del 25 % en Cataluña, no del tercio como en CC estatal.
- Forma del testamento (puede otorgarse testamento ológrafo, abierto o
  cerrado; los pactos sucesorios catalanes son válidos).
- Sucesión intestada si no hubiera testamento (orden de llamamientos
  del CCCat).

Aspectos que siguen otra ley:
- Tributación sucesoria del piso de Madrid: ISD madrileño (lex rei
  sitae no sucesoria, pero sí fiscal).
- Inscripción registral del piso de Madrid: Registro Propiedad Madrid,
  procedimiento del Reglamento Hipotecario estatal.

Citas verificadas:
- art. 13.2 CC — BOE-A-1889-4763 vigente.
- art. 14 CC — BOE-A-1889-4763 vigente.
- art. 421-3 CCCat — DOGC núm. 5217.
- art. 451-1 CCCat — DOGC núm. 5217.

Avisos al letrado:
⚠️ Si el testamento se otorgó antes del cambio de vecindad civil del
   causante a catalana, podría discutirse la ley aplicable
   (transitorias del CCCat).
⚠️ Si los herederos tienen vecindad civil distinta a la catalana, la
   partición sigue siendo catalana (ley del causante), pero la
   inscripción registral en Madrid puede requerir adaptaciones.
```

### 5. Cuando NO aplica derecho foral

Output:

```
🏛️ Análisis foral

Materia: …
Puntos de conexión detectados: …

Resultado: ❌ No aplica derecho foral. Ley aplicable: Código Civil estatal.

Razón: ninguna de las partes tiene vecindad civil foral, los bienes
están sitos en territorio común, y no hay punto de conexión adicional
que active foral.
```

### 6. Cuando la aplicabilidad es discutible

Algunos casos no son blanco/negro:

- Vecindad civil mixta en pareja (uno catalán, otra común): aplica
  art. 9.2 CC con elección o residencia habitual.
- Comunidad Valenciana en materias no cubiertas por Ley 6/2024.
- Vecindad civil adquirida por residencia continuada (art. 14.5 CC)
  sin manifestación expresa.

En estos casos:

```
Resultado: ⚠️ Aplicabilidad foral DISCUTIBLE.

Escenario A (probable): aplica CC estatal porque [razón].
Escenario B: podría defenderse aplicabilidad foral catalana porque [razón].

Recomendación: pregunte al cliente / aporte documentación que despeje
la duda antes de fijar estrategia.
```

### 7. Persistencia en matter

Si hay matter activo, el resultado del foral-check se guarda en
`matter.md` del matter, sección "Análisis foral". Las skills
posteriores del mismo matter no tienen que re-correrlo (salvo
`--redo`).

## Ejemplos

```
/robin:foral-check
Pareja catalana se va a casar. ¿Régimen económico aplicable? Ella
nacida en Lleida, él nacido en Madrid, residen en Barcelona desde
hace 12 años.
```

```
/robin:foral-check
Compraventa de mas en Girona entre vendedor catalán y comprador
francés. ¿Qué ley aplica?
```

```
/robin:foral-check
Cliente de Bilbao quiere testar dejando todo a su pareja sin hijos.
Vecindad civil vasca por residencia. ¿Tiene libertad de testar
completa?
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

- **Después de aplicar:** la skill procesal que toque ya con el régimen foral correcto cargado (sucesiones, familia, contratos, etc.).
- **Si la vecindad civil es dudosa:** pedir al letrado los datos del cliente antes de continuar — el régimen foral es no negociable.

**Severity floor cruzado:** si una skill anterior calificó algo 🔴, esta
skill NO puede bajarlo a 🟢 sin justificar el cambio en una frase. Los
ratings de upstream son el suelo, no el techo.


## Lo que esta skill NO hace

- **No decide la vecindad civil del cliente:** la deduce a partir de los datos del caso y avisa al letrado para confirmar.
- **No prepara escritos forales:** identifica el régimen aplicable y deriva a la skill procesal correspondiente.
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

