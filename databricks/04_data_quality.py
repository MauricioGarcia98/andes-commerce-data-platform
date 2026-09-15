# Databricks notebook source
# MAGIC %md
# MAGIC # 04 - Data Quality en Databricks
# MAGIC 
# MAGIC Registra controles de calidad en `ops.data_quality_results` para que puedan ser consumidos por el dashboard y la App.

from pyspark.sql import functions as F
from datetime import datetime, timezone

catalog = spark.sql("SELECT current_catalog() AS catalog").first()["catalog"]
run_id = spark.sql("SELECT uuid() AS run_id").first()["run_id"]

checks = []

def add_check(dataset, rule, status, checked, failed, severity="ERROR", detail=""):
    checks.append((run_id, dataset, rule, status, int(checked), int(failed), severity, detail))

# Critical tests on Gold
fact_order = spark.table(f"`{catalog}`.`gold`.fact_order")
fact_sales = spark.table(f"`{catalog}`.`gold`.fact_sales_line")

rows = fact_order.count()
dup = fact_order.groupBy("order_id").count().filter("count > 1").count()
add_check("gold.fact_order", "order_id_unique", "PASS" if dup == 0 else "FAIL", rows, dup)

invalid_status = fact_order.filter(~F.col("status").isin("COMPLETED", "CANCELLED", "RETURNED", "PENDING")).count()
add_check("gold.fact_order", "status_domain", "PASS" if invalid_status == 0 else "FAIL", rows, invalid_status)

sales_rows = fact_sales.count()
negative_net = fact_sales.filter(F.col("net_amount") < 0).count()
add_check("gold.fact_sales_line", "net_amount_non_negative", "PASS" if negative_net == 0 else "FAIL", sales_rows, negative_net)

null_product = fact_sales.filter(F.col("product_id").isNull()).count()
add_check("gold.fact_sales_line", "product_fk_present", "PASS" if null_product == 0 else "FAIL", sales_rows, null_product)

result_df = spark.createDataFrame(checks, ["run_id","dataset","rule","status","records_checked","records_failed","severity","detail"])
result_df = result_df.withColumn("checked_at_utc", F.current_timestamp())

(
    result_df.write
    .format("delta")
    .mode("append")
    .saveAsTable(f"`{catalog}`.`ops`.data_quality_results")
)

summary = result_df.groupBy("status").count().collect()
print(summary)
