-- Gold: preguntas de negocio

-- 1. Revenue y margen por categoría
SELECT
    category,
    SUM(net_sales) AS revenue,
    SUM(gross_margin) AS gross_margin,
    ROUND(SUM(gross_margin) * 100.0 / NULLIF(SUM(net_sales),0), 2) AS margin_pct
FROM gold.fact_sales_line
WHERE recognized_revenue_flag = true
GROUP BY category
ORDER BY revenue DESC;

-- 2. Ticket promedio por canal
SELECT
    channel,
    SUM(net_sales) / COUNT(DISTINCT order_id) AS average_order_value
FROM gold.fact_sales_line
WHERE recognized_revenue_flag = true
GROUP BY channel;

-- 3. Tiendas con mayor riesgo de inventario
SELECT
    store_id,
    COUNT(*) AS inventory_records,
    SUM(CASE WHEN stock_status = 'CRITICAL' THEN 1 ELSE 0 END) AS critical_records,
    SUM(CASE WHEN stock_status = 'LOW' THEN 1 ELSE 0 END) AS low_records
FROM gold.fact_inventory_snapshot
GROUP BY store_id
ORDER BY critical_records DESC, low_records DESC;

-- 4. Clientes de mayor valor
SELECT
    customer_id,
    SUM(net_sales) AS revenue,
    COUNT(DISTINCT order_id) AS orders,
    SUM(net_sales) / COUNT(DISTINCT order_id) AS average_order_value
FROM gold.fact_sales_line
WHERE recognized_revenue_flag = true
GROUP BY customer_id
ORDER BY revenue DESC
LIMIT 20;

-- 5. Detección conceptual de categorías con volumen alto y margen bajo
SELECT
    category,
    SUM(quantity) AS units,
    SUM(net_sales) AS revenue,
    ROUND(SUM(gross_margin) * 100.0 / NULLIF(SUM(net_sales),0),2) AS margin_pct
FROM gold.fact_sales_line
WHERE recognized_revenue_flag = true
GROUP BY category
HAVING SUM(quantity) > 5000
ORDER BY margin_pct ASC;
