---
name: informe-interno
argument-hint: [asunto/frente a poner al dia del equipo]
description: >-
  Redacta un informe interno de situación dirigido AL EQUIPO: abre con un resumen
  ejecutivo accionable (decisiones tomadas y pendientes, riesgos vivos, quién tiene la
  pelota) y desarrolla el estado con registro técnico alto (articulado, NIFs,
  importes, cifras). Úsala SIEMPRE que el usuario pida "informe interno", "informe al
  equipo", "resumen ejecutivo interno", "estado del asunto para el equipo", "pon al
  equipo al día", "nota interna de situación", "briefing interno", "traspaso de
  asunto", o haya que coordinar al equipo, preparar una reunión o dejar constancia del
  estado y las acciones pendientes de un frente. Es lo OPUESTO al informe al cliente.
  Si el asunto toca la exposición personal del usuario, señálalo: su interés ≠ el del
  grupo. No lo improvises como resumen plano: consulta esta skill (resumen ejecutivo,
  estado por frente, riesgos por gravedad, acciones con responsable y fecha).
---

# /robin:informe-interno

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "informe-interno"` y `version_plugin: "2.5.6"`.
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
