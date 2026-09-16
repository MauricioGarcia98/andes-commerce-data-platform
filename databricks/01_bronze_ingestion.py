# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC # 01 - Bronze Ingestion
# MAGIC
# MAGIC Carga los CSV de la carpeta `data/sample/` a tablas Delta gestionadas en Unity Catalog.
# MAGIC
# MAGIC Principio: **Bronze conserva la forma de la fuente lo máximo posible** y agrega metadata operacional.

# COMMAND ----------

from pyspark.sql import functions as F

catalog = spark.sql("SELECT current_catalog() AS catalog").first()["catalog"]
raw_path = f"/Volumes/{catalog}/bronze/raw_files"

sources = {
    "customers": "customers.csv",
    "products": "products.csv",
    "stores": "stores.csv",
    "promotions": "promotions.csv",
    "orders": "orders.csv",
    "order_items": "order_items.csv",
    "payments": "payments.csv",
    "inventory": "inventory.csv",
    "promotion_redemptions": "promotion_redemptions.csv",
}

run_id = spark.sql("SELECT uuid() AS run_id").first()["run_id"]

# COMMAND ----------

for table_name, filename in sources.items():
    path = f"{raw_path}/{filename}"

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(path)
    )

    bronze_df = (
        df
        .withColumn("_source_file", F.lit(filename))
        .withColumn("_ingestion_run_id", F.lit(run_id))
        .withColumn("_ingested_at_utc", F.current_timestamp())
        .withColumn(
            "_source_row_hash",
            F.sha2(
                F.to_json(F.struct(*[F.col(c) for c in df.columns])),
                256
            )
        )
    )

    (
        bronze_df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(f"`{catalog}`.`bronze`.`{table_name}`")
    )

    print(f"Bronze loaded: {table_name}")

print(f"run_id={run_id}")