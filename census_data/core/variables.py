import censusdata
import requests
import pandas as pd

def get_counties(state, year):
    counties = []
    geo = censusdata.geographies(censusdata.censusgeo([('state', state), ('county', '*')]), 'acs5', year)
    for key in list(geo):
        value = geo[key].params()
        county = value[1][1]
        counties.append(county)
    return counties

def get_data_by_block_group(variables, state, county_list, api_key, variable_names):
    data = []
    for county in county_list:
        url = 'https://api.census.gov/data/2019/acs/acs5?get=' + variables + '&for=block%20group:*&in=state:' + state + '%20county:' + county + '&key=' + api_key
        response = requests.get(url)
        if response.status_code == 200:
            batch = response.json()[1:]
            data.extend(batch)
        else:
            print('API connection failed')
    headers = variable_names + ["state", "county", "tract", "block_group"]
    df = pd.DataFrame(data=data, columns=headers)
    return df

def get_data_by_tract(variables, state, api_key, variable_names):
    data = []
    url = 'https://api.census.gov/data/2019/acs/acs5?get=' + variables + '&for=tract:*&in=state:' + state + '&key=' + api_key
    response = requests.get(url)
    if response.status_code == 200:
        batch = response.json()[1:]
        data.extend(batch)
    else:
        print('API connection failed')
    headers = variable_names + ["state", "county", "tract"]
    df = pd.DataFrame(data=data, columns=headers)
    return df