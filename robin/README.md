# Robin — Asistente Jurídico Español

Plugin único del marketplace `claude-for-spanish-law`. Convierte a Claude en un asistente para el abogado español, sobre el MCP de Robin y su corpus oficial verificable.

## Slash commands por rama

### Configuración del despacho (instala primero)

- `/robin:cold-start-interview` — Configuración inicial (5-10 min). Escribe el playbook del despacho.
- `/robin:customize` — Edita el playbook después del cold-start.
- `/robin:matter-workspace` — Gestión de carpetas de asunto (un cliente, un caso).
- `/robin:doctor` — Diagnóstico de conexión MCP y de playbook.
- `/robin:help` — Catálogo completo de skills agrupadas por rama.

### Transversales (core)

- `/robin:verificar-citas` — Verifica ECLI, BOE-A, expedientes contra fuente oficial.
- `/robin:jurisprudencia` — Búsqueda asistida en CENDOJ con jerarquía TS > AN > TSJ > AP.
- `/robin:normativa` — Búsqueda asistida en BOE y 17 boletines autonómicos.
- `/robin:foral-check` — Detector de aplicabilidad foral.
- `/robin:plazos` — Cómputo de plazos procesales y prescripciones.
- `/robin:calculadora` — 14 calculadoras (despido, alimentos, intereses, baremo tráfico, etc.).

### Civil y procesal civil (LEC)

- `/robin:civil-demanda` `/robin:civil-contestacion` `/robin:civil-reconvencion`
- `/robin:civil-recurso-apelacion` `/robin:civil-recurso-casacion` `/robin:civil-recurso-infraccion-procesal`
- `/robin:civil-monitorio` `/robin:civil-ejecucion`
- `/robin:civil-medidas-cautelares` `/robin:civil-diligencias-preliminares`
- `/robin:civil-analizar-escrito` `/robin:civil-simular-oposicion`
- `/robin:civil-viabilidad`

### Mercantil y societario

- `/robin:societario-due-diligence` `/robin:societario-m-and-a`
- `/robin:societario-pacto-socios` `/robin:societario-acuerdo-junta`
- `/robin:societario-constitucion` `/robin:societario-modificacion-estructural`
- `/robin:societario-litigio` `/robin:societario-responsabilidad-administradores`

### Contratación mercantil

- `/robin:contrato-revisar` `/robin:contrato-redactar`
- `/robin:contrato-nda` `/robin:contrato-prestacion-servicios`
- `/robin:contrato-distribucion` `/robin:contrato-agencia` `/robin:contrato-franquicia` `/robin:contrato-suministro`

### RGPD y protección de datos

- `/robin:rgpd-dictamen` `/robin:rgpd-pia` `/robin:rgpd-dpa`
- `/robin:rgpd-dsar` `/robin:rgpd-brecha-aepd`
- `/robin:rgpd-transferencias` `/robin:rgpd-cookies`
- `/robin:rgpd-ai-act` `/robin:rgpd-auditoria-cumplimiento`

### Laboral y Seguridad Social

- `/robin:laboral-despido` `/robin:laboral-despido-colectivo`
- `/robin:laboral-sancion` `/robin:laboral-msct`
- `/robin:laboral-convenio` `/robin:laboral-accidente`
- `/robin:laboral-conciliacion-smac` `/robin:laboral-demanda-social`
- `/robin:laboral-prestacion-ss`

### Penal

- `/robin:penal-querella` `/robin:penal-denuncia`
- `/robin:penal-defensa` `/robin:penal-acusacion`
- `/robin:penal-fase-intermedia` `/robin:penal-recurso`
- `/robin:penal-calcular-pena`

### Administrativo

- `/robin:admin-recurso-reposicion` `/robin:admin-recurso-alzada`
- `/robin:admin-contencioso` `/robin:admin-medidas-cautelares`
- `/robin:admin-responsabilidad-patrimonial`
- `/robin:admin-contratacion-publica` `/robin:admin-sancion`

### Tributario

- `/robin:tributario-alegaciones` `/robin:tributario-recurso-reposicion`
- `/robin:tributario-rea` `/robin:tributario-contencioso`
- `/robin:tributario-devolucion` `/robin:tributario-inspeccion`

### Familia y sucesiones

- `/robin:familia-divorcio` `/robin:familia-custodia` `/robin:familia-alimentos`
- `/robin:familia-modificacion-medidas` `/robin:familia-ejecucion-medidas`
- `/robin:sucesiones-particion` `/robin:sucesiones-testamento` `/robin:sucesiones-impugnacion`

### Concursal

- `/robin:concursal-solicitud` `/robin:concursal-preconcurso`
- `/robin:concursal-plan-reestructuracion` `/robin:concursal-segunda-oportunidad`
- `/robin:concursal-calificacion`

### Extranjería y nacionalidad

- `/robin:extranjeria-arraigo` `/robin:extranjeria-residencia`
- `/robin:extranjeria-reagrupacion` `/robin:extranjeria-asilo`
- `/robin:extranjeria-nacionalidad` `/robin:extranjeria-expulsion`

### Seguros y tráfico

- `/robin:seguros-reclamacion-aseguradora` `/robin:seguros-baremo-trafico`
- `/robin:seguros-juicio-verbal-automovil` `/robin:seguros-lucro-cesante`

### Propiedad intelectual e industrial

- `/robin:ip-registro-marca` `/robin:ip-registro-patente`
- `/robin:ip-infraccion` `/robin:ip-licencia` `/robin:ip-software`

### Inmobiliario y urbanismo

- `/robin:inmobiliario-arrendamiento-urbano` `/robin:inmobiliario-propiedad-horizontal`
- `/robin:inmobiliario-compraventa` `/robin:inmobiliario-urbanismo`
- `/robin:inmobiliario-expropiacion`

### Compliance sectorial

- `/robin:compliance-programa-31bis` `/robin:compliance-aml`
- `/robin:compliance-whistleblowing` `/robin:compliance-esg`
- `/robin:compliance-cnmc` `/robin:compliance-cnmv` `/robin:compliance-bde`

### Trabajo de despacho

- `/robin:cliente-email` `/robin:cliente-hoja-encargo`
- `/robin:dictamen` `/robin:memorandum` `/robin:informe-juridico` `/robin:resumen-ejecutivo`

## Agents (de vigilancia, corren en background o programados)

- `/agents` → seleccionar de la lista.
- `vigilancia-plazos` — alerta de plazos críticos de los asuntos activos.
- `vigilancia-jurisprudencia-territorio` — sentencias nuevas de la AP/TSJ del despacho.
- `vigilancia-aepd` — resoluciones AEPD por sector (si despacho hace RGPD).
- `vigilancia-convenios-colectivos` — actualizaciones del convenio aplicable a clientes.
- `vigilancia-doctrina-teac` — nueva doctrina TEAC en el área tributaria.
- `vigilancia-doctrina-dgt` — nuevas consultas vinculantes DGT.
- `vigilancia-cnmv-cnmc` — circulares y sanciones sectoriales.

## Cómo lee Robin tu despacho

Toda skill lee, antes de actuar, el playbook editable en:

```
~/.claude/plugins/config/claude-for-spanish-law/robin/CLAUDE.md
```

Si no existe o tiene `[PLACEHOLDER]`, la skill para y te pide ejecutar `cold-start-interview`.
Editar ese archivo cambia el comportamiento de Robin en todas las skills al instante.
