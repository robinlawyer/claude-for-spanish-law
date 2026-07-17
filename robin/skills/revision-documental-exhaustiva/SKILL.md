---
name: revision-documental-exhaustiva
description: >
  Revisión exhaustiva documento a documento de un data room o expediente
  completo con Robin Search (búsqueda documental local): recorre TODOS los
  ficheros —no el top-K semántico—, extrae hallazgos con traza fichero+página,
  lleva un ledger de cobertura, y entrega un informe con garantía de que no se
  ha saltado ningún documento. Habilita due diligence documental, revisión de
  contratos en masa y doc review de litigios. Delega el análisis jurídico
  especializado en la skill de materia (M&A → societario-due-diligence).
argument-hint: "[objetivo de la revisión + carpeta/caso + materia si se conoce]"
---

# /robin:revision-documental-exhaustiva

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "revision-documental-exhaustiva"`.
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
