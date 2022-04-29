import streamlit as st
import altair as alt
import utils
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static

def decade_dashboard(placeholder, top_names, top_names_evolution):
    if top_names.empty and top_names_evolution.empty:
        placeholder.info('No hay información disponible!')
    else:
        with placeholder.container():
            table_col, chart_col = st.columns((4,5))

            # tabla Top 5
            table_col.write('**Top 5 (masculino y femenino) de la década**')
            table_col.dataframe(top_names, height=600)

            # Grafico Uso en el tiempo
            chart_col.write('**Evolución histórica del uso de los nombres del Top 5**')

            top_names_evolution_chart = alt.Chart(
                top_names_evolution,
            ).mark_line().encode(
                x=alt.X('year', axis=alt.Axis(title='Año')),
                y=alt.Y('year_number:Q', axis=alt.Axis(title='Cantidad de usos')),
                color='name:N'
            ).properties(width=600, height=350)

            chart_col.altair_chart(top_names_evolution_chart)

def name_progress_dasboard(placeholder, name_progress):
    # graficos de la evolucion en el tiempo del nombre
    uses_data = name_progress[['year','year_number']].copy()
    uses_data.set_index('year', inplace=True)
    ranking_data = name_progress[['year','year_ranking']].copy()
    ranking_data.set_index('year', inplace=True)

    with placeholder.container():                
        st.write('**Cantidad de usos a lo largo del tiempo**')
        st.line_chart(uses_data)
        st.write('**Puesto en el ranking a lo largo del tiempo**')
        st.line_chart(ranking_data)

        # # highlights del nombre
        st.write('**Valores destacados**')
        st.dataframe(utils.get_name_highlights(name_progress))


# Mapa de calor geografico (Estados Unidos). 
# Uso de determinado nombre a lo largo del pais
def name_ranking_choropleth(name_data):
    # geoJson de Estados Unidos (limites de cada Estado)
    url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
    usa_geojson = f'{url}/us-states.json'
    
    if name_data.empty:
        st.info('No hay información disponible!')
    else:
        st.write('#')
        st.write('**Ranking de popularidad en cada Estado**')
        
        # location: usa_center
        m = folium.Map(location=[40, -95], width=800, height=500, zoom_start=4)
        custom_threshold = (name_data['ranking'].quantile((0,0.2,0.4,0.6,0.8,1))).tolist()

        folium.Choropleth(
            geo_data=usa_geojson,
            data=name_data,
            columns=["state", "ranking"],
            key_on="feature.id",
            fill_color='Blues_r',
            nan_fill_color='White',
            fill_opacity=0.7,
            line_opacity=.1,
            legend_name='Ranking',
            threshold_scale=custom_threshold
        ).add_to(m)

        # folium.LayerControl().add_to(m)
        
        folium_static(m, width=800, height=500)     
