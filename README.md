# Dashboard Estratégico ISO 38500

Dashboard interactivo para visualizar métricas de Gobierno de TI (ISO 38500) - INFIVALLE.

 Guía de Inicio Rápido

 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

 1. Instalación del Entorno

```bash
# Clonar o descargar el repositorio
git clone <repository-url>
cd dashboard_ISO38500

# Crear un entorno virtual (recomendado)
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instalar las dependencias
pip install -r requirements.txt
```

 2. Configuración de la Base de Datos

```bash
# Crear la base de datos desde el archivo Excel
python crear_base_datos.py

# (Opcional) Verificar que la base de datos se creó correctamente
python verificar_bd.py
```

### 3. Ejecutar el Dashboard

```bash
# Iniciar la aplicación Streamlit
streamlit run app.py
```

La aplicación se abrirá automáticamente en `http://localhost:8501`

---

 Estructura del Proyecto

```
dashboard_ISO38500/
├── app.py                          # Aplicación principal Streamlit
├── crear_base_datos.py             # Script para crear la BD desde Excel
├── data_loader.py                  # Cargador de datos
├── verificar_bd.py                 # Verificación de integridad de BD
├── exportar_bd_excel.py            # Exportación de datos a Excel
├── organizar.py                    # Utilidades de organización
├── requirements.txt                # Dependencias de Python
├── data/                           # Directorio de datos fuente
│   └── Herramienta_Medicion_MD_Estado_Colombia_INFIVALLE_LLENADO.xlsm
├── database/                       # Base de datos generada
└── docs/                           # Documentación
    └── NORMALIZACION_DATOS.md
```

---

 Comandos Útiles para Desarrolladores

| Comando | Descripción |
|---------|-------------|
| `streamlit run app.py` | Inicia el dashboard en modo desarrollo |
| `python crear_base_datos.py` | (Re)genera la base de datos desde datos fuente |
| `python verificar_bd.py` | Valida la integridad de los datos |
| `python exportar_bd_excel.py` | Exporta datos procesados a Excel |
| `streamlit run app.py --logger.level=debug` | Ejecuta con logs de depuración |

---

 Dependencias Principales

- **Streamlit** - Framework web interactivo
- **Pandas** - Procesamiento y análisis de datos
- **Plotly** - Visualizaciones interactivas
- **openpyxl** - Lectura/escritura de archivos Excel
- **python-docx** - Manipulación de documentos Word

---

 Solución de Problemas

**Problema:** El dashboard no inicia
- Verifica que todas las dependencias estén instaladas: `pip install -r requirements.txt`
- Comprueba que Python 3.8+ está instalado: `python --version`

**Problema:** Error al crear la base de datos
- Asegúrate de que el archivo Excel existe en `data/`
- Ejecuta `python verificar_bd.py` para más detalles

---

 Documentación Adicional

Para más información sobre normalización de datos, consulta [NORMALIZACION_DATOS.md](docs/NORMALIZACION_DATOS.md)
