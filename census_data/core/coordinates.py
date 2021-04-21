import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def get_and_print_block_groups():
    data = pd.read_csv('Allegheny_County_Census_Block_Groups_2016.csv')
    data['coordinates'] = data['INTPTLAT'].astype(str) + ', ' + data['INTPTLON'].astype(str)
    print(data['coordinates'])
    return data

def get_and_print_tracts():
    tracts = list(pd.read_csv('Allegheny_County_Census_Tracts_2016.csv')['GEOID'])
    coord_data = pd.read_csv('2016_Gaz_tracts_national.txt', sep='\t')
    coord_data.columns = [c.strip() for c in coord_data.columns]
    data = coord_data[coord_data['GEOID'].isin(tracts)]
    data['coordinates'] = data['INTPTLAT'].astype(str) + ', ' + data['INTPTLONG'].astype(str)
    print(data['coordinates'])
    return data