---
name: contrato-extraer-fechas
description: >
  Localiza en los contratos de un expediente (con RobinSearch, en local) las
  fechas de vencimiento, renovación automática y preaviso, se las propone al
  abogado en una tabla con fichero, página y cita de la cláusula, y SOLO tras
  su confirmación las deja vigiladas con `vigilar_fechas` para que Robin avise
  por correo. Úsala cuando el letrado diga "sácame los vencimientos de estos
  contratos", "qué contratos se renuevan solos", "avísame antes de que venza
  el preaviso", "calendario de renovaciones de la cartera", o al cerrar una
  revisión documental de contratos.
argument-hint: "[carpeta o caso indexado en RobinSearch + tipo de contratos si se conoce]"
---

# /robin:contrato-extraer-fechas

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "contrato-extraer-fechas"`.
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
