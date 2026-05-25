---
name: verificar-citas
description: >
  Verifica que todas las citas jurídicas de un texto existen, están vigentes y
  dicen lo que se les atribuye. Detecta ECLI inventados, BOE-A inexistentes,
  artículos derogados, expedientes AEPD/CNMC/TEAC mal referenciados. Úsala
  cuando recibas un escrito de la contraparte, antes de presentar un escrito
  propio, o cuando el letrado diga "verifica esto", "comprueba las citas",
  "esto huele a inventado".
argument-hint: "[texto a verificar — pégalo entero o pasa ruta de archivo]"
---

# /robin:verificar-citas

Verificador exhaustivo de citas jurídicas. Es la red de seguridad de
todo Robin: ninguna skill que genere escrito cierra sin pasar por aquí.

## Procedimiento

### 1. Extracción

Recorre el texto y extrae:

| Tipo | Patrón |
|---|---|
| ECLI | `ECLI:ES:TS:AAAA:NNNN`, `ECLI:ES:TC:AAAA:NNNN`, `ECLI:ES:AN:AAAA:NNNN`, `ECLI:ES:TSJ<CC>:AAAA:NNNN`, `ECLI:ES:AP<PROV>:AAAA:NNNN`, `ECLI:EU:C:AAAA:NNN`, `ECLI:EU:T:AAAA:NNN`, `ECLI:CE:ECHR:AAAA:NNN` |
| BOE-A | `BOE-A-AAAA-NNNNN` |
| Artículos de ley | "artículo 1124 CC", "art. 348 LECrim", "art. 56 LJCA", "art. 31 bis CP", "DA 7ª LGT", etc. |
| Expedientes AEPD | `PS/00xxx/AAAA`, `E/0xxxx/AAAA` |
| Consultas DGT | `V0xxx-AA` |
| Resoluciones TEAC | número/año-vocalía |
| Acuerdos no jurisdiccionales TS | "Acuerdo Pleno TS de DD/MM/AAAA" |
| Sentencias citadas como "STS 1234/2024" sin ECLI | Las marcas como "ECLI pendiente" y las verifica por número/año |
| Disposiciones DA/DT/DF/DD | "Disposición Adicional Séptima Ley X" |

### 2. Verificación

Para cada cita extraída:

- **ECLI** → `mcp__robin__verificar_cita` + (si verifica) opcional
  `mcp__robin__obtener_sentencia_completa` para confirmación cruzada.
- **BOE-A o artículo** → `mcp__robin__obtener_articulo_ley`. Si la
  norma está derogada o el artículo modificado, devuelve fecha y
  norma derogatoria/modificativa.
- **AEPD / DGT / TEAC / CNMC / CNMV / BdE / TACRC / TCU / Consejo de
  Estado** → tool de búsqueda específica con número de expediente.
- **Acuerdo Pleno TS** → provisionalmente vía
  `mcp__robin__buscar_jurisprudencia` con query "acuerdo no
  jurisdiccional Pleno" + fecha (tool dedicada pendiente en backend).
- **STS sin ECLI** → `mcp__robin__buscar_jurisprudencia` con número y
  año.

Si el corpus de Robin no incluye una sentencia o norma esperada
(típicamente STS pre-2020 o normativa autonómica muy reciente),
**márcala** como "no verificable contra corpus Robin" — eso es
distinto de "inventada". Robin lo distingue: en sentencias suele ser
cobertura temporal; en normas, sincronización con BOE.

### 3. Output

Tabla:

| # | Cita | Tipo | Robin | Vigencia | Observaciones |
|---|---|---|---|---|---|
| 1 | STS 1234/2024 ECLI:ES:TS:2024:5421 | Sentencia | ✅ verificada | n/a | Sala 1ª, ratio decidendi sobre cláusulas abusivas |
| 2 | art. 1124 CC | Norma | ✅ verificada | vigente | Última modif. ninguna |
| 3 | STS 999/1999 | Sentencia | ⚠️ no en corpus | n/a | Pre-2020, cobertura limitada. Confirmar en CENDOJ. |
| 4 | ECLI:ES:TS:2025:9999 | Sentencia | ❌ NO EXISTE | n/a | Posiblemente inventada. Buscar alternativa |
| 5 | art. 18.1 Ley 35/2002 | Norma | ❌ Ley 35/2002 no existe en BOE | n/a | Verificar referencia |

**Resumen ejecutivo al final**:

```
Total citas extraídas: 23
✅ Verificadas y vigentes: 19
⚠️ No en corpus Robin (confirmación manual): 2
❌ Inválidas o inventadas: 2

Riesgo: ALTO si se presenta el escrito como está. 
Recomendación: sustituir las 2 inválidas antes de presentar.
```

### 4. Sustitución (cuando el usuario lo pida)

Si tras la verificación el letrado pide ayuda para sustituir las
citas inválidas, llama:

- `mcp__robin__buscar_jurisprudencia` con la tesis que la cita
  inválida pretendía apoyar.
- `mcp__robin__buscar_por_hechos_analogos` si la cita estaba en un
  bloque de hechos.

Propón 2-3 alternativas verificadas con ECLI explícito.

### 5. Modo "fast"

Si el usuario pasa `--fast`, omite confirmaciones cruzadas y reporta
solo el resultado de `verificar_cita`. Útil para verificar escritos
muy largos rápidamente. Riesgo: alguna sentencia válida puede ser
marcada como dudosa si `verificar_cita` falla por timeout puntual.

### Política frente a citas no verificables

**NUNCA borrar silenciosamente.** Si encuentras una cita que no se
puede verificar:

1. **Inventada (resultado claro de no-existe)**: márcala roja,
   propónla para sustituir.
2. **No en corpus** (cobertura): márcala amarilla, deja la decisión al
   letrado.
3. **Verificada pero dice otra cosa que lo que se cita**: márcala
   roja con explicación. Esto pasa cuando el LLM original "alucinó"
   el contenido de una sentencia que sí existe.
4. **Norma derogada/modificada**: márcala amarilla con norma
   sustitutoria.

## Ejemplos

```
/robin:verificar-citas
[pegado del escrito de la contraparte]
```

```
/robin:verificar-citas
Archivo: ~/casos/2026/recurso-apelacion-borrador.docx
```

```
/robin:verificar-citas --fast
[escrito muy largo]
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

- **Antes de empezar:** ninguno — esta skill es la red de seguridad, la llama todo lo demás antes de cerrar.
- **Si una cita aparece como inventada:** `/robin:jurisprudencia` o `/robin:normativa` con la tesis que la cita pretendía apoyar, para proponer alternativas verificadas.

**Severity floor cruzado:** si una skill anterior calificó algo 🔴, esta
skill NO puede bajarlo a 🟢 sin justificar el cambio en una frase. Los
ratings de upstream son el suelo, no el techo.


## Lo que esta skill NO hace

- **No reescribe el escrito por su cuenta:** marca las citas problemáticas y propone alternativas verificadas, pero la decisión es del letrado.
- **No certifica vigencia normativa en sede notarial ni registral:** usa fuente primaria si es para una escritura.
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

