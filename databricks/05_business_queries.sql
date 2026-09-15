-- Andes Commerce - consultas de negocio sobre Gold

-- Revenue y margen por categoría
SELECT
  category,
  ROUND(SUM(revenue), 2) AS revenue,
  ROUND(SUM(gross_margin), 2) AS gross_margin,
  ROUND(100 * SUM(gross_margin) / NULLIF(SUM(revenue), 0), 2) AS margin_pct
FROM mart_sales_by_category
GROUP BY category
ORDER BY revenue DESC;

-- Riesgo de inventario
SELECT
  risk_priority,
  COUNT(*) AS sku_store_combinations
FROM mart_inventory_risk
GROUP BY risk_priority
ORDER BY risk_priority;

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

-- Reconciliación de revenue
SELECT
  ROUND(SUM(revenue_recognized), 2) AS recognized_revenue
FROM fact_order;
