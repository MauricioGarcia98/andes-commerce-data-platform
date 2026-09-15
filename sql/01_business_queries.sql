-- SQL de referencia para la capa analítica.
-- Estas consultas se ampliarán una vez construidas las capas Silver/Gold.

-- 1. Revenue por canal
SELECT
    channel,
    ROUND(SUM(total_amount), 2) AS revenue
FROM orders
WHERE status = 'COMPLETED'
GROUP BY channel;

-- 2. Pedidos por estado
SELECT status, COUNT(*) AS orders
FROM orders
GROUP BY status;

-- 3. Productos con mayor volumen vendido
SELECT
    product_id,
    SUM(quantity) AS units
FROM order_items
GROUP BY product_id
ORDER BY units DESC
LIMIT 10;
