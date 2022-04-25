import streamlit as st
import pandas as pd
import altair as alt
import queries
import utils

st.set_page_config(layout='wide')

# estado para grafico de search_by_name
if 'input_name' not in st.session_state:
    st.session_state.input_name = ''

# cargo los top de la decada y su evolucion en el tiempo
def get_decade_top_data(decade):
    decade_top_names = queries.get_top_names_decade(decade)
    decade_top_names_evolution = queries.get_top_names_decade_evolution(decade)
    return (decade_top_names, decade_top_names_evolution)

# presiona 'Buscar', solo actualiza el state.input_name
def handle_search_name(name):
    st.session_state.input_name = name


st.header("Tendencias de Nombres en Estados Unidos 1910-2020")

page = st.sidebar.selectbox(
    'Seleccionar buscador:',
    ['Por década', 'Por nombre']
)

if page == 'Por década':
    # Buscador por decada
    st.write('''
    ### Buscador por década
    Este permite encontrar los 5 **nombres** femeninos y masculinos **más utilizados en la década indicada**, y su evolución a lo largo del tiempo.
    ''')

    decade = st.selectbox(
        'Seleccione una década',
        queries.get_data_decades()
    )
    
    # contenedor de datos y msjs info
    dash_placeholder = st.empty()

    # load data, decada seleccionada
    dash_placeholder.info('Buscando...')
    top_names, top_names_evolution = get_decade_top_data(decade)

    if top_names.empty and top_names_evolution.empty:
        dash_placeholder.info('No hay información disponible!')
    else:
        with dash_placeholder.container():
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

else:
    # Buscador por Nombre
    st.write('''
    ### Buscador por nombre
    Este nos permite ingresar un nombre y conocer la evolución de su uso a lo largo del tiempo, además del ranking ocupado en comparación con el resto de los nombres.
    ''')

    input_name_col, btn_search = st.columns((7,1))
    input_name = input_name_col.text_input(
        'Nombre',
        placeholder='Ingrese un nombre',
        key='input_name',
    )
    btn_search.write('#')
    btn_search.button(
        'Buscar',
        on_click=handle_search_name,
        args=(input_name,),
        disabled=(not input_name)
    )
    
    # Streamlit se redispara en cada cambio en un widget (input, btn)
    # entonces queda medio event oriented, no necesito tanto el event_handler
    # Solo utilizo los on_change para actualizar el state.input_name
    # la carga de los datos en funcion de ese valor, la hago aca directamente

    # contendra los mapas o los mensajes de info
    # 'El nombre no existe', 'Buscando...', etc
    charts_placeholder = st.empty()    
    
    # si no esta vacio el input
    if st.session_state.input_name:
        charts_placeholder.info('Buscando...')
        name_progress = queries.get_selected_name_evolution(st.session_state.input_name)

        if name_progress.empty:
            charts_placeholder.info('El nombre {} no se encuentra en la lista'.format(st.session_state.input_name.capitalize()))
        else:
            # graficos de la evolucion en el tiempo del nombre
            uses_data = name_progress[['year','year_number']].copy()
            uses_data.set_index('year', inplace=True)
            ranking_data = name_progress[['year','year_ranking']].copy()
            ranking_data.set_index('year', inplace=True)

            with charts_placeholder.container():                
                st.write('**Cantidad de usos a lo largo del tiempo**')
                st.line_chart(uses_data)
                st.write('**Puesto en el ranking a lo largo del tiempo**')
                st.line_chart(ranking_data)

                # # highlights del nombre
                st.write('**Valores destacados**')
                st.dataframe(utils.get_name_highlights(name_progress))
