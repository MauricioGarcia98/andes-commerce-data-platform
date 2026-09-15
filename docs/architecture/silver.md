# Capa Silver

## Propósito

Silver transforma la copia Bronze en datasets analíticos confiables sin modificar la evidencia original.

## Principios

- Bronze es inmutable para el flujo conceptual del proyecto.
- Silver estandariza strings, enums, fechas, enteros y decimales.
- Las claves primarias se controlan para detectar duplicados.
- Los registros inválidos se rechazan hacia `data/quarantine/` y conservan el origen de la fila.
- Cada registro Silver conserva `source_run_id`, `source_row_number`, `silver_processed_at_utc` y `record_hash`.
- Para `order_items` se calculan `gross_amount` y `net_amount`.

## ¿Por qué cuarentena?

Un registro inválido no debe desaparecer. El objetivo es separar el dato que puede continuar del que necesita análisis, manteniendo evidencia para debugging y reproceso.

## Idempotencia conceptual

El `source_run_id` identifica la ejecución Bronze que originó el dato. El `record_hash` permite detectar cambios posteriores y ayuda a construir mecanismos de deduplicación más avanzados en Databricks.

## Antes de Gold

Silver no contiene métricas de negocio finales. Su responsabilidad es dejar los datos limpios, consistentes y trazables para que Gold pueda enfocarse en preguntas de negocio.
