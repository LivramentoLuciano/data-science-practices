import streamlit as st
import altair as alt
import utils
import pandas as pd
import numpy as np
# import plotly.graph_objects as go
# import matplotlib.pyplot as plt

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
    if name_progress.empty:
        placeholder.info('El nombre {} no se encuentra en la lista'.format(st.session_state.input_name.capitalize()))
    else:
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


# para choropleth (heatmap geografico)
USA_STATES_LOCATION_PATH = './data/statelatlong.csv'
usa_states_location = pd.read_csv(USA_STATES_LOCATION_PATH)

# Mapa de calor geografico (Estados Unidos). 
# Uso de determinado nombre a lo largo del pais
def usa_choropleth_name(name_data):
    map_container = st.container()    

    if name_data.empty:
        map_container.info('No hay información disponible!')
    else:
        map_container.write('**Cantidad de usos a lo largo del tiempo**')
        # Asignar lat y long a los datos del nombre por Estado
        usa_states_location.rename(columns={'State': 'state'}, inplace=True)
        name_data_latlong = pd.merge(name_data, usa_states_location, on='state')
        
        map_container.write(name_data_latlong)
        # map_container.map(df)



# def global_choropleth(data):
    # fig = go.Figure(data = go.Choropleth(
    #     locations=
    # ))

    # fig = go.Figure(data=go.Choropleth(
    #     locations = filtered_data['countryterritorycode'],
    #     z = np.log10(filtered_data['cases']),
    #     # text = ['Country: {}<br>Number of new cases: {} <br> Number of deaths: {} <br>'.format(filtered_data['countriesandterritories'].iloc[i],
    #     #                                                                                     filtered_data['cases'].iloc[i],
    #     #                                                                                     filtered_data['deaths'].iloc[i],) \
    #     #         for i in range(len(filtered_data['cases']))
    #     #         ],
    #     colorscale = 'Bluered_r',
    #     autocolorscale=False,
    #     reversescale=True,
    #     marker_line_color='darkgray',
    #     marker_line_width=0.5,
    #     colorbar = dict(len=0.75,
    #                     title='New Cases of Coronavirus',
    #                     tickprefix='1.e',
    #                     ticktext=[str(x) for x in np.linspace(np.min(filtered_data['cases']), 
    #                                             np.max(filtered_data['cases']),
    #                                         num=10)])
    #     # colorbar_title = 'New Cases of Coronavirus'
    # ))

    # fig.update_layout(
    #     title_text='Cases of Coronavirus Globally',
    #     autosize=False,
    #     geo=dict(
    #         showframe=False,
    #         showcoastlines=False,
    #         projection_type='equirectangular'
    #     ),
    #     annotations = [dict(
    #         x=0.55,
    #         y=0.1,
    #         xref='paper',
    #         yref='paper',
    #         text='Source: <a href="https://opendata.ecdc.europa.eu/covid19/casedistribution/csv">\
    #             European Centre for Disease Prevention and Control</a>',
    #         showarrow = False
    #     )],
    #     margin = dict(l=10,r=50, b=40, t=40, pad=4),
    #     width=800,
    #     height=600,
    # )

    # st.pyplot(fig)