---
name: laboral-clasificacion
description: >
  Laboralidad frente a trabajo autónomo: decide si una relación de servicios es
  laboral (falso autónomo), autónoma común o de autónomo económicamente
  dependiente (TRADE), con los indicios de dependencia y ajenidad de la
  doctrina del Tribunal Supremo. Úsala para revisar un contrato de prestación
  de servicios o mercantil antes de firmarlo, para defender o atacar una
  demanda de reconocimiento de relación laboral, ante un acta de la Inspección
  de Trabajo, en plataformas digitales y repartidores, o cuando el letrado diga
  "¿es un falso autónomo?", "laboralidad", "TRADE", "freelance que trabaja solo
  para nosotros".
argument-hint: "[descripción de la relación o contrato + posición (empresa/trabajador) + contexto (preventivo, demanda, Inspección)]"
---

# /robin:laboral-clasificacion

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "laboral-clasificacion"`.
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
