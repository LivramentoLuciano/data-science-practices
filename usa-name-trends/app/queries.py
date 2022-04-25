from google.cloud import bigquery
import utils

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
           SUM(number) AS Usos, 
           RANK() OVER (
               PARTITION BY gender
               ORDER BY SUM(number) DESC
           ) AS Ranking
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE year >= @decade AND year < (@decade + 10)
    GROUP BY name, gender
    ORDER BY Ranking ASC
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
    
    data_decades = utils.to_decades(years.year.to_list())
    return data_decades
