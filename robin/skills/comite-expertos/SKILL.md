---
name: comite-expertos
description: >
  Convoca un panel de expertos multi-perspectiva para analizar una decisión,
  operación, escrito, oferta, activo o estrategia desde varios ángulos
  profesionales independientes y enfrentados, y después sintetiza consenso,
  discrepancias y una recomendación accionable. Cada perfil jurídico ancla sus
  citas en el MCP de Robin (buscar_*, obtener_*, verificar_cita, simular_oposicion,
  estimar_viabilidad_caso) — nunca de memoria. Úsala SIEMPRE que el usuario pida
  "opinión del comité de expertos", "panel de expertos", "comité", "varios puntos
  de vista", "opinión multidisciplinar", "que lo miren distintos perfiles",
  "devil's advocate múltiple", "mesa redonda", o cuando plantee una decisión de
  calado (¿presento este escrito?, ¿lanzo esta oferta?, ¿compro este activo?,
  ¿acepto este convenio?, ¿qué estrategia sigo?) y convenga contrastarla desde
  perfiles distintos (concursalista, fiscalista, litigador, MD de fondo distressed,
  asesor de la AC, urbanista, laboralista, magistrado hipotético, etc.). Dispárala
  también cuando el usuario quiera estresar una tesis única contrastándola con
  perfiles que discrepen, aunque no diga literalmente "comité".
argument-hint: "[decisión, operación, escrito u oferta a someter al panel]"
---

# /robin:comite-expertos

Convocar un panel de perfiles profesionales distintos, hacer que cada uno analice
**el mismo asunto desde su vértice de forma independiente**, y después sintetizar
dónde coinciden, dónde chocan y qué se decide. El valor no está en sumar
opiniones: está en **provocar el desacuerdo genuino** que un único analista tiende
a suavizar, y en obligar a cada perfil a defender su lectura antes de conocer la de
los demás.

## Cuándo aporta

Un solo hilo de razonamiento converge demasiado rápido y hereda un sesgo (el del
que redacta). Un panel bien montado descompone el problema en las tensiones reales
del asunto: lo que es óptimo para el fiscalista puede ser suicida para el
litigador; lo que maximiza recuperación puede disparar riesgo de calificación.
Sacar esas tensiones a la luz **antes** de decidir es el objetivo.

## Regla dura — el panel no cita de memoria

Este es el foso de Robin frente a un LLM suelto: **cada voz jurídica se ancla en el
corpus verificable de Robin**. Ningún perfil sostiene una norma, una sentencia, un
plazo o una cuantía sin haberla pasado por una tool de Robin. Si Robin devuelve
`hits=[]` o `existe=false`, el perfil lo dice y **no usa esa cita** (ver
§ *No silent supplement*). Un panel de cinco voces alucinando ECLIs no es un
comité: es cinco veces el mismo riesgo.

## Pipeline

1. **Base factual común (si hay expediente).** Si el asunto trae documentos o
   hechos, `mcp__robin__analizar_expediente` primero, para que todos los perfiles
   partan de los mismos hechos y no discutan sobre bases distintas. Complementa con
   `mcp__robin__cronologia_hechos` o `mcp__robin__mapa_documental` si el asunto es
   procesal.

2. **Selecciona los perfiles según el asunto (no una plantilla fija).** Entre 3 y 5
   perfiles con **intereses o criterios legítimamente enfrentados** sobre este
   asunto concreto. Perfiles redundantes (dos que dirían lo mismo) desperdician el
   ejercicio. Guíate por la materia:
   - **Operación distressed / NPL / compra de deuda:** MD de fondo de special
     situations, asesor de la AC / acreedor privilegiado, fiscalista de la
     estructura, litigador de rescisorias.
   - **Escrito o estrategia procesal (incl. Pieza Sexta):** letrado director del
     frente, litigador de la contraparte (que ataca el escrito), magistrado
     hipotético que lo va a resolver, y —si hay exposición personal del usuario— un
     asesor que vela por su posición individual, no por "el grupo".
   - **Activo inmobiliario / subasta:** director de inversión, urbanista/técnico,
     fiscalista de adquisición, gestor de riesgo posesorio y de cargas.
   - **M&A / SPA:** MD de PE (comprador), socio de M&A del vendedor, fiscalista de
     neutralidad, laboralista de contingencias (art. 44 ET).
   - **Convenio / plan de reestructuración:** AC, acreedor disidente, deudor,
     asesor financiero.

   Nombra explícitamente el panel al empezar, con una línea de por qué cada perfil
   está en la mesa.

3. **Cada experto interviene por separado, con voz propia y anclado en Robin.**
   Cada perfil emite su análisis **desde su función**, sin diplomacia de comité,
   tomando posición. Y cada afirmación jurídica se apoya en la tool que
   corresponda:
   - Norma o articulado → `mcp__robin__buscar_normativa` /
     `mcp__robin__obtener_articulo_ley` (vigencia y pinpoint).
   - Jurisprudencia → `mcp__robin__buscar_jurisprudencia` (y
     `buscar_tjue`/`buscar_tedh`/`buscar_tc`/extranjera según toque).
   - El **litigador de la contraparte** monta su ataque con
     `mcp__robin__simular_oposicion` o `mcp__robin__analizar_escrito_contraparte`.
   - Números de viabilidad → `mcp__robin__estimar_viabilidad_caso`.
   - Plazos, prescripción, preclusión → `mcp__robin__calculo_plazos`.
   - Doctrina de reguladores (AEPD, CNMC, CNMV, BdE, DGT, TEAC…) →
     `mcp__robin__buscar_doctrina_general` o la tool sectorial.

   Para cada perfil:
   - **Tesis** en una frase (¿a favor, en contra, condicionado?).
   - **Lo que ve que los demás no** — el ángulo específico de su vértice.
   - **Riesgos o líneas rojas** que detecta desde su especialidad.
   - **Su recomendación** concreta, con las citas de Robin que la sostienen.

   No homogenices la voz: el litigador de la contraparte suena hostil, el
   fiscalista prudente, el MD del fondo frío con los números. Si dos perfiles
   llegarían a la misma conclusión, uno sobra: sustitúyelo por otro que tensione.

4. **Verifica TODAS las citas** que hayan usado los perfiles con
   `mcp__robin__verificar_cita` antes de pasar a la síntesis. Una cita que no pasa,
   cae.

5. **Síntesis** — el output que de verdad importa (ver Formato).

## Formato

```
👥 Comité de expertos — [asunto]

Panel convocado: [perfil 1], [perfil 2], … — [una línea de por qué estos]

[Perfil 1 — p. ej. MD fondo distressed]
- Tesis: …
- Ángulo propio: …
- Riesgos / líneas rojas: …
- Recomendación: … [con citas robin-verified]

[Perfil 2] … (ídem para cada perfil)

Síntesis
- Consenso: … (lo que comparten perfiles enfrentados — lo más sólido)
- Discrepancias sustanciales: … (dónde chocan y qué asume cada uno; no las
  resuelvas artificialmente)
- Recomendación integrada: … (a qué perfil doy más peso en este caso y por qué;
  mójate — el usuario quiere una decisión, no un empate)
- Condiciones y próximos pasos: … (qué verificar, blindar o negociar)
```

Ajusta la profundidad al peso de la decisión: 3 voces breves para una cuestión
acotada; 5 voces desarrolladas + síntesis extensa para una operación o un escrito
de calado. Registro técnico alto, castellano peninsular, sin preámbulos.

## Source attribution tiering — Robin es la única fuente

Toda cita en el output procede de Robin (o del propio letrado). Si no encaja en uno
de estos cuatro tags, **se elimina** — no se sustituye por conocimiento del modelo
ni por búsqueda web:

| Tag | Cuándo usar |
|---|---|
| `[robin-verified]` | Pasó `mcp__robin__verificar_cita`. Confianza alta. |
| `[robin-verbatim]` | Pinpoint literal leído en `mcp__robin__obtener_sentencia_completa` o `mcp__robin__obtener_articulo_ley` (FJ X / art. Z apartado N). |
| `[robin-corpus]` | Devuelta por una tool `buscar_*` pero no re-verificada — usable en panorámica, no para apoyo argumental directo de un perfil. |
| `[user-provided]` | Citada por el letrado en el input. No alterar; verifícala en Robin y márcala `[user-provided · robin-verified]` si pasa. |

**Prohibido**: `[model-knowledge]`, `[web-search]` o cualquier tag que admita la
memoria del modelo o una fuente externa como sustituto de Robin.

## No silent supplement — Robin va a misa

1. **Si Robin devuelve dato → ese dato es la verdad operativa.** Si crees que Robin
   se equivoca, repórtalo al letrado; nunca lo sustituyas por tu recuerdo.
2. **Si Robin devuelve `hits=[]` o `existe=false` → NO HAY CITA.** El perfil que la
   quería usar declara la ausencia y prescinde de ella. No se rellena con
   conocimiento general ni con web. Una cita verosímil pero inventada es mala
   praxis que asume el letrado — no se corre ese riesgo.
3. **Ante el hueco**, ofrece al letrado: (1) reformular la búsqueda; (2) probar otra
   tool de Robin más específica; (3) dejar la tesis del perfil sin esa cita y
   marcarlo. No hay opción "vía web" ni "vía memoria del modelo".

## Foral check

Si el asunto es civil, mercantil, contratación, familia, sucesiones o inmobiliario
y hay punto de conexión foral (vecindad civil o sito del inmueble en Cataluña,
Galicia, Aragón, Navarra, País Vasco, Baleares o C. Valenciana), lanza
`/robin:foral-check` y que el perfil aplique la Compilación foral PRIMERO; el CC
estatal es supletorio (art. 13.2 CC).

## Destination check

Antes de devolver el output, comprueba el destino. Si va a canal abierto, lista
amplia, contraparte o "todo el equipo", verifica si está dentro del círculo de
secreto profesional (art. 542.3 LOPJ + art. 5 EGAE). Si parece fuera, señálalo y
ofrece versión confidencial interna, versión sanitizada, o ambas. Nunca metas
silenciosamente cabecera de secreto profesional en un texto que va a publicarse.

## Matter context

Lee `## Matter workspaces` en
`~/.claude/plugins/config/claude-for-spanish-law/robin/CLAUDE.md`. Si dice
`Habilitado: ✗` (default para asesoría interna), salta este bloque — opera a nivel
practice. Si está habilitado y no hay matter activo, pregunta: "¿En qué asunto va
esto? Ejecuta `/robin:matter-workspace switch <slug>` o di `practice-level`." Carga
`matter.md` del matter activo. Guarda outputs en
`~/.claude/plugins/config/claude-for-spanish-law/robin/matters/<slug>/`. Nunca leas
archivos de otro matter salvo que `Cross-matter context` esté `on`.

## Cross-skill handoffs

- **Antes:** `/robin:foral-check` si la materia lo pide.
- **Como un perfil más:** `/robin:analisis-pre-mortem` sobre la opción que el panel
  recomiende — el comité elige el camino, el pre-mortem lo estresa.
- **Si el asunto es un escrito propio:** `/robin:civil-simular-oposicion` alimenta
  la voz del litigador de la contraparte.
- **Al cierre:** `/robin:verificar-citas` sobre el material citado.

## Antipatrones

- **Consenso de cartón:** cinco perfiles que dicen lo mismo con otras palabras. Si
  pasa, elegiste mal los perfiles — reformula con vértices enfrentados.
- **Voz única disfrazada:** todos suenan igual. Cada perfil piensa distinto porque
  le pagan por proteger cosas distintas.
- **Empate cómodo:** terminar sin recomendación. La síntesis debe mojarse.
- **Perfil de relleno:** un "experto en X" que no cambia nada. Fuera.
- **Panel que alucina:** un perfil citando de memoria. Sin `verificar_cita`, la
  cita no existe.

## Lo que esta skill NO hace

- **No decide por el letrado:** propone una recomendación integrada razonada; el
  letrado decide.
- **No fabrica:** si Robin no devuelve un dato, ningún perfil lo inventa.
- **No fija criterios de despacho** (tono, costas, política de provisión): vienen
  del playbook editable en el `CLAUDE.md` del plugin.

## Closing action

Cuando el panel toca materia jurídica, cierra con el árbol de próximos pasos
(default — el despacho puede sobrescribir en `## Política de cierre` del playbook):

> ¿Qué hacemos ahora?
> 1. **Ejecutar** la recomendación integrada (dime y preparo el entregable).
> 2. **Pre-mortem** de la opción elegida antes de comprometerse.
> 3. **Reconvocar** el panel con otro perfil o con hechos nuevos.
> 4. **Escalar a socio** para decisión.
> 5. **Standby** — guardo en el matter y volvemos cuando decidas.
