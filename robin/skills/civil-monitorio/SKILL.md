---
name: civil-monitorio
description: >
  Petición de procedimiento monitorio (arts. 812 ss LEC) para deudas dinerarias
  vencidas, exigibles y documentadas. Sin tope de cuantía desde 2011. Requisito MASC (art. 5 LO 1/2025): el monitorio
  no está entre las excepciones de los arts. 5.2 y 5.3; hay criterios judiciales
  dispares, lo prudente es acreditar el intento (art. 264.4.º LEC).
argument-hint: "[acreedor, deudor, importe, documentación]"
---

# /robin:civil-monitorio

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "civil-monitorio"` y `version_plugin: "2.5.7"`.
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
