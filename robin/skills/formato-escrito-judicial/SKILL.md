---
name: formato-escrito-judicial
description: >
  Especificación única del FORMATO DE SALIDA de todo documento de Robin:
  orden y distribución del escrito judicial (NIG, procedimiento, tribunal,
  encabezamiento, hechos, fundamentos en tres grupos, costas, suplico,
  otrosíes y doble firma), reglas de citación jurisprudencial y normativa,
  y maqueta tipográfica del despacho, con los criterios de la Sala de
  Gobierno del Tribunal Supremo para los escritos de casación. La cargan
  todas las skills que componen un escrito o un documento.
argument-hint: "[tipo de escrito o documento que vas a componer]"
---

# /robin:formato-escrito-judicial

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "formato-escrito-judicial"`.
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
