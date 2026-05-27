"""
INFIVALLE - Dashboard Estratégico PETI 2025-2028
Developed as a professional executive decision-making tool.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os
import io

# ─────────────────────────── GLOBAL CHART PALETTE ───────────────────────────
# Must be defined BEFORE any function that references it
PLOTLY_TEMPLATE = dict(
    paper_bgcolor="rgba(21,33,51,0)",
    plot_bgcolor ="rgba(21,33,51,0)",
    font=dict(family="Inter", color="#94a3b8", size=11),
    margin=dict(l=12, r=12, t=36, b=12),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color="#cbd5e1", size=10),
        orientation="h",
        y=-0.18
    ),
)

COLORS = {
    "Fortaleza":    "#22c55e",
    "Debilidad":    "#ef4444",
    "Oportunidad":  "#0ea5e9",
    "Amenaza":      "#f59e0b",
}

# ─────────────────────────── PAGE CONFIG ───────────────────────────
st.set_page_config(
    page_title="INFIVALLE - Dashboard Estratégico PETI",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────── CUSTOM CSS ───────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root Variables ── */
:root {
    --bg-main:      #0d1b2a;
    --bg-card:      #152133;
    --bg-sidebar:   #0b1625;
    --accent-blue:  #1a6fc4;
    --accent-teal:  #0ea5e9;
    --accent-green: #22c55e;
    --accent-amber: #f59e0b;
    --accent-red:   #ef4444;
    --text-primary: #f1f5f9;
    --text-muted:   #94a3b8;
    --border:       rgba(255,255,255,0.07);
    --glow-blue:    0 0 20px rgba(26,111,196,0.35);
    --glow-green:   0 0 16px rgba(34,197,94,0.3);
}

/* ── Base Reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
}

.main .block-container {
    padding: 1.2rem 2rem 2rem 2rem !important;
    max-width: 100% !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stCheckbox label,
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3, [data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: var(--text-primary) !important;
}

/* ── Header Banner ── */
.header-banner {
    background: linear-gradient(135deg, #0b2545 0%, #163c6b 50%, #1a5296 100%);
    border: 1px solid rgba(26,111,196,0.4);
    border-radius: 16px;
    padding: 1.4rem 2rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.4rem;
    box-shadow: var(--glow-blue), 0 4px 24px rgba(0,0,0,0.5);
}
.header-title {
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #fff;
    line-height: 1.2;
}
.header-subtitle {
    font-size: 0.85rem;
    color: #90c0f0;
    font-weight: 400;
    margin-top: 4px;
}
.logo-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 10px;
    padding: 8px 14px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.3px;
    color: #fff;
    backdrop-filter: blur(8px);
}
.logo-icon {
    width: 30px;
    height: 30px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    font-weight: 800;
}
.logo-infivalle { background: linear-gradient(135deg, #1a6fc4, #0ea5e9); }
.logo-corpu     { background: linear-gradient(135deg, #16a34a, #22c55e); }
.logos-container { display: flex; gap: 10px; }
.badge-separator {
    width: 1px;
    height: 36px;
    background: rgba(255,255,255,0.15);
}

/* ── Metric Cards ── */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem 1.4rem 1rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--glow-blue);
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 14px 14px 0 0;
}
.metric-card.blue::before   { background: linear-gradient(90deg, #1a6fc4, #0ea5e9); }
.metric-card.green::before  { background: linear-gradient(90deg, #16a34a, #22c55e); }
.metric-card.amber::before  { background: linear-gradient(90deg, #d97706, #f59e0b); }
.metric-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.9px;
    color: var(--text-muted);
    margin-bottom: 8px;
}
.metric-value {
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 8px;
}
.metric-value.blue  { color: #60a5fa; }
.metric-value.green { color: #4ade80; }
.metric-value.amber { color: #fbbf24; }
.metric-delta {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.78rem;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 20px;
}
.delta-pos { background: rgba(34,197,94,0.15); color: #4ade80; }
.delta-neg { background: rgba(239,68,68,0.15);  color: #f87171; }
.metric-sub {
    font-size: 0.7rem;
    color: var(--text-muted);
    margin-top: 6px;
}

/* ── Section Headers ── */
.section-header {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.4px;
    color: var(--accent-teal);
    margin: 1.6rem 0 0.6rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border), transparent);
}

/* ── Chart Containers ── */
.chart-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.1rem 1.2rem 0.5rem;
    height: 100%;
}
.chart-title {
    font-size: 0.82rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 2px;
}
.chart-subtitle {
    font-size: 0.68rem;
    color: var(--text-muted);
    margin-bottom: 10px;
}

/* ── Sidebar Logo ── */
.sb-logo {
    text-align: center;
    padding: 18px 12px 14px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 16px;
}
.sb-logo-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: #fff;
    letter-spacing: -0.3px;
}
.sb-logo-sub {
    font-size: 0.68rem;
    color: #90c0f0;
    margin-top: 3px;
}
.sb-badge {
    display: inline-block;
    background: linear-gradient(135deg, #1a6fc4, #0ea5e9);
    color: #fff;
    font-size: 0.62rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    margin-top: 6px;
    letter-spacing: 0.5px;
}

/* ── Dividers ── */
hr {
    border: none;
    border-top: 1px solid var(--border) !important;
    margin: 1rem 0 !important;
}

/* ── Streamlit overrides ── */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}
.stCheckbox span { color: var(--text-primary) !important; }
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
.stDataFrame { border: 1px solid var(--border) !important; }
[data-testid="stExpander"] { border: 1px solid var(--border) !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────── DATA LOADING ───────────────────────────
import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
LOCAL_DB_PATH = PROJECT_DIR / "database" / "peti_infivalle.db"
APPDATA_DB_PATH = Path.home() / ".gemini" / "antigravity" / "peti_infivalle.db"

def get_db_path():
    if LOCAL_DB_PATH.exists():
        return LOCAL_DB_PATH
    if APPDATA_DB_PATH.exists():
        return APPDATA_DB_PATH
    return LOCAL_DB_PATH

def load_table(table_name):
    db_path = get_db_path()
    try:
        conn = sqlite3.connect(str(db_path))
        df = pd.read_sql_query(f'SELECT * FROM "{table_name}"', conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error cargando tabla '{table_name}' desde {db_path}: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=600)
def load_data():
    return {
        "kpis": load_table("kpis"),
        "heatmap": load_table("heatmap"),
        "objectives": load_table("objectives"),
        "dofa": load_table("dofa"),
        "mintic_questions": load_table("mintic_questions"),
        "mintic_avg": load_table("mintic_avg"),
        "portafolio_olas": load_table("portafolio_olas"),
        "trazabilidad": load_table("trazabilidad"),
        "projects": load_table("projects"),
        "macro_kpis": load_table("macro_kpis"),
        "bsc_perspectives": load_table("bsc_perspectives"),
        "mintic_maturity": load_table("mintic_maturity"),
        "incidentes_semanales": load_table("incidentes_semanales"),
        "log_ejecucion_flujo": load_table("log_ejecucion_flujo"),
    }

data = load_data()

# ─────────────────────────── SIDEBAR ───────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <div style="font-size:2rem;">🏛️</div>
        <div class="sb-logo-title">INFIVALLE</div>
        <div class="sb-logo-sub">Oficina de Tecnologías de la Información</div>
        <span class="sb-badge">PETI 2025 – 2028</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**🔍 Perspectiva del Dashboard**")
    view_options = ["🏛️ Cuadro de Mando Estratégico", "⚙️ Gobernanza y Automatización (ISO 38500)"]
    selected_view = st.selectbox("Seleccione Perspectiva", view_options, index=0, label_visibility="collapsed")
    st.markdown("---")

    # Conditionally render filters based on selected view
    if selected_view == "🏛️ Cuadro de Mando Estratégico":
        st.markdown("**📅 Período de Análisis**")
        year_options = ["Todos", "2025", "2026", "2027", "2028"]
        selected_year = st.selectbox("Año de Ejecución", year_options, index=0, label_visibility="collapsed")

        st.markdown("---")
        st.markdown("**🎯 Pilares Estratégicos**")
        pilar_options = [
            "OBJ-01 Gobierno TI",
            "OBJ-02 Seguridad Digital",
            "OBJ-03 Servicios Digitales",
            "OBJ-04 Infraestructura y Nube",
            "OBJ-05 Datos e Inteligencia",
            "OBJ-06 Capacidades y Cambio",
        ]
        selected_pilares = st.multiselect(
            "Filtrar Pilares DOFA/BSC",
            pilar_options,
            default=pilar_options,
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown("**📋 Estado del Proyecto**")
        cb_planificado   = st.checkbox("🔵 Planificado",   value=True)
        cb_en_ejecucion  = st.checkbox("🟡 En Ejecución",  value=True)
        cb_finalizado    = st.checkbox("🟢 Finalizado",    value=True)

        st.markdown("---")
        st.markdown("**⚔️ Categoría Fuerzas de Porter**")
        cb_amenazas      = st.checkbox("🔴 Amenazas",      value=True)
        cb_fortalezas    = st.checkbox("🟢 Fortalezas",    value=True)
        cb_oportunidades = st.checkbox("🔵 Oportunidades", value=True)

        # Initialize operational values with default fallbacks
        selected_criticidad = ["Alta", "Media", "Baja"]
        selected_estado_inc = ["Resuelto", "En Proceso", "Abierto"]
    else:
        st.markdown("**⚡ Filtros Operativos (Incidentes)**")
        
        st.markdown("**🔥 Criticidad**")
        criticidad_options = ["Alta", "Media", "Baja"]
        selected_criticidad = st.multiselect(
            "Filtro Criticidad",
            criticidad_options,
            default=criticidad_options,
            label_visibility="collapsed",
        )

        st.markdown("---")
        st.markdown("**🚦 Estado del Incidente**")
        estado_inc_options = ["Resuelto", "En Proceso", "Abierto"]
        selected_estado_inc = st.multiselect(
            "Filtro Estado Incidente",
            estado_inc_options,
            default=estado_inc_options,
            label_visibility="collapsed",
        )

        # Initialize strategic values with default fallbacks
        selected_year = "Todos"
        selected_pilares = [
            "OBJ-01 Gobierno TI",
            "OBJ-02 Seguridad Digital",
            "OBJ-03 Servicios Digitales",
            "OBJ-04 Infraestructura y Nube",
            "OBJ-05 Datos e Inteligencia",
            "OBJ-06 Capacidades y Cambio",
        ]
        cb_planificado = True
        cb_en_ejecucion = True
        cb_finalizado = True
        cb_amenazas = True
        cb_fortalezas = True
        cb_oportunidades = True

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.62rem;color:#475569;text-align:center;line-height:1.5">
        <strong style="color:#64748b">Corporación Universitaria</strong><br>
        Antonio José de Sucre<br>
        Gobierno y Servicios de TI<br>
        <span style="color:#1a6fc4">■</span> 2025-2028
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────── HEADER BANNER ───────────────────────────
st.markdown("""
<div class="header-banner">
  <div>
    <div class="header-title"> INFIVALLE — Dashboard Estratégico PETI</div>
    <div class="header-subtitle">
        Plan Estratégico de Tecnologías de la Información · ISO 38500:2024 &nbsp;·&nbsp; Horizonte 2025–2028 &nbsp;·&nbsp; Oficina de Tecnologías de la Información
    </div>
  </div>
  <div class="logos-container">
    <div class="logo-badge">
      <div class="logo-icon logo-infivalle">IF</div>
      <div>
        <div style="font-size:0.72rem;font-weight:800">INFIVALLE</div>
        <div style="font-size:0.6rem;color:#90c0f0;font-weight:400">Instituto Financiero del Valle</div>
      </div>
    </div>
    <div class="badge-separator"></div>
    <div class="logo-badge">
      <div class="logo-icon logo-corpu">CU</div>
      <div>
        <div style="font-size:0.72rem;font-weight:800">CORPU AJS</div>
        <div style="font-size:0.6rem;color:#86efac;font-weight:400">Antonio José de Sucre</div>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────── OPERATIONAL PERSPECTIVE ───────────────────────────
def render_operational_view(data, selected_criticidad, selected_estado_inc):
    st.markdown('<div class="section-header">Gobernanza Operativa — Monitoreo de Automatización e Incidentes (ISO 38500)</div>', unsafe_allow_html=True)
    
    # Filter incidents based on sidebar
    inc_df = data["incidentes_semanales"].copy()
    if selected_criticidad:
        inc_df = inc_df[inc_df["Criticidad"].isin(selected_criticidad)]
    if selected_estado_inc:
        inc_df = inc_df[inc_df["Estado"].isin(selected_estado_inc)]
        
    total_incidents = len(inc_df)
    avg_res_time = round(inc_df["Tiempo_Resolucion_h"].mean(), 1) if total_incidents else 0.0
    high_incidents = int(inc_df["Criticidad"].eq("Alta").sum())
    
    # Load logs
    logs_df = data["log_ejecucion_flujo"].copy()
    total_executions = len(logs_df)
    successful_pct = round(logs_df["Estado"].eq("Éxito").mean() * 100, 1) if total_executions else 100.0
    active_findings = int(logs_df.iloc[-1]["Hallazgos_Detectados"]) if not logs_df.empty else 0
    
    op_col1, op_col2, op_col3, op_col4, op_col5 = st.columns(5)
    
    op_col1.markdown(f"""
    <div class="metric-card blue">
        <div class="metric-label">Incidentes Semanales</div>
        <div class="metric-value blue">{total_incidents}</div>
        <span class="metric-delta delta-pos">Activos</span>
        <div class="metric-sub">Periodo actual: Semana 21</div>
    </div>
    """, unsafe_allow_html=True)
    
    op_col2.markdown(f"""
    <div class="metric-card green">
        <div class="metric-label">Tiempo Res. Promedio</div>
        <div class="metric-value green">{avg_res_time}h</div>
        <span class="metric-delta delta-pos">SLA: &lt;8h</span>
        <div class="metric-sub">Cumplimiento metas SLA</div>
    </div>
    """, unsafe_allow_html=True)
    
    op_col3.markdown(f"""
    <div class="metric-card amber">
        <div class="metric-label">Incidentes Criticos</div>
        <div class="metric-value amber">{high_incidents}</div>
        <span class="metric-delta delta-neg">Requiere OTI</span>
        <div class="metric-sub">Fallo severo detectado</div>
    </div>
    """, unsafe_allow_html=True)
    
    op_col4.markdown(f"""
    <div class="metric-card blue">
        <div class="metric-label">Tasa de Exito Flujo</div>
        <div class="metric-value blue">{successful_pct}%</div>
        <span class="metric-delta delta-pos">Alta Confiabilidad</span>
        <div class="metric-sub">Monitoreo automatico Lunes 07:00</div>
    </div>
    """, unsafe_allow_html=True)
    
    op_col5.markdown(f"""
    <div class="metric-card green">
        <div class="metric-label">Ultimos Hallazgos</div>
        <div class="metric-value green">{active_findings}</div>
        <span class="metric-delta delta-pos">Auditoria ISO</span>
        <div class="metric-sub">Registrado en log de control</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Incidentes chart (full width) ──
    st.markdown('<div class="section-header">Analitica de Incidentes</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Incidentes por Area Impactada y Criticidad</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-subtitle">Analisis operativo para justificar priorizacion de soporte tecnico</div>', unsafe_allow_html=True)
    if not inc_df.empty:
        fig_inc = px.bar(
            inc_df,
            x="Area_Impactada",
            color="Criticidad",
            color_discrete_map={"Alta": "#ef4444", "Media": "#f59e0b", "Baja": "#0ea5e9"},
            barmode="group",
            height=300
        )
        fig_inc.update_layout(**PLOTLY_TEMPLATE)
        st.plotly_chart(fig_inc, use_container_width=True, key="incidents_chart")
    else:
        st.info("No hay incidentes para mostrar con los filtros seleccionados.")
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Excel Downloads (4 datasets del flujo) ──
    st.markdown('<div class="section-header">Descarga de Insumos del Flujo de Automatizacion</div>', unsafe_allow_html=True)

    def _to_excel(df):
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        return buf.getvalue()

    col_d1, col_d2, col_d3, col_d4 = st.columns(4, gap="medium")

    with col_d1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">KPI Semanales</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-subtitle">Indicadores de metas y formulas PETI</div>', unsafe_allow_html=True)
        kpi_df = data["kpis"].copy()
        st.dataframe(kpi_df.head(4), hide_index=True, height=140)
        st.download_button(
            label="Descargar KPI_Semanales.xlsx",
            data=_to_excel(kpi_df),
            file_name="KPI_Semanales.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key="dl_kpi"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_d2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Portafolio PETI</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-subtitle">Proyectos activos con presupuesto y estado</div>', unsafe_allow_html=True)
        proj_df = data["projects"].copy()
        st.dataframe(proj_df.head(4), hide_index=True, height=140)
        st.download_button(
            label="Descargar Portafolio_PETI.xlsx",
            data=_to_excel(proj_df),
            file_name="Portafolio_PETI.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key="dl_projects"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_d3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Incidentes Semanal</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-subtitle">Registro de soporte tecnico con criticidad</div>', unsafe_allow_html=True)
        st.dataframe(inc_df.head(4), hide_index=True, height=140)
        st.download_button(
            label="Descargar Incidentes_Semanal.xlsx",
            data=_to_excel(inc_df),
            file_name="Incidentes_Semanal.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key="dl_incidentes"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with col_d4:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">Log de Ejecucion</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-subtitle">Trazabilidad del flujo de automatizacion</div>', unsafe_allow_html=True)
        log_df = data["log_ejecucion_flujo"].copy()
        st.dataframe(log_df.head(4), hide_index=True, height=140)
        st.download_button(
            label="Descargar Log_Ejecucion.xlsx",
            data=_to_excel(log_df),
            file_name="Log_Ejecucion.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key="dl_log"
        )
        st.markdown('</div>', unsafe_allow_html=True)

# Check view selection and divert if operational view is requested
if selected_view == "⚙️ Gobernanza y Automatización (ISO 38500)":
    render_operational_view(data, selected_criticidad, selected_estado_inc)
    st.stop()

# ─────────────────────────── KPI METRICS ROW ───────────────────────────
st.markdown('<div class="section-header"> Indicadores Macro — Cuadro de Mando Integral</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

project_filter = data["projects"].copy()
if selected_year != "Todos":
    project_filter = project_filter[project_filter["Vigencia"].str.contains(selected_year, na=False)]

pilar_codes = [p.split()[0] for p in selected_pilares]

if not project_filter.empty:
    if pilar_codes:
        oe_col = "OE Inst."
        project_filter = project_filter[project_filter[oe_col].apply(
            lambda x: any(pc.replace("OBJ-0", "OE-0") in str(x) for pc in pilar_codes)
        )]

    status_map = []
    if cb_planificado:   status_map.append("Planificado")
    if cb_en_ejecucion:  status_map.append("En Ejecución")
    if cb_finalizado:    status_map.append("Finalizado")
    if status_map:
        project_filter = project_filter[project_filter["Estado"].isin(status_map)]

project_count = len(project_filter)
avg_progress = int(project_filter["Progreso"].mean() * 100) if project_count else 0
finalized_pct = int(project_filter["Estado"].eq("Finalizado").mean() * 100) if project_count else 0
capex_total = int(project_filter["CAPEX (M$)"].sum())

gov_project_count = int(project_filter["Dominio MGGTI"].eq("Gobierno").sum())
response_count = int(data["kpis"]["Objetivo PETI"].str.contains("OBJ-01", na=False).sum())
traceability_pct = int(data["trazabilidad"]["KPI"].notna().mean() * 100) if not data["trazabilidad"].empty else 0
iso_ref_count = int(data["trazabilidad"]["Marco Normativo"].astype(str).str.contains("ISO|MGGTI|MIPG|SGSI", case=False, na=False).sum())

kpi_data = [
    ("col1", "blue",  "Progreso Portafolio",       f"{avg_progress}%",  f"{finalized_pct}% finalizados",   "Base: portafolio activo",   True),
    ("col2", "green", "CAPEX Total PETI",          f"{capex_total:,}M",  "Presupuesto consolidado",     "2025–2028",               True),
    ("col3", "amber", "KPIs Gobierno TI",          str(response_count),  f"{int(response_count / len(data['kpis']) * 100) if len(data['kpis']) else 0}% del portafolio", "Objetivos con KPI", True),
    ("col4", "blue",  "Trazabilidad KPI",           f"{traceability_pct}%", "Cobertura de KPI",          "Objetivos con seguimiento", True),
    ("col5", "green", "Referencias ISO/MGGTI",     str(iso_ref_count),   "Normativa detectada",      "SGSI, MIPG, ISO 27001",    True),
]

for (cname, color, label, value, delta, sub, pos), col in zip(kpi_data, [col1, col2, col3, col4, col5]):
    delta_cls = "delta-pos" if pos else "delta-neg"
    arrow     = "▲" if pos else "▼"
    col.markdown(f"""
    <div class="metric-card {color}">
        <div class="metric-label">{label}</div>
        <div class="metric-value {color}">{value}</div>
        <span class="metric-delta {delta_cls}">{arrow} {delta}</span>
        <div class="metric-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-header"> Gobierno TI — ISO 38500 2024</div>', unsafe_allow_html=True)
col_iso1, col_iso2 = st.columns([1.1, 0.9], gap="medium")

iso_scores = {
    "Estrategia": min(100, 60 + len(selected_pilares) * 6),
    "Riesgo y Cumplimiento": min(100, 50 + iso_ref_count * 12),
    "Recursos y CAPEX": min(100, 40 + int(capex_total / 50)),
    "Desempeño": avg_progress,
    "Responsabilidad": min(100, 40 + gov_project_count * 20),
    "Transparencia": traceability_pct,
}

with col_iso1:
    fig_iso = go.Figure()
    fig_iso.add_trace(go.Scatterpolar(
        r=list(iso_scores.values()) + [list(iso_scores.values())[0]],
        theta=list(iso_scores.keys()) + [list(iso_scores.keys())[0]],
        fill="toself",
        fillcolor="rgba(34,197,94,0.18)",
        line=dict(color="#22c55e", width=2.5),
        marker=dict(size=6, color="#22c55e"),
        name="Evaluación ISO 38500",
    ))
    fig_iso.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.1)", tickfont=dict(size=8, color="#64748b")),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.1)", tickfont=dict(size=9, color="#94a3b8")),
        ),
        paper_bgcolor="rgba(21,33,51,0)",
        font=dict(family="Inter", color="#94a3b8", size=10),
        margin=dict(l=20, r=20, t=20, b=20),
        height=360,
        showlegend=False,
    )
    st.plotly_chart(fig_iso, width="stretch", key="iso_chart")

with col_iso2:
    st.markdown("""
    <div style='padding: 0 0.5rem;'>
        <div style='font-size:0.9rem;font-weight:700;color:#fff;margin-bottom:0.85rem;'>Resumen de Gobernanza TI</div>
        <div style='color:#94a3b8;font-size:0.82rem;line-height:1.5;'>
            • Proyectos con dominio Gobierno TI: <strong>{gov_project_count}</strong><br>
            • KPIs definidos en OBJ-01: <strong>{response_count}</strong><br>
            • Trazabilidad de KPI: <strong>{traceability_pct}%</strong><br>
            • Referencias ISO / MIPG / SGSI: <strong>{iso_ref_count}</strong><br>
            • CAPEX total alineado: <strong>{capex_total:,}M</strong><br>
        </div>
    </div>
    """.format(gov_project_count=gov_project_count, response_count=response_count, traceability_pct=traceability_pct, iso_ref_count=iso_ref_count, capex_total=capex_total), unsafe_allow_html=True)

    kpi_table = data["kpis"].copy()
    if selected_pilares:
        filter_codes = "|".join(pilar_codes)
        kpi_table = kpi_table[kpi_table["Objetivo PETI"].str.contains(filter_codes, na=False)]
    st.markdown("<div style='margin-top:0.7rem;font-size:0.78rem;color:#94a3b8;'>KPIs estratégicos mostrados según filtro de pilares</div>", unsafe_allow_html=True)
    st.dataframe(kpi_table[["Código KPI", "Nombre KPI", "Objetivo PETI", "Meta 2028", "Responsable"]].reset_index(drop=True), height=220)

# PLOTLY_TEMPLATE and COLORS are defined at the top of the file (after imports)

# ─────────────────────────── ROW 1: DOFA + PORTER ───────────────────────────
st.markdown('<div class="section-header"> Análisis Estratégico — Matriz DOFA & Fuerzas de Porter</div>', unsafe_allow_html=True)

col_dofa, col_porter = st.columns([1.1, 0.9], gap="medium")

# ── DOFA Stacked Bar ──
with col_dofa:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"> Análisis Matriz DOFA por Pilar TI</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-subtitle">Debilidades · Fortalezas · Oportunidades · Amenazas por Objetivo Estratégico</div>', unsafe_allow_html=True)

    dofa_df = data["dofa"].copy()

    # Apply Porter filter
    allowed_cuadrantes = []
    if cb_fortalezas:    allowed_cuadrantes.append("Fortaleza")
    if cb_amenazas:      allowed_cuadrantes.append("Amenaza")
    if cb_oportunidades: allowed_cuadrantes.append("Oportunidad")
    allowed_cuadrantes.append("Debilidad")  # always included

    dofa_df = dofa_df[dofa_df["Cuadrante"].isin(allowed_cuadrantes)]

    # Build objective-based pivot
    obj_col = "Objetivo PETI relacionado"
    cuad_col = "Cuadrante"

    # Explode objectives (some rows have 2+ objectives)
    dofa_exp = dofa_df.copy()
    dofa_exp[obj_col] = dofa_exp[obj_col].str.split(r",\s*")
    dofa_exp = dofa_exp.explode(obj_col)
    dofa_exp[obj_col] = dofa_exp[obj_col].str.strip()

    # Filter to selected pilares
    pilar_codes = [p.split()[0] for p in selected_pilares]
    if pilar_codes:
        dofa_exp = dofa_exp[dofa_exp[obj_col].isin(pilar_codes)]

    pivot = dofa_exp.groupby([obj_col, cuad_col]).size().reset_index(name="count")

    if not pivot.empty:
        fig_dofa = px.bar(
            pivot,
            x="count",
            y=obj_col,
            color=cuad_col,
            color_discrete_map=COLORS,
            orientation="h",
            barmode="stack",
            labels={"count": "Factores", obj_col: "Objetivo"},
            height=340,
        )
        fig_dofa.update_layout(**PLOTLY_TEMPLATE)
        fig_dofa.update_traces(marker_line_width=0)
        fig_dofa.update_yaxes(tickfont=dict(size=10))
        st.plotly_chart(fig_dofa, width="stretch", key="dofa_chart")
    else:
        st.info("Selecciona al menos un pilar y cuadrante para visualizar la DOFA.")
    st.markdown('</div>', unsafe_allow_html=True)

# ── Porter's 5 Forces Sunburst ──
with col_porter:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"> Impacto Modelo 5 Fuerzas de Porter</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-subtitle">Niveles de riesgo institucional por fuerza competitiva</div>', unsafe_allow_html=True)

    porter_data = {
        "Fuerza": [
            "Rivalidad Competidores",    "Rivalidad Competidores",
            "Nuevos Entrantes",          "Nuevos Entrantes",
            "Productos Sustitutos",      "Productos Sustitutos",
            "Poder Clientes",            "Poder Clientes",
            "Poder Proveedores",         "Poder Proveedores",
        ],
        "Nivel": [
            "Alto", "Medio",
            "Alto", "Medio",
            "Alto", "Bajo",
            "Medio", "Alto",
            "Medio", "Alto",
        ],
        "Valor": [65, 35, 70, 30, 55, 45, 40, 60, 45, 55],
        "Color": [
            "#ef4444", "#f59e0b",
            "#ef4444", "#22c55e",
            "#f59e0b", "#22c55e",
            "#0ea5e9", "#ef4444",
            "#0ea5e9", "#f59e0b",
        ]
    }
    porter_df = pd.DataFrame(porter_data)

    # Apply Porter filter to what forces to show
    force_filter = []
    if cb_amenazas:      force_filter += ["Rivalidad Competidores", "Nuevos Entrantes"]
    if cb_oportunidades: force_filter += ["Poder Clientes"]
    if cb_fortalezas:    force_filter += ["Poder Proveedores", "Productos Sustitutos"]
    if not force_filter:
        force_filter = porter_df["Fuerza"].unique().tolist()

    porter_filtered = porter_df[porter_df["Fuerza"].isin(force_filter)]

    if not porter_filtered.empty:
        fig_sun = px.sunburst(
            porter_filtered,
            path=["Fuerza", "Nivel"],
            values="Valor",
            color="Nivel",
            color_discrete_map={"Alto": "#ef4444", "Medio": "#f59e0b", "Bajo": "#22c55e"},
            height=340,
        )
        fig_sun.update_layout(
            paper_bgcolor="rgba(21,33,51,0)",
            font=dict(family="Inter", color="#e2e8f0", size=10),
            margin=dict(l=0, r=0, t=10, b=0),
        )
        fig_sun.update_traces(
            textfont=dict(size=10, color="#fff"),
            insidetextfont=dict(color="#fff"),
        )
        st.plotly_chart(fig_sun, width="stretch", key="porter_chart")
    else:
        st.info("Selecciona al menos una categoría de Porter en la barra lateral.")
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────── ROW 2: GANTT + HEATMAP ───────────────────────────
st.markdown('<div class="section-header"> Hoja de Ruta Estratégica & Asignación de Recursos TI</div>', unsafe_allow_html=True)

col_gantt, col_heatmap = st.columns([1.15, 0.85], gap="medium")

# ── Gantt Chart ──
with col_gantt:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"> Estrategia TI Road Map — Cronograma por Olas 2025-2028</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-subtitle">Distribución de iniciativas por dominio y vigencia. Hitos marcados con diamante.</div>', unsafe_allow_html=True)

    projects_df = data["projects"].copy()

    # Filter by year
    if selected_year != "Todos":
        projects_df = projects_df[projects_df["Vigencia"].str.contains(selected_year, na=False)]

    # Filter by pilar
    pilar_codes = [p.split()[0] for p in selected_pilares]
    if pilar_codes:
        oe_col = "OE Inst."
        mask = projects_df[oe_col].apply(
            lambda x: any(pc.replace("OBJ-0", "OE-0") in str(x) for pc in pilar_codes)
        )
        projects_df = projects_df[mask] if mask.any() else projects_df

    # Filter by status
    status_map = []
    if cb_planificado:   status_map.append("Planificado")
    if cb_en_ejecucion:  status_map.append("En Ejecución")
    if cb_finalizado:    status_map.append("Finalizado")
    if status_map:
        projects_df = projects_df[projects_df["Estado"].isin(status_map)]

    # Build Gantt data
    color_domain_map = {
        "Gobierno":     "#1a6fc4",
        "Estrategia":   "#0ea5e9",
        "Seguridad":    "#ef4444",
        "Información":  "#a855f7",
        "Sistemas":     "#22c55e",
        "Servicios TI": "#f59e0b",
    }

    # Map year range from Vigencia
    def parse_year_range(v):
        v = str(v).strip()
        parts = [p.strip() for p in v.split("-")]
        try:
            start = int(parts[0])
        except:
            start = 2025
        try:
            raw_end = int(parts[-1]) if len(parts) > 1 else start
            # Expand 2-digit suffix years: "2026-27" → end=2027
            if raw_end < 100:
                century = (start // 100) * 100
                raw_end = century + raw_end
            end = raw_end
        except:
            end = start
        return start, end


    gantt_rows = []
    for _, row in projects_df.iterrows():
        start, end = parse_year_range(row.get("Vigencia", "2025"))
        dom = row.get("Dominio MGGTI", "Gobierno")
        gantt_rows.append({
            "Task": f"{row.get('Cód.', '')} — {row.get('Proyecto', '')}",
            "Start": f"{start}-01-01",
            "Finish": f"{end}-12-31",
            "Dominio": dom,
            "Color": color_domain_map.get(dom, "#64748b"),
            "Status": row.get("Estado", "Planificado"),
            "CAPEX": row.get("CAPEX (M$)", 0),
        })

    if gantt_rows:
        gantt_df = pd.DataFrame(gantt_rows)
        gantt_df["Start"]  = pd.to_datetime(gantt_df["Start"])
        gantt_df["Finish"] = pd.to_datetime(gantt_df["Finish"])

        fig_gantt = px.timeline(
            gantt_df,
            x_start="Start",
            x_end="Finish",
            y="Task",
            color="Dominio",
            color_discrete_map=color_domain_map,
            hover_data={"Status": True, "CAPEX": True},
            height=390,
        )
        # Milestones (single-year projects)
        milestones = gantt_df[gantt_df["Start"] == gantt_df["Finish"]].copy()
        if not milestones.empty:
            fig_gantt.add_trace(go.Scatter(
                x=milestones["Start"],
                y=milestones["Task"],
                mode="markers",
                marker=dict(symbol="diamond", size=10, color="#fbbf24"),
                name="Hito",
                showlegend=True,
            ))

        fig_gantt.update_layout(**PLOTLY_TEMPLATE)
        fig_gantt.update_layout(
            xaxis=dict(
                tickformat="%Y",
                gridcolor="rgba(255,255,255,0.05)",
                dtick="M12",
            ),
            yaxis=dict(autorange="reversed", tickfont=dict(size=8)),
            legend=dict(orientation="h", y=-0.14, font=dict(size=9)),
        )
        fig_gantt.update_traces(opacity=0.88, marker_line_width=0)
        st.plotly_chart(fig_gantt, width="stretch", key="gantt_chart")
    else:
        st.info("No hay proyectos que coincidan con los filtros activos.")
    st.markdown('</div>', unsafe_allow_html=True)

# ── Heatmap ──
with col_heatmap:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"> Mapa de Calor — Justificación de Recursos TI</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-subtitle">Priorización Transformación Digital: Área Funcional × Proceso TI</div>', unsafe_allow_html=True)

    heatmap_df = data["heatmap"].copy()
    heatmap_df = heatmap_df.rename(columns={"Área Funcional": "Area"})

    numeric_cols = [c for c in heatmap_df.columns if c not in ["Area", "Promedio"]]
    z_vals = heatmap_df[numeric_cols].apply(pd.to_numeric, errors="coerce").fillna(0).values
    y_labels = heatmap_df["Area"].tolist()
    x_labels = numeric_cols

    fig_heat = go.Figure(go.Heatmap(
        z=z_vals,
        x=x_labels,
        y=y_labels,
        colorscale=[
            [0.0, "#163c6b"],
            [0.2, "#1e5294"],
            [0.4, "#22c55e"],
            [0.6, "#f59e0b"],
            [0.8, "#ef4444"],
            [1.0, "#7c0000"],
        ],
        showscale=True,
        colorbar=dict(
            title=dict(text="Score", font=dict(size=9, color="#94a3b8")),
            tickfont=dict(size=9, color="#94a3b8"),
            thickness=12,
            len=0.9,
        ),
        hovertemplate="<b>%{y}</b><br>Proceso: %{x}<br>Score: %{z}<extra></extra>",
    ))

    fig_heat.update_layout(
        paper_bgcolor="rgba(21,33,51,0)",
        plot_bgcolor ="rgba(21,33,51,0)",
        font=dict(family="Inter", color="#94a3b8", size=9),
        margin=dict(l=10, r=40, t=10, b=30),
        height=390,
        xaxis=dict(tickangle=-35, tickfont=dict(size=8)),
        yaxis=dict(tickfont=dict(size=8), autorange="reversed"),
    )
    st.plotly_chart(fig_heat, width="stretch", key="heatmap_chart")
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────── ROW 3: BSC RADAR + MinTIC Radar ───────────────────────────
st.markdown('<div class="section-header"> Cuadro de Mando Integral (BSC) & Madurez Digital MinTIC</div>', unsafe_allow_html=True)

col_radar1, col_radar2, col_mintic = st.columns([1, 1, 1], gap="medium")

# ── BSC Spider ──
with col_radar1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"> Radar BSC — Perspectivas Estratégicas</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-subtitle">Alineación de las 4 perspectivas del Balanced Scorecard</div>', unsafe_allow_html=True)

    if not data["bsc_perspectives"].empty:
        bsc_df = data["bsc_perspectives"].copy()
        bsc_categories = bsc_df["Perspective"].tolist()
        bsc_actual = bsc_df["Actual"].tolist()
        bsc_meta = bsc_df["Meta"].tolist()
    else:
        bsc_categories = ["Contribución\nCorporativa", "Orientación\nal Usuario", "Excelencia\nOperativa", "Capacidades\nFuturas"]
        bsc_actual = [72, 78, 85, 63]
        bsc_meta   = [90, 90, 99, 90]

    fig_bsc = go.Figure()
    fig_bsc.add_trace(go.Scatterpolar(
        r=bsc_meta + [bsc_meta[0]],
        theta=bsc_categories + [bsc_categories[0]],
        fill="toself",
        fillcolor="rgba(26,111,196,0.1)",
        line=dict(color="#1a6fc4", width=1.5, dash="dash"),
        name="Meta 2028",
    ))
    fig_bsc.add_trace(go.Scatterpolar(
        r=bsc_actual + [bsc_actual[0]],
        theta=bsc_categories + [bsc_categories[0]],
        fill="toself",
        fillcolor="rgba(34,197,94,0.2)",
        line=dict(color="#22c55e", width=2.5),
        name="Actual 2025",
        marker=dict(size=7, color="#22c55e"),
    ))
    fig_bsc.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True, range=[0, 100],
                gridcolor="rgba(255,255,255,0.1)",
                tickfont=dict(size=8, color="#64748b"),
                ticksuffix="%",
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.1)",
                tickfont=dict(size=9, color="#94a3b8"),
            ),
        ),
        paper_bgcolor="rgba(21,33,51,0)",
        font=dict(family="Inter", color="#94a3b8"),
        legend=dict(orientation="h", y=-0.12, font=dict(size=9, color="#cbd5e1"), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=30, r=30, t=20, b=40),
        height=310,
    )
    st.plotly_chart(fig_bsc, width="stretch", key="bsc_chart")
    st.markdown('</div>', unsafe_allow_html=True)

# ── MinTIC Radar ──
with col_radar2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">🇨🇴 Madurez Digital Colombia (MinTIC)</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-subtitle">Dimensiones de Transformación Digital — Escala 0–4</div>', unsafe_allow_html=True)

    if not data["mintic_maturity"].empty:
        mintic_df = data["mintic_maturity"].copy()
        mintic_dims = [d.replace(" y ", "\ny ") for d in mintic_df["Dimension"].tolist()]
        mintic_actual = mintic_df["Actual"].tolist()
        mintic_ideal = mintic_df["Ideal"].tolist()
    else:
        mintic_dims = ["Personas\ny Cultura", "Procesos", "Datos", "Tecnología"]
        mintic_actual = [2.0, 2.33, 2.0, 2.33]
        mintic_ideal  = [4.0, 4.0,  4.0, 4.0]

    fig_mintic = go.Figure()
    fig_mintic.add_trace(go.Scatterpolar(
        r=mintic_ideal + [mintic_ideal[0]],
        theta=mintic_dims + [mintic_dims[0]],
        fill="toself",
        fillcolor="rgba(14,165,233,0.08)",
        line=dict(color="#0ea5e9", width=1.5, dash="dot"),
        name="Ideal (4.0)",
    ))
    fig_mintic.add_trace(go.Scatterpolar(
        r=mintic_actual + [mintic_actual[0]],
        theta=mintic_dims + [mintic_dims[0]],
        fill="toself",
        fillcolor="rgba(245,158,11,0.25)",
        line=dict(color="#f59e0b", width=2.5),
        name="INFIVALLE 2025",
        marker=dict(size=8, color="#f59e0b"),
    ))
    fig_mintic.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True, range=[0, 4],
                gridcolor="rgba(255,255,255,0.1)",
                tickfont=dict(size=8, color="#64748b"),
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.1)",
                tickfont=dict(size=9, color="#94a3b8"),
            ),
        ),
        paper_bgcolor="rgba(21,33,51,0)",
        font=dict(family="Inter", color="#94a3b8"),
        legend=dict(orientation="h", y=-0.12, font=dict(size=9, color="#cbd5e1"), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=30, r=30, t=20, b=40),
        height=310,
    )
    st.plotly_chart(fig_mintic, width="stretch", key="mintic_chart")
    st.markdown('</div>', unsafe_allow_html=True)

# ── CAPEX by Wave ──
with col_mintic:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"> CAPEX por Dominio PETI</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-subtitle">Asignación presupuestal por dominio tecnológico (M$)</div>', unsafe_allow_html=True)

    projects_full = data["projects"].copy()
    if not projects_full.empty and "Dominio MGGTI" in projects_full.columns:
        capex_grp = (
            projects_full
            .groupby("Dominio MGGTI")["CAPEX (M$)"]
            .sum()
            .reset_index()
            .sort_values("CAPEX (M$)", ascending=True)
        )
        capex_colors = ["#1a6fc4","#0ea5e9","#ef4444","#a855f7","#22c55e","#f59e0b"]
        fig_capex = go.Figure(go.Bar(
            x=capex_grp["CAPEX (M$)"],
            y=capex_grp["Dominio MGGTI"],
            orientation="h",
            marker=dict(
                color=capex_colors[:len(capex_grp)],
                line=dict(width=0),
            ),
            text=capex_grp["CAPEX (M$)"].apply(lambda v: f"${v:,}M"),
            textposition="outside",
            textfont=dict(size=9, color="#94a3b8"),
        ))
        fig_capex.update_layout(**PLOTLY_TEMPLATE)
        fig_capex.update_layout(
            height=310,
            xaxis=dict(title="Millones $COP", tickfont=dict(size=8), gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(tickfont=dict(size=9), gridcolor="rgba(255,255,255,0.0)"),
        )
        st.plotly_chart(fig_capex, width="stretch", key="capex_chart")
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────── DATASET TABLE ───────────────────────────
st.markdown('<div class="section-header"> Dataset General de Acciones PETI INFIVALLE</div>', unsafe_allow_html=True)

projects_table = data["projects"].copy()

# Apply all active filters
if selected_year != "Todos":
    projects_table = projects_table[projects_table["Vigencia"].str.contains(selected_year, na=False)]

status_filter = []
if cb_planificado:   status_filter.append("Planificado")
if cb_en_ejecucion:  status_filter.append("En Ejecución")
if cb_finalizado:    status_filter.append("Finalizado")
if status_filter:
    projects_table = projects_table[projects_table["Estado"].isin(status_filter)]

# Select display columns
display_cols = ["Cód.", "Proyecto", "Dominio MGGTI", "Área Líder", "Vigencia", "CAPEX (M$)", "Estado", "Progreso"]
available_cols = [c for c in display_cols if c in projects_table.columns]
projects_display = projects_table[available_cols].reset_index(drop=True)
projects_display.columns = [c.strip() for c in projects_display.columns]

# Status emoji mapping
def status_emoji(s):
    return {"Finalizado": "✅ Finalizado", "En Ejecución": "🔄 En Ejecución", "Planificado": "📋 Planificado"}.get(s, s)

if "Estado" in projects_display.columns:
    projects_display["Estado"] = projects_display["Estado"].map(status_emoji)

if "CAPEX (M$)" in projects_display.columns:
    projects_display["CAPEX (M$)"] = pd.to_numeric(projects_display["CAPEX (M$)"], errors="coerce").fillna(0).astype(int)

col_config = {}
if "Progreso" in projects_display.columns:
    col_config["Progreso"] = st.column_config.ProgressColumn(
        label="Progreso",
        min_value=0.0,
        max_value=1.0,
        format="%.0%",
    )
if "CAPEX (M$)" in projects_display.columns:
    col_config["CAPEX (M$)"] = st.column_config.NumberColumn(
        label="CAPEX (M$)",
        format="$%d M",
    )

st.dataframe(
    projects_display,
    width="stretch",
    height=380,
    column_config=col_config,
    hide_index=True,
)

# ─────────────────────────── FOOTER ───────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center;font-size:0.65rem;color:#334155;padding:10px 0 4px">
    <strong style="color:#475569">INFIVALLE</strong> — Plan Estratégico de Tecnologías de la Información 2025–2028 &nbsp;·&nbsp;
    Desarrollado en el marco de <em>Gobierno y Servicios de TI</em> — Corporación Universitaria Antonio José de Sucre &nbsp;·&nbsp;
    <span style="color:#1a6fc4">Streamlit</span> + <span style="color:#0ea5e9">Plotly</span> + <span style="color:#22c55e">Pandas</span>
</div>
""", unsafe_allow_html=True)
