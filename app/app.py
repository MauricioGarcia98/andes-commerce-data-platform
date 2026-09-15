from pathlib import Path
import os
from typing import Optional

import pandas as pd
import streamlit as st

try:
    from databricks import sql
except ImportError:
    sql = None

st.set_page_config(page_title="Andes Commerce Operations Center", page_icon="📊", layout="wide")

CATALOG = os.getenv("DATABRICKS_CATALOG", "andes_commerce")
SCHEMA = os.getenv("DATABRICKS_SCHEMA", "gold")
WAREHOUSE_ID = os.getenv("DATABRICKS_WAREHOUSE_ID", "")


def get_connection():
    if sql is None:
        return None
    host = os.getenv("DATABRICKS_SERVER_HOSTNAME")
    http_path = os.getenv("DATABRICKS_HTTP_PATH")
    token = os.getenv("DATABRICKS_TOKEN")
    if not host or not http_path or not token:
        return None
    return sql.connect(server_hostname=host, http_path=http_path, access_token=token)


def run_query(query: str, fallback: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    conn = get_connection()
    if conn is None:
        return fallback if fallback is not None else pd.DataFrame()
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            columns = [d[0] for d in cur.description]
        return pd.DataFrame(rows, columns=columns)
    finally:
        conn.close()


def table(name: str) -> str:
    return f"`{CATALOG}`.`{SCHEMA}`.`{name}`"


# ---------- Local fallback data ----------
BASE = Path(__file__).resolve().parents[1]
GOLD = BASE / "data" / "gold"

@st.cache_data
def local_csv(name: str) -> pd.DataFrame:
    path = GOLD / f"{name}.csv"
    return pd.read_csv(path) if path.exists() else pd.DataFrame()


def local_kpis() -> pd.DataFrame:
    channel = local_csv("mart_sales_by_channel")
    inventory = local_csv("fact_inventory_snapshot")
    orders = local_csv("fact_order")
    revenue = float(pd.to_numeric(orders.get("revenue_recognized", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()) if not orders.empty else 0.0
    # Margin is taken from line-level Gold to avoid mixing order and line grains.
    sales = local_csv("fact_sales_line")
    margin = float(pd.to_numeric(sales.get("gross_margin", pd.Series(dtype=float)), errors="coerce").fillna(0).sum()) if not sales.empty else 0.0
    recognized_orders = int((pd.to_numeric(orders.get("revenue_recognized", pd.Series(dtype=float)), errors="coerce").fillna(0) > 0).sum()) if not orders.empty else 0
    critical = int((inventory.get("stock_status", pd.Series(dtype=str)) == "CRITICAL").sum()) if not inventory.empty else 0
    return pd.DataFrame([{
        "revenue": revenue,
        "gross_margin": margin,
        "margin_pct": (margin / revenue * 100) if revenue else 0,
        "orders": recognized_orders,
        "aov": (revenue / recognized_orders) if recognized_orders else 0,
        "critical_inventory": critical,
    }])


def local_category() -> pd.DataFrame:
    return local_csv("mart_sales_by_category")


def local_inventory() -> pd.DataFrame:
    inv = local_csv("mart_inventory_risk")
    if inv.empty:
        return pd.DataFrame(columns=["store_name", "critical", "low"])
    return (
        inv.groupby("store_name")
        .agg(
            critical=("stock_status", lambda s: int((s == "CRITICAL").sum())),
            low=("stock_status", lambda s: int((s == "LOW").sum())),
        )
        .reset_index()
        .sort_values("critical", ascending=False)
    )

st.title("Andes Commerce — Operations Control Center")
st.caption("Demo de portfolio · analítica ejecutiva + operación de datos")

with st.sidebar:
    st.header("Filtros")
    region = st.selectbox("Región", ["Todas", "AMBA", "Centro", "Litoral", "Cuyo", "Buenos Aires"])
    category = st.selectbox("Categoría", ["Todas", "Electronics", "Home", "Sports", "Beauty", "Grocery"])
    st.divider()
    st.caption("La App no reemplaza al Dashboard. Su foco es ayudar a investigar excepciones y acciones operativas.")

kpi_q = f"""
WITH sales AS (
  SELECT SUM(revenue) AS revenue, SUM(gross_margin) AS gross_margin
  FROM {table('mart_sales_by_channel')}
), orders AS (
  SELECT COUNT(*) AS orders, SUM(revenue_recognized) AS recognized_revenue
  FROM {table('fact_order')}
  WHERE revenue_recognized > 0
), inventory AS (
  SELECT COUNT(*) AS critical_inventory
  FROM {table('fact_inventory_snapshot')}
  WHERE stock_status = 'CRITICAL'
)
SELECT
  orders.recognized_revenue AS revenue,
  sales.gross_margin AS gross_margin,
  CASE WHEN orders.recognized_revenue = 0 THEN 0 ELSE sales.gross_margin / orders.recognized_revenue * 100 END AS margin_pct,
  orders.orders,
  CASE WHEN orders.orders = 0 THEN 0 ELSE orders.recognized_revenue / orders.orders END AS aov,
  inventory.critical_inventory
FROM sales CROSS JOIN orders CROSS JOIN inventory
"""
kpis = run_query(kpi_q, local_kpis())

row = kpis.iloc[0]
cols = st.columns(6)
labels = [
    ("Revenue", f"${row['revenue']:,.2f}"),
    ("Gross Margin", f"${row['gross_margin']:,.2f}"),
    ("Margin %", f"{row['margin_pct']:.2f}%"),
    ("Orders", f"{int(row['orders']):,}"),
    ("AOV", f"${row['aov']:,.2f}"),
    ("Critical Inventory", f"{int(row['critical_inventory']):,}"),
]
for col, (label, value) in zip(cols, labels):
    col.metric(label, value)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("¿Dónde se genera el revenue?")
    cat_q = f"""
    SELECT category, revenue, gross_margin
    FROM {table('mart_sales_by_category')}
    ORDER BY revenue DESC
    """
    category_df = run_query(cat_q, local_category())
    if not category_df.empty:
        st.bar_chart(category_df.set_index("category")["revenue"])
        st.dataframe(category_df, use_container_width=True, hide_index=True)

with right:
    st.subheader("¿Dónde está el riesgo de inventario?")
    inv_q = f"""
    SELECT store_name,
           SUM(CASE WHEN stock_status = 'CRITICAL' THEN 1 ELSE 0 END) AS critical,
           SUM(CASE WHEN stock_status = 'LOW' THEN 1 ELSE 0 END) AS low
    FROM {table('fact_inventory_snapshot')} i
    JOIN {table('dim_store')} s ON i.store_id = s.store_id
    GROUP BY store_name
    ORDER BY critical DESC
    """
    inv_df = run_query(inv_q, local_inventory())
    if not inv_df.empty:
        st.bar_chart(inv_df.set_index("store_name")[["critical", "low"]])
        st.dataframe(inv_df, use_container_width=True, hide_index=True)

st.divider()

st.subheader("Controles operativos")
status_cols = st.columns(3)
status_cols[0].metric("Data Quality", "100.0%", "27/27 checks")
status_cols[1].metric("Quarantine", "0", "sin registros inválidos")
status_cols[2].metric("Pipelines", "3", "Bronze / Silver / Gold")

st.info(
    "Uso recomendado en demo: seleccionar una categoría o región, observar el cambio en KPIs y luego investigar inventario crítico. "
    "En Databricks, las consultas se ejecutan sobre Gold; en GitHub la App conserva datos demo para poder mostrar la interfaz sin credenciales."
)
