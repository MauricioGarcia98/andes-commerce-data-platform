# Paso a paso

## 1. Problema de negocio
Leer `docs/business/business_case.md`.

## 2. Fuentes y generadores
Leer `docs/data/generator_strategy.md` y ejecutar los generadores por tabla o `run_all_generators.py`.

## 3. Bronze
Ingestar las fuentes sin cambiar su significado y registrar metadata de ejecución.

## 4. Data Quality
Ejecutar reglas de calidad y revisar `data/dq_results/`.

## 5. Quality Lab
Ejecutar incidentes controlados para aprender diagnóstico y cuarentena.

## 6. Silver
Normalizar, tipificar, validar, deduplicar, enriquecer y conservar trazabilidad.

## 7. Gold
Diseñar por grain y por preguntas de negocio:

- dimensions;
- facts;
- marts.

## 8. Reconciliación
Comparar pedidos completados + pagos aprobados contra revenue reconocido de Gold.

## 9. Dashboard
Construir AI/BI Dashboard sobre Gold. Cada visual debe responder una pregunta.

## 10. App
Construir Databricks App orientada a operación y control, no una copia del dashboard.

## 11. Entrevista
Estudiar el dossier de cada capa y ser capaz de defender trade-offs.
