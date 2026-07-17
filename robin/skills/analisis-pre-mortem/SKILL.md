---
name: analisis-pre-mortem
description: >
  Ejecuta un análisis pre-mortem: asume que la operación, escrito, estrategia,
  inversión o proyecto YA HA FRACASADO en un horizonte futuro y razona hacia atrás
  las causas del fracaso, ordenándolas por probabilidad × impacto, con señales
  tempranas (tripwires) y mitigaciones. Cada modo de fallo con sustancia jurídica se
  verifica en el MCP de Robin (¿la norma sigue vigente?, ¿hay jurisprudencia
  contraria?, ¿el plazo está precluido?) — nunca de memoria. Úsala SIEMPRE que el
  usuario pida "pre-mortem", "premortem", "análisis pre-mortem", "asume que ha
  salido mal", "por qué podría fracasar", "qué puede salir mal", "stress-test de
  riesgos", "red team esto", "antes de presentar/lanzar/comprar dime los riesgos", o
  cuando esté a punto de tomar una decisión de calado (presentar un escrito, lanzar
  una oferta de levantamiento, comprar deuda o un activo, aceptar un convenio, firmar
  un SPA) y convenga estresarla antes de comprometerse. Dispárala también cuando
  detectes exceso de optimismo en un plan y ayude anticipar los modos de fallo,
  aunque el usuario no diga "pre-mortem".
argument-hint: "[operación, escrito o decisión a estresar antes de comprometerse]"
---

# /robin:analisis-pre-mortem

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "analisis-pre-mortem"`.
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
