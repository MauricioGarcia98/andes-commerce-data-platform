# Databricks notebook source
# MAGIC %md
# MAGIC # 02 - Silver Transform
# MAGIC 
# MAGIC Limpieza, tipificación y deduplicación sobre Bronze. El objetivo es producir tablas confiables para Gold.

from pyspark.sql import functions as F
from pyspark.sql.window import Window

catalog = spark.sql("SELECT current_catalog() AS catalog").first()["catalog"]

# Customers
customers = spark.table(f"`{catalog}`.`bronze`.customers")
customers = (
    customers
    .withColumn("customer_id", F.trim("customer_id"))
    .withColumn("email", F.lower(F.trim("email")))
    .withColumn("signup_date", F.to_date("signup_date"))
    .withColumn("customer_segment", F.upper(F.trim("customer_segment")))
)
customers = customers.dropDuplicates(["customer_id"])
customers.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"`{catalog}`.`silver`.customers")

# Products
products = spark.table(f"`{catalog}`.`bronze`.products")
products = (
    products
    .withColumn("product_id", F.trim("product_id"))
    .withColumn("sku", F.trim("sku"))
    .withColumn("unit_cost", F.col("unit_cost").cast("decimal(18,2)"))
    .withColumn("list_price", F.col("list_price").cast("decimal(18,2)"))
    .withColumn("active_flag", F.col("active_flag").cast("boolean"))
    .dropDuplicates(["product_id"])
)
products.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"`{catalog}`.`silver`.products")

# Stores
stores = spark.table(f"`{catalog}`.`bronze`.stores")
stores = (
    stores
    .withColumn("store_id", F.trim("store_id"))
    .withColumn("channel", F.upper(F.trim("channel")))
    .withColumn("active_flag", F.col("active_flag").cast("boolean"))
    .dropDuplicates(["store_id"])
)
stores.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"`{catalog}`.`silver`.stores")

# Orders
orders = spark.table(f"`{catalog}`.`bronze`.orders")
orders = (
    orders
    .withColumn("order_id", F.trim("order_id"))
    .withColumn("customer_id", F.trim("customer_id"))
    .withColumn("store_id", F.when(F.trim("store_id") == "", None).otherwise(F.trim("store_id")))
    .withColumn("order_date", F.to_date("order_date"))
    .withColumn("channel", F.upper(F.trim("channel")))
    .withColumn("status", F.upper(F.trim("status")))
    .withColumn("total_amount", F.col("total_amount").cast("decimal(18,2)"))
    .dropDuplicates(["order_id"])
)
orders.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"`{catalog}`.`silver`.orders")

# Order items
items = spark.table(f"`{catalog}`.`bronze`.order_items")
items = (
    items
    .withColumn("order_item_id", F.trim("order_item_id"))
    .withColumn("quantity", F.col("quantity").cast("int"))
    .withColumn("unit_price", F.col("unit_price").cast("decimal(18,2)"))
    .withColumn("discount_amount", F.col("discount_amount").cast("decimal(18,2)"))
    .withColumn("gross_amount", F.round(F.col("quantity") * F.col("unit_price"), 2))
    .withColumn("net_amount", F.round(F.col("gross_amount") - F.col("discount_amount"), 2))
    .dropDuplicates(["order_item_id"])
)
items.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"`{catalog}`.`silver`.order_items")

# Payments
payments = spark.table(f"`{catalog}`.`bronze`.payments")
payments = (
    payments
    .withColumn("payment_id", F.trim("payment_id"))
    .withColumn("payment_status", F.upper(F.trim("payment_status")))
    .withColumn("amount", F.col("amount").cast("decimal(18,2)"))
    .dropDuplicates(["payment_id"])
)
payments.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"`{catalog}`.`silver`.payments")

# Inventory
inventory = spark.table(f"`{catalog}`.`bronze`.inventory")
inventory = (
    inventory
    .withColumn("snapshot_date", F.to_date("snapshot_date"))
    .withColumn("on_hand_qty", F.col("on_hand_qty").cast("int"))
    .withColumn("reorder_point", F.col("reorder_point").cast("int"))
    .withColumn("stock_status", F.upper(F.trim("stock_status")))
    .dropDuplicates(["product_id", "store_id", "snapshot_date"])
)
inventory.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"`{catalog}`.`silver`.inventory")

# Promotions
promotions = spark.table(f"`{catalog}`.`bronze`.promotions")
promotions = (
    promotions
    .withColumn("promotion_id", F.trim("promotion_id"))
    .withColumn("discount_pct", F.col("discount_pct").cast("decimal(5,2)"))
    .withColumn("start_date", F.to_date("start_date"))
    .withColumn("end_date", F.to_date("end_date"))
    .dropDuplicates(["promotion_id"])
)
promotions.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"`{catalog}`.`silver`.promotions")

# Promotion redemptions
red = spark.table(f"`{catalog}`.`bronze`.promotion_redemptions")
red = (
    red
    .withColumn("redemption_id", F.trim("redemption_id"))
    .withColumn("discount_amount", F.col("discount_amount").cast("decimal(18,2)"))
    .dropDuplicates(["redemption_id"])
)
red.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"`{catalog}`.`silver`.promotion_redemptions")

print("Silver transformation completed.")
