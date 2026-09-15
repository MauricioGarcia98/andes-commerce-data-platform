# Data Quality Framework

## Objetivo

El pipeline no debe asumir que los datos de las fuentes son correctos. Antes de publicar Silver y Gold se ejecutan controles explícitos.

## Dimensiones iniciales

- Completeness: campos obligatorios presentes.
- Uniqueness: claves sin duplicados.
- Validity: valores pertenecen al dominio esperado.
- Referential integrity: claves existen en datasets relacionados.
- Consistency: tipos y reglas de negocio coherentes.

## Severidad

### CRITICAL
El fallo impide considerar confiable el dataset.

### WARNING
El dataset puede continuar con una alerta, según el caso de negocio.

## Resultado

Cada ejecución genera:

`data/dq_results/dq_results.csv`

`data/dq_results/dq_summary.json`

El score inicial es una métrica operativa del framework. No debe confundirse con una medida estadística absoluta de calidad empresarial.

## Capa de cuarentena

En Silver implementaremos una estrategia de cuarentena para registros inválidos. Los registros rechazados no desaparecen: quedan disponibles para diagnóstico y reproceso.

## Pregunta de entrevista

**¿Por qué no borrar registros inválidos?**

Porque eliminar evidencia dificulta trazabilidad, debugging y reproceso. Es preferible separar los registros rechazados de los aceptados y conservar el motivo del rechazo.
