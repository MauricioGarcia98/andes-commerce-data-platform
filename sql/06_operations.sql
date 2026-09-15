-- Ejemplos para el futuro Operations Control Center en Databricks SQL
SELECT * FROM pipeline_runs ORDER BY start_time_utc DESC LIMIT 20;
SELECT * FROM pipeline_runs WHERE status='FAILED' ORDER BY start_time_utc DESC;
SELECT * FROM dq_results WHERE status='FAIL' ORDER BY run_id DESC;
SELECT run_id,pipeline_name,records_in,records_out,records_rejected,dq_score,duration_seconds
FROM pipeline_metrics ORDER BY run_id DESC;
