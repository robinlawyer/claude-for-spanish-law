# Quick Start

**60 segundos** para instalar y empezar a usar Robin.

## Instalación en Claude Desktop

1. [Descarga Claude Desktop](https://claude.com/download) (Mac o Windows).
2. Asegúrate de tener cuenta en [robinlawyer.ai](https://robinlawyer.ai) con plan que incluya MCP. Si no, regístrate y suscríbete.
3. En Claude Desktop → Ajustes → Directorio → Plugins → **Añadir marketplace**, pega:
   ```
   https://api.robinlawyer.ai/plugins.git
   ```
4. Instala el plugin:
   ```
   /plugin install robin@claude-for-spanish-law
   ```

   Esto instala Robin **con el MCP incluido**. No hay que añadir el conector aparte: la conexión a `api.robinlawyer.ai/mcp` ya viene declarada en el plugin. La primera skill que lo necesite te pide OAuth con tu cuenta de robinlawyer.ai (un click).
5. **Reinicia Claude Desktop.** No es opcional.
6. Configura el playbook del despacho:
   ```
   /robin:cold-start-interview
   ```
   Tarda entre 5 y 10 minutos. Aprende cómo trabaja tu despacho — partido judicial habitual, AP/TSJ de referencia, política de costas, tono, áreas activas, vecindad civil habitual de los clientes — y escribe tu playbook editable en `~/.claude/plugins/config/claude-for-spanish-law/robin/CLAUDE.md`. Las skills lo leen antes de cada respuesta.
7. **Autentica el MCP de Robin** cuando la primera skill te lo pida (OAuth con tu cuenta de robinlawyer.ai). Sin autenticación, Robin para — no fabrica datos.

## Instalación en Claude Code (CLI)

```
/plugin marketplace add https://api.robinlawyer.ai/plugins.git
/plugin install robin@claude-for-spanish-law
```

Reinicia el CLI. Luego `/robin:cold-start-interview` como arriba.

### Instala en scope de usuario, no de proyecto

Cuando `/plugin install` pregunte, elige **scope de usuario**. Las skills necesitan leer documentos que te pegas desde Lexnet, escritos en Drive o en el escritorio. Scope de proyecto te limita al directorio actual.

## Tu primer escrito

Ejemplos para empezar (todos con verificación de citas obligatoria al cierre):

```
/robin:civil-demanda
Quiero demandar a una empresa de telefonía por servicios mal facturados:
1.247 € en cargos no contratados durante 14 meses. Mi cliente es un autónomo
de Vigo, factura empresarial.
```

```
/robin:laboral-despido
Mi cliente ha sido despedido disciplinariamente por supuestas faltas de
asistencia. Trabaja como camarero en un restaurante de Barcelona, contrato
indefinido desde 2019, salario 1.450 €/mes brutos. La carta de despido es
vaga, no enumera las faltas con fecha. Quiero impugnar.
```

```
/robin:rgpd-dictamen
Una clínica de fisioterapia me pregunta si puede grabar las sesiones de
los pacientes para uso docente interno. ¿Qué base jurídica le sirve y qué
información tiene que dar al paciente?
```

```
/robin:contrato-revisar
Adjunto un contrato de prestación de servicios entre mi cliente (empresa
española) y un proveedor de software irlandés. Necesito tu opinión sobre:
ley aplicable, jurisdicción, limitación de responsabilidad, IP, datos
personales y terminación. El cliente firma en una semana.
```

```
/robin:familia-divorcio
Pareja casada en 2014 en régimen económico de gananciales, dos hijos
menores (8 y 5), vivienda habitual en Cataluña a nombre de los dos.
Quieren divorcio de mutuo acuerdo. Vecindad civil de él: catalana
(nacido en Lleida); de ella: común. ¿Cómo abordamos régimen económico
y, sobre todo, custodia?
```

## Slash commands principales

| Comando | Para qué sirve |
|---|---|
| `/robin:cold-start-interview` | Configura el playbook del despacho. Empieza por aquí siempre. |
| `/robin:customize` | Edita el playbook (cambios puntuales o re-onboarding). |
| `/robin:matter-workspace` | Crea o cambia de carpeta de asunto. Aísla el contexto entre clientes. |
| `/robin:verificar-citas` | Verifica un texto pegado: ECLI, BOE-A, expedientes AEPD/TEAC/DGT. |
| `/robin:civil-demanda` | Redacta demanda civil. |
| `/robin:civil-contestacion` | Redacta contestación con análisis previo del escrito del actor. |
| `/robin:laboral-despido` | Revisa despido y prepara demanda social si procede. |
| `/robin:rgpd-dictamen` | Dictamen RGPD/LOPDGDD sobre tratamiento concreto. |
| `/robin:penal-querella` | Querella o denuncia penal. |
| `/robin:admin-recurso-reposicion` | Recurso de reposición/alzada contra acto administrativo. |
| `/robin:tributario-rea` | Reclamación económico-administrativa ante TEAR/TEAC. |
| `/robin:familia-divorcio` | Convenio regulador o demanda de divorcio. |
| `/robin:societario-due-diligence` | DD legal de compraventa de SL/SA. |
| `/robin:contrato-revisar` | Revisa contrato contra ley imperativa, doctrina y mejores prácticas. |
| `/robin:foral-check` | Detector de aplicabilidad foral sobre un caso. |

El catálogo completo aparece con `/robin:help`.

## Qué pasa en la primera skill

La primera vez que invocas algo que requiere Robin, Claude pide autorización para conectar al MCP. Acepta. Después, todas las skills usan ese login automáticamente. Si revocas, cambias de cuenta o expira la licencia, el plugin te lo dice y pide reautenticar.

Si algo no funciona: `/robin:doctor` te diagnostica el estado del MCP y del playbook.
