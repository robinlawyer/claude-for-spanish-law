---
name: revisar-propio-escrito
description: >
  Revisión exhaustiva de un escrito propio antes de presentarlo. Verificación
  de citas, coherencia argumental, errores procesales, política de despacho,
  detección de cláusulas problemáticas.
argument-hint: "[escrito propio en borrador]"
---

# /robin:revisar-propio-escrito

Pipeline:

1. **`mcp__robin__revisar_propio_escrito`** con el texto del borrador.

2. **Verificación de citas obligatoria**. Recorre el escrito y para
   cada ECLI, BOE-A, expediente o artículo citado, llama
   `mcp__robin__verificar_cita`. Las inválidas se marcan ROJAS y se
   sustituyen.

3. **Coherencia argumental**:
   - Cada fundamento jurídico responde al hecho que pretende rebatir.
   - Tesis del actor (si contestación) cubierta punto por punto.
   - Súplica coherente con los hechos y los fundamentos.

4. **Errores procesales típicos**:
   - Cauce procesal correcto para la cuantía / materia.
   - Jurisdicción competente.
   - Legitimación activa y pasiva acreditadas.
   - Plazos respetados.
   - Documentos esenciales aportados (poderes, certificaciones).

5. **Política del despacho**: tono, registro, longitud, fórmulas
   marca de la casa (del playbook).

6. **Detector foral si procede** — verifica que no se cita CC
   estatal cuando aplica foral.

7. **Simulación de oposición**:
   `mcp__robin__simular_oposicion` para anticipar
   contraataques predecibles. Refuerza puntos débiles antes de
   presentar.

8. **Devuelve el escrito** marcado:
   - `✅` partes verificadas y robustas.
   - `⚠️` puntos a reforzar (con sugerencia).
   - `❌` errores que hay que corregir antes de presentar.
   - `[propuesta]` redacción alternativa para los problemáticos.

## Output

```
🔍 Revisión escrito — [tipo]

Resumen
[3 líneas: estado general, errores críticos, listo o no para presentar]

Errores críticos (corregir antes de presentar)
❌ [Punto] — [problema] — [propuesta de corrección]

Avisos importantes
⚠️ [Punto] — [debilidad] — [refuerzo sugerido]

Verificación de citas
[tabla: cita | tipo | Robin | observaciones]

Puntos fuertes
✅ [Punto] — bien construido

Simulación de oposición
[3-5 contraataques predecibles + cómo blindar el escrito frente a ellos]
```

## Avisos típicos

- Si la skill detecta inconsistencia entre súplica y hechos
  numerados: error grave, suele provocar inadmisión parcial.
- Si hay alguna cita imposible de verificar: opción de buscar
  alternativa con `/robin:jurisprudencia`.
- Si el escrito vulnera la política del despacho (tono, fórmulas
  prohibidas): se marca y se reescribe.

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

- **Antes de empezar:** `/robin:verificar-citas` sobre el escrito ya redactado para detectar citas problemáticas.
- **En medio del flujo:** la tool `mcp__robin__simular_oposicion` para anticipar los argumentos contrarios y reforzar los puntos débiles.
- **Al cierre:** el escrito se devuelve al letrado para firma; esta skill no presenta ni firma.

**Severity floor cruzado:** si una skill anterior calificó algo 🔴, esta
skill NO puede bajarlo a 🟢 sin justificar el cambio en una frase. Los
ratings de upstream son el suelo, no el techo.


## Lo que esta skill NO hace

- **No reescribe automáticamente:** marca los puntos débiles y propone alternativas para que el letrado decida.
- **No suple a un revisor humano para escritos sensibles (recursos extraordinarios, querellas, escritos ante TC/TS).:** No suple a un revisor humano para escritos sensibles (recursos extraordinarios, querellas, escritos ante TC/TS).
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

