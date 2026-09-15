# Operaciones y observabilidad

La plataforma debe poder operarse y recuperarse, no solamente producir un dataset.

## Señales
- pipeline status;
- records in/out/rejected;
- DQ score;
- duration;
- logs;
- source manifest;
- incidentes.

## Estados
SUCCESS / WARNING / FAILED / RUNNING

## Regla de promoción
Una regla crítica fallida bloquea la promoción a Gold.

## Idempotencia conceptual
Un mismo lote debe poder reprocesarse sin crear duplicados, usando claves de negocio, hashes o MERGE/UPSERT al llevar el patrón a Databricks.
