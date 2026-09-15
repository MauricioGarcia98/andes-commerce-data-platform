# Entrevista - Ingestion y Data Quality

## Preguntas y puntos que debes poder explicar

### 1. ¿Por qué existe Bronze?
Para separar aterrizaje de datos y transformación, preservar trazabilidad y permitir reprocesos.

### 2. ¿Bronze debe estar limpio?
No necesariamente. Debe ser controlado, trazable y cercano a la fuente. La limpieza fuerte pertenece a Silver.

### 3. ¿Qué diferencia hay entre una regla de calidad y un Data Contract?
El contrato define lo que la fuente promete respecto de esquema y comportamiento esperado. La regla ejecuta una comprobación concreta sobre los datos.

### 4. ¿Qué ocurre cuando falla una regla CRITICAL?
El dataset debe quedar impedido para promoción a la siguiente capa o pasar por un proceso explícito de cuarentena, según el diseño.

### 5. ¿Por qué guardar los registros rechazados?
Para trazabilidad, debugging, análisis de causa raíz y reproceso.

### 6. ¿Qué es idempotencia?
Ejecutar una misma operación una o varias veces produce el mismo estado final esperado, sin duplicar datos.

### 7. ¿Qué harías si la fuente agrega una columna?
Evaluaría schema evolution. No asumiría que todo cambio es seguro; validaría compatibilidad y ownership.

### 8. ¿Qué harías si cambia el tipo de una columna?
Detectaría el cambio, clasificaría su severidad y bloquearía o adaptaría la ingesta según el contrato.

### 9. ¿Por qué medir DQ?
Porque permite convertir “los datos parecen correctos” en una señal observable y comparable entre ejecuciones.

### 10. ¿El DQ score garantiza calidad empresarial?
No. Resume las reglas implementadas. La calidad real depende de que las reglas sean completas y correctas respecto del negocio.

### 11. ¿Por qué no hacer todas las validaciones en Python antes de Bronze?
Porque perderíamos una separación útil entre aterrizaje y validación. Algunas validaciones dependen de contexto y relaciones que se resuelven mejor en Silver.

### 12. ¿Cómo escalarías este framework?
Separaría configuración de reglas y lógica de ejecución, paralelizaría checks independientes cuando el runtime lo justifique y registraría resultados como una tabla operativa.
