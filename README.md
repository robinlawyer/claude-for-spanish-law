# Claude for Spanish Law

**Marketplace oficial de Robin para Claude.** Un único plugin (`robin`) que convierte a Claude en un asistente jurídico español de nivel profesional — sobre el corpus oficial verificable de Robin y con cero alucinación de citas.

Inspirado en la arquitectura de [`anthropics/claude-for-legal`](https://github.com/anthropics/claude-for-legal) — adaptada al derecho continental español. No es un fork: las fuentes documentales, las skills, las calculadoras y los flujos procesales están reescritos para España.

## Por qué un único plugin (y no quince)

`claude-for-legal` divide la abogacía estadounidense en doce plugins porque allí los abogados son hiperespecialistas (privacy counsel ≠ corporate counsel ≠ litigation counsel). En España, especialmente fuera de los grandes despachos de Madrid y Barcelona, el abogado típico lleva tres o cuatro ramas a la vez. Forzarle a instalar y configurar quince plugins por separado es fricción gratuita.

**Robin es un único plugin con más de cien skills agrupadas por rama.** El cold-start se configura una sola vez para todo el despacho. Las skills se activan por contexto, no por instalación.

## Qué cubre

| Rama | Skills clave |
|---|---|
| **Civil y procesal civil (LEC)** | Demanda, contestación, reconvención, recursos (reposición, apelación, casación, infracción procesal), monitorio, ejecución, medidas cautelares |
| **Mercantil y societario** | DD de compraventa de SL/SA, pacto de socios, juntas y acuerdos, M&A, modificaciones estructurales, litigio societario |
| **Contratación mercantil** | Revisión y redacción de NDAs, prestación de servicios, distribución, agencia, franquicia, suministro |
| **RGPD y protección de datos** | Dictámenes, EIPD, DPA, DSAR, notificación de brecha AEPD, transferencias internacionales, cookies, AI Act |
| **Laboral y SS** | Despidos, despido colectivo, MSCT, sanciones, accidente de trabajo, papeleta SMAC, demanda social, prestaciones SS |
| **Penal** | Querellas, denuncias, defensa, acusación particular, fase intermedia, recursos penales, cálculo de pena, compliance 31 bis |
| **Administrativo y contencioso** | Reposición, alzada, contencioso, responsabilidad patrimonial, contratación pública, sanciones |
| **Tributario** | Alegaciones, reposición, REA TEAR/TEAC, contencioso-tributario, devolución, inspección |
| **Familia y sucesiones** | Divorcio, custodia, alimentos, modificación de medidas, partición hereditaria, testamentos, foral sucesorio |
| **Concursal** | Solicitud, preconcurso, plan de reestructuración, segunda oportunidad, calificación |
| **Extranjería** | Arraigo, residencia, reagrupación, asilo, nacionalidad, recursos contra expulsión |
| **Seguros y tráfico** | Reclamación a aseguradora, baremo tráfico, juicio verbal del automóvil |
| **Propiedad intelectual e industrial** | Marcas, patentes, infracción, licencias, software |
| **Inmobiliario y urbanismo** | LAU, propiedad horizontal, compraventa, TRLS, expropiación |
| **Compliance sectorial** | 31 bis CP, AML, whistleblowing (LO 2/2023), CNMC, CNMV, BdE, ESG |
| **Transversales (core)** | Verificación de citas, búsqueda asistida, foral checker, plazos procesales, calculadoras |
| **Cliente y despacho** | Email cliente, hoja de encargo, dictamen, memorándum, informe jurídico |

## Por qué Robin y no otra cosa

| Capa | Resto del mercado | Robin |
|---|---|---|
| **Corpus normativo** | El que tu cliente pague (Aranzadi, Lefebvre, vLex) | Embebido y propio: BOE histórico, 17 boletines autonómicos, 855 disposiciones DA/DT/DF/DD, DOUE |
| **Jurisprudencia** | Indexada parcialmente, sin ECLI consistente | TS/AN/TSJ/AP con ECLI verificable, TC, TJUE/TGUE, TEDH, acuerdos no jurisdiccionales TS post LO 1/2025 |
| **Doctrina administrativa** | Buscador genérico | AEPD por expediente, DGT consultas vinculantes, TEAC vinculante, Consejo de Estado, CNMC/CNMV/BdE, TACRC, TCU, Defensor del Pueblo |
| **Verificación** | Confías en lo que escribe el LLM | `verificar_cita` obligatorio antes de devolver cualquier escrito |
| **Derecho foral** | Inexistente o tratado como excepción rara | Detector automático: si los hechos caen en Galicia / Cataluña / Aragón / Navarra / País Vasco / Baleares / Valencia, prioridad foral sobre CC estatal (art. 13.2 CC) |
| **Calculadoras** | Hojas Excel internas | 14 calculadoras con auto-update IPC / IRAV / baremo de tráfico / pensiones SS |
| **Modelos oficiales** | Plantillas Word descargables | 10 modelos CGPJ post-LO 1/2025 + 33 modelos mercantiles |

## Instalación rápida

Ver [QUICKSTART.md](./QUICKSTART.md). En 60 segundos:

```
/plugin marketplace add https://api.robinlawyer.ai/plugins.git
/plugin install robin@claude-for-spanish-law
```

El marketplace **se sirve desde el servidor de Robin**, no desde GitHub. Una sola instalación trae todo: skills, agents y el cableado al MCP de Robin. La primera skill abre OAuth con tu cuenta de robinlawyer.ai (un click).

Reinicia Claude Desktop. Luego:

```
/robin:cold-start-interview
```

5-10 minutos para configurar el playbook del despacho (jurisdicción habitual, política de costas, tono, áreas activas, partido judicial, AP/TSJ de referencia, etc.).

## Conexión con el MCP de Robin

El plugin declara un único `mcpServer` apuntando a `https://api.robinlawyer.ai/mcp`. La primera skill que necesita Robin abre el OAuth en el navegador con tu cuenta de robinlawyer.ai. Sin autenticación, las skills paran de inmediato y dicen por qué — Robin nunca fabrica datos.

## Licencia

Plugin: ver [LICENSE](./LICENSE).
MCP server `api.robinlawyer.ai/mcp` y sus contenidos: propiedad de Robin, sujeto a [términos de servicio](https://robinlawyer.ai/terms).

## Contribuir

Ver [CONTRIBUTING.md](./CONTRIBUTING.md).
