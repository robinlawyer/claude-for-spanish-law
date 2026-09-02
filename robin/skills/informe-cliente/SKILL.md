---
name: informe-cliente
argument-hint: [asunto o hito a comunicar al cliente]
description: >-
  Redacta un informe de situación y próximos pasos dirigido AL CLIENTE en román
  paladino — lenguaje claro y llano, sin jerga procesal, sin latinajos, sin citas
  de articulado —, de forma que el cliente entienda dónde está su asunto, qué va a
  pasar y qué se espera de él sin necesitar traducción. Úsala SIEMPRE que el
  usuario pida "informe para el cliente", "informe al cliente", "explícaselo al
  cliente", "en román paladino", "en lenguaje llano", "que lo entienda el
  cliente", "carta de situación al cliente", "update al cliente", "cómo va esto
  para el cliente", o cuando haya que trasladar a un cliente el estado de un
  asunto tras un hito (auto, resolución, notificación, apertura de un frente
  nuevo) o responder a un "cuéntame cómo va". Es lo OPUESTO al informe interno:
  aquí prima la sencillez y la tranquilidad informada, no la densidad técnica. NO
  la improvises con registro de despacho: esta skill fija el método (traducir todo
  tecnicismo, tres cosas que el cliente debe saber, titular en una línea, sin
  alarmismo ni falso optimismo) que un informe técnico reciclado no da — consúltala
  en vez de responder directamente.
---

# /robin:informe-cliente

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "informe-cliente"`.
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
