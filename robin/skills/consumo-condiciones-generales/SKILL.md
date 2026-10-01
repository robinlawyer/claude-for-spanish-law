---
name: consumo-condiciones-generales
description: >
  Control de condiciones generales en contratos con consumidores: doble control
  de incorporación (Ley 7/1998, LCGC) y de contenido o abusividad (TRLGDCU),
  más el control de transparencia material. Úsala para revisar o redactar
  condiciones generales de un empresario (web, app, suscripciones, financiación,
  suministros, viajes), para preparar una reclamación o demanda de nulidad por
  abusividad, o cuando el letrado diga "¿es abusiva esta cláusula?", "revisa los
  términos y condiciones", "cláusula suelo/gastos/vencimiento anticipado",
  "transparencia material".
argument-hint: "[texto o fichero de las condiciones + posición (empresario/consumidor) + sector]"
---

# /robin:consumo-condiciones-generales

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "consumo-condiciones-generales"`.
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
