import os
import sqlite3
import pandas as pd
from pathlib import Path

# Database Paths
PROJECT_DIR = Path(__file__).resolve().parent
LOCAL_DB_PATH = PROJECT_DIR / "dashboard.db"
# Fallback for the original developer's machine
APPDATA_DB_PATH = Path.home() / ".gemini" / "antigravity" / "dashboard.db"

def get_db_path():
    # Primary: look in the same folder as the script (portable)
    if LOCAL_DB_PATH.exists():
        return LOCAL_DB_PATH
    # Fallback: check AppData (original developer location)
    if APPDATA_DB_PATH.exists():
        return APPDATA_DB_PATH
    # Default to local so errors point to the right place
    return LOCAL_DB_PATH

def load_table(table_name):
    db_path = get_db_path()
    try:
        conn = sqlite3.connect(str(db_path))
        df = pd.read_sql_query(f'SELECT * FROM "{table_name}"', conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error loading SQLite table '{table_name}' from {db_path}: {e}")
        return pd.DataFrame()

def get_all_data():
    """
    Consolidated interface for all datasets.
    Reads exclusively from the pre-populated SQLite database.
    """
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

if __name__ == '__main__':
    # Diagnostic check
    db_path = get_db_path()
    print(f"Using database at: {db_path}")
    print(f"File exists: {db_path.exists()}")
    if db_path.exists():
        data = get_all_data()
        for name, df in data.items():
            print(f"  - {name}: shape={df.shape}")
