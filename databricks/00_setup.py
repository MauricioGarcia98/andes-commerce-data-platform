# Databricks notebook source
# MAGIC %md
# MAGIC # 00 - Setup
# MAGIC 
# MAGIC Este notebook prepara los objetos de Unity Catalog utilizados por Andes Commerce.
# MAGIC 
# MAGIC - bronze: ingesta y datos cercanos a la fuente
# MAGIC - silver: datos limpios y tipificados
# MAGIC - gold: modelos orientados al negocio
# MAGIC - ops: metadata operacional y controles
# MAGIC - bronze.raw_files: volumen administrado para cargar los CSV de `data/sample/`
# MAGIC 
# MAGIC El notebook usa el catálogo por defecto del workspace para evitar hardcodear un nombre de catálogo.

catalog = spark.sql("SELECT current_catalog() AS catalog").first()["catalog"]

for schema in ["bronze", "silver", "gold", "ops"]:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS `{catalog}`.`{schema}`")

spark.sql(f"CREATE VOLUME IF NOT EXISTS `{catalog}`.`bronze`.raw_files")

print(f"Catalog: {catalog}")
print("Schemas: bronze, silver, gold, ops")
print(f"Raw upload path: /Volumes/{catalog}/bronze/raw_files")
