---
name: analisis-pre-mortem
description: >
  Ejecuta un análisis pre-mortem: asume que la operación, escrito, estrategia,
  inversión o proyecto YA HA FRACASADO en un horizonte futuro y razona hacia atrás
  las causas del fracaso, ordenándolas por probabilidad × impacto, con señales
  tempranas (tripwires) y mitigaciones. Cada modo de fallo con sustancia jurídica se
  verifica en el MCP de Robin (¿la norma sigue vigente?, ¿hay jurisprudencia
  contraria?, ¿el plazo está precluido?) — nunca de memoria. Úsala SIEMPRE que el
  usuario pida "pre-mortem", "premortem", "análisis pre-mortem", "asume que ha
  salido mal", "por qué podría fracasar", "qué puede salir mal", "stress-test de
  riesgos", "red team esto", "antes de presentar/lanzar/comprar dime los riesgos", o
  cuando esté a punto de tomar una decisión de calado (presentar un escrito, lanzar
  una oferta de levantamiento, comprar deuda o un activo, aceptar un convenio, firmar
  un SPA) y convenga estresarla antes de comprometerse. Dispárala también cuando
  detectes exceso de optimismo en un plan y ayude anticipar los modos de fallo,
  aunque el usuario no diga "pre-mortem".
argument-hint: "[operación, escrito o decisión a estresar antes de comprometerse]"
---

# /robin:analisis-pre-mortem

Un pre-mortem invierte la pregunta. En vez de "¿qué riesgos tiene esto?" —que
invita a listar preocupaciones tibias— se parte de un hecho consumado: **estamos en
el futuro y la operación ha fracasado sin paliativos**. Desde ahí se razona hacia
atrás: *¿qué ocurrió para que llegáramos aquí?* El marco desbloquea el sesgo de
optimismo y el compromiso emocional con el plan propio: es más honesto explicar un
fracaso ya sucedido que admitir que el plan vivo puede tener grietas.

## El encuadre — hazlo explícito al empezar

Fija un **horizonte y un escenario de fracaso concretos**. No "podría ir mal", sino:
*"Es [fecha realista]. La [operación/escrito/inversión] ha fracasado: [qué significa
fracaso aquí — se desestimó, no se vendió en plazo, la calificación fue culpable, la
recuperación quedó por debajo del coste]. Reconstruimos por qué."*

Horizontes por defecto:

- **Operaciones RE / NPL / distressed:** máximo 12 meses entre compra y venta (regla
  de tempo). Fracaso típico: *no haber vendido en plazo* o recuperación por debajo de
  la tesis.
- **Escritos y frentes procesales:** el hito de resolución relevante (auto,
  sentencia, calificación). Cuidado especial con **exposición personal** del usuario
  (p. ej. personado en Pieza Sexta): un modo de fallo es que la estrategia buena
  "para el grupo" perjudique su posición individual.
- **M&A / SPA:** el cierre y la ventana de *claims* posterior.

## Regla dura — los modos de fallo jurídicos se verifican en Robin

Un pre-mortem que se apoya en "creo que la norma es X" o "me suena una sentencia
contraria" no estresa nada: hereda el mismo riesgo de alucinación que quiere evitar.
**Todo modo de fallo con sustancia jurídica pasa por una tool de Robin.** Si Robin
devuelve `hits=[]` o `existe=false`, eso *también es información* del pre-mortem
(p. ej. "no consta jurisprudencia que respalde nuestra tesis" es en sí un modo de
fallo), pero no se rellena con memoria del modelo (ver § *No silent supplement*).

## Pipeline

1. **Base factual (si hay expediente).** Si el asunto trae documentos/hechos,
   `mcp__robin__analizar_expediente` y, en procesal, `mcp__robin__cronologia_hechos`
   para fijar los hitos reales sobre los que razonar el fracaso.

2. **Genera los modos de fallo — barrido sistemático, no por ocurrencia.** Recorre
   al menos estas familias y quédate con las que apliquen, anclando cada una en la
   tool de Robin que la sostiene o la refuta:
   - **Sustantivas / jurídicas:** tesis de fondo débil, norma derogada o mal citada,
     prueba insuficiente, plazo precluido, órgano equivocado. → Vigencia con
     `mcp__robin__obtener_articulo_ley`; jurisprudencia contraria con
     `mcp__robin__buscar_jurisprudencia`; plazos con `mcp__robin__calculo_plazos`.
   - **De contraparte / adversario:** qué hizo el otro lado que no anticipamos
     (oposición, recurso, rescisoria, mejor postor). → `mcp__robin__simular_oposicion`
     o `mcp__robin__analizar_escrito_contraparte`.
   - **Financieras / de mercado:** el activo no se vendió al precio/plazo previsto,
     coste oculto (cargas, fiscalidad, posesorio), tipos o liquidez. → cuantías con
     las calculadoras de Robin (`calcular_*`) donde apliquen.
   - **De ejecución / operativas:** dependencia de un tercero que falló, documentación
     que no llegó, coordinación entre frentes (penal↔concursal) contradictoria.
   - **De gobernanza / personales:** conflicto de interés, persona vinculada,
     exposición del usuario, incoherencia entre lo dicho en un procedimiento y en otro.
   - **Externas / de cola:** cambio normativo, resolución sorpresa, actuación de un
     organismo (AEAT, AC, juzgado, regulador). → doctrina con
     `mcp__robin__buscar_doctrina_general` / tool sectorial.

3. **Contraste de viabilidad.** Cuando el asunto lo permita,
   `mcp__robin__estimar_viabilidad_caso` da el escenario adverso cuantificado que
   ancla el "fracaso consumado" en algo más que intuición.

4. **Verifica** con `mcp__robin__verificar_cita` toda cita que sustente un modo de
   fallo antes de tabularlo. Un asesino apoyado en una sentencia inventada no es un
   asesino: es ruido.

5. **Prioriza y tabula** (ver Formato).

## Prioriza — no todos los fallos pesan igual

Ordena por **probabilidad × impacto**. El objetivo no es una lista larga sino
identificar los **2-3 "asesinos"**: los modos de fallo que, solos, hunden la
operación. Para cada modo relevante:

- **Mecanismo:** la cadena causal concreta que lleva al fracaso.
- **Señal temprana (tripwire):** el indicio observable de que el fallo se
  materializa — para reaccionar antes del punto de no retorno.
- **Mitigación / pre-compromiso:** qué hacer *ahora* para reducir probabilidad o
  impacto, o qué decidir por anticipado si salta el tripwire.

## Formato

```
🔮 Pre-mortem — [asunto]

Escenario asumido: Es [fecha]. [Descripción del fracaso consumado].

Modos de fallo (ordenados por probabilidad × impacto)

| Causa | Mecanismo | Señal temprana | Prob. | Impacto | Mitigación / tripwire |
|-------|-----------|----------------|-------|---------|-----------------------|
| …     | …         | …              | A/M/B | A/M/B   | …                     |

Los asesinos (2-3)
Los fallos que por sí solos hunden la operación, desarrollados y con su cita
robin-verified cuando son jurídicos:
1. …

Pre-compromisos y próximos pasos
Qué blindar, verificar o decidir por anticipado antes de comprometerse.
```

Ajusta la profundidad al peso de la decisión. Registro técnico alto, castellano
peninsular, directo, sin disclaimers genéricos.

## Source attribution tiering — Robin es la única fuente

Toda cita que sustente un modo de fallo procede de Robin (o del propio letrado). Si
no encaja en uno de estos tags, **se elimina**:

| Tag | Cuándo usar |
|---|---|
| `[robin-verified]` | Pasó `mcp__robin__verificar_cita`. |
| `[robin-verbatim]` | Pinpoint literal leído en `mcp__robin__obtener_sentencia_completa` o `mcp__robin__obtener_articulo_ley`. |
| `[robin-corpus]` | Devuelta por `buscar_*`, no re-verificada — usable en panorámica, no como base de un asesino. |
| `[user-provided]` | Citada por el letrado. Verifícala en Robin; márcala `[user-provided · robin-verified]` si pasa. |

**Prohibido**: `[model-knowledge]`, `[web-search]` o cualquier tag que admita
memoria del modelo o fuente externa como sustituto de Robin.

## No silent supplement — Robin va a misa

1. **Si Robin devuelve dato → es la verdad operativa.** Si crees que se equivoca,
   repórtalo al letrado; no lo sustituyas por tu recuerdo.
2. **Si Robin devuelve `hits=[]` o `existe=false` → NO HAY CITA.** Declara la
   ausencia (que puede ser en sí un modo de fallo) y para. No rellenes con memoria ni
   con web.
3. **Ante el hueco**, ofrece: (1) reformular búsqueda; (2) probar otra tool de Robin;
   (3) tabular el modo de fallo como "no verificable con el corpus" y marcarlo. No
   hay opción "vía web" ni "vía memoria del modelo".

## Foral check

Si un modo de fallo depende de derecho civil, mercantil, familia, sucesiones o
inmobiliario con punto de conexión foral (Cataluña, Galicia, Aragón, Navarra, País
Vasco, Baleares, C. Valenciana), lanza `/robin:foral-check`: aplicar CC estatal donde
rige derecho foral es en sí un asesino silencioso (art. 13.2 CC).

## Destination check

Antes de devolver el output, comprueba el destino. Si va a canal abierto, lista
amplia, contraparte o "todo el equipo", verifica si está dentro del círculo de
secreto profesional (art. 542.3 LOPJ + art. 5 EGAE). Un pre-mortem expone
debilidades propias: fuera del círculo es munición para el adversario. Si el destino
parece fuera, señálalo y ofrece versión confidencial interna, sanitizada, o ambas.

## Matter context

Lee `## Matter workspaces` en
`~/.claude/plugins/config/claude-for-spanish-law/robin/CLAUDE.md`. Si dice
`Habilitado: ✗` (default para asesoría interna), salta este bloque. Si está
habilitado y no hay matter activo, pregunta: "¿En qué asunto va esto? Ejecuta
`/robin:matter-workspace switch <slug>` o di `practice-level`." Carga `matter.md` del
matter activo. Guarda outputs en
`~/.claude/plugins/config/claude-for-spanish-law/robin/matters/<slug>/`. Nunca leas
archivos de otro matter salvo que `Cross-matter context` esté `on`.

## Cross-skill handoffs

- **Antes:** `/robin:foral-check` si algún modo de fallo lo pide.
- **Complemento natural:** `/robin:comite-expertos` — el comité elige el camino,
  el pre-mortem lo estresa. Se encadenan bien en cualquier orden.
- **Si el asunto es un escrito propio:** `/robin:civil-simular-oposicion` para el
  frente de contraparte.
- **Al cierre:** `/robin:verificar-citas` sobre el material citado.

## Antipatrones

- **Lista de la compra:** veinte riesgos genéricos sin jerarquía. El valor está en
  separar los asesinos del ruido.
- **Optimismo encubierto:** modos de fallo tibios ("podría haber cierto retraso") en
  vez de fracasos consumados ("no vendimos y el préstamo puente venció"). Comprométete
  con el fracaso: es la premisa.
- **Riesgos sin tripwire:** un riesgo que no puedes detectar a tiempo es
  inaccionable. Fuerza siempre la señal temprana.
- **Ignorar la exposición personal:** en asuntos del grupo, el fracaso "del grupo" y
  el "del usuario" no coinciden. Sepáralos.
- **Asesino inventado:** un modo de fallo apoyado en norma o sentencia no verificada.
  Sin Robin, no se tabula como jurídico.

## Lo que esta skill NO hace

- **No decide por el letrado:** identifica asesinos y mitigaciones; el letrado decide
  si sigue, blinda o aborta.
- **No fabrica:** si Robin no devuelve un dato, el modo de fallo se marca "no
  verificable", no se inventa.
- **No sustituye la due diligence:** un pre-mortem prioriza; la DD documenta.

## Closing action

Cuando el pre-mortem toca materia jurídica, cierra con el árbol de próximos pasos
(default — el despacho puede sobrescribir en `## Política de cierre` del playbook):

> ¿Qué hacemos ahora?
> 1. **Blindar** el asesino #1 con la mitigación propuesta (dime y lo preparo).
> 2. **Instalar los tripwires** como hitos de seguimiento en el matter.
> 3. **Comité de expertos** sobre la decisión de seguir / abortar.
> 4. **Escalar a socio** con los 2-3 asesinos como resumen ejecutivo.
> 5. **Standby** — guardo en el matter y volvemos cuando decidas.
