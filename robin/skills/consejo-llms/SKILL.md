---
name: consejo-llms
argument-hint: [pregunta o tesis a someter al consejo]
description: >-
  Convoca un consejo de varios modelos de lenguaje (LLMs) reales para que cada
  uno responda a la MISMA pregunta de forma independiente y a ciegas, y después
  sintetiza consenso, discrepancias y una recomendación única. A diferencia de
  comite-expertos —que simula perfiles profesionales con un mismo modelo— aquí
  la diversidad es de MODELO: cada consejero es un tier de Claude distinto (Opus,
  Sonnet, Fable, Haiku) que razona con una arquitectura y un temple propios.
  Úsala SIEMPRE que el usuario pida "consejo de LLMs", "consejo de modelos",
  "council of LLMs", "que respondan varios modelos", "compara modelos", "qué
  dicen distintos modelos", "ensemble de modelos", "segunda opinión de otro
  modelo", "contrasta esto con otro LLM", o cuando quiera reducir el riesgo de
  alucinación o de sesgo de un único modelo en una respuesta de calado
  (un dictamen, una tesis jurídica dudosa, una cifra crítica, una decisión
  irreversible). Dispárala también cuando el usuario quiera un veredicto más
  robusto que el de un solo modelo, aunque no diga literalmente "consejo de
  LLMs". NO improvises la respuesta multi-modelo de memoria: esta skill fija el
  método (fan-out real a varios modelos ciegos entre sí, detección de consenso vs.
  divergencia, arbitraje razonado) que un único hilo no puede dar por definición
  — consúltala en vez de responder directamente.
---

# /robin:consejo-llms

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "consejo-llms"`.
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
