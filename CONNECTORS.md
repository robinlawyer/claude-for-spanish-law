# Connectors

Los plugins de `claude-for-spanish-law` comparten un único MCP server obligatorio (Robin) y aceptan connectors opcionales para integrarse con el flujo de trabajo del despacho.

## Obligatorio

### Robin

```json
{
  "type": "http",
  "url": "https://api.robinlawyer.ai/mcp",
  "title": "Robin",
  "description": "Asistente jurídico español. Corpus oficial verificable, jurisprudencia con ECLI, normativa BOE y autonómica, doctrina administrativa (AEPD/DGT/TEAC/Consejo de Estado/CNMC/CNMV/BdE/TACRC/TCU), 14 calculadoras procesales con auto-update, 33 modelos mercantiles y 10 modelos CGPJ."
}
```

Autenticación: OAuth 2.0 contra `https://api.robinlawyer.ai/oauth/authorize`. La primera skill que necesita Robin abre el flujo en el navegador; en sucesivas, el token se renueva en segundo plano.

Sin esta conexión, **ninguna skill** del bundle hace trabajo sustantivo. Es deliberado: Robin no compite por velocidad con un LLM razonando solo, compite por exactitud verificable.

## Opcionales (por plugin)

Cada plugin declara en su `.mcp.json` solo los connectors que aporta o recomienda. La línea de base es Robin + nada más; opcionales se añaden cuando el caso de uso lo justifica.

### Google Drive

```json
{
  "type": "http",
  "url": "https://drivemcp.googleapis.com/mcp/v1",
  "title": "Google Drive"
}
```

Recomendado para `robin-mercantil-societario` (data rooms), `robin-litigacion-civil` (expedientes), `robin-contratacion` (repositorios de contratos firmados). Lee solo lo que el usuario apunte.

### Microsoft 365

```json
{
  "type": "http",
  "url": "https://mcp.microsoft365.com/mcp",
  "title": "Microsoft 365"
}
```

Equivalente a Drive para despachos en ecosistema Microsoft. Recomendado en los mismos plugins.

### iManage / NetDocuments

DMS jurídicos populares en despachos grandes. Si el despacho ya los usa:

```json
{
  "type": "http",
  "url": "https://cloudimanage.com/mcp/work",
  "title": "iManage"
}
```

No vienen activos por defecto en ningún plugin de este bundle. Se añaden en el archivo de configuración del usuario cuando el despacho contrata.

### DocuSign

Útil en `robin-mercantil-societario` y `robin-contratacion` para envío de firma. Opcional.

## Connectors que NO recomendamos

- **Slack / Teams como destinatario de output**: el secreto profesional impide que el escrito viaje por canales corporativos abiertos sin clasificación previa. Si el despacho lo quiere, que sea decisión explícita del compliance interno.
- **Conectores con LLMs de terceros**: Robin ya orquesta su propio razonamiento. Añadir otro LLM por encima sin coordinación introduce inconsistencias.

## Política frente a `claude-for-legal`

`claude-for-legal` (Anthropic) declara 20+ connectors (Westlaw, LexisNexis, CourtListener, Ironclad, etc.). En España la mayoría de esos no existen o sus equivalentes (Aranzadi, Lefebvre, vLex, CGAE) no publican MCP server propio a fecha de redacción.

Nuestra apuesta es: **el dato jurídico viaja con Robin**. Si en el futuro Aranzadi/Lefebvre/vLex publican MCP, los añadimos como opcionales — pero ni un solo plugin debe depender de un connector externo para hacer trabajo correcto.
