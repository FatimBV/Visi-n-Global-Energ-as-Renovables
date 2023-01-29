#-------------------------Librerias necesarias-------------------------#
from asyncore import write
import numpy as np
import pandas as pd
import seaborn as sns

# From symbol import return_stmt
sns.set()
import matplotlib.pyplot as plt
import streamlit as st
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Mapas interactivos
import geopandas as gpd
from geopandas.tools import geocode
from branca.colormap import LinearColormap

# Plotly graphs
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.offline import iplot, init_notebook_mode
import plotly.io as pio
import streamlit as st

# Displays
import re
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from IPython.core.display import display, HTML
import streamlit.components.v1 as components

# Enlaces 
import webbrowser

# Modelización 
from statsmodels.tsa.arima.model import ARIMA

#---------------------------------------- Funciones ---------------------------------------------------------------#

def Display_country_filter(df):
    country_list = [''] + list(df['Entity'].unique())
    country_list.sort()
    country_name= st.sidebar.selectbox('Entity', country_list)
    return country_name

def Display_time_filters(df):
    year_list= list(df['Year'].unique())
    year_list.sort()
    year = st.sidebar.selectbox('Year',year_list,len(year_list)-1)
    return year

def Display_Total_Energy(df, year, country_name):
    
    report_type = ['Electricity from wind (TWh)','Electricity from hydro (TWh)','Electricity from solar (TWh)','Electricity from other renewables including bioenergy (TWh)']
    for i in report_type:
        accum = df.loc[(df['Entity'] == country_name) & (df['Year'] == year)][report_type].sum()
        n_tot = accum.sum()
    st.metric('Produce un total de: (TWh)',round(n_tot,2))

def Display_report_type():
    report_type = ['Electricity from wind (TWh)','Electricity from hydro (TWh)','Electricity from solar (TWh)','Electricity from other renewables including bioenergy (TWh)']
    return st.sidebar.radio('Report Type', report_type)

def Display_energy_type(df, year, country_name, report_type):
    n_type = df.loc[(df['Entity'] == country_name) & (df['Year'] == year)][report_type].sum()
    st.metric(f'De los cuales: {report_type}',n_type)

#---------------------------------------- carga de datos ----------------------------------------------------------#

st.set_option('deprecation.showPyplotGlobalUse', False)

prod = pd.read_csv('prod.csv')
prod.drop(['Unnamed: 0'],axis=1, inplace=True)

cons20_all = pd.read_csv('cons20_all.csv')
cons20_all.drop(['Unnamed: 0'],axis=1, inplace=True)

prod20_all = pd.read_csv('prod20_all.csv')
prod20_all.drop(['Unnamed: 0'],axis=1, inplace=True)

prod_of_cons20 = pd.read_csv('prod_of_cons20.csv')
prod_of_cons20.drop(['Unnamed: 0'],axis=1, inplace=True)

cons15_20 = pd.read_csv('cons15_20.csv')
cons15_20.drop(['Unnamed: 0'],axis=1, inplace=True)

map_hist = pd.read_csv('map_hist.csv')
map_hist.drop(['Unnamed: 0'],axis=1, inplace=True)
 
#-------------------------------------------- Diseño Pagina -----------------------------------------------------------------#
st.set_page_config(page_title="Energías Renovables", layout="wide", page_icon="⚡") # después establecer el título de página, su layout e icono 

st.markdown("<h1 color: white;'> Energía renovable en el mundo </h1>", unsafe_allow_html=True)
st.image('World.jpg', width=800)

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://iea.imgix.net/d5bd88a4-4394-43a2-9064-0e1ce1a17067/MicrosoftTeams-image1.png?auto=compress%2Cformat&fit=min&q=80&rect=0%2C2665%2C9486%2C6330&w=1800&h=1201&fit=crop&fm=jpg&q=70&auto=format");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url() 
#-------------------------------------------------------- Texto Sidebar ------------------------------

st.sidebar.header("Selección de Información")

#----------------------------------------------------- Tratamiento datasets --------------------------------------------#

#------------------------------------------------------------- ARIMA ----------------------------------------------
col_ser = ['Year','Total Energy TWh']
Total = prod[col_ser]
tot_ener_prod = Total.groupby('Year').sum()
p = 3 # Coeficientes de autoregresión
d = 2 # Orden de diferenciación
q = 1 # Ajuste media móvil
n = 5 # número de predicciones
series = tot_ener_prod['Total Energy TWh']
todo=series.values

for _ in range(n):
    model = ARIMA(todo, order=(p,d,q))
    model_fit = model.fit()
    preds = model_fit.predict()
    todo = np.append(todo, model_fit.forecast()[0], axis=None)
    preds = np.append(preds, model_fit.forecast()[0], axis=None)

#----------------------------------------------------------- Botones ----------------------------------------------------------

col1,col2 = st.columns(2)
with col1: 
    url = 'https://www.fortiaenergia.es/documentacion-3/'
    if(st.button("Fortia")): # vamos a los informes anuales clasificados por producción de energía
                webbrowser.open_new_tab(url)

with col2: 
    url ='https://www.ree.es/es/datos/mercados/componentes-precio-energia-cierre-desglose'
    if(st.button("Future with API")): # vamos a los informes anuales clasificados por producción de energía
                    webbrowser.open_new_tab(url)

#-------------------------------------------------------- Displays Datos -----------------------------------------------------------------------------------------------------------------------------------------------------#
year = Display_time_filters(prod)
country_name = Display_country_filter(prod)
report_type = Display_report_type()

#-------------------------------------------------------- Display metrics ----------------------------------------------#

st.subheader(f'Desglose {country_name}')
col1,col2 = st.columns(2)

with col1:        
    Display_Total_Energy(prod, year, country_name)

with col2:
    Display_energy_type(prod, year, country_name, report_type)

#---------------------------------------------- Línea separadora e imagen de Análisis ---------------------------------
with st.container():
#crea linea separadora o ("##") para crear espacios
    st.write("---") 

st.markdown("<h2 style='text-align: center; color: white;'> Análisis </h2>", unsafe_allow_html=True)
st.image('energ.jpg')
#-------------------------------------------------------- Esquema columnas --------------------------------------------------------------------#
#columnas:
tabs = st.tabs(["Consumo y Producción Mundial","Consumo y Producción eléctricos", "Tendencias", "Previsión", "Conclusiones"])
plt.style.use('dark_background')
colores = ["#2E86C1",  # Azul
           "#cb4335",  # Rojo
           "#eb984e",  # Marron
           "#979a9a"   # Gris
          ]

#col1 Consumo y Producción Mundial:
tab_plots = tabs[0]
with tab_plots:

    st.title("Tipos de Energía más consumidos")
    st.markdown("# Grafico de consumos energéticos \n ### Se ha tomado como año de referencia 2020")
    # Grafico consumos energéticos por los 20 países que más consumen
    fig=plt.figure(figsize=(8,13), dpi=200).legend(fontsize=8)
    cons20_all.iloc[0:20].plot.bar(x='Entity',xlabel='Mayores Consumidores',ylabel='Electricidad Consumida TWh', color = colores, linewidth=0.3, fontsize=10,stacked=True).grid(axis='x')
    st.pyplot(plt.gcf())
    # Grafico producción energética del top 20 
    st.title ("Tipos de energía más producidos")
    st.markdown("# Producción energética")
    fig=plt.figure(figsize=(8,13), dpi=200).legend(fontsize=8)
    prod20_all.iloc[0:20].plot.bar(x='Entity',xlabel='Mayores Productores',ylabel='Electricidad Producida TWh', color = colores, linewidth=0.3, fontsize=10).grid(axis='x')
    st.pyplot(plt.gcf())

#col2 Consumo y Producción eléctricos:
tab_plots = tabs[1]
with tab_plots:

    st.title ("Métrica electricidad de energéticas consumidas")
    st.markdown("<h3 style='text-align: left; color: white;'> Año referencia 2020 </h3>", unsafe_allow_html=True)
    fig=plt.figure(figsize=(8,13), dpi=200).legend(fontsize=8)
    prod_of_cons20.iloc[0:20].plot.bar(x='Entity',xlabel='Mayores Consumidores',ylabel='Electricidad Consumida TWh', color = colores, linewidth=0.3, fontsize=10).grid(axis='x')
    st.pyplot(plt.gcf())  
 
#col3 Tendencias:
tab_plots = tabs[2]
with tab_plots:
    
    st.title ("Tendencia de consumo")
    cons15_20.iloc[0:20].plot.bar(x='Entity', color = colores, linewidth=0.3,fontsize=8).grid(axis='x')
    st.pyplot(plt.gcf()) 

    st.title ("Progresión anual del total")
    map_hist= prod
    map_hist= map_hist.sort_values(['Year'],ascending=True)
    fig = px.scatter_geo(map_hist, locations='Code',color="Total Energy TWh",
                     hover_name="Entity", size="Total Energy TWh",
                     animation_frame="Year", projection="natural earth",
                    template='plotly_dark')
    st.plotly_chart(fig)


#col4 Evolución histórica:
tab_plots = tabs[3]
with tab_plots:
    st.title ("Tendencia de producción")
    fig, ax = plt.subplots()
    ax.plot([x+1965 for x in range(len(series))], series.values, 'b-')
    ax.plot([x+1965 for x in range(d,len(series)+n)], preds[d:], 'r--')
    plt.legend(['Serie temporal', 'Predicciones'])
    st.pyplot(plt.gcf())


#col5 Conclusiones: 
tab_plots = tabs[4]
with tab_plots:
    st.markdown("### Resumen")
    st.markdown('##### De acuerdo con los resultados de nuestro modelo predictivo, en los próximos 5 años la producción de energía eléctrica procedente de renovables crecerá. Se espera que no crezca la producción procedente de energía hidroeléctrica, ya que en su mayor parte proviene de presas y los requerimientos de estas infraestructuras dificulta su proliferación, no como en el caso de las de tipo solar o eólicas. Por otra parte, en los países que proporcionalmente más energía eléctrica producen, no aumentará dicha producción, en algunos casos por su tipo de economía y en otros por la magnitud del remanente sobrante')

#------------------------ Enlace consulta rápida --------------------------
st.markdown("#### Importe por período de tiempo y tipo de energía:")
link = 'https://aleasoft.com/es/mercados-energia/mibel-espana-precios-demanda/'   
st.markdown(link, unsafe_allow_html=True)
