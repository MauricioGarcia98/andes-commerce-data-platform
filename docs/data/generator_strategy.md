# Estrategia de generación

Cada tabla posee un generador independiente.

## Motivos

- Permitir ejecutar y probar una fuente específica.
- Facilitar debugging.
- Mantener responsabilidades acotadas.
- Permitir escalar cada dataset de manera diferente.
- Simular fuentes independientes.

## Reproducibilidad

Todos los generadores reciben una seed fija.

## Integridad referencial

Los generadores que dependen de claves existentes leen catálogos o IDs generados previamente.

## No crear datos absurdos

Los generadores deben respetar reglas de negocio. Por ejemplo:

- no puede existir un order_item sin order_id;
- quantity debe ser positiva;
- list_price debe ser >= unit_cost;
- un payment rechazado no debería contarse como revenue;
- un pedido cancelado no debería aumentar ventas reconocidas.

## Orden recomendado

1. stores
2. customers
3. products
4. promotions
5. orders
6. order_items
7. payments
8. inventory
9. promotion_redemptions
