---
name: civil-recurso-infraccion-procesal
description: >
  Infracción de normas procesales en el recurso de casación civil. El recurso
  extraordinario por infracción procesal está suprimido (arts. 468-476 LEC sin
  contenido desde el 20-3-2024, RDL 6/2023): la infracción procesal se alega como
  motivo de casación (art. 477.2 LEC), con denuncia previa en la instancia, de haber
  sido posible (art. 479.2).
argument-hint: "[sentencia AP recurrida + infracción procesal invocada]"
---

# /robin:civil-recurso-infraccion-procesal

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "civil-recurso-infraccion-procesal"` y `version_plugin: "2.5.6"`.
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
