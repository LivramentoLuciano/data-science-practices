import streamlit as st
import pandas as pd
import queries
import dashboards

st.set_page_config(layout='wide')

# estado para grafico de search_by_name
if 'input_name' not in st.session_state:
    st.session_state.input_name = ''

# cargo los top de la decada y su evolucion en el tiempo
def load_data_decade_top(decade):
    decade_top_names = queries.get_top_names_decade(decade)
    decade_top_names_evolution = queries.get_top_names_decade_evolution(decade)
    return (decade_top_names, decade_top_names_evolution)

# presiona 'Buscar', solo actualiza el state.input_name
def handle_search_name(name):
    st.session_state.input_name = name

def load_data_name_evolution(name):
    return queries.get_selected_name_evolution(name)

def load_data_name_by_state(name):
    return queries.get_name_use_by_state(name)

def show_dashboard_name(name_progress, name_by_state, placeholder):
    dashboards.name_dashboard(name_progress, name_by_state, placeholder)

def show_dashboard_decade(top_names, top_names_evolution, placeholder):
    dashboards.decade_dashboard(top_names, top_names_evolution, placeholder)

st.header("Tendencias de Nombres en Estados Unidos 1910-2020")

page = st.sidebar.selectbox(
    'Seleccionar buscador:',
    ['Por década', 'Por nombre']
)

if page == 'Por década':
    # Buscador por decada
    st.subheader('Buscador por década')
    st.write('Este permite encontrar los 5 **nombres** femeninos y masculinos **más utilizados en la década indicada**, \
        y su evolución a lo largo del tiempo.')

    decade = st.selectbox(
        'Seleccione una década',
        queries.get_data_decades()
    )

    # contenedor de datos y msjs info
    dash_placeholder = st.info('Buscando...')    

    # Cargo data (decada seleccionada)
    top_names, top_names_evolution = load_data_decade_top(decade)

    # Muestro dashboard: Tabla top names + Grafico de su uso en el tiempo
    show_dashboard_decade(top_names, top_names_evolution, dash_placeholder)

else:
    # Buscador por Nombre
    st.subheader('Buscador por nombre')
    st.write(' Este nos permite ingresar un nombre y conocer la evolución de su uso a lo largo del tiempo,\
         además del ranking ocupado en comparación con el resto de los nombres.')

    # text-input
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
      
    
    # si no esta vacio el input
    if st.session_state.input_name:
        # Cargo data (evolucion en el tiempo del nombre buscado)
        dash_placeholder = st.info('Buscando...')
        name_progress_data = load_data_name_evolution(st.session_state.input_name)

        # hay info disponible?
        if name_progress_data.empty:
            dash_placeholder.info('El nombre {} no se encuentra en la lista'.format(st.session_state.input_name.capitalize()))
        else:
            # Cargo data (Uso del Nombre por Estado)
            name_by_state_data = load_data_name_by_state(st.session_state.input_name)
            
            # Muestro Dashboard: Usos y Ranking, Highlights, Choropleth Ranking
            show_dashboard_name(name_progress_data, name_by_state_data, dash_placeholder)