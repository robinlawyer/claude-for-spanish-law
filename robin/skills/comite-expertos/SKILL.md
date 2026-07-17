---
name: comite-expertos
description: >
  Convoca un panel de expertos multi-perspectiva para analizar una decisión,
  operación, escrito, oferta, activo o estrategia desde varios ángulos
  profesionales independientes y enfrentados, y después sintetiza consenso,
  discrepancias y una recomendación accionable. Cada perfil jurídico ancla sus
  citas en el MCP de Robin (buscar_*, obtener_*, verificar_cita, simular_oposicion,
  estimar_viabilidad_caso) — nunca de memoria. Úsala SIEMPRE que el usuario pida
  "opinión del comité de expertos", "panel de expertos", "comité", "varios puntos
  de vista", "opinión multidisciplinar", "que lo miren distintos perfiles",
  "devil's advocate múltiple", "mesa redonda", o cuando plantee una decisión de
  calado (¿presento este escrito?, ¿lanzo esta oferta?, ¿compro este activo?,
  ¿acepto este convenio?, ¿qué estrategia sigo?) y convenga contrastarla desde
  perfiles distintos (concursalista, fiscalista, litigador, MD de fondo distressed,
  asesor de la AC, urbanista, laboralista, magistrado hipotético, etc.). Dispárala
  también cuando el usuario quiera estresar una tesis única contrastándola con
  perfiles que discrepen, aunque no diga literalmente "comité".
argument-hint: "[decisión, operación, escrito u oferta a someter al panel]"
---

# /robin:comite-expertos

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "comite-expertos"`.
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
