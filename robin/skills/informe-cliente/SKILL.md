---
name: informe-cliente
argument-hint: [asunto o hito a comunicar al cliente]
description: >-
  Redacta un informe de situación y próximos pasos dirigido AL CLIENTE en román
  paladino — sin jerga procesal, latinajos ni citas de articulado —, para que entienda
  dónde está su asunto, qué va a pasar y qué se espera de él. Úsala SIEMPRE que el
  usuario pida "informe para el cliente", "informe al cliente", "explícaselo al
  cliente", "en román paladino", "en lenguaje llano", "que lo entienda el cliente",
  "carta de situación al cliente", "update al cliente", "cómo va esto para el
  cliente", o haya que trasladar al cliente el estado tras un hito (auto, resolución,
  notificación, frente nuevo) o responder a un "cuéntame cómo va". Es lo OPUESTO al
  informe interno: prima la sencillez y la tranquilidad informada. No la improvises
  con registro de despacho: consulta esta skill (traducir tecnicismos, tres cosas que
  debe saber, titular en una línea, sin alarmismo ni falso optimismo).
---

# /robin:informe-cliente

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "informe-cliente"` y `version_plugin: "2.5.7"`.
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
