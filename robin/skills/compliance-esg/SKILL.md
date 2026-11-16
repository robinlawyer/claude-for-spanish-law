---
name: compliance-esg
description: >
  Cumplimiento ESG: Directiva CSRD (UE) 2022/2464 y normas ESRS (Reglamento Delegado 2023/2772), con
  los aplazamientos de la Directiva (UE) 2025/794 (comprueba en vivo con
  buscar_legislacion_ue si hay modificaciones posteriores), Taxonomía
  UE, CS3D (diligencia debida en sostenibilidad), normativa nacional.
argument-hint: "[empresa + tamaño + sector + obligaciones aplicables]"
---

# /robin:compliance-esg

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "compliance-esg"` y `version_plugin: "2.5.6"`.
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
