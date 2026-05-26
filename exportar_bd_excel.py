import sqlite3
import pandas as pd
import os
import sys
from pathlib import Path

# Force UTF-8 encoding
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

PROJECT_DIR = Path(__file__).resolve().parent
LOCAL_DB_PATH = PROJECT_DIR / "database" / "peti_infivalle.db"
APPDATA_DB_PATH = Path.home() / ".gemini" / "antigravity" / "peti_infivalle.db"
OUTPUT_EXCEL_PATH = PROJECT_DIR / "database" / "BASE_DATOS_NORMALIZADA.xlsx"

def get_db_path():
    if LOCAL_DB_PATH.exists():
        return LOCAL_DB_PATH
    if APPDATA_DB_PATH.exists():
        return APPDATA_DB_PATH
    return None

def main():
    print("=" * 60)
    print(" EXPORTADOR DE BASE DE DATOS A EXCEL ")
    print("=" * 60)
    
    db_path = get_db_path()
    if not db_path:
        print("ERROR: No se encontró la base de datos 'peti_infivalle.db'.")
        print("Ejecuta primero 'crear_base_datos.py' para inicializarla.")
        return
        
    print(f"Leyendo tablas desde: {db_path}...")
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Get tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        
        if not tables:
            print("La base de datos no contiene tablas.")
            conn.close()
            return
            
        # Ensure database/ folder exists
        OUTPUT_EXCEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"Exportando {len(tables)} tablas a Excel...")
        
        # Write to Excel
        with pd.ExcelWriter(OUTPUT_EXCEL_PATH, engine='openpyxl') as writer:
            for table in tables:
                df = pd.read_sql_query(f'SELECT * FROM "{table}"', conn)
                df.to_excel(writer, sheet_name=table, index=False)
                print(f"  - Tabla '{table}' exportada ({len(df)} registros)")
                
        conn.close()
        print(f"\n[OK] Excel generado exitosamente en: {OUTPUT_EXCEL_PATH}")
        
    except Exception as e:
        print(f"\n[ERROR] No se pudo exportar a Excel: {e}")
        print("\nNota: Si el error es 'PermissionDenied' o similar, podría deberse al Acceso Controlado a Carpetas de Windows.")
        print("Intenta abrir tu terminal de Windows y ejecutar el script manualmente:")
        print("  py exportar_bd_excel.py")

if __name__ == '__main__':
    main()
