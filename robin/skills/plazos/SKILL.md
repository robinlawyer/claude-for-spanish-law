---
name: plazos
description: >
  Cómputo de plazos procesales y administrativos. Hábiles o naturales, con
  exclusión correcta de sábados, domingos, festivos estatales/autonómicos/
  locales y agosto inhábil cuando proceda. También plazos de prescripción y
  caducidad. Úsala antes de presentar cualquier escrito sujeto a plazo o
  cuando el letrado diga "cuánto plazo tengo", "se me ha pasado", "cuándo
  vence".
argument-hint: "[tipo de plazo + fecha de inicio + provincia/jurisdicción]"
---

# /robin:plazos

Cómputo exacto usando `mcp__robin__calculo_plazos`, que incorpora
calendarios laborales 2025-2026 (estatales + 17 autonómicos +
locales más relevantes) y las reglas de cómputo por norma procesal.

## Procedimiento

### 1. Identificar el tipo de plazo

| Tipo | Norma | Cómputo |
|---|---|---|
| **Civil (LEC)** | art. 133 LEC | Días hábiles judiciales. Agosto inhábil en general (art. 183 LOPJ) salvo actuaciones urgentes |
| **Penal (LECrim)** | art. 197 LECrim | Días hábiles judiciales. Agosto hábil para diligencias urgentes |
| **Laboral (LRJS)** | art. 43 LRJS | Días hábiles judiciales. Agosto inhábil salvo modalidades urgentes |
| **Contencioso (LJCA)** | art. 128 LJCA | Días hábiles. Agosto inhábil salvo procesos urgentes |
| **Administrativo (Ley 39/2015)** | arts. 30, 32, 33 | Días hábiles por defecto; meses o años, naturales |
| **Tributario (LGT)** | art. 30, 49.1 | Mes/año por defecto, naturales. Plazos en días, hábiles |
| **Concursal (TRLC)** | art. 519 | Hábiles judiciales |
| **Cómputo de prescripción civil** | art. 1969 CC + ley sectorial | Naturales desde dies a quo |
| **Caducidad** | norma sectorial | Naturales por defecto, salvo norma específica |
| **Procesal UE** | Reglamento procedimiento TJUE | Reglas propias |

### 2. Recoger datos críticos del usuario

- **Tipo de plazo** (de la tabla).
- **Fecha del hecho inicial** (notificación, presentación, dies a
  quo de prescripción, etc.).
- **Provincia / localidad** (para festivos locales).
- **Jurisdicción** (civil, penal, contencioso, social, mercantil).

Si falta dato y es crítico, pregunta. Una sola pregunta por dato.

### 3. Llamar a la tool

`mcp__robin__calculo_plazos` con:

```json
{
  "tipo_plazo": "civil_recurso_apelacion",
  "fecha_inicio": "2026-05-23",
  "duracion": 20,
  "unidad": "dias_habiles",
  "provincia": "barcelona",
  "jurisdiccion": "civil"
}
```

Para prescripciones / caducidades:

```json
{
  "tipo_plazo": "prescripcion_general_civil",
  "dies_a_quo": "2021-03-15",
  "duracion": 5,
  "unidad": "años"
}
```

### 4. Output

```
📅 Cómputo

Plazo: presentación de recurso de apelación civil
Fecha de notificación de la sentencia: 23 de mayo de 2026 (sábado)
Dies a quo: 25 de mayo de 2026 (lunes, primer día hábil siguiente)
Cómputo: 20 días hábiles
Jurisdicción: civil
Territorio: Barcelona (calendario estatal + autonómico Cataluña + local Barcelona)

Festivos / inhábiles dentro del plazo:
- 30 mayo (Día de Castilla y León — irrelevante)
- 5 junio (Corpus, festivo local Barcelona si procede)
- 24 junio (San Juan — festivo en Cataluña y Galicia)
- 29 junio (Día de San Pedro — festivo local en algunos municipios)

📌 Fecha límite de presentación: 23 de junio de 2026 (martes).

⚠️ Atención:
- Quedan 31 días corridos / 20 días hábiles.
- El despacho está cerrado del 1 al 15 de agosto. No afecta a este
  plazo concreto (vence en junio), pero ten presente para plazos que
  caigan en agosto.

Avisos:
✅ Verificado contra calendarios oficiales (CGPJ + CCAA + local).
```

### 5. Múltiples plazos en un caso

Si el usuario pega varias notificaciones o pasos procesales, Robin
calcula cada uno y los ordena en línea temporal. Útil al abrir matter:

```
📅 Plazos críticos del matter "acme-vs-tdc"

15 jun 2026 (mar) ⚠️ Contestación a demanda — vence en 12 días hábiles
23 jul 2026 (jue)    Audiencia previa
…
```

### 6. Avisos especiales

- **Agosto inhábil**: por defecto, civil/laboral/contencioso lo
  consideran inhábil. Penal NO en diligencias urgentes. Robin lo
  resuelve por jurisdicción.
- **Días con dos calendarios distintos**: en cómputo de plazos del
  partido judicial X y CCAA Y, prevalece el calendario judicial del
  CGPJ. Robin lo aplica correctamente.
- **Plazos en meses o años**: cuentan de fecha a fecha (art. 5 CC).
  Si el día equivalente no existe en el mes destino, último día del
  mes (típico 31 enero → 28/29 febrero).
- **Prescripción interrumpida por reclamación extrajudicial**: el
  letrado debe informar de la interrupción. Robin no la asume.

### 7. Integración con matter

Si hay matter activo, los plazos calculados se guardan en
`matter.md` del matter, sección "Plazos críticos", con marca de
urgencia (rojo si quedan ≤ 7 días, amarillo ≤ 30, verde > 30). El
agent `vigilancia-plazos` los revisa diariamente.

## Ejemplos

```
/robin:plazos
"He recibido el día 23 de mayo una sentencia desestimando la demanda
en juicio ordinario civil. ¿Hasta cuándo tengo para apelar? Estoy en
Madrid."
```

```
/robin:plazos
"Plazo de prescripción para reclamar daños por culpa
extracontractual del 10 de febrero de 2020."
```

```
/robin:plazos
"Plazo de 15 días para alegaciones en procedimiento sancionador
administrativo notificado el 1 de agosto. Sevilla."
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

- **Antes de empezar:** asegurarse de tener la fecha de notificación correcta — preguntarla al letrado si falta.
- **Al cierre:** las tools `mcp__robin__tasa_judicial` y `mcp__robin__deposito_recurso` si el plazo es para presentar recurso con tasa o depósito; o `/robin:calculadora` para encadenar el cálculo en una skill.

**Severity floor cruzado:** si una skill anterior calificó algo 🔴, esta
skill NO puede bajarlo a 🟢 sin justificar el cambio en una frase. Los
ratings de upstream son el suelo, no el techo.


## Lo que esta skill NO hace

- **No presenta nada en plazo:** calcula y avisa, pero la presentación es del despacho.
- **No sustituye al sistema de agenda del despacho:** el cómputo es puntual, no continuado.
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

