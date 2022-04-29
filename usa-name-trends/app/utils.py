import numpy as np
import pandas as pd

def get_name_highlights(name_evolution):
    ''' Devuelve los valores destacados respecto a la evolución del uso de un nombre en el tiempo: 
    Cuál fue el año de su máximo uso y mejor ranking
    
    >> get_name_highlights(name_evolution)
    'El nombre John tuvo su máximo uso (29200) en el año 1945 y su mejor ubicación en el ranking (3°) en el año 1960'
    '''
    name_evolution = name_evolution.set_index('year')
    
    max_uses = name_evolution.year_number.max()
    best_rank = name_evolution.year_ranking.min()
    # idxmax() devuelve solo la primer ocurrencia
    max_uses_year = name_evolution.year_number.idxmax()
    best_rank_year = name_evolution.year_ranking.idxmin()

    # ToDo: falla en Streamlit al intentar printear Dataframe con valores 'lista'
    # max_uses_year = list(name_evolution[name_evolution.year_number == max_uses].index.values)
    # best_rank_year = list(name_evolution[name_evolution.year_ranking == best_rank].index.values)
    
    highlights = pd.DataFrame(data={
        'value': [max_uses, best_rank],
        'year': [max_uses_year, best_rank_year],  
    }, index=['max_uses', 'best_ranking'])
    
    return highlights


def to_decades(years):
    ''' Devuelve un listado de decadas (1910, 1920, ...) a partir de un listado de años recibidos
    [1911,1912,1914, 1925,...]
    
    @args:
        years: lista de años sobre los que se calculara las decadas a las que hace alusión
    
    >> to_decades([1911,1912,1914, 1925,...])
    [1910, 1920]
    '''
    # cada numero // 10 (cociente), luego multiplico *10 y me quedo con los unique
    years = np.array(years)
    decades = (years // 10) * 10
    decades = np.unique(decades)

    # convierto a int para poder utilizarlo en mains
    return [int(d) for d in decades]