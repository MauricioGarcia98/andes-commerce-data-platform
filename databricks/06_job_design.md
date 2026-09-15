# Diseño de Job — Andes Commerce

## DAG conceptual

```text
01_Bronze
   |
   v
02_Silver
   |
   +----> 04_DQ_Silver
   |
   v
03_Gold
   |
   +----> 05_DQ_Gold
   |
   v
06_Publish
```

## Reglas
- Gold no se ejecuta si Silver falla.
- Publish no se ejecuta si DQ crítico de Gold falla.
- Retry para errores transitorios de infraestructura.
- No usar retries ciegos para errores de calidad.

## Parámetros
`processing_date`, `source_path`, `run_id`

## Observabilidad por tarea
start, end, status, records, error, run_id.
