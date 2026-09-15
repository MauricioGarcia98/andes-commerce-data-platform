# CI/CD

## Objetivo

Automatizar controles básicos antes de integrar cambios al repositorio.

## CI actual

GitHub Actions ejecuta `pytest` en cada push a `main` y en pull requests.

## Qué protege

- estructura de generadores;
- framework de Data Quality;
- transformaciones Silver;
- reconciliaciones Gold;
- reglas de negocio críticas.

## Qué NO hace todavía

No despliega automáticamente notebooks de Databricks a producción. Para este portfolio se deja documentado como evolución futura.

## Evolución

1. tests unitarios;
2. tests de integración;
3. validación de SQL/notebooks;
4. bundle/deploy controlado de Databricks;
5. promoción por ambientes.
