---
name: cowork-tareas-programadas
description: >
  Plantillas OPCIONALES de tareas programadas de Claude Cowork que llaman a Robin
  como conector remoto: informe semanal de novedades del BOE y del DOUE que
  vigila el abogado y resumen de sus fechas próximas. Son una comodidad: ningún
  aviso de Robin depende de ellas (los avisos los manda el propio servidor de
  Robin por correo). Úsala cuando el letrado diga "prográmame un informe
  semanal", "tarea programada en Cowork", "quiero un resumen cada lunes en
  Claude", "automatiza el repaso de novedades".
argument-hint: "[qué quiere recibir (novedades, fechas próximas o ambas) + día y hora]"
---

# /robin:cowork-tareas-programadas

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "cowork-tareas-programadas"`.
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
