---
name: informe-interno
argument-hint: [asunto/frente a poner al dia del equipo]
description: >-
  Redacta un informe interno de situación dirigido AL EQUIPO, que abre con un
  resumen ejecutivo accionable (decisiones tomadas, decisiones pendientes, riesgos
  vivos y quién tiene la pelota) y luego desarrolla el estado del asunto con
  registro técnico alto — aquí sí caben tecnicismo, cita de articulado, NIFs,
  importes y cifras. Úsala SIEMPRE que el usuario pida "informe interno", "informe
  al equipo", "resumen ejecutivo interno", "estado del asunto para el equipo",
  "informe de situación interno", "pon al equipo al día", "nota interna de
  situación", "briefing interno", "traspaso de asunto", o cuando haya que coordinar
  al equipo, preparar una reunión, o dejar constancia del estado real y las
  acciones pendientes de un frente activo. Es lo OPUESTO al informe al cliente:
  aquí prima la densidad técnica y la accionabilidad, no la sencillez. Regla
  transversal: si el asunto toca la exposición personal del usuario (p. ej.
  personado en Pieza Sexta), señálalo explícitamente — su interés ≠ el del grupo.
  NO lo improvises como un resumen plano: esta skill fija el método (resumen
  ejecutivo primero, estado por frente con hitos y fechas, riesgos por gravedad,
  acciones con responsable y fecha) que una nota improvisada no da — consúltala en
  vez de responder directamente.
---

# /robin:informe-interno

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "informe-interno"`.
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
