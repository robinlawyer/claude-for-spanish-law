---
name: extranjeria-nacionalidad
description: >
  Adquisición de la nacionalidad española por residencia, carta de
  naturaleza, opción, matrimonio. La opción de la DA 8.ª Ley 20/2022 (Memoria
  Democrática) tenía plazo de dos años desde el 21-10-2022, prorrogable un año
  (DA 8.ª.2): está cerrada; queda la carta de naturaleza del art. 33 Ley 20/2022
  para brigadistas internacionales y sus descendientes.
argument-hint: "[vía de adquisición + situación del solicitante]"
---

# /robin:extranjeria-nacionalidad

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "extranjeria-nacionalidad"`.
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
