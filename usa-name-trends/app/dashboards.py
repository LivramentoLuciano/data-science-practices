import streamlit as st
import altair as alt
import utils
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import urllib, json

def get_uses_chart(name_progress):
    ''' Altair chart de evolución del uso de un nombre a lo largo del tiempo.
    Incluye anotaciones interactivas.
    '''
    max_uses, max_uses_year = utils.get_name_highlights(name_progress).loc['max_uses']
    highlight = [(max_uses_year, f"Máximo Uso: {max_uses}, año {max_uses_year}")]

    uses_chart = get_base_time_chart(
        name_progress,
        y_column='year_number',
        y_label='Cantidad de Usos',
        y_tooltip_label='Uso',
        highlight=highlight
    )
    return uses_chart    

def get_ranking_chart(name_progress):
    ''' Altair chart de evolución del ranking de un nombre a lo largo del tiempo.
    Incluye anotaciones interactivas.
    '''    
    best_ranking, best_ranking_year = utils.get_name_highlights(name_progress).loc['best_ranking']
    highlight = [(best_ranking_year, f"Mejor Ranking: {best_ranking}, año {best_ranking_year}")]

    ranking_chart = get_base_time_chart(
        name_progress,
        y_column='year_ranking',
        y_label='Puesto en el Ranking',
        y_tooltip_label='Ranking',
        highlight=highlight
    )
    return ranking_chart

# Chart (altair) temporal basico. Interactivo, con anotaciones.
def get_base_time_chart(data, y_column, y_label,y_tooltip_label, highlight):
    hover = alt.selection_single(
        fields=["year"],
        nearest=True,
        on="mouseover",
        empty="none",
    )   

    line = alt.Chart(data).mark_line().encode(
        x=alt.X('year', axis=alt.Axis(title='Año')),
        y=alt.Y(f'{y_column}:Q', axis=alt.Axis(title=y_label)),
    )     

    points = line.transform_filter(hover).mark_circle(size=65)

    tooltips = alt.Chart(data).mark_rule().encode(
        x="year",
        y=y_column,
        opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
        tooltip=[
            alt.Tooltip("year", title="Año"),
            alt.Tooltip(y_column, title=y_tooltip_label),
        ],
    ).add_selection(hover)

    annotations_df = pd.DataFrame(highlight, columns=["year", "Destacado"])
    annotations_df["y"] = 0

    annotation_layer = alt.Chart(annotations_df).mark_text(
        size=20, text="⬇", dx=-6, dy=-10, align="left"
    ).encode(
        x="year",
        y=alt.Y("y:Q"),
        tooltip=["Destacado"],
    ).interactive()

    return (line + points + tooltips + annotation_layer).interactive()

def name_progress_charts(name_progress):
    ''' Container con graficos de la evolución del uso de un nombre 
    (uso y ranking) a lo largo del tiempo. Incluye anotaciones interactivas.
    '''
    charts_container = st.container()
    with charts_container: 
        uses, ranking = st.columns(2)                       
        with uses:
            st.write('**Cantidad de usos a lo largo del tiempo**')
            uses_chart = get_uses_chart(name_progress)
            st.altair_chart(uses_chart, use_container_width=True)
            
        with ranking:
            st.write('**Puesto en el ranking a lo largo del tiempo**')
            ranking_chart = get_ranking_chart(name_progress)
            st.altair_chart(ranking_chart, use_container_width=True)            

    return charts_container

def name_ranking_choropleth(name_data):
    ''' Choropleth (mapa de calor geográfico) representando la popularidad (ranking)
    de un nombre a lo largo del territorio de los Estados Unidos.

    Devuelve un st.container() con titulo + choropleth, o mensaje de 'Info no disponible'
    '''    
    # geoJson de Estados Unidos (geometria de cada Estado)
    url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
    geojson_url = f'{url}/us-states.json'

    # para tooltips necesito el geoJson (no su url)
    geojson_url_op = urllib.request.urlopen(geojson_url)
    geojson = json.loads(geojson_url_op.read().decode())    
    
    map_container = st.container()

    with map_container:
        st.write('**Ranking de popularidad en cada Estado (actualidad)**')
        
        if name_data.empty:
            st.info('No hay información disponible sobre el uso de este nombre en este año!')
        else:
            # Mapa basico (location: centro de USA)
            m = folium.Map(location=[40, -95], width=800, height=500, zoom_start=4)

            # Agrego Choropleth (heatmap en funcion del ranking)
            custom_threshold = (name_data['ranking'].quantile((0,0.2,0.4,0.6,0.8,1))).tolist()
            folium.Choropleth(
                geo_data=geojson_url,
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

            # Agrego tooltips (Nombre Estado y Ranking, al pasar el mouse)
            # geojson + los datos de mi interes (ranking, usos)
            geojson_with_data = utils.add_name_data_to_geojson(geojson, name_data)
            folium.features.GeoJson(
                data=geojson_with_data,
                smooth_factor=2,
                style_function=lambda x: {'color':'grey','fillColor':'transparent','weight':0.1},
                tooltip=folium.features.GeoJsonTooltip(
                    fields=['name','ranking'],
                    aliases=['Estado:','Ranking:'], 
                    localize=True,
                    sticky=False,
                    labels=True,
                    style="""
                        background-color: #F0EFEF;
                        border: 1px solid grey;
                        border-radius: 3px;
                        box-shadow: 3px;
                    """,
                    max_width=200,
                ),
                highlight_function=lambda x: {'weight':1,'fillColor':'grey'},
            ).add_to(m)

            folium_static(m, width=800, height=500)  

    return map_container  

def name_dashboard(name_progress, name_by_state, placeholder):
    '''Container del Dashboard de una Búsqueda por Nombre
    Posee un gráfico de evolución del uso del nombre (uso y ranking) 
    y un choropleth de su uso a lo largo del territorio de USA
    '''
    with placeholder.container():
        st.write('#### Resultados:')
        name_progress_charts(name_progress)  
        name_ranking_choropleth(name_by_state)

def decade_dashboard(top_names, top_names_evolution, placeholder):
    '''Container del Dashboard de una Búsqueda por Década
    Posee una tabla con el Top 5 histórico de nombres (masculinos y femeninos)
    y un gráfico de evolución del uso de estos nombre
    '''
    with placeholder.container():
        if top_names.empty and top_names_evolution.empty:
            st.write('#### Resultados:')
            st.info('No hay información disponible!')
        else:
            st.write('#### Resultados:')
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