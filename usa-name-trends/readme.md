# Tendencias de Nombres en Estados Unidos (1910-2020)
Este proyecto se basa en la construcción de un buscador de tendencias en los nombres de personas en los Estados Unidos, desde el 1910 a la actualidad, a partir de los datos públicos disponibles en [USA Name Data](https://www.kaggle.com/datasets/datagov/usa-names?select=usa_1910_current) (*Dataset* de *BigQuery*).

El mismo se puede encontrar en: [WebApp Tendencia Nombres USA](https://share.streamlit.io/livramentoluciano/data-science-practices/main/usa-name-trends/app/app.py)

## Funcionalidad
Esta pequeña aplicación consta de 2 buscadores:
- **Buscador de nombres tendencia de cada década:** simplemente se selecciona una década e indicará los 5 nombres masculinos y femeninos más recurrentes en la misma, como así también la evolución histórica de su uso.
- **Buscador por nombre:** por medio de este se puede ingresar un nombre y el programa nos mostrará la evolución de su uso a lo largo del tiempo, tanto en cantidad como en ranking correspondiente (uso en comparación con el resto de los nombres del mismo año). Además, se presenta un mapa de calor geográfico en el cual se visualiza la popularidad del nombre en cada uno de los estados de USA, en la actualidad.

ToDo's: 
- Timelapse: gráfico dinámico con el ranking top 5 de nombres tendencia a lo largo del tiempo (que se pueda observar como cada nombre va bajando/subiendo en el ranking al pasar los años, o bien como nuevos nombres aparecen en el ranking).
- Buscar forma de presentar al usuario sugerencias sobre el por qué un nombre fue tendencia en cierta época (ejemplo, Diana -> Lady di)

## Contenido adicional. Estructura.
Además de la pequeña aplicación interactiva, este proyecto cuenta con un análisis completo de los datos en cuestión. Para una mejor comprensión de este análisis, se dividió al mismo en 2 archivos:
- *demographics_analysis*
- *names_analysis*

### Demographics Analysis
En este archivo se puede encontrar un análisis demográfico exhaustivo con todo tipo de gráficos, echando luz sobre distintos aspectos de la natalidad en Estados Unidos, a lo largo de los años y de su geografía. Se pueden observar cuestiones como:
- Cantidad de nacimientos registrados desde 1910.
    - Distinción por género. Acumulado total y evolución anual.
    - Distinción por Estado. Evolución anual de cada Estado. Análisis particular de los Estados con mayor cantidad de nacimientos registrados.
    - Combinación de anteriores, observando evolución anual y por Estado de la relación hombres/mujeres nacidxs.
    
### Names Analysis
Por otra parte, en este archivo el análisis se centra en los nombres elegidos por los estadounidendes, observándose cuestiones como:
- Cantidad total de nombres utilizados en la historia. Distinción por género.
- Evolución en el tiempo de la variedad de nombres utilizados. Distinción por género.
- Nombres más utilizados en la historia y en la actualidad. 
    - Evolución a lo largo del tiempo.
    - Uso a lo largo del territorio.

## Screenshots
- Video App

https://user-images.githubusercontent.com/27143242/166303971-ceddcfde-3e60-467d-9753-9514c665f1d6.mp4

- Buscador por década

<img src="app/screenshots/year_search.png" alt="Buscador por década" width="600"/>

- Buscador por nombre

<img src="app/screenshots/name_search_a.png" alt="Buscador por nombre" width="600"/>

<img src="app/screenshots/name_search_b.png" alt="Buscador por nombre" width="600"/>


## Tecnologías aplicadas
Entre las herramientas tecnológicas utilizadas, se pueden destacar:
- SQL/BigQuery
- Python/Seaborn/GUI (Interface)
