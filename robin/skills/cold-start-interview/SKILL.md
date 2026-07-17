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

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "cold-start-interview"`.
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
