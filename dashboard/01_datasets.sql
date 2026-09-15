-- Datasets sugeridos para AI/BI Dashboard.
-- Ajustar el catálogo/esquema al workspace real.

-- Executive KPIs
SELECT
  SUM(revenue) AS revenue,
  SUM(gross_margin) AS gross_margin,
  SUM(orders) AS orders,
  CASE WHEN SUM(orders) = 0 THEN 0 ELSE SUM(revenue)/SUM(orders) END AS aov,
  CASE WHEN SUM(revenue) = 0 THEN 0 ELSE SUM(gross_margin)/SUM(revenue) END AS margin_pct
FROM andes_commerce.gold.mart_sales_by_channel;

-- Sales by category
SELECT category, revenue, gross_margin
FROM andes_commerce.gold.mart_sales_by_category
ORDER BY revenue DESC;

-- Store performance
SELECT *
FROM andes_commerce.gold.mart_store_performance
ORDER BY revenue DESC;

-- Inventory risk
SELECT *
FROM andes_commerce.gold.mart_inventory_risk
ORDER BY critical_count DESC;

-- Customer value
SELECT *
FROM andes_commerce.gold.mart_customer_value
ORDER BY revenue DESC;
