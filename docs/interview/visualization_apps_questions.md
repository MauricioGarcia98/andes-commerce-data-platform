# Entrevista — Visualización, AI/BI y Databricks Apps

## 1. ¿Por qué no hacer solo un dashboard?
Porque el dashboard está orientado al análisis. La App está orientada a interacción operativa y a investigar excepciones.

## 2. ¿Qué problema resuelve el dashboard?
Reduce la necesidad de consolidar manualmente información y permite analizar métricas consistentes desde Gold.

## 3. ¿Qué problema resuelve la App?
Facilita tareas operativas como investigar inventario crítico, revisar calidad y explorar el estado general de la plataforma.

## 4. ¿Por qué no usar Power BI?
No se afirma que AI/BI sea superior. En este proyecto se utiliza AI/BI porque el consumidor está dentro del entorno Databricks y la demo busca mostrar integración con Gold, filtros y cross-filtering.

## 5. ¿Qué diferencia hay entre un filtro y un parámetro?
Un filtro limita registros/valores para visualizaciones. Un parámetro puede sustituirse directamente dentro de la consulta y ofrece mayor flexibilidad para modificar cómo se ejecuta la consulta.

## 6. ¿Por qué evitar un KPI calculado directamente sobre muchas tablas?
Para reducir riesgo de doble conteo y centralizar definiciones importantes en Gold/metric views cuando corresponda.

## 7. ¿Qué harías si un usuario cuestiona un KPI?
Trazo la métrica hacia Gold, verifico su definición, grain, filtros y reconciliación contra la fuente.

## 8. ¿Por qué la App usa Streamlit?
Porque Databricks Apps soporta Streamlit y permite construir aplicaciones de datos sin mantener una infraestructura web separada.

## 9. ¿Guardarías un token en GitHub?
No. En producción utilizaría la identidad/credenciales gestionadas por la aplicación y permisos mínimos.

## 10. ¿Qué pasa si la App se cae?
El Dashboard sigue siendo una vía de análisis independiente. La App es un componente de consumo/operación y no debe convertirse en dependencia del pipeline.

## 11. ¿Qué debería ver un gerente?
KPIs, tendencias, riesgos y excepciones.

## 12. ¿Qué debería ver un Data Engineer?
Pipeline status, DQ, registros rechazados, tiempos, freshness, errores y lineage.
