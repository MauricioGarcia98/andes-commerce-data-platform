# Capa Gold

## Propósito

Gold traduce datos confiables de Silver a modelos que responden preguntas de negocio. No es una copia de Silver: cambia el diseño hacia consumo analítico.

## Granularidad

### fact_sales_line
Una fila por línea de pedido aceptada.

Uso: revenue, unidades, descuentos, costo y margen.

### fact_order
Una fila por pedido.

Uso: ticket promedio, conteo de pedidos, estados y métricas a nivel de cabecera.

### fact_inventory_snapshot
Una fila por producto + tienda + fecha de snapshot.

Uso: stock y riesgo.

### dim_customer
Una fila por cliente.

### dim_product
Una fila por producto.

### dim_store
Una fila por tienda/canal físico.

### dim_promotion
Una fila por promoción.

### dim_date
Una fila por fecha.

## Regla crítica: evitar doble conteo

No se debe sumar revenue de `fact_order` y `fact_sales_line` en la misma métrica. Se eligió `fact_sales_line` como fuente principal para métricas de ventas porque permite explicar el cálculo hasta producto y línea.

## Reconocimiento de revenue

Se considera revenue reconocido cuando:

- el pedido está `COMPLETED`;
- el pago está `APPROVED`.

El revenue Gold se calcula a partir de `net_amount` de las líneas reconocidas.

Esto evita tratar como ventas reales pedidos cancelados, devueltos o pagos rechazados.

## Marts

- `mart_sales_by_category`
- `mart_sales_by_channel`
- `mart_store_performance`
- `mart_inventory_risk`
- `mart_customer_value`

Estos marts están diseñados para responder las preguntas del Business Case y alimentar el dashboard/app.
