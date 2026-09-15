# Especificación AI/BI Dashboard

## Objetivo

Construir un dashboard de autoservicio para dirección comercial y analistas. El dashboard debe responder preguntas de negocio, no decorar el proyecto.

Databricks AI/BI Dashboards permite crear datasets desde tablas/vistas/consultas SQL y aplicar filtros globales, de página y de widget. También soporta cross-filtering y drill-through.

## Página 1 — Executive Overview

### Pregunta
¿Cómo está funcionando el negocio?

### KPIs
- Revenue reconocido
- Gross Margin
- Margin %
- Orders
- Average Order Value
- Critical Inventory

### Visuales
1. Revenue trend
2. Revenue by channel
3. Margin by category
4. Inventory risk summary

## Página 2 — Sales Performance

### Pregunta
¿Dónde estamos vendiendo y dónde estamos perdiendo rentabilidad?

Visuales:
- revenue por categoría;
- margen por categoría;
- revenue por canal;
- unidades vendidas;
- evolución temporal.

Filtros:
- date range;
- region;
- store;
- category;
- channel.

## Página 3 — Inventory Risk

### Pregunta
¿Dónde debemos actuar primero?

Visuales:
- CRITICAL vs LOW vs HEALTHY;
- riesgo por tienda;
- productos críticos;
- stock actual vs reorder point.

Acción sugerida:
seleccionar un store/category para cross-filtering y drill-through.

## Página 4 — Customer Value

### Pregunta
¿Qué clientes y segmentos explican el valor comercial?

Visuales:
- revenue por segmento;
- top customers;
- AOV;
- frecuencia de compra;
- distribución geográfica.

## Reglas

- Todo visual debe responder una pregunta.
- No mostrar una métrica sin definición.
- Las métricas monetarias deben distinguir revenue reconocido de bruto facturado.
- Evitar mezclar facts con grains incompatibles.
- Usar filtros para investigación, no para ocultar problemas.
