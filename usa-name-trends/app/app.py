import streamlit as st
import pandas as pd
import queries
import dashboards

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

    # Dashboard: Tabla nombres top y Grafico evolucion en el tiempo
    dashboards.decade_dashboard(dash_placeholder, top_names, top_names_evolution)

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
    charts_placeholder = st.empty()    
    
    # si no esta vacio el input
    if st.session_state.input_name:
        charts_placeholder.info('Buscando...')
        name_progress = queries.get_selected_name_evolution(st.session_state.input_name)

        # Dashboard: Graficos Uso y Ranking en el tiempo + Highlights
        dashboards.name_progress_dasboard(charts_placeholder, name_progress)
