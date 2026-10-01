---
name: startups-stock-options
description: >
  Planes de incentivos sobre el capital de una startup: stock options, phantom
  shares, RSU y entregas de participaciones a empleados y colaboradores.
  Estructura del plan, vesting y cliff, good leaver y bad leaver, aspectos
  societarios (autocartera, aumento de capital, pacto de socios), laborales y
  fiscales, incluido el régimen específico de empresas emergentes de la Ley
  28/2022. Úsala para diseñar, redactar o revisar un plan de incentivos, una
  carta de concesión o las cláusulas de leaver, o cuando el letrado diga
  "ESOP", "plan de opciones", "phantom", "vesting", "good/bad leaver",
  "incentivos para el equipo de la startup".
argument-hint: "[tipo de sociedad y fase + instrumento (opciones/phantom/participaciones) + beneficiarios + objetivo]"
---

# /robin:startups-stock-options

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "startups-stock-options"`.
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
