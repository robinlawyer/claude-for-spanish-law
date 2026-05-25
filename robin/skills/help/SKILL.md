---
name: help
description: >
  Catálogo completo de skills de Robin agrupadas por rama. Úsala cuando el
  letrado diga "qué puedes hacer", "qué skills hay", "cómo se llama lo de
  …", "ayuda", "menú".
---

# /robin:help

Muestra el catálogo completo de skills agrupadas por rama. Tras el
listado, ofrece un buscador conversacional ("¿qué necesitas hacer?")
para sugerir la skill más adecuada.

## Procedimiento

1. **Lee el playbook** para saber qué áreas tiene activas el despacho.
   Marca con ★ las skills de las áreas activas. Las demás aparecen
   atenuadas en el listado pero siguen disponibles.

2. **Muestra el catálogo organizado.**

---

### Configuración del despacho

| Comando | Para qué |
|---|---|
| `/robin:cold-start-interview` | Configuración inicial. Empezamos siempre por aquí. |
| `/robin:customize` | Editar el playbook después del cold-start. |
| `/robin:matter-workspace` | Crear / cambiar / cerrar carpetas de asunto. |
| `/robin:doctor` | Diagnóstico de Robin (MCP, playbook, integraciones). |
| `/robin:help` | Este menú. |

### Transversales (core)

| Comando | Para qué |
|---|---|
| `/robin:verificar-citas` | Verifica un texto pegado: ECLI, BOE-A, expedientes AEPD/TEAC/DGT. |
| `/robin:jurisprudencia` | Búsqueda asistida en CENDOJ con jerarquía. |
| `/robin:normativa` | BOE + 17 boletines autonómicos + DOUE. |
| `/robin:foral-check` | Detector de aplicabilidad foral. |
| `/robin:plazos` | Cómputo de plazos procesales y prescripciones. |
| `/robin:calculadora` | 14 calculadoras: despido, alimentos, intereses, baremo, etc. |

### Civil y procesal civil (LEC)

`/robin:civil-demanda` · `/robin:civil-contestacion` · `/robin:civil-reconvencion` ·
`/robin:civil-recurso-apelacion` · `/robin:civil-recurso-casacion` ·
`/robin:civil-recurso-infraccion-procesal` · `/robin:civil-monitorio` ·
`/robin:civil-ejecucion` · `/robin:civil-medidas-cautelares` ·
`/robin:civil-diligencias-preliminares` · `/robin:civil-analizar-escrito` ·
`/robin:civil-simular-oposicion` · `/robin:civil-viabilidad`

### Mercantil y societario

`/robin:societario-due-diligence` · `/robin:societario-m-and-a` ·
`/robin:societario-pacto-socios` · `/robin:societario-acuerdo-junta` ·
`/robin:societario-constitucion` ·
`/robin:societario-modificacion-estructural` · `/robin:societario-litigio` ·
`/robin:societario-responsabilidad-administradores`

### Contratación mercantil

`/robin:contrato-revisar` · `/robin:contrato-redactar` ·
`/robin:contrato-nda` · `/robin:contrato-prestacion-servicios` ·
`/robin:contrato-distribucion` · `/robin:contrato-agencia` ·
`/robin:contrato-franquicia` · `/robin:contrato-suministro`

### RGPD y protección de datos

`/robin:rgpd-dictamen` · `/robin:rgpd-pia` · `/robin:rgpd-dpa` ·
`/robin:rgpd-dsar` · `/robin:rgpd-brecha-aepd` ·
`/robin:rgpd-transferencias` · `/robin:rgpd-cookies` ·
`/robin:rgpd-ai-act` · `/robin:rgpd-auditoria-cumplimiento`

### Laboral y SS

`/robin:laboral-despido` · `/robin:laboral-despido-colectivo` ·
`/robin:laboral-sancion` · `/robin:laboral-msct` · `/robin:laboral-convenio` ·
`/robin:laboral-accidente` · `/robin:laboral-conciliacion-smac` ·
`/robin:laboral-demanda-social` · `/robin:laboral-prestacion-ss`

### Penal

`/robin:penal-querella` · `/robin:penal-denuncia` · `/robin:penal-defensa` ·
`/robin:penal-acusacion` · `/robin:penal-fase-intermedia` ·
`/robin:penal-recurso` · `/robin:penal-calcular-pena`

### Administrativo y contencioso

`/robin:admin-recurso-reposicion` · `/robin:admin-recurso-alzada` ·
`/robin:admin-contencioso` · `/robin:admin-medidas-cautelares` ·
`/robin:admin-responsabilidad-patrimonial` ·
`/robin:admin-contratacion-publica` · `/robin:admin-sancion`

### Tributario

`/robin:tributario-alegaciones` · `/robin:tributario-recurso-reposicion` ·
`/robin:tributario-rea` · `/robin:tributario-contencioso` ·
`/robin:tributario-devolucion` · `/robin:tributario-inspeccion`

### Familia y sucesiones

`/robin:familia-divorcio` · `/robin:familia-custodia` ·
`/robin:familia-alimentos` · `/robin:familia-modificacion-medidas` ·
`/robin:familia-ejecucion-medidas` · `/robin:sucesiones-particion` ·
`/robin:sucesiones-testamento` · `/robin:sucesiones-impugnacion`

### Concursal

`/robin:concursal-solicitud` · `/robin:concursal-preconcurso` ·
`/robin:concursal-plan-reestructuracion` ·
`/robin:concursal-segunda-oportunidad` · `/robin:concursal-calificacion`

### Extranjería y nacionalidad

`/robin:extranjeria-arraigo` · `/robin:extranjeria-residencia` ·
`/robin:extranjeria-reagrupacion` · `/robin:extranjeria-asilo` ·
`/robin:extranjeria-nacionalidad` · `/robin:extranjeria-expulsion`

### Seguros y tráfico

`/robin:seguros-reclamacion-aseguradora` · `/robin:seguros-baremo-trafico` ·
`/robin:seguros-juicio-verbal-automovil` · `/robin:seguros-lucro-cesante`

### Propiedad intelectual e industrial

`/robin:ip-registro-marca` · `/robin:ip-registro-patente` ·
`/robin:ip-infraccion` · `/robin:ip-licencia` · `/robin:ip-software`

### Inmobiliario y urbanismo

`/robin:inmobiliario-arrendamiento-urbano` ·
`/robin:inmobiliario-propiedad-horizontal` ·
`/robin:inmobiliario-compraventa` · `/robin:inmobiliario-urbanismo` ·
`/robin:inmobiliario-expropiacion`

### Compliance sectorial

`/robin:compliance-programa-31bis` · `/robin:compliance-aml` ·
`/robin:compliance-whistleblowing` · `/robin:compliance-esg` ·
`/robin:compliance-cnmc` · `/robin:compliance-cnmv` · `/robin:compliance-bde`

### Trabajo de despacho

`/robin:cliente-email` · `/robin:cliente-hoja-encargo` ·
`/robin:dictamen` · `/robin:memorandum` · `/robin:informe-juridico` ·
`/robin:resumen-ejecutivo`

---

3. **Después del listado, ofrece búsqueda conversacional:**

   > "¿Buscas algo concreto? Descríbeme lo que necesitas hacer (en
   > una frase) y te sugiero la skill correcta."

   Cuando el usuario describa, mapea su descripción a una skill y
   propónsela explicando en una línea qué hace. Si la descripción
   encaja con dos o tres, ofrécele las opciones.
