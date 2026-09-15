# Estructura del repositorio

```text
andes-commerce-data-platform/
├── README.md
├── docs/
├── generators/
├── data/sample/
├── src/
├── sql/
├── databricks/
├── dashboard/
├── app/
├── observability/
├── incidents/
├── runbooks/
├── tests/
└── .github/workflows/ci.yml
```

## Convención

`generators/` produce fuentes independientes.
`src/` contiene lógica reutilizable.
`sql/` contiene análisis y reconciliaciones.
`databricks/` contiene la implementación cloud.
`dashboard/` y `app/` contienen la capa de consumo.
`observability/`, `incidents/` y `runbooks/` contienen operación.
`tests/` protege contratos y transformaciones.
