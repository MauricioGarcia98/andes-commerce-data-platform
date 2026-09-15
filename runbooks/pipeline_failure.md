# Runbook — Pipeline Failure

## Objetivo
Resolver una ejecución fallida sin acciones destructivas.

## 1. Detectar
Revisar `observability/pipeline_runs.csv`, `observability/dq_results.csv` y los logs del run.

## 2. Clasificar
- Data Quality
- Source
- Transformation
- Infrastructure

## 3. Diagnosticar
1. Identificar `run_id`.
2. Identificar stage.
3. Revisar primera regla crítica fallida.
4. Comparar `records_in` vs `records_out`.
5. Revisar cambios de esquema.
6. Revisar la fuente.
7. Confirmar reproducibilidad.

## 4. Recuperar
Corregir causa, conservar Bronze, reprocesar el lote afectado, ejecutar DQ y validar reconciliación.

## 5. Cerrar
Registrar causa raíz, impacto, solución, run de recuperación y acción preventiva.

## Entrevista
Reiniciar ciegamente puede duplicar datos o repetir el error. Primero se identifica la causa y luego se decide entre retry, rerun parcial o backfill controlado.
