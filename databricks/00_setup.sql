-- Andes Commerce - Databricks Setup
-- Ejecutar una sola vez en un notebook SQL.
-- Unity Catalog viene habilitado automáticamente en workspaces nuevos de Databricks.

CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
CREATE SCHEMA IF NOT EXISTS ops;

CREATE VOLUME IF NOT EXISTS bronze.raw_files;

SELECT current_catalog() AS catalog_actual;
