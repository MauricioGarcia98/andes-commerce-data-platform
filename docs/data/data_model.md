# Modelo de datos

## Dimensiones

- customers
- products
- stores
- dates
- promotions

## Hechos

- orders
- order_items
- payments
- inventory
- promotion_redemptions

## Grain

### orders
Una fila por pedido.

### order_items
Una fila por línea de producto dentro de un pedido.

### payments
Una fila por transacción de pago.

### inventory
Una fila por producto y tienda para un snapshot de inventario.

### promotion_redemptions
Una fila por promoción aplicada a una línea/pedido.

## Relaciones principales

customers 1 -> N orders
orders 1 -> N order_items
products 1 -> N order_items
stores 1 -> N orders
orders 1 -> N payments
products + stores -> inventory
promotions 1 -> N promotion_redemptions
