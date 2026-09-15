# Databricks notebook source
# MAGIC %md
# MAGIC # 03 - Gold Model
# MAGIC 
# MAGIC Modelos de negocio para análisis. El grain está documentado explícitamente para evitar doble conteo.

from pyspark.sql import functions as F

catalog = spark.sql("SELECT current_catalog() AS catalog").first()["catalog"]

def save(df, name):
    df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"`{catalog}`.`gold`.`{name}`")

customers = spark.table(f"`{catalog}`.`silver`.customers")
products = spark.table(f"`{catalog}`.`silver`.products")
stores = spark.table(f"`{catalog}`.`silver`.stores")
orders = spark.table(f"`{catalog}`.`silver`.orders")
items = spark.table(f"`{catalog}`.`silver`.order_items")
payments = spark.table(f"`{catalog}`.`silver`.payments")
inventory = spark.table(f"`{catalog}`.`silver`.inventory")
promotions = spark.table(f"`{catalog}`.`silver`.promotions")

# Dimensions
save(customers.select(*[c for c in customers.columns if not c.startswith("_")]), "dim_customer")
save(products.select(*[c for c in products.columns if not c.startswith("_")]), "dim_product")
save(stores.select(*[c for c in stores.columns if not c.startswith("_")]), "dim_store")
save(promotions.select(*[c for c in promotions.columns if not c.startswith("_")]), "dim_promotion")

# Fact order: 1 row per order
fact_order = (
    orders.join(
        payments.filter(F.col("payment_status") == "APPROVED").select("order_id", "payment_status"),
        "order_id", "left"
    )
    .withColumn("revenue_recognized", F.when((F.col("status") == "COMPLETED") & F.col("payment_status").isNotNull(), F.col("total_amount")).otherwise(F.lit(0)))
)
save(fact_order, "fact_order")

# Fact sales line: 1 row per order item
fact_sales_line = (
    items.join(orders.select("order_id", "customer_id", "store_id", "order_date", "channel", "status"), "order_id", "left")
    .join(products.select("product_id", "category", "unit_cost"), "product_id", "left")
    .withColumn("recognized_revenue", F.when(F.col("status") == "COMPLETED", F.col("net_amount")).otherwise(F.lit(0)))
    .withColumn("cost_amount", F.round(F.col("quantity") * F.col("unit_cost"), 2))
    .withColumn("gross_margin", F.round(F.col("recognized_revenue") - F.col("cost_amount"), 2))
)
save(fact_sales_line, "fact_sales_line")

# Inventory snapshot: 1 row per product/store/snapshot_date
save(inventory, "fact_inventory_snapshot")

# Business marts
sales_by_category = (
    fact_sales_line.groupBy("category")
    .agg(
        F.round(F.sum("recognized_revenue"),2).alias("revenue"),
        F.round(F.sum("gross_margin"),2).alias("gross_margin"),
        F.sum("quantity").alias("units")
    )
    .withColumn("margin_pct", F.round(F.when(F.col("revenue") != 0, F.col("gross_margin") / F.col("revenue") * 100).otherwise(0),2))
)
save(sales_by_category, "mart_sales_by_category")

store_performance = (
    fact_sales_line.groupBy("store_id")
    .agg(
        F.round(F.sum("recognized_revenue"),2).alias("revenue"),
        F.round(F.sum("gross_margin"),2).alias("gross_margin"),
        F.sum("quantity").alias("units")
    )
    .withColumn("margin_pct", F.round(F.when(F.col("revenue") != 0, F.col("gross_margin") / F.col("revenue") * 100).otherwise(0),2))
)
save(store_performance, "mart_store_performance")

inventory_risk = (
    inventory.withColumn(
        "risk_priority",
        F.when(F.col("on_hand_qty") <= F.col("reorder_point"), F.lit("CRITICAL"))
         .when(F.col("on_hand_qty") <= F.col("reorder_point") * 2, F.lit("LOW"))
         .otherwise(F.lit("HEALTHY"))
    )
)
save(inventory_risk, "mart_inventory_risk")

customer_value = (
    fact_order.filter(F.col("revenue_recognized") > 0)
    .groupBy("customer_id")
    .agg(
        F.countDistinct("order_id").alias("orders"),
        F.round(F.sum("revenue_recognized"),2).alias("revenue"),
        F.round(F.avg("revenue_recognized"),2).alias("avg_order_value"),
        F.max("order_date").alias("last_order_date")
    )
)
save(customer_value, "mart_customer_value")

print("Gold model completed.")
