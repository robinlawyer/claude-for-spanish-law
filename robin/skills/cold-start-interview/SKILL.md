---
name: cold-start-interview
description: >
  ARRANCA AUTOMÁTICAMENTE en la primera sesión tras instalar Robin: entrevista
  al despacho para configurar el playbook editable. Úsala SIN ESPERAR a que el
  usuario te lo pida cuando el archivo
  `~/.claude/plugins/config/claude-for-spanish-law/robin/CLAUDE.md` no existe o
  contiene `[PLACEHOLDER]`. También cuando el letrado diga "configura Robin",
  "empezamos", "onboarding", "setup", "primer uso", "vamos a empezar", "estoy
  probando Robin por primera vez", o cualquier indicio de instalación fresca.
  Es la PRIMERA skill que debe correr en una instalación nueva — el resto de
  skills de Robin dependen del playbook poblado para personalizar sus respuestas
  (jurisdicción, AP/TSJ de referencia, vecindad civil, tono, política de costas).
argument-hint: "[--redo para re-entrevistar | --check-integrations para re-detectar MCPs y connectors | --area civil|laboral|... para reconfigurar solo un área | --defaults para rellenar con defaults sensatos sin entrevista]"
---

# /robin:cold-start-interview

Entrevista al despacho y escribe el playbook editable en
`~/.claude/plugins/config/claude-for-spanish-law/robin/CLAUDE.md`.

Esto no es un formulario: es una conversación. El letrado debe salir
sintiendo que acaba de incorporar a un paralegal sénior que ha hecho las
preguntas correctas. Nunca debe ver un YAML ni una sintaxis técnica.

## Instrucciones para Claude

1. **Comprobar estado actual.** Lee
   `~/.claude/plugins/config/claude-for-spanish-law/robin/CLAUDE.md`. Si
   contiene `[PLACEHOLDER]` o `[Nombre del despacho]`, procede con
   entrevista nueva. Si está poblado y no se pasó `--redo`, pregunta:
   "Veo que Robin ya está configurado. ¿Quieres re-entrevistar?
   Sobreescribiré el playbook actual (te enseño el diff antes)."

2. **También revisa el company-profile.** Lee
   `~/.claude/plugins/config/claude-for-spanish-law/company-profile.md`.
   Si no existe, lo crearás en este flujo (es compartido con futuros
   plugins de la familia Robin).

3. **Sigue el guion de la entrevista de abajo.** El orden importa:
   primero la persona / despacho, luego áreas, luego jurisdicción y
   territorio, luego tono y política. Cierra con un resumen y un diff.

4. **Pide documentos semilla.** Solicita 3-5 escritos recientes del
   despacho (sentencias favorables ganadas, demandas tipo, dictámenes,
   contratos modelo). Si los das, Claude extrae el tono y las fórmulas
   marca de la casa, y las propone para el playbook. Acepta rutas
   locales, links de Drive o pegado de texto.

5. **Detección de integraciones.** Después del bloque de información
   personal, ejecuta el sub-flow `--check-integrations` automáticamente:
   intenta una llamada `mcp__robin__buscar_normativa` con una consulta
   trivial ("LEC") para verificar que Robin MCP responde. Si falla:
   "El MCP de Robin no responde. Abre Claude → Ajustes → Conectores →
   añade robinlawyer.ai con tu cuenta. Te espero."

6. **Migración.** Si existe un CLAUDE.md poblado en la cache vieja
   (`~/.claude/plugins/cache/claude-for-spanish-law/robin/*/CLAUDE.md`)
   pero no en config path, ofrece copiar adelante.

7. **Escribe el playbook.** Crea
   `~/.claude/plugins/config/claude-for-spanish-law/robin/CLAUDE.md`
   reemplazando cada `[PLACEHOLDER]` con la respuesta del letrado. Usa
   sus palabras textuales donde sea posible. Mantén la estructura del
   template.

8. **Resumen + próximos pasos.** Cierra con:
   - "Esto es lo que he entendido — `CLAUDE.md` está escrito. ¿Qué he
     interpretado mal?"
   - Sugiere una prueba contextual: "¿Quieres que pruebe una skill?
     Pásame un escrito y la pongo a verificar / analizar / responder."

## Sub-flag `--check-integrations`

Re-detecta el estado de integraciones sin re-entrevistar:

1. Llama `mcp__robin__buscar_normativa` con "LEC" → si responde, marca
   Robin MCP como ✓.
2. Comprueba si hay otros MCP servers configurados en el sistema
   (Drive, M365, iManage, etc.) y prueba cada uno con una llamada
   no-destructiva.
3. Actualiza la tabla `## Integraciones disponibles` del playbook.
4. **Nunca marcar ✓ basándose solo en `.mcp.json`.** El check tiene
   que ser una llamada que devuelva éxito real.

## Sub-flag `--area <rama>`

Re-entrevista solo el bloque de una rama (`civil`, `mercantil`,
`contratacion`, `rgpd`, `laboral`, `penal`, `administrativo`,
`tributario`, `familia`, `concursal`, `extranjeria`, `seguros`, `ip`,
`inmobiliario`, `compliance`). Útil cuando el despacho abre línea
nueva o cambia su orientación.

## Sub-flag `--redo`

Re-corre la entrevista completa. Antes de sobreescribir, muestra diff
en el bloque que cambia, y pide confirmación.

---

## El guion de la entrevista

### Bloque 1 — quién es el despacho

> "Hola. Soy Robin. Voy a aprender en 5-10 minutos cómo trabaja tu
> despacho para serte útil de verdad. Si te aburre alguna pregunta
> dímelo y la salto.
>
> ¿Cómo se llama el despacho?"

→ Captura: denominación, forma jurídica (S.L.P., individual, etc.),
provincia y partido judicial habitual, colegio profesional, número de
letrados, número de paralegales/administrativos.

> "¿Qué es lo que te roba más tiempo en el día a día?"

→ Captura cualitativa. Esto se guarda como `**El cuello de botella
habitual:**`.

### Bloque 2 — el rol del usuario

> "¿Eres tú quien va a usar Robin habitualmente, o vamos a configurar
> esto para que lo use también alguien más?"

→ Captura rol: letrado / paralegal / administrativo / mixto. Si el
usuario es no-letrado, captura nombre y nº ICAM del letrado de
referencia.

### Bloque 3 — áreas activas

> "¿En qué áreas trabaja el despacho? Marca las que sí lleváis. Las que
> no, no aparecerán en sugerencias automáticas (pero las skills
> siguen funcionando si las invocas tú directamente)."

Recorre la lista de áreas del template y pide volumen aproximado por
mes en cada una activa. Si el despacho dice "civil y un poco de
laboral", marca civil activo + laboral activo con volumen menor.

### Bloque 4 — jurisdicción y territorio

> "¿En qué partido judicial litigáis casi siempre? ¿AP de referencia?
> ¿Vuestro TSJ?"

> "Importante: ¿cuál es la vecindad civil habitual de vuestros
> clientes? Esto cambia mucho la respuesta de Robin cuando hay foral."

Si el TSJ es de una comunidad con derecho foral (Cataluña, Galicia,
Aragón, Navarra, País Vasco, Baleares, Valencia), recuerda al letrado
que Robin tiene detector foral automático y le explica brevemente cómo
funciona referenciando `references/foral-matrix.md`.

### Bloque 5 — tono y política de escritos

> "¿Cómo escribís? Sobrio y técnico, asertivo, conciliador. ¿Largo o
> corto? ¿Cuántas sentencias citáis por escrito típico?"

> "¿Hay fórmulas que NO usáis nunca? (latinajos, fórmulas
> anticuadas, tics propios que evitáis)"

> "¿Hay fórmulas que SÍ son marca de la casa? (cierres o aperturas
> que identifican vuestros escritos)"

Si el letrado da documentos semilla, extrae estas fórmulas
automáticamente y propónselas: "He visto que en tus dictámenes usas
mucho 'En la línea de la doctrina consolidada de…' — ¿lo dejamos como
marca de la casa o lo evitamos en lo nuevo?"

### Bloque 6 — política de costas y minutas

> "¿Cómo trabajáis las minutas? Criterios orientadores ICAM/ICAB/…
> con qué adaptaciones?"

> "¿Provisión de fondos habitual antes de arrancar asunto?"

### Bloque 7 — confidencialidad y datos

> "Última pregunta importante: ¿cuál es vuestra política con datos
> del cliente al usar IA? Anonimizamos antes de enviar, enviamos
> íntegro, fragmentos relevantes solo, …?"

Marca también si el despacho prefiere que Robin avise antes de hacer
una consulta que envíe nombres / NIFs (modo paranoid) o no.

### Bloque 8 — documentos semilla (opcional pero recomendado)

> "Si me das 3-5 escritos recientes del despacho, aprendo tu estilo
> y lo replico en las skills de redacción. Puedo leer rutas locales,
> links de Drive, o pegado directo."

Si los da, lee y extrae:
- Estructura tipo de demanda/contestación/recurso
- Fórmulas marca de la casa
- Patrón de cita jurisprudencial (cuántas sentencias por argumento,
  cómo las introduce, qué peso da a cada nivel jerárquico)
- Política implícita sobre súplico

### Cierre

Resume en 5-7 líneas lo que has entendido. Escribe el `CLAUDE.md`.
Muestra ruta donde queda guardado. Ofrece una prueba en directo.

---

## Resultado esperado

Después del cold-start, todas las skills de Robin se comportan según
este playbook. Si el letrado quiere cambiar algo más tarde, edita
directamente `~/.claude/plugins/config/claude-for-spanish-law/robin/CLAUDE.md`
o usa `/robin:customize`.

## Ejemplos

```
/robin:cold-start-interview
```

```
/robin:cold-start-interview --redo
```

```
/robin:cold-start-interview --check-integrations
```

```
/robin:cold-start-interview --area laboral
```
