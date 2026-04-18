# CEIA - Análisis de Datos - Trabajo Práctico Final

Análisis exploratorio y preprocesamiento del dataset de crímenes de Chicago 2025, realizado como trabajo práctico final para la materia Análisis de Datos de la CEIA.

## Dataset

- **Fuente**: [Chicago Data Portal - Crimes 2025](https://data.cityofchicago.org/Public-Safety/Crimes-2025/t7ek-mgzi/about_data)
- **Registros**: 236,686
- **Features**: 22 columnas (ID, fecha, tipo de crimen, ubicación, coordenadas, arresto, etc.)

## Entregables del TP

Los únicos notebooks que conforman la entrega oficial del grupo son:

1. `tp_final_eda.ipynb` — **Parte 1: EDA del dataset de Chicago Crimes 2025.** Exploración y comprensión de los datos (tipos de variables, distribuciones de arrestos y crímenes domésticos, top de tipos de crimen, análisis por Community Area, patrones temporales, correlaciones), detección de valores faltantes con clasificación MCAR/MAR/MNAR, análisis de outliers, visualizaciones geográficas y hallazgos finales.
2. `tp_final_parte2.ipynb` — **Parte 2: Preprocesamiento, feature engineering y reducción de dimensionalidad.** Split train/test estratificado, tratamiento de valores faltantes, generación de nuevas features (temporales, `distancia_cbd`, `is_violent`, interacciones), codificación de categóricas (OneHotEncoder + TargetEncoder), escalado con `StandardScaler`, balanceo con SMOTE, selección de features por correlación y `mutual_info_classif`, y extracción con PCA.

## Material complementario

El resto de los archivos del repositorio **no forma parte de la entrega**: son aportes individuales de los integrantes del grupo y recursos auxiliares que acompañaron el desarrollo de los dos notebooks oficiales.

- `1.analisis_inicial.ipynb` — análisis inicial previo del grupo.
- `1.tp_final_eda_fran.ipynb` — versión previa del EDA aportada por Franco.
- `2.tp_final_parte2_fran.ipynb` — versión previa de la parte 2 aportada por Franco.
- `3_tp_final_nuevas_features_Agus.ipynb` — exploración de nuevas features por Agus.
- `EDA_individual_Agus.py` — EDA individual de Agus en formato script.
- `TP parte 2_Aye.ipynb` — trabajo individual de Aye sobre la parte 2.
- `Análisis de datos - Trabajo grupal - 1B2026.pdf` — consigna original del TP.
- Datasets y recursos auxiliares usados en los merges y visualizaciones: `Crimes_-_2025_20260312.csv`, `Boundaries_-_Community_Areas_20260329.csv`, `Chicago_Police_Department_-_Illinois_Uniform_Crime_Reporting_(IUCR)_Codes_20260329.csv`, `Chicago_districts_map.png`.

## Requisitos

- Python >= 3.11, < 3.13
- Dependencias listadas en `pyproject.toml`

## Instalación

```bash
uv sync
```

## Uso

Abrir y ejecutar los dos notebooks de la entrega en orden en Jupyter o un IDE compatible:

1. `tp_final_eda.ipynb`
2. `tp_final_parte2.ipynb`
