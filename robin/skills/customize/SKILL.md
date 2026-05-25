---
name: customize
description: >
  Edita el playbook del despacho sin re-correr toda la entrevista cold-start.
  Úsala cuando el letrado diga "cambia el tono", "ajusta la AP de
  referencia", "marca el área de extranjería como activa", "actualiza los
  criterios de costas", o cualquier ajuste puntual al playbook. Útil
  después de cambios en el despacho (nuevo socio, nueva área, mudanza de
  partido judicial, cambio de política RGPD interna).
argument-hint: "[sección a editar — 'tono', 'areas', 'jurisdiccion', 'costas', 'rgpd-interno', 'company-profile']"
---

# /robin:customize

Edita el playbook
(`~/.claude/plugins/config/claude-for-spanish-law/robin/CLAUDE.md`) o
el company-profile compartido
(`~/.claude/plugins/config/claude-for-spanish-law/company-profile.md`)
sin re-correr toda la entrevista.

## Instrucciones

1. **Verifica que el playbook existe.** Si no o sigue con
   `[PLACEHOLDER]`, deriva al usuario a `/robin:cold-start-interview`.
   No proceder.

2. **Si el usuario indicó sección,** ve directamente a esa sección y
   pregunta qué cambia.

3. **Si no indicó sección,** muestra el menú:

   > "¿Qué quieres cambiar?
   > 1. Tono y registro de escritos
   > 2. Áreas activas (marcar/desmarcar ramas)
   > 3. Jurisdicción y territorio (partido judicial, AP, TSJ,
   >    vecindad civil habitual)
   > 4. Política de costas y honorarios
   > 5. Política de confidencialidad y RGPD interno
   > 6. Datos del despacho (denominación, NIF, sedes, colegio) →
   >    company-profile
   > 7. Otro (especificar)"

4. **Lee la sección actual** del playbook y muéstrala al usuario antes
   de proponer cambios. "Hoy tienes: [bloque actual]. ¿Cómo lo
   actualizamos?"

5. **Recoge el cambio.** Acepta libre redacción. Si el usuario es
   ambiguo, pide concreción.

6. **Muestra diff antes de guardar.** Formato:
   ```
   - [línea antigua]
   + [línea nueva]
   ```

7. **Confirma y guarda.** Sobreescribe la sección. **No tocar el
   resto del archivo.**

8. **Avisa de efectos colaterales.** Si el cambio toca áreas activas,
   tono o jurisdicción, recuerda que afecta a TODAS las skills. Si
   toca política RGPD interna, recuerda que muchos clientes la querrán
   ver formalizada.

## Edición directa del archivo

Si el letrado prefiere editar el playbook en su editor:

> "También puedes abrir el archivo en tu editor favorito y editar
> directamente. La ruta es:
> `~/.claude/plugins/config/claude-for-spanish-law/robin/CLAUDE.md`.
> Robin lo leerá tal como esté en la siguiente skill."

## Ejemplos

```
/robin:customize tono
```

```
/robin:customize areas
```

```
/robin:customize jurisdiccion
```

```
/robin:customize
"Hemos abierto departamento de penal económico. Marca penal como
activo. Estimación 4-6 querellas o defensas al mes. El responsable
es Jaime Hernández, ICAM 73219."
```
