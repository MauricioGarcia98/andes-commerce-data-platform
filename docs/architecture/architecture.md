# Arquitectura

## AS-IS

POS --------Ecommerce ----> archivos / bases aisladas -> Excel / reporting manual
CRM ----------/
ERP ----------/

Problemas:
- fuentes heterogéneas;
- definiciones diferentes;
- poca trazabilidad;
- procesos manuales.

## TO-BE

              +----------------------+
              |   Source Systems     |
              | CSV / JSON / SQLite  |
              +----------+-----------+
                         |
                         v
                    +---------+
                    | Bronze  |
                    +----+----+
                         |
                         v
                    +---------+
                    | Silver  |
                    | Clean   |
                    | DQ      |
                    +----+----+
                         |
                         v
                    +---------+
                    |  Gold   |
                    | Business|
                    +----+----+
                         |
              +----------+-----------+
              |                      |
              v                      v
        AI/BI Dashboard       Databricks App

## Decisiones

### ¿Por qué separar Bronze/Silver/Gold?

Para preservar trazabilidad, separar limpieza de lógica de negocio y facilitar reutilización.

### ¿Por qué Python + SQLite local?

Porque la máquina local tiene recursos limitados y no necesita procesamiento distribuido.

### ¿Por qué Databricks para la capa distribuida?

Porque el objetivo del portfolio incluye demostrar Spark/PySpark y patrones Lakehouse sin exigir infraestructura local pesada.

### ¿Por qué no Kafka?

No se necesita streaming real para este caso. Agregarlo introduciría complejidad sin resolver un problema actual.

### ¿Por qué no Airflow local?

La PC del proyecto es deliberadamente limitada. La orquestación se demostrará en el entorno cloud.
