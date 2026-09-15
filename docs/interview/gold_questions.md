# Entrevista — Gold, modelado y negocio

## 1. ¿Por qué no exponer Silver directamente al dashboard?

Porque Silver optimiza confiabilidad y estandarización, mientras Gold optimiza consumo y semántica de negocio. Separarlos evita repetir lógica de negocio en cada dashboard.

## 2. ¿Cuál es el grain de fact_sales_line?

Una fila por línea de pedido aceptada.

## 3. ¿Cuál es el grain de fact_order?

Una fila por pedido.

## 4. ¿Por qué tener ambas facts?

Porque responden preguntas distintas. Line-level permite analizar producto, descuento, costo y margen. Order-level simplifica métricas de pedido y reduce cálculos repetidos.

## 5. ¿Cómo evitás doble conteo?

Definiendo el grain explícitamente y estableciendo qué fact es la fuente de cada métrica.

## 6. ¿Qué significa revenue reconocido en este proyecto?

Una venta de un pedido `COMPLETED` cuyo pago está `APPROVED`.

## 7. ¿Por qué no usar total_amount de orders como revenue Gold?

Porque es un valor de cabecera generado independientemente de las líneas. Para trazabilidad analítica se calcula el revenue desde las líneas de venta reconocidas.

## 8. ¿Qué harías si source total_amount y line totals no coinciden?

No ocultaría la discrepancia. La convertiría en una regla de reconciliación, mediría su frecuencia y acordaría con negocio cuál es la fuente de verdad.

## 9. ¿Star schema o snowflake?

Para este caso elegiría un modelo tipo estrella porque prioriza consumo analítico y simplicidad de consultas.

## 10. ¿Por qué una dimensión de fecha?

Centraliza la semántica temporal y facilita análisis por año, mes, trimestre, semana y día.

## 11. ¿Qué KPI mostrarías al director comercial?

Revenue, margen, ticket promedio, pedidos y riesgo de inventario.

## 12. ¿Qué KPI mostrarías al gerente de tienda?

Revenue de la tienda, margen, unidades, pedidos y productos en estado CRITICAL/LOW.
