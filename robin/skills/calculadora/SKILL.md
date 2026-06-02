---
name: calculadora
description: >
  Acceso unificado a las 14 calculadoras procesales de Robin con auto-update
  IPC, IRAV, baremo tráfico y bases de cotización SS. Úsala cuando el letrado
  diga "calcula X" o pase datos cuantitativos sobre despido, alimentos,
  intereses, baremo, herencia, plusvalía, pena, costas, etc.
argument-hint: "[tipo de cálculo] [datos relevantes]"
---

# /robin:calculadora

Despacha al cálculo específico llamando a la tool correspondiente.

## Procedimiento

### 1. Identificar el tipo de cálculo

Si el usuario lo nombra (ej. "calcula la indemnización por despido"),
directo. Si no, pregunta:

> "¿Qué necesitas calcular?
> 1. Indemnización por despido (objetivo / disciplinario / colectivo)
> 2. Pensión de alimentos (CC o foral)
> 3. Pensión compensatoria
> 4. Intereses moratorios (CC, mercantil, ley morosidad, tributario)
> 5. Baremo de tráfico (Ley 35/2015 actualizada)
> 6. Pena (CP, atenuantes / agravantes)
> 7. Costas procesales (criterios ICAM/colegio del partido)
> 8. Tasa judicial
> 9. Depósito recurso
> 10. Herencia y legítimas (CC o foral)
> 11. Plusvalía municipal (post STC 182/2021)
> 12. Actualización de renta IRAV/IPC (LAU)
> 13. Prestación de la Seguridad Social (jubilación, IT, IP, viudedad)
> 14. Plazos procesales y prescripciones → /robin:plazos"

### 2. Mapear a tool

| Cálculo | Tool |
|---|---|
| Indemnización por despido | `mcp__robin__calcular_indemnizacion_despido` |
| Pensión alimentos | `mcp__robin__calcular_pension_alimentos` |
| Pensión compensatoria | `mcp__robin__calcular_pension_compensatoria` |
| Intereses moratorios | `mcp__robin__calcular_intereses_demora` |
| Baremo tráfico | `mcp__robin__calcular_baremo_trafico` |
| Pena (CP) | `mcp__robin__calcular_pena` |
| Costas procesales | `mcp__robin__calcular_costas_procesales` |
| Tasa judicial | `mcp__robin__tasa_judicial` |
| Depósito recurso | `mcp__robin__deposito_recurso` |
| Herencia y legítimas | `mcp__robin__calcular_herencia` |
| Plusvalía municipal | `mcp__robin__calcular_plusvalia_municipal` |
| Actualización renta IRAV/IPC | `mcp__robin__calcular_actualizacion_renta` |
| Prestación SS | `mcp__robin__calcular_prestacion_seguridad_social` |

### 3. Recoger inputs

Cada tool requiere su set de datos. Pide solo lo imprescindible.
Ejemplos:

**Despido**:
- Antigüedad (fecha de alta efectiva en empresa).
- Salario regulador (mensual o anual; bruto; con prorrateo de pagas
  extraordinarias).
- Tipo de despido (objetivo art. 52 ET, disciplinario art. 54 ET,
  colectivo art. 51 ET, improcedente, nulo).
- Fecha del despido.
- Convenio aplicable (si tiene topes específicos).

**Alimentos**:
- Edad del/los hijo/s.
- Ingresos netos del progenitor obligado.
- Ingresos netos del progenitor custodio (o ambos en custodia
  compartida).
- Necesidades específicas del menor (escolares, médicas).
- Régimen de custodia.
- Vecindad civil de los progenitores (si foral, aplicarán reglas
  propias).

**Baremo tráfico**:
- Fecha del accidente (importante para versión vigente del baremo +
  actualización IPC).
- Lesiones temporales: días impeditivos, no impeditivos, hospitalarios.
- Secuelas: tipo + puntos.
- Daño moral por pérdida de calidad de vida si procede.
- Pretium doloris específico (familiares fallecidos).
- Edad de la víctima.

**Pena**:
- Tipo penal exacto (artículo CP).
- Atenuantes invocables.
- Agravantes invocables.
- Subtipos aplicables (atenuado/agravado).
- Existencia de continuidad delictiva.

### 4. Aplicar correcciones forales si procede

Para alimentos, herencia, compensatoria: si las partes tienen
vecindad civil foral, Robin aplica la regla foral correspondiente
(p. ej., legítima global 25 % en Cataluña vs. tercios en CC estatal).

### 5. Output

```
🧮 Indemnización por despido

Datos:
- Trabajador: Juan Pérez (NIF anonimizado por política del despacho)
- Antigüedad: 5 años 7 meses (01/10/2020 → 14/05/2026)
- Salario regulador: 1.890 € brutos/mes con prorrateo de pagas
- Tipo: despido improcedente (decisión judicial pendiente)
- Convenio: hostelería de Andalucía (sin topes específicos)

Cálculo:
- Indemnización por improcedente (art. 56.1 ET):
  33 días/año × salario diario regulador.
- Salario diario regulador: 1.890 € × 12 / 365 = 62,14 € / día.
- Días indemnizables: 33 × 5,617 años = 185,4 días.
- Importe bruto: 185,4 × 62,14 = 11.521,03 €.

🟦 Indemnización ESTIMADA: 11.521,03 € brutos.

Avisos:
⚠️ Si la antigüedad incluye períodos como fijo discontinuo, se computa
   tiempo total trabajado (STS 24/11/2014, rec. 2592/2013).
⚠️ El cálculo asume art. 56.1 ET vigente. Si el tribunal aprecia
   nulidad, la consecuencia cambia (readmisión obligatoria).

Citas verificadas:
- art. 56.1 ET — BOE-A-2015-11430 vigente.
- STS de 24/11/2014 — ECLI:ES:TS:2014:5210 verificada.
```

### 6. Verificación al cierre

Antes de devolver, `mcp__robin__verificar_cita` sobre cualquier
norma o sentencia que aparezca en la justificación del cálculo.

## Notas sobre actualización automática

Las siguientes calculadoras usan tablas con auto-update:

- **Baremo tráfico**: IPC + Anexo Ley 35/2015. Robin las actualiza
  automáticamente cada enero.
- **Actualización renta LAU**: IRAV/IPC mensual del INE.
- **Prestación SS**: bases de cotización mínimas y máximas + topes
  pensión.
- **Costas procesales**: criterios orientadores del colegio (Robin
  tiene 6 colegios cargados; resto, manual).

Si el usuario calcula sobre una fecha donde Robin aún no tiene
datos actualizados, devuelve el último valor disponible + aviso de
"valor a confirmar con publicación oficial cuando salga".

## Ejemplos

```
/robin:calculadora
"Indemnización por despido. Trabajador con 8 años, 2.150 €/mes brutos
prorrateando pagas, despido objetivo por causas económicas."
```

```
/robin:calculadora baremo-trafico
"Accidente 15 abril 2025. Atropello en paso de cebra. Lesionado
varón 47 años, 35 días impeditivos, 12 días hospitalarios, secuela
limitación movilidad cervical 7 puntos."
```

```
/robin:calculadora intereses
"34.500 € impagados de factura. Vencimiento 1 marzo 2024. Ley de
morosidad porque comprador es empresa."
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

- **Antes de empezar:** identificar correctamente la calculadora aplicable. Si la materia es laboral, derivar a la skill `/robin:laboral-despido` (o la skill laboral que corresponda); si es tributaria, a `/robin:tributario-recurso-reposicion` (o la skill tributaria correspondiente).
- **Al cierre:** la skill procesal que tenga que incorporar el cálculo en el escrito.

**Severity floor cruzado:** si una skill anterior calificó algo 🔴, esta
skill NO puede bajarlo a 🟢 sin justificar el cambio en una frase. Los
ratings de upstream son el suelo, no el techo.


## Lo que esta skill NO hace

- **No es asesoramiento fiscal/laboral:** devuelve el cálculo determinístico con la fórmula y los inputs aplicados.
- **No firma el dictamen:** el letrado revisa y firma.
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

