---
name: civil-contestacion
description: >
  Contestación a demanda civil. Excepciones procesales si proceden, hechos
  numerados rebatiendo punto por punto, fundamentos jurídicos, súplica.
  Análisis previo del escrito del actor obligatorio.
argument-hint: "[pega la demanda del actor o describe sus hechos y peticiones]"
---

# /robin:civil-contestacion

Pipeline:

1. **Análisis del escrito del actor**.
   `/robin:civil-analizar-escrito` sobre la demanda. Obtienes: hechos
   admitidos / negados / aclarados (estructura art. 405 LEC), tesis
   del actor, debilidades estructurales, citas a verificar.

2. **Verifica las citas del actor**. `mcp__robin__verificar_cita`
   sobre cada ECLI/artículo. Cualquier cita inventada o derogada =
   munición a tu favor; menciónalo en la contestación.

3. **Foral-check**. Si rama civil/familia/inmobiliario, lanzar
   `/robin:foral-check`.

4. **Excepciones procesales**. Detecta posibles excepciones (art.
   416 LEC): falta de jurisdicción, competencia objetiva o
   territorial, litispendencia, cosa juzgada, defecto legal en modo
   de proponer la demanda, falta de legitimación, prescripción /
   caducidad. **Aliéganlas SIEMPRE antes del fondo.**

5. **Llama a `mcp__robin__preparar_contestacion`** con los hechos +
   la tesis defensiva. Recibirás esqueleto con hechos
   admitidos/negados/aclarados + fundamentos jurídicos.

6. **Reconvención**. Pregunta si procede (art. 406 LEC). Si sí,
   `/robin:civil-reconvencion` en paralelo.

7. **Refuerza con jurisprudencia contraria a la tesis del actor**.
   `/robin:jurisprudencia` con la tesis del actor + filtro
   `--norma <referencia>` para sentencias que apliquen el mismo
   precepto en sentido contrario.

8. **Verifica TODAS las citas propias** antes de cerrar.

9. **Persiste** en matter activo.

## Formato

Estructura LEC art. 405:

```
AL TRIBUNAL DE INSTANCIA DE [partido judicial], SECCIÓN CIVIL, Nº [N]

Procedimiento: Juicio [ordinario/verbal] [nº/año]
Demandante: […]
Demandado: […]

Don/Doña [letrado], ICAM [nº], en nombre y representación de
[demandado] según poder […]

CONTESTACIÓN A LA DEMANDA

EXCEPCIONES PROCESALES

[Si proceden, antes del fondo]

HECHOS

Por el orden correlativo de la demanda:
Primero. — [admitido / negado / matizado]. [Razón si procede]
Segundo. — […]
…

FUNDAMENTOS JURÍDICOS

I. Procesales (respondiendo a los del actor).
II. De fondo.
   1. [Norma + jurisprudencia con ECLI rebatiendo la tesis del actor]
   2. […]
III. Costas. Petición de imposición al actor por temeridad o mala fe
     si procede (art. 394.2 LEC).

SUPLICA AL TRIBUNAL DE INSTANCIA

Que tenga por presentada esta contestación, se sirva admitirla y,
tras los trámites legales, dicte sentencia desestimando íntegramente
la demanda, con imposición de costas al actor.

[OTROSÍES si proceden]

En [lugar], a [fecha]
[firma letrado]
```

Cierre con:
- **Citas verificadas** (propias y del actor).
- **Citas del actor que NO verifican** (lista separada — usable
  para alegato oral).
- **Avisos**.

## Avisos típicos

- Si la cuantía discutida es superior a la fijada por el actor →
  excepción de inadecuación de procedimiento.
- Si el actor cita normativa derogada como vigente → mencionar
  expresamente y proponer norma vigente.
- Si la prescripción es discutible → preferible alegarla en
  contestación y no esperar a la audiencia previa.

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

