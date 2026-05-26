import sqlite3
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

def get_db_path():
    if LOCAL_DB_PATH.exists():
        print(f"[INFO] Utilizando base de datos local en: {LOCAL_DB_PATH}")
        return LOCAL_DB_PATH
    if APPDATA_DB_PATH.exists():
        print(f"[INFO] Utilizando base de datos en AppData (Fallback): {APPDATA_DB_PATH}")
        return APPDATA_DB_PATH
    print(f"[WARNING] No se encontró ninguna base de datos en las rutas estándar.")
    return None

def main():
    print("=" * 60)
    print(" DIAGNÓSTICO E INTEGRIDAD DE LA BASE DE DATOS ")
    print("=" * 60)
    
    db_path = get_db_path()
    if not db_path:
        print("ERROR: Ejecuta 'crear_base_datos.py' para inicializar la base de datos.")
        return
        
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("[WARNING] La base de datos está vacía (no contiene tablas).")
            conn.close()
            return
            
        print("\nTablas encontradas y recuento de registros:")
        print("-" * 50)
        print(f"{'Nombre de la Tabla':<25} | {'Registros (Filas)':<18}")
        print("-" * 50)
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM \"{table_name}\";")
            count = cursor.fetchone()[0]
            print(f"{table_name:<25} | {count:<18}")
            
        print("-" * 50)
        conn.close()
        print("\n[OK] ¡La base de datos está lista y es funcional!")
        
    except Exception as e:
        print(f"ERROR: No se pudo leer la base de datos: {e}")

if __name__ == '__main__':
    main()
