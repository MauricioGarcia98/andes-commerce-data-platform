# Guion de entrevista — Andes Commerce

## 60 segundos

Andes Commerce es una plataforma E2E para resolver fragmentación de datos de ventas e inventario. Integra varias fuentes, conserva una capa Bronze, limpia y valida en Silver y publica un modelo Gold orientado a negocio. Sobre Gold se construyen analítica y una aplicación operativa.

## 3 minutos

1. Explicar el problema de negocio.
2. Mostrar AS-IS y TO-BE.
3. Mostrar generadores independientes por tabla.
4. Explicar Bronze/Silver/Gold.
5. Mostrar una regla DQ y un incidente.
6. Mostrar una métrica Gold.
7. Mostrar Dashboard/App.
8. Explicar observabilidad y recovery.

## Pregunta final que conviene anticipar

¿Qué harías si el volumen creciera 100x?

Respuesta orientativa: conservaría el contrato y el modelo lógico, pero revisaría particionamiento, tamaño de archivos, estrategia incremental, joins, distribución de workloads, autoscaling y costo. No asumiría que simplemente aumentar compute es suficiente.
