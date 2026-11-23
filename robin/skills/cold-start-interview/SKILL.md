---
name: cold-start-interview
description: >
  Entrevista inicial al despacho para configurar el playbook editable
  (`~/.claude/plugins/config/claude-for-spanish-law/robin/CLAUDE.md`): tres
  preguntas rápidas (despacho, tribunales de referencia y tono). Úsala cuando
  el letrado salude con "Hola Robin" (o variantes directas: "hola robin",
  "Hola, Robin") y la entrevista no esté hecha — ese saludo es el atajo
  oficial de entrada, exactamente equivalente a escribir
  /robin:cold-start-interview. Y cuando diga "configura Robin", "onboarding",
  "setup", "primer uso", "vamos a empezar" o "estoy probando Robin por primera
  vez". La entrevista está hecha si el playbook ya tiene el nombre del
  despacho, aunque le queden [PLACEHOLDER], salvo que su primera línea diga
  «Configuración: a medias». NO la arranques por tu cuenta
  mientras el abogado te pide otro trabajo: Robin funciona igual sin
  configurar y las skills usan valores por defecto sensatos (jurisdicción,
  AP/TSJ de referencia, vecindad civil, tono, política de costas).
argument-hint: "[--rapido para el modo de tres preguntas | --redo para retomar lo pendiente o re-entrevistar | --check-integrations para re-detectar MCPs y connectors | --area civil|laboral|... para reconfigurar solo un área | --avisos para configurar solo los avisos de fechas | --defaults para rellenar con defaults sensatos sin entrevista]"
---

# /robin:cold-start-interview

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "cold-start-interview"` y `version_plugin: "2.5.6"`.
2. SIGUE VERBATIM el `body` que devuelve: es el pipeline completo y al día
   (qué tools de Robin invocar, en qué orden, qué citas verificar y el
   formato de entrega). No improvises pasos, no cites jurisprudencia ni
   normativa de memoria y no sustituyas ninguna fuente de Robin por
   conocimiento del modelo.
3. Si la llamada a `obtener_skill` falla, devuelve un error, indica que la
   suscripción no está activa, o el MCP de Robin no está conectado o no
   responde: NO ejecutes la skill por tu cuenta. Muestra al usuario este
   mensaje, tal cual y en una línea propia, y detente:

   > «No se puede acceder a Robin Lawyer. Comprueba que el conector de
   > Robin esté activo y tu suscripción en robinlawyer.ai/account, o
   > inténtalo de nuevo en unos minutos.»
