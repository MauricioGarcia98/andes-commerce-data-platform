# Databricks App — Operations Control Center

Esta aplicación es complementaria al AI/BI Dashboard.

## Qué problema resuelve

El dashboard responde preguntas analíticas. La App ayuda a investigar excepciones operativas:

- inventario crítico;
- resultados de Data Quality;
- estado general de pipelines;
- KPI principales;
- exploración por categoría/región.

## Tecnologías

- Streamlit
- Databricks SQL Connector
- Unity Catalog / Gold
- Databricks Apps

## Por qué Streamlit

Databricks Apps soporta Streamlit como framework para construir aplicaciones de datos sobre la plataforma.

## Demo sin credenciales

Si no existen variables de conexión, la aplicación utiliza datos demo estáticos para permitir mostrar la interfaz durante una entrevista.

## Variables para Databricks

```text
DATABRICKS_SERVER_HOSTNAME
DATABRICKS_HTTP_PATH
DATABRICKS_TOKEN
DATABRICKS_CATALOG
DATABRICKS_SCHEMA
DATABRICKS_WAREHOUSE_ID
```

En un despliegue real se debe preferir autenticación de aplicación/identidad administrada y permisos mínimos, no almacenar tokens en el repositorio.
