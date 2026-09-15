-- Validaciones que usaremos para comparar Bronze vs Silver.

-- Conteo total por dataset.
-- El mismo patrón se trasladará a Databricks SQL.

-- Ejemplo order_items: el net_amount debe ser coherente.
SELECT
    order_item_id,
    quantity,
    unit_price,
    discount_amount,
    gross_amount,
    net_amount
FROM silver_order_items
WHERE CAST(net_amount AS DECIMAL(18,2)) < 0;

-- Productos donde el precio final es menor al costo.
SELECT
    product_id,
    unit_cost,
    list_price
FROM silver_products
WHERE CAST(list_price AS DECIMAL(18,2)) < CAST(unit_cost AS DECIMAL(18,2));

-- Pedidos aceptados cuya clave debería ser única.
SELECT
    order_id,
    COUNT(*) AS row_count
FROM silver_orders
GROUP BY order_id
HAVING COUNT(*) > 1;
