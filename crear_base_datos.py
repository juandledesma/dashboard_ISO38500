import sqlite3
import pandas as pd
import os
import zipfile
import xml.etree.ElementTree as ET
import sys
from pathlib import Path

# Force UTF-8 encoding for standard output to prevent windows terminal character map errors
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Paths
PROJECT_DIR = Path(__file__).resolve().parent

EXCEL_PATH_CLEAN = PROJECT_DIR / "data" / "INFIVALLE_Dataset_PETI_2025_2028.xlsx"
EXCEL_PATH_ORIG = PROJECT_DIR / "data" / "INFIVALLE_Dataset_PETI_2025_2028 (1).xlsx"
EXCEL_PATH = EXCEL_PATH_CLEAN if EXCEL_PATH_CLEAN.exists() else EXCEL_PATH_ORIG

DOCX_PATH_CLEAN = PROJECT_DIR / "data" / "PETI_INFIVALLE_2025_2028_PRO_v4_ENTREGA.docx"
DOCX_PATH_ORIG = PROJECT_DIR / "data" / "PETI_INFIVALLE_2025_2028_PRO_v4_ENTREGA (5).docx"
DOCX_PATH = DOCX_PATH_CLEAN if DOCX_PATH_CLEAN.exists() else DOCX_PATH_ORIG

def clean_text(text):
    if not isinstance(text, str):
        return text
    return text.strip().replace('\xa0', ' ').replace('\u2013', '-').replace('\u2014', '-').replace('\u2264', '<=')

def parse_docx_table(docx_path, table_idx):
    try:
        z = zipfile.ZipFile(docx_path)
        xml_content = z.read('word/document.xml')
        root = ET.fromstring(xml_content)
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        
        tables = root.findall('.//w:tbl', ns)
        if table_idx >= len(tables):
            return pd.DataFrame()
            
        tbl = tables[table_idx]
        rows = tbl.findall('.//w:tr', ns)
        
        table_rows = []
        for row in rows:
            cells = row.findall('.//w:tc', ns)
            row_cells = []
            for cell in cells:
                cell_text = "".join([t.text for t in cell.findall('.//w:t', ns) if t.text])
                row_cells.append(clean_text(cell_text))
            table_rows.append(row_cells)
            
        if not table_rows:
            return pd.DataFrame()
            
        headers = table_rows[0]
        data = table_rows[1:]
        
        max_cols = len(headers)
        cleaned_data = []
        for r in data:
            if len(r) < max_cols:
                r = r + [""] * (max_cols - len(r))
            elif len(r) > max_cols:
                r = r[:max_cols]
            cleaned_data.append(r)
            
        df = pd.DataFrame(cleaned_data, columns=headers)
        return df
    except Exception as e:
        print(f"Error parsing Word table {table_idx}: {e}")
        return pd.DataFrame()

def get_db_connections():
    conns = []
    
    # 1. Local workspace path
    try:
        db_path_local = PROJECT_DIR / "database" / "peti_infivalle.db"
        # Ensure parent folder exists
        db_path_local.parent.mkdir(parents=True, exist_ok=True)
        # Remove existing if exists to recreate
        if db_path_local.exists():
            try:
                db_path_local.unlink()
            except Exception as e:
                print(f"Could not delete existing local db: {e}")
        conn_local = sqlite3.connect(str(db_path_local))
        conns.append(("Local Workspace", conn_local))
        print("Connected to Local SQLite database.")
    except Exception as e:
        print(f"Could not connect to local db (it might be blocked by Windows Controlled Folder Access): {e}")
        
    # 2. Trusted AppData path
    try:
        appdata_dir = Path.home() / ".gemini" / "antigravity"
        appdata_dir.mkdir(parents=True, exist_ok=True)
        db_path_appdata = appdata_dir / "peti_infivalle.db"
        if db_path_appdata.exists():
            try:
                db_path_appdata.unlink()
            except Exception as e:
                print(f"Could not delete existing AppData db: {e}")
        conn_appdata = sqlite3.connect(str(db_path_appdata))
        conns.append(("AppData Storage", conn_appdata))
        print("Connected to AppData SQLite database.")
    except Exception as e:
        print(f"Could not connect to AppData db: {e}")
        
    return conns

def main():
    print("[Starting] SQLite database creation...")
    
    # Ensure source files exist
    if not EXCEL_PATH.exists():
        print(f"Error: Source Excel file not found at {EXCEL_PATH}")
        return
    if not DOCX_PATH.exists():
        print(f"Error: Source Word file not found at {DOCX_PATH}")
        return

    # ─────────────────────────── 1. LOAD & CLEAN DATA ───────────────────────────
    print("Reading Excel Sheet: KPI_BSC...")
    kpis_df = pd.read_excel(EXCEL_PATH, sheet_name="KPI_BSC", skiprows=2)
    kpis_df = kpis_df.dropna(subset=["Código KPI"])
    kpis_df.columns = [c.strip() for c in kpis_df.columns]
    for c in kpis_df.columns:
        if kpis_df[c].dtype == object:
            kpis_df[c] = kpis_df[c].apply(clean_text)

    print("Reading Excel Sheet: Heatmap_TI...")
    heatmap_df = pd.read_excel(EXCEL_PATH, sheet_name="Heatmap_TI", skiprows=1)
    heatmap_df = heatmap_df.dropna(subset=["Área Funcional"])
    heatmap_df = heatmap_df[~heatmap_df["Área Funcional"].str.contains("LEYENDA", na=False)]
    heatmap_df.columns = [c.strip() for c in heatmap_df.columns]
    heatmap_df = heatmap_df.rename(columns={"Área Funcional": "Area"})
    for c in heatmap_df.columns:
        if c != "Area":
            heatmap_df[c] = pd.to_numeric(heatmap_df[c], errors='coerce').fillna(0)
        else:
            heatmap_df[c] = heatmap_df[c].apply(clean_text)

    print("Reading Excel Sheet: Objetivos_PETI...")
    objectives_df = pd.read_excel(EXCEL_PATH, sheet_name="Objetivos_PETI", skiprows=1)
    objectives_df = objectives_df.dropna(subset=["Código"])
    objectives_df.columns = [c.strip() for c in objectives_df.columns]
    for c in objectives_df.columns:
        if objectives_df[c].dtype == object:
            objectives_df[c] = objectives_df[c].apply(clean_text)

    print("Reading Excel Sheet: DOFA_TI...")
    dofa_df = pd.read_excel(EXCEL_PATH, sheet_name="DOFA_TI", skiprows=1)
    dofa_df = dofa_df.dropna(subset=["Código"])
    dofa_df.columns = [c.strip() for c in dofa_df.columns]
    for c in dofa_df.columns:
        if dofa_df[c].dtype == object:
            dofa_df[c] = dofa_df[c].apply(clean_text)

    print("Reading Excel Sheet: MinTIC_TD...")
    mintic_df = pd.read_excel(EXCEL_PATH, sheet_name="MinTIC_TD", skiprows=1)
    mintic_df_clean = mintic_df.dropna(subset=["Código"])
    
    # Extract dimensions questions (Q1 to Q17)
    mintic_questions_df = mintic_df_clean[mintic_df_clean["Código"].str.startswith("Q", na=False)].copy()
    mintic_questions_df.columns = [c.strip() for c in mintic_questions_df.columns]
    mintic_questions_df["Puntaje (0-4)"] = pd.to_numeric(mintic_questions_df["Puntaje (0–4)"], errors='coerce').fillna(0)
    for c in mintic_questions_df.columns:
        if mintic_questions_df[c].dtype == object:
            mintic_questions_df[c] = mintic_questions_df[c].apply(clean_text)
            
    # Extract dimension averages
    mintic_avg_df = mintic_df_clean[~mintic_df_clean["Código"].str.startswith("Q", na=False) & ~mintic_df_clean["Código"].str.contains("PROMEDIO", na=False)].copy()
    mintic_avg_df.columns = [c.strip() for c in mintic_avg_df.columns]
    for c in mintic_avg_df.columns:
        if mintic_avg_df[c].dtype == object:
            mintic_avg_df[c] = mintic_avg_df[c].apply(clean_text)

    print("Reading Excel Sheet: Portafolio_Olas...")
    portafolio_df = pd.read_excel(EXCEL_PATH, sheet_name="Portafolio_Olas", skiprows=1)
    portafolio_df = portafolio_df.dropna(subset=["Ola"])
    portafolio_df.columns = [c.strip() for c in portafolio_df.columns]
    for c in portafolio_df.columns:
        if portafolio_df[c].dtype == object:
            portafolio_df[c] = portafolio_df[c].apply(clean_text)

    print("Reading Excel Sheet: Trazabilidad...")
    trazabilidad_df = pd.read_excel(EXCEL_PATH, sheet_name="Trazabilidad", skiprows=1)
    trazabilidad_df = trazabilidad_df.dropna(subset=["OBJ PETI"])
    trazabilidad_df.columns = [c.strip() for c in trazabilidad_df.columns]
    for c in trazabilidad_df.columns:
        if trazabilidad_df[c].dtype == object:
            trazabilidad_df[c] = trazabilidad_df[c].apply(clean_text)

    print("Reading DOCX: General Projects (Table 19)...")
    projects_df = parse_docx_table(DOCX_PATH, 18)  # Table 19 is index 18
    if not projects_df.empty:
        projects_df.columns = [c.strip() for c in projects_df.columns]
        if 'Plazo (m)' in projects_df.columns:
            projects_df['Plazo (m)'] = pd.to_numeric(projects_df['Plazo (m)'], errors='coerce').fillna(12).astype(int)
        if 'CAPEX (M$)' in projects_df.columns:
            projects_df['CAPEX (M$)'] = pd.to_numeric(projects_df['CAPEX (M$)'], errors='coerce').fillna(0).astype(int)
            
        # Map progress and status
        def assign_status_and_progress(row):
            vigencia = str(row.get('Vigencia', '2025'))
            code = str(row.get('Cód.', ''))
            
            if '2025' in vigencia and not '-' in vigencia:
                if code in ['G-01', 'G-02', 'E-01', 'S-02']:
                    return 'Finalizado', 1.0
                else:
                    return 'En Ejecución', 0.85
            elif '2025' in vigencia and '-' in vigencia: 
                return 'En Ejecución', 0.60
            elif '2026' in vigencia:
                if '-' in vigencia: 
                    return 'Planificado', 0.15
                else:
                    return 'En Ejecución', 0.40
            else:
                return 'Planificado', 0.0
                
        status_progress = projects_df.apply(assign_status_and_progress, axis=1)
        projects_df['Estado'] = [x[0] for x in status_progress]
        projects_df['Progreso'] = [x[1] for x in status_progress]

    # Additional tables for database-driven radars and KPI cards
    print("Generating database-driven KPI cards table...")
    macro_kpis_data = {
        "KPI": [
            "Progreso General PETI",
            "Cumplimiento de Metas TI",
            "Alineación BSC Estratégico",
            "Madurez MGGTI Actual",
            "Trámites Digitalizados SUIT"
        ],
        "Value": ["88%", "75%", "92%", "1.2/5", "18%"],
        "Delta": ["+5%", "+2%", "+8%", "→4.0", "→85%"],
        "Subtext": [
            "vs. trimestre anterior",
            "vs. línea base 2024",
            "vs. PETI anterior",
            "Meta 2028 MinTIC",
            "Meta 2028"
        ],
        "Color": ["blue", "green", "amber", "blue", "green"],
        "Positive": [1, 1, 1, 1, 1]
    }
    macro_kpis_df = pd.DataFrame(macro_kpis_data)

    print("Generating database-driven BSC perspectives table...")
    bsc_perspectives_data = {
        "Perspective": [
            "Contribución Corporativa",
            "Orientación al Usuario",
            "Excelencia Operativa",
            "Capacidades Futuras"
        ],
        "Actual": [72, 78, 85, 63],
        "Meta": [90, 90, 99, 90]
    }
    bsc_perspectives_df = pd.DataFrame(bsc_perspectives_data)

    print("Generating database-driven MinTIC maturity dimensions table...")
    mintic_maturity_data = {
        "Dimension": ["Personas y Cultura", "Procesos", "Datos", "Tecnología"],
        "Actual": [2.00, 2.33, 2.00, 2.33],
        "Ideal": [4.00, 4.00, 4.00, 4.00]
    }
    mintic_maturity_df = pd.DataFrame(mintic_maturity_data)

    print("Generating weekly operational incidents table...")
    incidentes_data = {
        "ID": ["INC-001", "INC-002", "INC-003", "INC-004", "INC-005", "INC-006", "INC-007"],
        "Semana": ["Semana 20", "Semana 20", "Semana 20", "Semana 21", "Semana 21", "Semana 21", "Semana 21"],
        "Incidente": [
            "Caída del canal transaccional SUIT",
            "Fallo de replicación base de datos en nube",
            "Alerta de consumo inusual de CPU en servidor BD",
            "Bloqueo de cuentas en portal de tesorería",
            "Error de sincronización de saldos contabilidad",
            "Lentitud en consultas del módulo de cartera",
            "Falso positivo en escáner de malware perimetral"
        ],
        "Criticidad": ["Alta", "Alta", "Media", "Baja", "Alta", "Media", "Baja"],
        "Estado": ["Resuelto", "Resuelto", "Resuelto", "Resuelto", "Resuelto", "En Proceso", "Resuelto"],
        "Tiempo_Resolucion_h": [3.5, 4.2, 1.2, 0.5, 6.0, 12.0, 0.2],
        "Area_Impactada": ["Servicios Digitales", "Infraestructura", "Seguridad", "Tesorería", "Cartera", "Cartera", "Seguridad"]
    }
    incidentes_df = pd.DataFrame(incidentes_data)

    print("Generating automation execution logs table...")
    logs_data = {
        "Timestamp": [
            "2026-05-04 07:00:12",
            "2026-05-11 07:00:15",
            "2026-05-18 07:00:08",
            "2026-05-23 19:30:45"
        ],
        "Flujo": [
            "Gobernanza Semanal PETI - ISO 38500",
            "Gobernanza Semanal PETI - ISO 38500",
            "Gobernanza Semanal PETI - ISO 38500",
            "Gobernanza Semanal PETI - ISO 38500"
        ],
        "Estado": ["Éxito", "Éxito", "Éxito", "Simulación Manual"],
        "Registros_Combinados": [33, 33, 33, 33],
        "Hallazgos_Detectados": [0, 1, 0, 1],
        "Reporte_Enviado": [
            "Comité TI - Sin hallazgos críticos",
            "Comité TI - Alerta: Retraso en objetivo OBJ-02",
            "Comité TI - Sin hallazgos críticos",
            "Simulador - Alerta: 2 Incidentes de alta criticidad"
        ]
    }
    logs_df = pd.DataFrame(logs_data)

    # ─────────────────────────── 2. SAVE TO SQLITE ───────────────────────────
    conns = get_db_connections()
    if not conns:
        print("Error: No database connections could be established. Ingestion failed.")
        return

    tables = {
        "kpis": kpis_df,
        "heatmap": heatmap_df,
        "objectives": objectives_df,
        "dofa": dofa_df,
        "mintic_questions": mintic_questions_df,
        "mintic_avg": mintic_avg_df,
        "portafolio_olas": portafolio_df,
        "trazabilidad": trazabilidad_df,
        "projects": projects_df,
        "macro_kpis": macro_kpis_df,
        "bsc_perspectives": bsc_perspectives_df,
        "mintic_maturity": mintic_maturity_df,
        "incidentes_semanales": incidentes_df,
        "log_ejecucion_flujo": logs_df
    }

    for label, conn in conns:
        print(f"\nIngesting data into database: {label}...")
        try:
            for table_name, df in tables.items():
                if not df.empty:
                    df.to_sql(table_name, conn, if_exists='replace', index=False)
                    print(f"  Ingested table '{table_name}' ({len(df)} rows)")
            conn.commit()
            conn.close()
            print(f"Ingestion for {label} completed successfully.")
        except Exception as e:
            print(f"Error during ingestion for {label}: {e}")

    print("\n[Done] SQLite Data Migration completed successfully!")

if __name__ == '__main__':
    main()
