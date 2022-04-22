from google.cloud import bigquery
import pandas as pd

# Dataset:  bigquery-public-data -> usa_names -> usa_1910_current
# cliente bigquery para consultar database y config cuota segura
client = bigquery.Client()
safe_config = bigquery.QueryJobConfig(maximum_bytes_billed=10**10)

def get_top_names_decade(decade):
    '''  Devuelve un DataFrame con el Top 5 (masculino y femenino) 
    de nombres mas recurrentes de la década indicada
    
    @args:
        decade: década sobre la que interesa conocer la tendencia de nombres
    
    >> get_top_names_decade(1910)
    DataFrame(name, gender, decade_number, decade_ranking)   
    '''
    
    top_names_decade_query =  '''
    SELECT name AS Nombre, 
           gender AS Genero,
           SUM(number) AS NumUsosDecada, 
           RANK() OVER (
               PARTITION BY gender
               ORDER BY SUM(number) DESC
           ) AS RankingDecada
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE year >= @decade AND year < (@decade + 10)
    GROUP BY name, gender
    ORDER BY RankingDecada ASC
    LIMIT 10
    '''  
    # para pasaje de parametros variables a la query
    safe_config.query_parameters = [bigquery.ScalarQueryParameter("decade", "INT64", decade)]
    
    top_names_decade_query_job = client.query(top_names_decade_query, job_config=safe_config)
    top_names = top_names_decade_query_job.to_dataframe()
    return top_names

def get_top_names_decade_evolution(decade):
    ''' Devuelve un Dataframe con la evolucion en el tiempo 
    de los nombres más recurrentes de la década indicada.
    
    @args:
        - decade: década sobre la cual consultar los nombres más recurrentes 
          (de los cuales luego se analiza su evolcuión en toda la historia)
    
    >> get_top_names_decade_evolution(1930)
    Dataframe(year, name, gender, year_number)
    '''
    
    top_names_decade_evolution_query =  '''
    WITH top_names_decade AS (
        SELECT name, 
               gender,
               SUM(number) AS decade_number, 
               RANK() OVER (
                   PARTITION BY gender
                   ORDER BY SUM(number) DESC
               ) AS decade_ranking
        FROM `bigquery-public-data.usa_names.usa_1910_current`
        WHERE year >= @decade AND year < (@decade + 10)
        GROUP BY name, gender
        ORDER BY decade_ranking ASC
        LIMIT 10
    )

    SELECT n.year, n.name, n.gender, SUM(n.number) AS year_number    
    FROM `bigquery-public-data.usa_names.usa_1910_current` AS n
    RIGHT JOIN top_names_decade AS tnd
        ON tnd.name = n.name AND tnd.gender = n.gender
    GROUP BY n.year, n.name, n.gender
    '''  
    
    # para pasaje de parametros variables a la query
    safe_config.query_parameters = [bigquery.ScalarQueryParameter("decade", "INT64", decade)]
    
    top_names_decade_evolution_query_job = client.query(top_names_decade_evolution_query, job_config=safe_config)
    top_names_decade_evolution = top_names_decade_evolution_query_job.to_dataframe()
    
    # pivoteo data para poder graficar, porque st.line_chart no admite 'hue'
    # Ojo, no funcionarioasi hay mismo nombre con 2 generos (pero casi imposible entre los Top)
    # top_names_decade_evolution=top_names_decade_evolution.pivot('Anio', 'Nombre', 'NumUsosAnio')

    return top_names_decade_evolution 

def get_names_evolution(names):
    ''' Devuelve un Dataframe con la evolución (uso y ranking) año a año de los nombres indicados.
    
    >> get_names_evolution()
    Dataframe(year, name, year_number, year_ranking)
    '''
    names_evolution_query = '''
    WITH all_names_year_number AS (
        SELECT year, 
               name,
               SUM(number) AS year_number,
               RANK() OVER (
                   PARTITION BY year
                   ORDER BY SUM(number) DESC
              ) AS year_ranking 
        FROM `bigquery-public-data.usa_names.usa_1910_current`        
        GROUP BY year, name     
    )
    
    SELECT year, name, year_number, year_ranking
    FROM all_names_year_number
    WHERE name IN UNNEST(@names)
    GROUP BY year, name, year_number, year_ranking
    ORDER BY year, year_number DESC
    '''
   
    if isinstance(names, str): names = [names]
    
    # para pasaje de parametros variables a la query
    safe_config.query_parameters = [bigquery.ArrayQueryParameter("names", "STRING", names)]    
    
    names_evolution_query_job = client.query(names_evolution_query, job_config=safe_config)
    names_evolution = names_evolution_query_job.to_dataframe()
    return names_evolution

def get_selected_name_evolution(search_name):
    ''' Devuelve un Dataframe con la evolución (uso y ranking) año a año del nombre indicado
    
    >> get_names_evolution()
    Dataframe(year, name, year_number, year_ranking)
    (empty dataframe if 'search_name' doesn't exists in data)
    '''
    # capitalizo-> asi esta en el dataset
    search_name = search_name.capitalize()
    selected_name_evolution = get_names_evolution(search_name)
    
    return selected_name_evolution

def get_name_highlights(name_evolution):
    ''' Devuelve los valores destacados respecto a la evolución del uso de un nombre en el tiempo: 
    Cuál fue el año de su máximo uso y mejor ranking
    
    >> get_name_highlights(name_evolution)
    'El nombre John tuvo su máximo uso (29200) en el año 1945 y su mejor ubicación en el ranking (3°) en el año 1960'
    '''
    name_evolution.set_index('year', inplace=True)
    
    max_uses = name_evolution.year_number.max()
    best_rank = name_evolution.year_ranking.min()
    # idxmax() devuelve solo la primer ocurrencia
    max_uses_year = name_evolution.year_number.idxmax()
    best_rank_year = name_evolution.year_ranking.idxmin()

    # ToDo: falla en Streamlit al intentar printear Dataframe con valores 'lista'
    # max_uses_year = list(name_evolution[name_evolution.year_number == max_uses].index.values)
    # best_rank_year = list(name_evolution[name_evolution.year_ranking == best_rank].index.values)
    
    highlights = pd.DataFrame(data={
        'Valor': [max_uses, best_rank],
        'Año': [max_uses_year, best_rank_year],  
    }, index=['Máximo uso', 'Mejor ranking'])
    
    return highlights


# ToDo: resolver to_decades()
# Por ahora, harcodeo
def get_data_decades():
    ''' Devuelve los años sobre los que hay información disponible en el Dataset USA_Names.
    En particular, en forma de "décadas".
    
    @args:
    
    >> get_data_decades()
    [1910, 1920]
    '''
    
    years_query = '''
    SELECT year
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    GROUP BY year
    '''
    years_query_job = client.query(years_query, job_config=safe_config)
    years = years_query_job.to_dataframe()
    
    data_decades = to_decades(years.year.to_list())
    return data_decades

def to_decades(years):
    ''' Devuelve un listado de decadas (1910, 1920, ...) a partir de un listado de años recibidos
    [1911,1912,1914, 1925,...]
    
    @args:
        years: lista de años sobre los que se calculara las decadas a las que hace alusión
    
    >> to_decades([1911,1912,1914, 1925,...])
    [1910, 1920]
    '''
    decades = [1910, 1920, 1930,1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]
    return decades