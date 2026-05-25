---
name: doctor
description: >
  Diagnóstico del estado de Robin: conexión MCP, autenticación OAuth, playbook
  del despacho, integraciones secundarias, versiones, posibles bloqueos. Úsala
  cuando algo no funciona o antes de un trabajo importante para confirmar que
  todo está operativo.
argument-hint: "[--fix para intentar reparaciones automáticas seguras]"
---

# /robin:doctor

Chequeo integral. Reporta verde / amarillo / rojo por componente.

## Procedimiento

1. **MCP de Robin.**
   - Llama `mcp__robin__buscar_normativa` con consulta `LEC`. Espera
     hits > 0.
   - ✅ verde si responde con resultados.
   - 🟡 amarillo si responde pero sin resultados (puede ser problema
     de corpus puntual).
   - ❌ rojo si timeout, 401, 403, 503 o no responde. Sugiere acción
     concreta:
     - 401 → "Tu token de Robin ha caducado. Reautentica en Ajustes →
       Conectores → robinlawyer.ai."
     - 403 → "Tu plan no tiene acceso a esta tool. Revisa tu
       suscripción en https://robinlawyer.ai/pricing."
     - timeout → "El servidor de Robin no responde. Revisa
       https://status.robinlawyer.ai."

2. **Playbook del despacho.**
   - Lee
     `~/.claude/plugins/config/claude-for-spanish-law/robin/CLAUDE.md`.
   - Cuenta `[PLACEHOLDER]` restantes.
   - ✅ verde si 0.
   - 🟡 amarillo si 1-3 (incompleto pero usable).
   - ❌ rojo si > 3 o no existe. Sugiere
     `/robin:cold-start-interview`.

3. **Company profile.**
   - Lee
     `~/.claude/plugins/config/claude-for-spanish-law/company-profile.md`.
   - Mismo criterio.

4. **Matter activo.**
   - Lee
     `~/.claude/plugins/config/claude-for-spanish-law/robin/active-matter`.
   - Si existe, comprueba que la carpeta del matter existe y
     `matter.md` es legible.
   - Si no existe matter activo, marca con ⚪ (no es error).

5. **Integraciones secundarias.**
   - Para cada MCP listado en el `.mcp.json` del plugin distinto de
     Robin, prueba una llamada de catálogo.
   - Reporta estado de cada uno por separado.

6. **Versiones.**
   - Lee
     `~/.claude/plugins/cache/claude-for-spanish-law/robin/<version>/`
     y reporta versión instalada.
   - Comprueba contra el manifest del marketplace si hay versión más
     reciente. Si la hay, sugiere actualizar.

7. **Hooks.**
   - Si hay hooks configurados, prueba uno seguro (no destructivo)
     para confirmar que el ciclo `PreToolUse` no falla.

## `--fix` (modo reparación segura)

Intenta acciones reversibles:

1. Si playbook no existe → arranca `cold-start-interview`
   automáticamente.
2. Si matter activo apunta a carpeta inexistente → desactiva el
   matter (sin borrar nada).
3. Si versión obsoleta → muestra comando exacto para actualizar.

**`--fix` NO** revoca/genera tokens OAuth (eso lo decide el usuario),
NO borra archivos, NO toca el corpus de Robin.

## Output

Reporte estructurado:

```
🩺 Robin Doctor

✅ MCP Robin                   responde (latencia 230ms)
✅ OAuth                       válido hasta 2026-08-14
⚠️  Playbook                   2 [PLACEHOLDER] sin rellenar (sección tono)
✅ Company profile             ok
✅ Matter activo               rodriguez-vs-banco-popular-2026
✅ Integraciones (Drive)       ok
⚠️  Versión                    1.0.0 instalada — disponible 1.0.2 (cambios)
✅ Hooks                       0 configurados

Próximos pasos sugeridos:
1. Completar sección 'tono' del playbook → /robin:customize tono
2. Actualizar plugin → /plugin update robin@claude-for-spanish-law
```
