# Bronze Layer

## Objetivo

Bronze representa la primera capa controlada de aterrizaje. Conserva los datos lo más cerca posible de la fuente y agrega metadata de ingesta.

## Local

Para este portfolio se simula Bronze en:

`data/bronze/<run_id>/`

No pretende reemplazar el storage cloud.

## Cloud

En Databricks, Bronze se implementará posteriormente sobre almacenamiento compatible con Delta.

## Metadata

Cada ejecución registra:

- run_id
- source_file
- source_path
- target_path
- ingested_at_utc
- status

## Idempotencia

En la siguiente iteración se incorporará una estrategia explícita para evitar duplicar una misma carga cuando se reprocesa una fuente.
