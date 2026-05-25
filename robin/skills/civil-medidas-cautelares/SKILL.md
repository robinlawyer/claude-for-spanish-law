---
name: civil-medidas-cautelares
description: >
  Solicitud de medidas cautelares (arts. 721 ss LEC). Embargo preventivo,
  anotación preventiva, intervención judicial, depósito, formación de
  inventario, cesación provisional, etc.
argument-hint: "[medida solicitada + fumus boni iuris + periculum in mora]"
---

# /robin:civil-medidas-cautelares

Pipeline:

1. **Verifica requisitos** (art. 728 LEC):
   - **Fumus boni iuris**: apariencia de buen derecho.
   - **Periculum in mora**: riesgo de demora.
   - **Caución**: proporcional al perjuicio que la medida puede
     causar.

2. **Identifica medida idónea** (art. 727 LEC):
   - Embargo preventivo (cuantías líquidas).
   - Anotación preventiva (registro: inmuebles, marcas, sociedades).
   - Intervención o administración judicial.
   - Depósito de cosa mueble.
   - Formación de inventario.
   - Cesación provisional de actividad o conducta.
   - Otras adecuadas según la pretensión.

3. **Procedimiento**: regla general inaudita parte si urgencia o
   inefectividad (art. 733 LEC); si no, vista previa (art. 734).

4. **`mcp__robin__preparar_acto_pre_procesal`** con tipo=medida_cautelar.

5. **Documentar el fumus y el periculum**. Si hay documentación que
   acredite ambos, listarla.

6. **Caución**: estimar importe razonable. Si hay urgencia que
   permita exonerar caución (raro), justificarlo.

7. **Plazo de presentación de demanda principal** si la cautelar se
   pide antes: 20 días desde adopción (art. 730.2 LEC).

## Formato

```
AL JUZGADO […]

[…] SOLICITO MEDIDAS CAUTELARES previas / coetáneas / posteriores a
la demanda principal […]

I. Medida solicitada: […]
II. Fumus boni iuris: […]
III. Periculum in mora: […]
IV. Caución ofrecida: […]
V. Razones de urgencia que justifican audiencia previa o, en su caso,
    inaudita parte: […]

SUPLICO […]
```

## Avisos típicos

- Inaudita parte: solo cuando la audiencia previa frustraría la
  efectividad de la medida. Requiere motivación reforzada.
- Si la medida afecta a tercero (banco con cuenta del demandado,
  registro), preparar oficios.
- Caución sustitutoria: el demandado puede sustituir la medida por
  caución equivalente (art. 746 LEC).

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

