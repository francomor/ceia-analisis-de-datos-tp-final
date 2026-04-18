# CEIA - Análisis de Datos - Trabajo Práctico Final

Análisis exploratorio del dataset de crímenes de Chicago 2025, realizado como trabajo práctico final para la materia Análisis de Datos de la CEIA.

## Dataset

- **Fuente**: [Chicago Data Portal - Crimes 2025](https://data.cityofchicago.org/Public-Safety/Crimes-2025/t7ek-mgzi/about_data)
- **Registros**: 236,686
- **Features**: 22 columnas (ID, fecha, tipo de crimen, ubicación, coordenadas, arresto, etc.)

## Análisis realizado

### Notebooks principales

En orden de lectura recomendado:

1. `1.tp_final_eda_fran.ipynb` — Primer EDA del dataset de Chicago Crimes 2025 (inspección general, nulos, distribuciones de arrestos y crímenes domésticos, top de tipos de crimen, análisis por Community Area y distribución temporal).
2. `2.tp_final_parte2_fran.ipynb` — Segunda parte del TP, continuación del análisis.
3. `3_tp_final_nuevas_features_Agus.ipynb` — Generación de nuevas features a partir del dataset.

### Material complementario

Aportes individuales de los participantes y recursos del grupo:

- `1.analisis_inicial.ipynb` — análisis inicial previo.
- `TP parte 2_Aye.ipynb` — trabajo individual de Aye sobre la parte 2.
- `EDA_individual_Agus.py` — EDA individual de Agus.
- `Análisis de datos - Trabajo grupal - 1B2026.pdf` — consigna original del TP.

## Requisitos

- Python >= 3.11, < 3.13
- Dependencias listadas en `pyproject.toml`

## Instalación

```bash
uv sync
```

## Uso

Abrir y ejecutar los notebooks principales en orden (`1.tp_final_eda_fran.ipynb`, `2.tp_final_parte2_fran.ipynb`, `3_tp_final_nuevas_features_Agus.ipynb`) en Jupyter o un IDE compatible.
