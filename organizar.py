import os
import shutil
import sys
from pathlib import Path

# Force UTF-8 encoding
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

PROJECT_DIR = Path(__file__).resolve().parent

# Define mappings: source filename in root -> destination filename in data/
FILE_MAPPINGS = {
    "Analisis_Matriz_DOFA_Alineacion_Gobernanza_CORREGIDO (2).docx": "Análisis de la Matriz DOFA y Las 5 Fuerzas.docx",
    "CadenaValor-Infivalle (2).pdf": "Cadena_Valor_TI.pdf",
    "Canvas_TI_INFIVALLE_PETI2025-2028 (1).pdf": "Canvas_TI_INFIVALLE_PETI2025-2028.pdf",
    "Documentos_Diagnostico_Fuerzas_Porter_CORREGIDO (1).docx": "Documentos_DiagnosticoFuerzasPorter.docx",
    "Herramienta_Medicion_MD_Estado_Colombia_INFIVALLE_LLENADO.xlsm": "Herramienta_Medicion_MD_Estado_Colombia_INFIVALLE_LLENADO.xlsm",
    "INFIVALLE_Dataset_PETI_2025_2028 (1).xlsx": "INFIVALLE_Dataset_PETI_2025_2028.xlsx",
    "INFIVALLE_Estrategia_TI_2025_2028 (1).docx": "INFIVALLE_Estrategia_TI_2025_2028.docx",
    "Justificación de asignación (1).docx": "Justificación de asignación.docx",
    "PETI_INFIVALLE_2025_2028_PRO_v4_ENTREGA (5).docx": "PETI_INFIVALLE_2025_2028_PRO_v4_ENTREGA.docx",
    "Strategy Maps __ BSC Designer® Online (1).pdf": "Strategy Maps __ BSC Designer® Online.pdf"
}

def main():
    print("=" * 60)
    print(" REORGANIZACIÓN PROFESIONAL DE CARPETAS ")
    print("=" * 60)
    
    # 1. Ensure folders exist
    os.makedirs(PROJECT_DIR / "data", exist_ok=True)
    os.makedirs(PROJECT_DIR / "database", exist_ok=True)
    os.makedirs(PROJECT_DIR / "docs", exist_ok=True)
    print("[1] Directorios 'data', 'database' y 'docs' verificados/creados.")
    
    # 2. Move and rename raw files
    print("\n[2] Moviendo y renombrando documentos originales a 'data/'...")
    for old_name, new_name in FILE_MAPPINGS.items():
        old_path = PROJECT_DIR / old_name
        new_path = PROJECT_DIR / "data" / new_name
        
        if old_path.exists():
            try:
                # If target exists, remove it first to avoid copy error
                if new_path.exists():
                    new_path.unlink()
                shutil.move(str(old_path), str(new_path))
                print(f"  ✓ Movido: '{old_name}' -> 'data/{new_name}'")
            except Exception as e:
                print(f"  ✗ Error al mover '{old_name}': {e}")
        else:
            if new_path.exists():
                print(f"  • Ya movido anteriormente: 'data/{new_name}'")
            else:
                print(f"  • Archivo original no encontrado (omitido): '{old_name}'")
                
    # 3. Copy the SQLite database from AppData
    print("\n[3] Copiando la base de datos SQLite activa a la carpeta 'database/'...")
    src_db = Path.home() / ".gemini" / "antigravity" / "peti_infivalle.db"
    dst_db = PROJECT_DIR / "database" / "peti_infivalle.db"
    
    if src_db.exists():
        try:
            shutil.copy2(str(src_db), str(dst_db))
            print(f"  ✓ Base de datos copiada exitosamente a: {dst_db}")
        except Exception as e:
            print(f"  ✗ No se pudo copiar la base de datos automáticamente: {e}")
            print(f"    (Por favor copia '{src_db}' y pégalo en '{dst_db}' manualmente)")
    else:
        print(f"  • No se encontró la base de datos origen en AppData.")
        print(f"    (Se creará una nueva al correr 'crear_base_datos.py')")
        
    # 4. Generate the normalized Excel file
    print("\n[4] Intentando generar el Excel de base de datos normalizada...")
    try:
        import exportar_bd_excel
        exportar_bd_excel.main()
    except Exception as e:
        print(f"  ✗ No se pudo ejecutar la exportación automática: {e}")
        
    # 5. Clean up old/temporary files
    print("\n[5] Limpiando archivos temporales e innecesarios de la raíz...")
    files_to_remove = [
        "copy_db.py",
        "test_write.py",
        "test.txt",
        "data_loader.py",
        "init_db.py"
    ]
    for f in files_to_remove:
        path = PROJECT_DIR / f
        if path.exists():
            try:
                path.unlink()
                print(f"  ✓ Eliminado de la raíz: '{f}'")
            except Exception as e:
                print(f"  ✗ No se pudo eliminar '{f}': {e}")
                
    print("\n" + "=" * 60)
    print(" ¡REORGANIZACIÓN COMPLETADA CON ÉXITO! ")
    print("=" * 60)
    print("\nEl espacio de trabajo ahora está limpio y profesional.")
    print("Para iniciar el dashboard, simplemente ejecuta:")
    print("  streamlit run app.py")
    print("=" * 60)

if __name__ == '__main__':
    main()
