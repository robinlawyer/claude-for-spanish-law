# Jerarquía jurisprudencial — cómo cita Robin

Toda skill que devuelva jurisprudencia ordena las sentencias según esta
jerarquía, con preferencia territorial al despacho cuando proceda.

## Orden general (descendente)

1. **Tribunal Constitucional (STC)** — vincula a todos los poderes
   públicos en el alcance del fallo (art. 5 LOPJ, art. 38 LOTC). Cita
   obligatoria si hay STC sobre el punto.

2. **Tribunal Supremo**
   - Pleno > Sala > Sección.
   - Recurso de casación, doctrina jurisprudencial, ratio decidendi.
   - Acuerdos no jurisdiccionales del Pleno post LO 1/2025. Se localizan
     vía `mcp__robin__buscar_jurisprudencia` con query "acuerdo no
     jurisdiccional Pleno" + fecha aproximada.

3. **Audiencia Nacional (Salas)** — vinculante en su ámbito; muy
   relevante en penal económico, contencioso y social colectivo.

4. **TSJ de referencia del despacho** — la doctrina del TSJ propio pesa
   más que la de otros TSJ. Robin la prioriza territorialmente.

5. **TSJ de otras CCAA** — relevante cuando hay criterio reiterado
   convergente.

6. **AP de referencia del despacho (sección concreta)** — la sección
   propia es la primera en aparecer.

7. **Otras AAPP del mismo TSJ** — segundo nivel.

8. **AAPP de otros TSJ** — tercer nivel; útil para mostrar criterio
   mayoritario nacional.

9. **Juzgados de instancia** — sólo cita Robin sentencias de juzgado
   si: el supuesto es muy específico, hay precedente reiterado del
   mismo juzgado, o el letrado lo pide expresamente.

## Tribunales europeos

- **TJUE** — cita obligatoria si hay derecho UE aplicable (RGPD,
  consumidores, igualdad, fiscalidad armonizada, libre prestación de
  servicios, etc.). Vincula a tribunales nacionales (arts. 4 bis LOPJ
  y 19 TUE).
- **TGUE** — cita relevante cuando se trate de actos UE, competencia,
  propiedad industrial UE.
- **TEDH** — vincula al Estado español; cita relevante en derechos
  fundamentales, equidad procesal, libertad de expresión, vida
  privada.

## Doctrina administrativa vinculante

Cuando el caso lo justifique, además de jurisprudencia:

- **DGT** — consultas vinculantes vinculan a la Administración
  tributaria (art. 89 LGT).
- **TEAC** — doctrina reiterada vincula a la Administración (art. 239.7
  LGT).
- **AEPD** — resoluciones por expediente; doctrina relevante en
  protección de datos.
- **CNMC, CNMV, BdE** — circulares y resoluciones sancionadoras en sus
  respectivos ámbitos.
- **TACRC** — doctrina en contratación pública.
- **TCU** — doctrina en gestión de fondos públicos.
- **Consejo de Estado** — dictámenes consultivos; vinculan formalmente
  solo si la ley los exige, pero pesan doctrinalmente.
- **Defensor del Pueblo** — recomendaciones; relevante en buena
  administración y derechos fundamentales.

## Reglas de cita

Toda sentencia se cita en este formato:

> STS [nº/año], Sala [1ª/2ª/3ª/4ª/5ª] [Pleno/Sección Xª], de [fecha]
> [(rec. nº)] — ECLI:ES:TS:AAAA:NNNN.

Ejemplos:

> STS 1234/2024, Sala 1ª, de 15 de octubre de 2024 (rec. 1100/2023) —
> ECLI:ES:TS:2024:5421.
>
> STC 56/2023, de 22 de mayo (recurso de amparo 4521-2022) —
> ECLI:ES:TC:2023:56.
>
> STJUE de 11 de diciembre de 2024, C-456/22, *Caso Glovo II* —
> ECLI:EU:C:2024:1010.
>
> SAP Barcelona 478/2025, Sección 14ª, de 7 de marzo de 2025 (rec.
> 989/2024) — ECLI:ES:APB:2025:478.

**El ECLI es obligatorio.** Una cita sin ECLI no se considera
verificada y no aparece en el escrito final. `verificar_cita` la marca
en rojo.

## Comportamiento ante contradicción

1. STC > resto, siempre.
2. Si TS Pleno > Sala > sección unificada → criterio del Pleno.
3. Si TS no ha unificado y hay disenso entre AAPP, Robin:
   - Cita ambas líneas.
   - Marca cuál sigue nuestra AP (la del despacho).
   - Recomienda al letrado decidir si abrir vía casación si la
     contradicción es relevante para el caso.
4. Si TJUE ha resuelto cuestión prejudicial sobre la misma cuestión:
   prima TJUE sobre cualquier sentencia nacional.

## Comportamiento ante jurisprudencia vieja

- TS antes de 2020: Robin la cita solo si el cliente la pide
  expresamente, si la doctrina sigue vigente literalmente, o si no hay
  posterior. Aviso al letrado: el corpus jurisprudencial completo de
  Robin se concentra en 2023+; STS clásicas pre-2020 pueden no estar
  indexadas. No es bug, es cobertura.
- Si una STS antigua sigue siendo *la* sentencia de referencia (típico
  en derecho civil clásico), Robin la cita aunque no esté en su corpus
  embebido, marcándola como "consulta cruzada CENDOJ" pendiente de
  verificación manual.
