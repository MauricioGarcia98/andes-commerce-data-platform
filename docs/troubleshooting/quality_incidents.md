# Laboratorio de incidentes

El proyecto incluye una fuente deliberadamente defectuosa en `data/quality_lab/`.

## Incidentes simulados

### INC-DQ-001 — Duplicate order_id
**Síntoma:** la clave de pedido aparece dos veces.

**Riesgo:** conteos de pedidos y métricas pueden inflarse.

**Respuesta esperada:** detectar antes de Gold, conservar evidencia y definir la regla de deduplicación con el owner del dato.

### INC-DQ-002 — customer_id inexistente
**Síntoma:** un pedido apunta a un cliente que no existe.

**Riesgo:** joins incompletos y pérdida de atribución.

**Respuesta esperada:** cuarentena del registro o resolución con la fuente propietaria, según el contrato.

### INC-DQ-003 — total_amount negativo
**Síntoma:** importe monetario inválido.

**Riesgo:** revenue incorrecto.

**Respuesta esperada:** bloquear la publicación del dato o clasificarlo como ajuste/refund explícito si el negocio lo define de esa forma.

### INC-DQ-004 — status desconocido
**Síntoma:** aparece un valor fuera del dominio acordado.

**Riesgo:** lógica CASE incompleta y métricas inconsistentes.

**Respuesta esperada:** revisar schema/data contract y determinar si hubo un cambio legítimo de dominio.

## Preguntas de entrevista

- ¿Cómo distinguirías un error de datos de un cambio legítimo de negocio?
- ¿Quién debería decidir la severidad de una regla?
- ¿Cuándo rechazarías un archivo completo y cuándo solamente filas?
- ¿Cómo reprocesarías solamente los registros corregidos?
- ¿Cómo evitarías que un retry duplique datos?
