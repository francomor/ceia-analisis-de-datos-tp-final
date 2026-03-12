# CEIA - Análisis de Datos - Trabajo Práctico Final

Análisis exploratorio del dataset de crímenes de Chicago 2025, realizado como trabajo práctico final para la materia Análisis de Datos de la CEIA.

## Dataset

- **Fuente**: Chicago Data Portal - Crimes 2025
- **Registros**: 236,686
- **Features**: 22 columnas (ID, fecha, tipo de crimen, ubicación, coordenadas, arresto, etc.)

## Análisis realizado

El notebook `1.analisis_inicial.ipynb` contiene el análisis exploratorio inicial:

- Inspección general del dataset (tipos de datos, dimensiones, estadísticas descriptivas)
- Análisis de valores nulos (91 registros sin coordenadas, 1097 sin descripción de ubicación)
- Distribución de arrestos (84% sin arresto, 16% con arresto)
- Distribución de crímenes domésticos (81% no doméstico, 19% doméstico)
- Relación entre arrestos y crímenes domésticos
- Top 10 tipos de crímenes más frecuentes (THEFT, BATTERY, CRIMINAL DAMAGE lideran)
- Tipos de crímenes con mayor tasa de arrestos
- Crimen prevalente por Community Area
- Distribución temporal de crímenes por mes

## Requisitos

- Python >= 3.11, < 3.13
- Dependencias listadas en `pyproject.toml`

## Instalación

```bash
uv sync
```

## Uso

Abrir y ejecutar el notebook `1.analisis_inicial.ipynb` en Jupyter o un IDE compatible.
