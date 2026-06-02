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

