---
name: civil-masc
description: >
  Requisito de procedibilidad del MASC (medios adecuados de solución de
  controversias, LO 1/2025) antes de una demanda civil: si se exige en el caso
  concreto, qué medio usar, cómo hacerlo con el mismo objeto que el futuro
  pleito, cómo documentarlo y cómo describirlo en la demanda, y qué efectos tiene
  en la prescripción y en las costas. Es la fuente única de Robin sobre el MASC:
  la cargan las skills que acaban en demanda civil. Úsala cuando el letrado diga
  "MASC", "requisito de procedibilidad", "negociación previa", "oferta vinculante
  confidencial", "¿tengo que negociar antes de demandar?", "me han inadmitido la
  demanda por no acreditar el MASC" o "la contraria no acudió a la negociación".
argument-hint: "[materia y tipo de proceso + partes + lo que ya se ha hecho para negociar (fechas, medio, respuesta)]"
---

# /robin:civil-masc

Skill de Robin Lawyer con **receta viva**: el pipeline completo se sirve
siempre actualizado desde el MCP de Robin. Este fichero solo contiene el
disparador; NO ejecutes nada de memoria.

Pasos:

1. Llama a la tool `obtener_skill` del MCP de Robin
   (`mcp__robin__obtener_skill`) con `nombre: "civil-masc"`.
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
