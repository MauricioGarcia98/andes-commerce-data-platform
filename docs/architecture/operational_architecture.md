# Arquitectura operativa

```text
Source -> Bronze -> Silver -> DQ -> Gold -> DQ -> Dashboard/App
                 \-> logs / metrics / run_id / lineage

DQ FAIL -> STOP PROMOTION -> Incident -> Root Cause -> Recovery Run -> Reconciliation -> Gold
```
