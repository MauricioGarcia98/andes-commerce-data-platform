# Entrevista - Silver

## Fundamentos

### 1. ¿Qué problema resuelve Silver?

Separar la ingestión raw de la transformación confiable. Bronze preserva la fuente; Silver estandariza y valida; Gold modela para el consumo del negocio.

### 2. ¿Por qué no transformar directamente Bronze?

Porque perderíamos trazabilidad y mezclaríamos responsabilidades. Mantener una capa raw permite reprocesar sin volver a pedir la fuente.

### 3. ¿Qué haces con un registro inválido?

No lo elimino silenciosamente. Lo mando a cuarentena junto con la razón del rechazo, run de origen y número de fila.

### 4. ¿Qué significa idempotencia?

Ejecutar de nuevo el mismo input no debería producir duplicados ni resultados inconsistentes.

### 5. ¿Por qué guardar record_hash?

Permite identificar cambios en el contenido de un registro y facilita patrones de deduplicación o change detection.

### 6. ¿Por qué no usar un hash como clave primaria?

Porque un hash identifica contenido, no necesariamente la identidad de negocio. Las claves de negocio siguen siendo necesarias.

## Casos incómodos

### ¿Qué harías si llegan dos filas con la misma order_id pero distinto total_amount?

No elegiría una arbitrariamente. Las marcaría como duplicado/conflicto, preservaría ambas y buscaría la regla de prioridad definida por el sistema fuente.

### ¿Por qué PySpark si el dataset actual es pequeño?

En local no lo necesito. El objetivo es separar generación y pruebas livianas de la implementación distribuida que ejecutaremos en Databricks. Para un workload pequeño real preferiría la alternativa más simple y económica.

### ¿Qué pasa si cambia una columna de la fuente?

El contrato debe detectarlo. En Databricks se podría gestionar schema evolution de forma controlada, pero no conviene aceptar cambios arbitrarios sin validación.
