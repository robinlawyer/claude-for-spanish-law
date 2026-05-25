---
name: jurisprudencia
description: >
  Búsqueda asistida de jurisprudencia con jerarquía y prioridad territorial.
  Devuelve sentencias con ECLI verificable del TC, TS, AN, TSJ, AAPP, TJUE,
  TGUE, TEDH. Úsala cuando el letrado diga "busca jurisprudencia sobre…",
  "qué dice el TS de…", "hay STC sobre…", "casos análogos a esto".
argument-hint: "[descripción de la tesis o supuesto a buscar | -- doctrina | -- foral | -- territorio <provincia>]"
---

# /robin:jurisprudencia

Busca jurisprudencia aplicando la jerarquía de
`references/jurisprudencia-jerarquia.md` y la prioridad territorial
del playbook del despacho.

## Procedimiento

### 1. Identificar el supuesto

Si el usuario describe el caso brevemente, extrae:

- **Rama jurídica** (civil, mercantil, laboral, penal, administrativo,
  tributario, etc.).
- **Tesis a defender** (qué quiere probar la sentencia).
- **Norma central aplicable** (si es identificable).
- **Hechos clave** que activan el supuesto.

Si la descripción es ambigua, pide concreción en una pregunta. Una
sola pregunta.

### 2. Búsqueda jerárquica

Ejecuta en este orden:

1. **TC** — si el supuesto puede tener relevancia constitucional
   (derechos fundamentales, igualdad, tutela judicial, intimidad,
   propiedad), llama `mcp__robin__buscar_tc` primero.

2. **TS** — `mcp__robin__buscar_jurisprudencia` con filtro
   `organo=Tribunal Supremo`. Si el caso tiene dimensión foral,
   considera además TSJ con competencia foral.

3. **TJUE / TGUE / TEDH** — si hay derecho UE o derechos
   fundamentales europeos.

4. **AN** — si penal económico, social colectivo o contencioso de
   Audiencia Nacional.

5. **TSJ de referencia del despacho** — leído del playbook.

6. **AP de referencia del despacho** — leído del playbook.

7. **AAPP del mismo TSJ** — si no hay AP de referencia o ésta no
   tiene sentencias relevantes.

### 3. Filtros opcionales

Acepta del usuario:

- `--territorio <provincia>` — restringe a AAPP de esa provincia.
- `--organo <TS|AN|TSJ|AP|todos>` — limita por jerarquía.
- `--sala <1|2|3|4|5|civil|penal|contencioso|social|militar>` —
  limita por sala.
- `--desde AAAA / --hasta AAAA` — rango temporal.
- `--norma <referencia>` — usa `norma_citada` para devolver solo
  sentencias que aplican esa norma.
- `--doctrina` — incluye TC + acuerdos no jurisdiccionales TS post LO
  1/2025 + dictámenes Consejo de Estado relevantes.
- `--foral` — busca con prioridad en la Compilación de la CCAA
  correspondiente.
- `--max <N>` — número de hits por nivel (default 5).

### 4. Doctrina administrativa cuando proceda

Si la rama es:

- **RGPD**: añadir `mcp__robin__buscar_aepd`.
- **Tributaria**: añadir `mcp__robin__buscar_teac` y
  `mcp__robin__buscar_dgt`.
- **Contratación pública**: añadir `mcp__robin__buscar_tacrc`.
- **Competencia / regulación CNMC**: añadir `mcp__robin__buscar_cnmc`.
- **Mercados / valores**: añadir `mcp__robin__buscar_cnmv`.
- **Banca**: añadir `mcp__robin__buscar_bde`.
- **Consultivo**: añadir `mcp__robin__buscar_consejo_estado`.
- **Buena administración**: `mcp__robin__buscar_defensor_pueblo`.
- **Gestión pública**: `mcp__robin__buscar_tcu`.

### 5. Output

Por cada nivel jurisprudencial, un bloque:

```
### TC
- STC 56/2023, de 22 mayo (rec. amparo 4521-2022) — ECLI:ES:TC:2023:56
  *Tesis:* La protección del art. 18 CE alcanza los datos de geolocalización
  obtenidos sin consentimiento explícito en relación laboral.
  *Encaje en tu caso:* Apoya directamente el motivo 2 de tu recurso.

### TS — Sala 1ª
- STS 1234/2024, de 15 oct (rec. 1100/2023) — ECLI:ES:TS:2024:5421
  *Tesis:* …
  *Encaje en tu caso:* …
```

Cada entrada lleva ECLI obligatorio, fecha completa, número de
recurso, una línea de ratio decidendi y una línea de "encaje en tu
caso".

### 6. Verificación previa

Antes de devolver, llama `mcp__robin__verificar_cita` sobre cada ECLI.
Si alguno no verifica, **no aparece en el output** (lo que es muy raro
porque la búsqueda devuelve directo del corpus, pero la verificación
es la red de seguridad).

### 7. Cierre

Incluye al final:

- **Cantidad total** de sentencias devueltas por nivel.
- **Sugerencia de cómo citarlas** en un escrito (orden, cuántas,
  argumento que cada una apoya).
- **Avisos**:
  - Si TS tiene disenso sobre el punto: dilo.
  - Si TJUE ha resuelto cuestión prejudicial sobre la misma cuestión:
    márcalo como cita obligatoria.
  - Si la cobertura del corpus Robin para el periodo solicitado es
    limitada (típico STS pre-2020), avísalo.

## Ejemplos

```
/robin:jurisprudencia
Cláusula suelo en hipoteca firmada por consumidor en 2014. La entidad
alega que la cláusula es transparente porque se entregó la FIPRE.
```

```
/robin:jurisprudencia --norma "art. 1124 CC" --organo TS --desde 2023
```

```
/robin:jurisprudencia --foral
Sucesión de catalán con bienes en Madrid y Barcelona, hijos de
distinta vecindad civil.
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


## Cross-skill handoffs

- **Antes de empezar:** `/robin:foral-check` si la materia es civil, mercantil, contratación, familia, sucesiones o inmobiliario.
- **En medio del flujo:** `/robin:normativa` cuando una sentencia gire sobre interpretación de un artículo concreto.
- **Al cierre:** `/robin:verificar-citas` sobre los ECLIs devueltos antes de que el letrado los integre en un escrito.

**Severity floor cruzado:** si una skill anterior calificó algo 🔴, esta
skill NO puede bajarlo a 🟢 sin justificar el cambio en una frase. Los
ratings de upstream son el suelo, no el techo.


## Lo que esta skill NO hace

- **No redacta el escrito:** solo devuelve sentencias con su contenido íntegro y ratio decidendi.
- **No suple la lectura del fallo por el letrado.:** No suple la lectura del fallo por el letrado.
- **No inventa ECLIs:** si una sentencia no está en el corpus de Robin, se dice expresamente.
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

