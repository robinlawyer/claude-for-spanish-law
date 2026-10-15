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
- Sucesiones: vecindad civil catalana del causante al fallecer (arts. 9.8 y 16 CC).
- Régimen económico matrimonial: el CCCat si es la ley que resulta del art. 9.2 CC
  (ley personal común de los cónyuges al casarse; en su defecto, la elegida en
  documento auténtico, la de la residencia habitual común inmediatamente posterior
  o la del lugar de celebración).
- Inmueble sito en Cataluña (derechos reales).
- Negocio celebrado en Cataluña por parte sometida a CCCat (obligaciones
  y contratos del Llibre Sisè).

## Galicia — Lei 2/2006 de Dereito Civil de Galicia (LDCG)

Materias propias:
- Régimen económico matrimonial (sociedad de gananciales modificada,
  capitulaciones).
- Sucesiones (apartación, mejora pactada, partición conjunta).
- Casa patrucial y veciña (arts. 51-53 LDCG), compañía familiar gallega, comunidad en mano común.
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

El Tribunal Constitucional anuló las leyes civiles valencianas por falta
de competencia:

- **STC 82/2016**: la Ley 10/2007, de régimen económico matrimonial
  valenciano, entera.
- **STC 192/2016**: la Ley 5/2011, de relaciones familiares de los hijos
  cuyos progenitores no conviven (custodia), entera.
- **STC 110/2016**: buena parte de la Ley 5/2012, de uniones de hecho
  formalizadas.

No existe ley valenciana de sucesiones (la Ley valenciana 6/2024 es de
simplificación administrativa). En régimen económico matrimonial,
custodia y sucesiones rige el Código Civil estatal; el derecho civil
valenciano subsistente es consuetudinario y muy limitado.

**Puntos de conexión:**
- Vecindad civil valenciana: compruébala, pero no presupongas norma
  propia; búscala con `buscar_normativa` (ccaa valenciana) y, si no la
  hay, aplica el CC.

---

## Reglas de conflicto que aplica `/robin:foral-check`

1. **Personalidad de la ley civil:** la vecindad civil determina la ley
   personal (art. 16.1.1.ª CC; su adquisición, art. 14 CC). Se aplica a sucesiones, capacidad, régimen
   económico matrimonial.
2. **Lex rei sitae:** inmuebles se rigen por la ley del lugar donde
   estén sitos.
3. **Ley elegida:** en contratos, las partes pueden elegir una ley con conexión con
   el negocio; en defecto, ley personal (vecindad civil) común, residencia habitual
   común y, en último término, lugar de celebración (arts. 10.5 y 16.1 CC).
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
