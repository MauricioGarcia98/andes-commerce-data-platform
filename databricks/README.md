# Implementación en Databricks

Esta carpeta lleva el diseño probado localmente a un Lakehouse sobre Databricks.

## Arquitectura

```text
CSV en Unity Catalog Volume
            |
            v
        Bronze Delta
            |
            v
        Silver Delta
            |
            v
         Gold Delta
        /          \
       v            v
   AI/BI         Databricks App
```

## Objetivo

Demostrar que el mismo caso de negocio puede evolucionar desde una arquitectura local liviana hacia una arquitectura cloud con Spark, Delta, Unity Catalog y orquestación.

## Archivos

- `00_setup.py` — prepara schemas y volume.
- `00_setup.sql` — alternativa SQL.
- `01_bronze_ingestion.py` — CSV -> Bronze Delta.
- `02_silver_transform.py` — Bronze -> Silver.
- `03_gold_model.py` — Silver -> Gold.
- `04_data_quality.py` — controles operativos.
- `05_business_queries.sql` — consultas de negocio.
- `06_job_design.md` — diseño de Lakeflow Job.

## Carga de datos

1. Ejecutar `00_setup.py`.
2. Obtener la ruta `/Volumes/<catalog>/bronze/raw_files` que imprime el notebook.
3. Desde Catalog Explorer seleccionar el volumen y subir los archivos de `data/sample/`.
4. Ejecutar `01_bronze_ingestion.py` y continuar en orden.

Databricks recomienda Unity Catalog para gobernar tablas y Volumes para archivos no tabulares. Los archivos pueden cargarse desde Catalog Explorer.

## Limitaciones del entorno gratuito

La implementación está pensada para Databricks Free Edition. Actualmente Free Edition utiliza únicamente serverless compute, tiene un SQL warehouse 2X-Small, hasta 5 tareas concurrentes en Jobs y hasta 3 Databricks Apps por cuenta. Por eso el proyecto utiliza datasets de portfolio y workflows pequeños.

## Fuentes oficiales

- https://docs.databricks.com/aws/en/getting-started/free-edition-limitations
- https://docs.databricks.com/aws/en/volumes/volume-files
- https://docs.databricks.com/aws/en/jobs
- https://docs.databricks.com/aws/en/dev-tools/databricks-apps
