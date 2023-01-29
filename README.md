# Energias-Renovables
Streamlit informativo Energías Renovables
<h1 align="center">VISION GLOBAL DE LAS ENERGÍAS RENOVABLES</h1>

<br>
<center><img src=https://twenergy.com/wp-content/uploads/2019/07/cabecera-8-1280x720.jpg></center>

### ♾️ Objetivo del proyecto

<p>Se trata de mostrar un análisis global de las energías renovables, así como el camino que aparentemente van a tomar las mismas,combinado con una pincelada de mercados de energía.</p>
Este proyecto pretende ser escalable, permitiendo integrarse a continuación de él la API actualizada de los precios de mercado. De esta forma podría crearse una posible aplicación de información en 'tiempo real', para un posible usuario (no doméstico, pues nuestro orden magnitud son TWh), o que prediga los pasos inminentes de la misma.</p>
El análisis se ha llevado a cabo tratando las variables globales por separado. El siguiente paso es indudablemente incluir el resto de datasets por tipo de energía, de los que obtendríamos datos como la capacidad por país de cada una, así como otros factores que les afectan.</p>

### Datos iniciales
#### Datasets empleados:

* modern-renewable-energy-consumption.csv
* modern-renewable-prod.csv
* renewable-share-energy.csv
* share-electricity-renewables.csv

#### Librerías necesarias:

* numpy
* pandas
* seaborn
* matplotlib.pyplot
* sklearn (preprocessing)
* plotly.express

* folium (Choropleth, HeatMap)
* geopandas
* LinearColormap

## 🔨 Funcionalidades del proyecto
### Cómo usar:
- `Funcionalidad 1`: Obtener información, seleccionar en la barra de la izquierda los datos que filtrarán la información que aparecerá en los displays de la derecha. Para observar los datos de consumo y producción energéticos internacionales desde 1965-2020, navegar por los gráficos de las pestañas que están a mitad de la página.
- `Funcionalidad 2`: Obtener informes en PDF clicar sobre botón Fortia, y escoger año
- `Funcionalidad 3`: Saber el precio actual de la energía, por tipo, y período de tiempo, clicar en el enlace del final de página, bajo las gráficas
- `Funcionalidad 4`: Escalar dicho proyecto clicar en el botón Future API y seguir desarrollando.

### Indice
1. Consumo de energía en el mundo
    1.1 Correlaciones entre energías
2. Producción de energía en el mundo
    2.1 Correlaciones entre energías
3. Consumo renovables en términos eléctricos por paises
4. Producción renovables en términos eléctricos por paises
5. Consumos y producciones de energía en métrica eléctrica
    5.1 Menores productores 
6. Proyección de futuro
    6.1 Consumo
    6.2 Producción
7. Modelización para previsión
    7.1 Métodos
        7.1.1 Mínimos cuadrados
        7.1.2 Moving average
        7.1.3 Metodo de diferenciación
    7.2. Aplicamos modelo autoregresivo
    7.3 Modelización
    7.4 Predicciones y visualización


###### Fuentes consultadas y agradecimientos; al final del notebook
####### Anexos
