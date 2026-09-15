-- Databricks notebook source
-- MAGIC %md
-- MAGIC # Setup SQL alternativo
-- MAGIC
-- MAGIC Esta versión SQL es opcional. El flujo principal utiliza `00_setup.py`.
-- COMMAND ----------
SELECT current_catalog() AS catalog_actual;
-- COMMAND ----------
-- Este bloque se ejecuta solo si el catálogo actual permite crear schemas.
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;
CREATE SCHEMA IF NOT EXISTS ops;
-- COMMAND ----------
CREATE VOLUME IF NOT EXISTS bronze.raw_files;
