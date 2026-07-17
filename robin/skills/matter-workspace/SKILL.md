---
name: matter-workspace
description: >
  Gestión de carpetas de asunto. Crea, lista, cambia o cierra el "matter"
  activo. Cada asunto del despacho tiene su carpeta dedicada con escritos,
  notas, cronología y outputs de las skills. Garantiza que Robin nunca
  mezcla contexto entre clientes. Úsala cuando el letrado diga "abre
  asunto nuevo", "vamos al caso X", "guarda esto en el expediente de Y",
  "cierra el asunto Z".
argument-hint: "[create <slug> | switch <slug> | list | close <slug> | rename <old> <new>]"
---

# /robin:matter-workspace

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "matter-workspace"`.
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
