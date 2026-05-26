# Documentación de Normalización y Estructura de Datos (SQLite)

Este documento detalla la estructura y el esquema de la base de datos relacional `peti_infivalle.db` utilizada por el Dashboard Estratégico PETI 2025-2028 de INFIVALLE.

Toda la información fue extraída y normalizada a partir de los documentos originales de planificación estratégica (Excel y Word) ubicados en la carpeta `data/`.

---

## Esquema de la Base de Datos

La base de datos contiene las siguientes tablas estructuradas:

### 1. `kpis`
Contiene los Indicadores Clave de Rendimiento (KPIs) definidos en el Balanced Scorecard (BSC).
*   **Columnas:**
    *   `Código KPI`: Identificador único (ej. `KPI-01`).
    *   `Perspectiva`: Perspectiva del BSC (Financiera, Procesos, etc.).
    *   `Objetivo Estratégico`: Objetivo PETI asociado.
    *   `Nombre del Indicador`: Descripción corta.
    *   `Fórmula`: Método de cálculo.
    *   `Meta 2028`: Objetivo final del plan.
    *   `Frecuencia`: Periodicidad del reporte (Mensual, Trimestral, Anual).
    *   `Responsable`: Proceso u oficina a cargo.

### 2. `heatmap`
Resultados de la priorización del mapa de calor de TI y procesos de INFIVALLE.
*   **Columnas:**
    *   `Area`: Área o proceso funcional analizado.
    *   `Impacto`, `Urgencia`, `Complejidad`, etc.: Puntuaciones numéricas para la matriz de decisión.

### 3. `objectives`
Objetivos estratégicos del PETI 2025-2028.
*   **Columnas:**
    *   `Código`: Identificador único (ej. `OBJ-01`).
    *   `Objetivo`: Enunciado del objetivo estratégico.
    *   `Descripción`: Detalle del alcance del objetivo.

### 4. `dofa`
Matriz DOFA (Debilidades, Oportunidades, Fortalezas, Amenazas) de la Oficina de TI.
*   **Columnas:**
    *   `Código`: Código único del factor (ej. `FO-01`, `DE-02`).
    *   `Tipo`: Categoría (Fortaleza, Debilidad, Oportunidad, Amenaza).
    *   `Descripción`: Texto descriptivo de la variable.

### 5. `projects`
Portafolio general de proyectos tecnológicos (Tabla 19 del PETI).
*   **Columnas:**
    *   `Cód.`: Código del proyecto (ej. `G-01`, `S-02`).
    *   `Proyecto`: Nombre del proyecto.
    *   `Objetivo`: Breve descripción.
    *   `Vigencia`: Años de ejecución (ej. `2025-2026`).
    *   `Plazo (m)`: Plazo estimado en meses.
    *   `CAPEX (M$)`: Costo de inversión estimado en millones de pesos COP.
    *   `Estado`: Estado operativo (`Finalizado`, `En Ejecución`, `No Iniciado`).
    *   `Progreso`: Porcentaje de avance de la ejecución (0.00 a 1.00).

### 6. `incidentes_semanales`
Registro histórico y actual de incidentes operativos de gobernanza de TI.
*   **Columnas:**
    *   `ID`: Identificador de incidente (ej. `INC-001`).
    *   `Semana`: Semana de reporte.
    *   `Incidente`: Descripción del incidente.
    *   `Criticidad`: Alta, Media o Baja.
    *   `Estado`: Resuelto o En Proceso.
    *   `Tiempo_Resolucion_h`: Tiempo transcurrido en horas.

### 7. `log_ejecucion_flujo`
Logs históricos generados por las automatizaciones y flujos de datos.
*   **Columnas:**
    *   `Timestamp`: Fecha y hora de ejecución.
    *   `Flujo`: Nombre del proceso ejecutado.
    *   `Estado`: Éxito o Falla.
    *   `Detalles`: Observaciones generales de la ejecución.

---

## Regeneración y Mantenimiento

*   **Para regenerar la base de datos:** Ejecuta el script `crear_base_datos.py` desde el directorio raíz.
*   **Para exportar los datos a Excel:** Ejecuta `exportar_bd_excel.py` para regenerar el archivo `database/BASE_DATOS_NORMALIZADA.xlsx`.
