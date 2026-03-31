import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1. Cargar el dataset
file_path = r'C:\Users\agust\Downloads\Crimes2025.csv'
# Cargamos y nos aseguramos de que 'Date' sea formato fecha
df = pd.read_csv(file_path)
df['Date'] = pd.to_datetime(df['Date'])
print(df.head())
# 2. Preparación de datos para análisis mensual
# Convertimos 'Arrest' (Boolean) a 1 y 0 para poder sumar
df['Arrest_Num'] = df['Arrest'].astype(int)

# Establecemos la fecha como índice para usar el remuestreo (resample)
df.set_index('Date', inplace=True)

# Agrupamos por mes ('ME' es Month End)
# Esto nos dará el total de crímenes y arrestos por cada mes de 2025
monthly_summary = df.resample('ME').agg(
    total_crimes=('ID', 'count'),
    total_arrests=('Arrest_Num', 'sum')
)

# Calculamos los casos sin arresto
monthly_summary['no_arrests'] = monthly_summary['total_crimes'] - monthly_summary['total_arrests']

# Cambiamos el nombre del índice a los nombres de los meses para que el gráfico sea legible
monthly_summary.index = monthly_summary.index.strftime('%B')

# 3. Visualizaciones Mensuales

# Gráfico 1: Evolución de Crímenes vs Arrestos
plt.figure(figsize=(12, 6))
plt.plot(monthly_summary.index, monthly_summary['total_crimes'], marker='o', label='Total Crímenes', color='royalblue', linewidth=2)
plt.plot(monthly_summary.index, monthly_summary['total_arrests'], marker='s', label='Arrestos Efectuados', color='limegreen', linewidth=2)
plt.fill_between(monthly_summary.index, monthly_summary['total_crimes'], alpha=0.1, color='royalblue')

plt.title('Tendencia Mensual de Criminalidad en Chicago (2025)', fontsize=15)
plt.xlabel('Mes', fontsize=12)
plt.ylabel('Cantidad de Casos', fontsize=12)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Gráfico 2: Top 5 Delitos del año (Bar Plot)
plt.figure(figsize=(10, 6))
top_crimes = df['Primary Type'].value_counts().head(5)
sns.barplot(x=top_crimes.values, y=top_crimes.index, palette='viridis')
plt.title('Top 5 Tipos de Delitos en 2025', fontsize=15)
plt.xlabel('Número de Reportes')
plt.ylabel('Tipo de Delito')
plt.show()

# 4. Estadísticas rápidas en consola
print("--- RESUMEN MENSUAL 2025 ---")
print(monthly_summary)
print("\n--- PORCENTAJE DE EFECTIVIDAD (ARRESTOS) ---")
efectividad = (monthly_summary['total_arrests'].sum() / monthly_summary['total_crimes'].sum()) * 100
print(f"La tasa de arrestos promedio en lo que va del 2025 es del: {efectividad:.2f}%")



# 1. Carga y preparación (asegúrate de tener df cargado del paso anterior)
# Agrupamos por día para detectar anomalías diarias
daily_crimes = df.groupby(df.index.date).size().rename('crime_count').to_frame()
daily_crimes.index = pd.to_datetime(daily_crimes.index)

# 2. Identificación de Outliers usando el método de IQR (Rango Intercuartílico)
Q1 = daily_crimes['crime_count'].quantile(0.25)
Q3 = daily_crimes['crime_count'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Marcamos los outliers
outliers = daily_crimes[(daily_crimes['crime_count'] < lower_bound) | (daily_crimes['crime_count'] > upper_bound)].copy()

# --- GRÁFICO 1: Boxplot Mensual para ver dispersión ---
plt.figure(figsize=(12, 6))
# Añadimos columna de mes para el boxplot
daily_crimes['Month'] = daily_crimes.index.strftime('%B')
sns.boxplot(data=daily_crimes, x='Month', y='crime_count', palette='Set3')
plt.title('Dispersión Diaria de Crímenes por Mes (Detección de Outliers)')
plt.ylabel('Crímenes por día')
plt.xticks(rotation=45)
plt.show()

# --- GRÁFICO 2: Serie temporal con Outliers marcados ---
plt.figure(figsize=(15, 6))
plt.plot(daily_crimes.index, daily_crimes['crime_count'], color='gray', alpha=0.5, label='Frecuencia Diaria')
plt.scatter(outliers.index, outliers['crime_count'], color='red', label='Outliers (Anomalías)', zorder=5)
plt.axhline(upper_bound, color='red', linestyle='--', alpha=0.3, label='Límite Superior')
plt.title('Detección de Anomalías en el Tiempo (2025)')
plt.legend()
plt.show()

# 3. Análisis de Causas de los Outliers
print(f"--- DÍAS DETECTADOS COMO OUTLIERS ({len(outliers)} días) ---")
if not outliers.empty:
    for date in outliers.index:
        print(f"\nFecha: {date.date()} - Total Crímenes: {outliers.loc[date, 'crime_count']}")
        
        # Filtramos los datos de ese día específico para ver qué pasó
        day_data = df[df.index.date == date.date()]
        top_crimes_day = day_data['Primary Type'].value_counts().head(3)
        top_locations_day = day_data['Location Description'].value_counts().head(3)
        
        print(f"  > Top 3 delitos ese día:\n{top_crimes_day.to_string()}")
        print(f"  > Lugares principales:\n{top_locations_day.to_string()}")
else:
    print("No se detectaron outliers estadísticos con el criterio IQR.")


# Crear columnas de hora y día de la semana
df['Hour'] = df.index.hour
df['DayOfWeek'] = df.index.day_name()

# Reordenar días de la semana
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Crear tabla pivote para el heatmap
pivot_table = df.pivot_table(values='ID', index='DayOfWeek', columns='Hour', aggfunc='count').reindex(days)

plt.figure(figsize=(15, 8))
sns.heatmap(pivot_table, cmap='YlOrRd', annot=False)
plt.title('Concentración de Crímenes: Día vs Hora (2025)')
plt.xlabel('Hora del Día')
plt.ylabel('Día de la Semana')
plt.show()


# 1. Identificar días de outliers en el df original
# .normalize() pone las horas en 00:00:00 para que coincidan con el índice de 'outliers'
df['is_outlier'] = df.index.normalize().isin(outliers.index)

# 2. Calcular la tasa de arrestos (promedio de la columna booleana * 100)
arrest_comparison = df.groupby('is_outlier')['Arrest'].mean() * 100

# 3. Gráfico
plt.figure(figsize=(8, 5))
sns.barplot(x=arrest_comparison.index, y=arrest_comparison.values, palette='coolwarm')

# Personalización
plt.title('¿Baja la eficacia policial en los días de pico criminal?', fontsize=13)
plt.ylabel('% de Arrestos Efectuados')
plt.xlabel('Tipo de Día')
plt.xticks([0, 1], ['Día Normal', 'Día de Anomalía (Outlier)'])
plt.ylim(0, arrest_comparison.max() + 5) # Dar un poco de margen arriba

# Añadir etiquetas de valor sobre las barras
for i, v in enumerate(arrest_comparison.values):
    plt.text(i, v + 0.5, f'{v:.1f}%', ha='center', fontweight='bold')

plt.show()

print(f"Tasa de arrestos en días normales: {arrest_comparison[False]:.2f}%")
print(f"Tasa de arrestos en días de anomalía: {arrest_comparison[True]:.2f}%")




# Filtramos solo los datos de los días con anomalías
df_outliers = df[df['is_outlier'] == True]

plt.figure(figsize=(12, 6))
# Contamos crímenes por distrito solo en los días de outliers
sns.countplot(data=df_outliers, x='District', order=df_outliers['District'].value_counts().index, palette='magma')
plt.title('Distritos con mayor volumen de crímenes durante los Outliers 2025')
plt.xlabel('ID del Distrito')
plt.ylabel('Cantidad de incidentes')
plt.xticks(rotation=0)
plt.show()