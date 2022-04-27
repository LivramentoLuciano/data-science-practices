import streamlit as st
import altair as alt
import utils

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