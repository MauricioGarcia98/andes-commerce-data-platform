# Data Contracts iniciales

Los contratos definen el esquema esperado y reglas mínimas para los datasets de entrada.

## customers

- customer_id: string, not null, unique.
- first_name: string, not null.
- last_name: string, not null.
- email: string, not null, unique lógico.
- signup_date: date, not null.
- customer_segment: enum [STANDARD, PREMIUM, BUSINESS].
- city: string, not null.

## products

- product_id: string, not null, unique.
- sku: string, not null, unique.
- category: string, not null.
- unit_cost: decimal, >= 0.
- list_price: decimal, >= 0.
- active_flag: boolean.

## stores

- store_id: string, not null, unique.
- store_name: string, not null.
- city: string, not null.
- region: string, not null.
- channel: enum [STORE, ECOMMERCE].

## orders

- order_id: string, not null, unique.
- customer_id: string, not null.
- store_id: string, nullable for pure ecommerce if modeled that way.
- order_date: date, not null.
- channel: enum [STORE, ECOMMERCE].
- status: enum [COMPLETED, CANCELLED, RETURNED, PENDING].
- total_amount: decimal, >= 0.

## order_items

- order_item_id: string, not null, unique.
- order_id: string, not null.
- product_id: string, not null.
- quantity: integer, > 0.
- unit_price: decimal, >= 0.
- discount_amount: decimal, >= 0.

## payments

- payment_id: string, not null, unique.
- order_id: string, not null.
- payment_method: enum [CARD, CASH, TRANSFER, WALLET].
- payment_status: enum [APPROVED, REJECTED, REFUNDED].
- amount: decimal, >= 0.
