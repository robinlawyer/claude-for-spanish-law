---
name: matter-workspace
description: >
  Gestión de carpetas de asunto. Crea, lista, cambia o cierra el "matter"
  activo. Cada asunto del despacho tiene su carpeta dedicada con escritos,
  notas, cronología y outputs de las skills. Garantiza que Robin nunca
  mezcla contexto entre clientes. Úsala cuando el letrado diga "abre
  asunto nuevo", "vamos al caso X", "guarda esto en el expediente de Y",
  "cierra el asunto Z".
argument-hint: "[create <slug> | switch <slug> | list | close <slug> | rename <old> <new>]"
---

# /robin:matter-workspace

Gestiona el espacio de trabajo por asunto. Cada matter es una carpeta
en:

```
~/.claude/plugins/config/claude-for-spanish-law/robin/matters/<slug>/
```

con:

```
<slug>/
├── matter.md             # ficha del asunto: cliente, partes, área, partido judicial, plazos
├── escritos/             # outputs de skills de redacción
├── analisis/             # outputs de skills de análisis
├── cronologia.md         # construida por civil-viabilidad o intake
├── citas-verificadas.md  # registro acumulado de citas usadas en el asunto
└── notas.md              # notas libres del letrado
```

## Instrucciones

### `create <slug>`

1. Pide los datos mínimos:
   - **Slug** (corto, kebab-case): `ines-perez-divorcio`, `acme-vs-tdc-mercantil`.
   - **Cliente** (nombre y NIF si lo da).
   - **Parte contraria** (si aplica).
   - **Área**: civil / mercantil / contratacion / rgpd / laboral / penal /
     administrativo / tributario / familia / concursal / extranjeria /
     seguros / ip / inmobiliario / compliance.
   - **Partido judicial** (si es litigioso).
   - **Estado**: instrucción / fondo / recurso / extrajudicial / cerrado.
2. **Detector foral si aplica.** Si el área es civil, mercantil,
   familia, sucesiones o inmobiliario, lanza `/robin:foral-check` con
   los datos del matter y persiste el resultado en `matter.md`.
3. Crea la estructura de directorios.
4. Escribe `matter.md` con la ficha.
5. Marca este matter como activo en
   `~/.claude/plugins/config/claude-for-spanish-law/robin/active-matter`.
6. Confirma: "Matter `<slug>` creado y activo. Las skills siguientes
   guardarán outputs aquí."

### `switch <slug>`

1. Verifica que el matter existe.
2. Cambia el matter activo escribiendo en `active-matter`.
3. Muestra la ficha (`matter.md`) en pantalla.
4. Lista los últimos 5 archivos modificados en el matter.

### `list`

1. Muestra todos los matters con:
   - Slug
   - Cliente
   - Área
   - Estado
   - Última actividad
   - Marca el activo con ★
2. Ordena por última actividad (más reciente primero).

### `close <slug>`

1. Confirma la acción ("¿Cerrar matter `<slug>`? Se mantiene en
   archivo histórico pero no aparecerá en `list` salvo
   `list --include-closed`.").
2. Mueve la carpeta a `matters/_closed/<slug>/`.
3. Si era el activo, vuelve a sin matter activo.

### `rename <old> <new>`

1. Verifica que `<new>` no existe.
2. Renombra la carpeta y actualiza `active-matter` si procede.
3. Avisa de que los archivos internos que hagan referencia al slug
   antiguo NO se actualizan automáticamente — el letrado decide si los
   reescribe.

## Comportamiento de otras skills sobre el matter activo

Toda skill de redacción o análisis:

1. Lee `active-matter` para saber dónde guardar el output.
2. Si no hay matter activo, pregunta al letrado: "¿En qué asunto va
   esto? (slug existente o `practice-level` para sin matter)". Si dice
   `practice-level`, el output va a un directorio de inbox, no a un
   matter.
3. Lee `matter.md` para incorporar contexto al prompt (parte, área,
   foral, partido judicial).
4. Guarda el output en la subcarpeta correspondiente del matter con
   nombre de archivo timestamp + tipo.
5. Si genera citas, las añade a `citas-verificadas.md` del matter.

## Privacidad

Los matters viven solo en local. Robin (el MCP) no los almacena. Si
el letrado quiere sincronizarlos entre dispositivos, debe usar su
propia solución (Drive, Dropbox, iCloud apuntando a `~/.claude/`).

## Ejemplos

```
/robin:matter-workspace create rodriguez-vs-banco-popular-2026
```

```
/robin:matter-workspace switch ines-perez-divorcio
```

```
/robin:matter-workspace list
```

```
/robin:matter-workspace close acme-resuelto-junio
```
