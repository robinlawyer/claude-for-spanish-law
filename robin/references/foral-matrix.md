# Matriz de Derecho Foral

Tabla de puntos de conexión para decidir cuándo una norma civil foral se
aplica con prioridad sobre el Código Civil estatal (art. 13.2 CC).

Cada fila identifica una norma foral en vigor y los puntos de conexión
que la activan. Es la fuente que `/robin:foral-check` consulta cuando
recibe un caso.

## Cataluña — Codi Civil de Catalunya (CCCat)

Libros vigentes:

| Libro | Materia | Ley aprobatoria |
|---|---|---|
| Primer | Disposiciones generales | Llei 29/2002 |
| Segon | Persona i família | Llei 25/2010 |
| Tercer | Persona jurídica | Llei 4/2008 |
| Quart | Successions | Llei 10/2008 |
| Cinquè | Drets reals | Llei 5/2006 |
| Sisè | Obligacions i contractes | Llei 3/2017 (parcial) |

**Puntos de conexión que activan CCCat:**
- Vecindad civil catalana de cualquiera de las partes (sucesiones y
  régimen económico matrimonial).
- Inmueble sito en Cataluña (derechos reales).
- Negocio celebrado en Cataluña por parte sometida a CCCat (obligaciones
  y contratos del Llibre Sisè).

## Galicia — Lei 2/2006 de Dereito Civil de Galicia (LDCG)

Materias propias:
- Régimen económico matrimonial (sociedad de gananciales modificada,
  capitulaciones).
- Sucesiones (apartación, mejora pactada, partición conjunta).
- Casa petrucial, veciñanza, comunidad en mano común.
- Aparcerías, derechos de retracto.

**Puntos de conexión:**
- Vecindad civil gallega de causante o cónyuges.
- Inmueble sito en Galicia en materia de retractos.

## Aragón — Código del Derecho Foral de Aragón (CDFA, DLeg. 1/2011)

Materias propias muy extensas:
- Persona y familia (custodia compartida con preferencia, alimentos
  entre parientes).
- Régimen económico matrimonial (consorcio conyugal).
- Sucesiones (libertad de testar, pacto sucesorio, fiducia sucesoria,
  legítima colectiva).
- Derecho de bienes (luces y vistas, servidumbres, retracto de
  abolorio).

**Puntos de conexión:**
- Vecindad civil aragonesa de las partes / causante.
- Inmueble sito en Aragón.

## Navarra — Fuero Nuevo (Ley 1/1973, recopilación reformada por LF 21/2019)

Materias propias muy extensas, incluyendo:
- Régimen económico matrimonial (conquistas, comunidad universal).
- Sucesiones (libertad de testar amplísima, pactos sucesorios, donación
  propter nuptias).
- Servidumbres, retractos, montes.
- Contratos y obligaciones (compraventa con pacto de retro, censo,
  treudo).

**Puntos de conexión:**
- Vecindad civil navarra (condición foral) de las partes / causante.
- Inmueble sito en Navarra.

## País Vasco — Ley 5/2015 de Derecho Civil Vasco (LDCV)

Aplicable en TODO el País Vasco desde 2015 (antes solo en algunas
comarcas):
- Sucesiones (libertad de testar, herencia troncal en Bizkaia/Llodio/
  Aramaio).
- Régimen económico matrimonial (comunicación foral en Bizkaia).
- Servidumbres y comunidades particulares.

**Puntos de conexión:**
- Vecindad civil vasca de las partes / causante.
- Inmueble troncal sito en zonas con derecho troncal vigente.

## Islas Baleares — Compilación de Derecho Civil (TR DLeg. 79/1990)

Materias propias:
- Régimen económico matrimonial (separación de bienes con presunción
  diferente).
- Sucesiones (legítima reducida, fideicomisos, definición).
- Pactos sucesorios (espolios, donación universal de bienes presentes y
  futuros).
- Derechos reales (alodial, censos, redención).

**Puntos de conexión:**
- Vecindad civil balear (de Mallorca, Menorca, Ibiza-Formentera, con
  algunas diferencias entre islas).
- Inmueble sito en Baleares.

## Comunidad Valenciana

Tras la STC 82/2016 (declaró inconstitucionales las leyes valencianas
sobre régimen económico matrimonial, custodia y arrendamientos rústicos
por falta de competencia retroactiva), Valencia recuperó terreno con:

- **Ley 6/2024** sobre sucesiones (en vigor 2025), apoyándose en la
  competencia recuperada vía Estatuto de Autonomía.

**Puntos de conexión:**
- Vecindad civil valenciana de causante (sucesiones, donde aplique
  Ley 6/2024).

Robin marca como "discutible" la aplicación foral valenciana en materias
no cubiertas por la 6/2024 hasta nuevo desarrollo legislativo.

---

## Reglas de conflicto que aplica `/robin:foral-check`

1. **Personalidad de la ley civil:** la vecindad civil determina la ley
   personal (art. 14 CC). Se aplica a sucesiones, capacidad, régimen
   económico matrimonial.
2. **Lex rei sitae:** inmuebles se rigen por la ley del lugar donde
   estén sitos.
3. **Ley elegida:** en contratos, las partes pueden elegir; en defecto,
   ley del lugar de cumplimiento (art. 10.5 CC).
4. **Supletoriedad del CC estatal (art. 13.2 CC):** el CC suple, no
   sustituye.
5. **Conflicto entre forales:** vecindad civil de las partes; si
   discrepan, la del causante en sucesiones, la del lugar del inmueble
   en derechos reales, etc.

---

## Cómo lo usa una skill

Una skill civil/mercantil/familia/sucesiones/inmobiliario que reciba
hechos llama a `mcp__robin__buscar_por_ccaa` con los hechos y a esta
matriz por contexto. Si hay punto de conexión foral activo, la skill:

1. Cita primero la norma foral aplicable.
2. Cita el CC estatal solo si suple o si la cuestión está expresamente
   no regulada en la foral.
3. Avisa al letrado en el bloque final si la aplicabilidad foral es
   discutible (típico: cliente con vecindad común pero inmueble en
   Cataluña; o cliente valenciano en materia post-STC 82/2016).
