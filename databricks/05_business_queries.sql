-- Databricks notebook source
-- MAGIC %md
-- MAGIC # 05 - Business Queries
-- MAGIC
-- MAGIC Consultas de negocio sobre la capa Gold.
-- COMMAND ----------
-- Revenue y margen por categoría
SELECT
  category,
  ROUND(SUM(revenue), 2) AS revenue,
  ROUND(SUM(gross_margin), 2) AS gross_margin,
  ROUND(100 * SUM(gross_margin) / NULLIF(SUM(revenue), 0), 2) AS margin_pct
FROM mart_sales_by_category
GROUP BY category
ORDER BY revenue DESC;
-- COMMAND ----------
-- Riesgo de inventario
SELECT
  risk_priority,
  COUNT(*) AS sku_store_combinations
FROM mart_inventory_risk
GROUP BY risk_priority
ORDER BY risk_priority;
-- COMMAND ----------
-- Clientes por valor
SELECT
  customer_id,
  orders,
  revenue,
  avg_order_value,
  last_order_date
FROM mart_customer_value
ORDER BY revenue DESC
LIMIT 20;
-- COMMAND ----------
-- Reconciliación de revenue
SELECT
  ROUND(SUM(revenue_recognized), 2) AS recognized_revenue
FROM fact_order;
