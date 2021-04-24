import json
import pandas as pd
import googlemaps

gmaps_key = '' # scrubbed for now, TODO: secrets config

def load_tract_coords():
    tracts = list(pd.read_csv('../Allegheny_County_Census_Tracts_2016.csv')['GEOID'])
    coord_data = pd.read_csv('../2016_Gaz_tracts_national.txt', sep='\t')
    coord_data.columns = [c.strip() for c in coord_data.columns]
    data = coord_data[coord_data['GEOID'].isin(tracts)]
    data['coordinates'] = data.loc[:, 'INTPTLAT'].astype(str) + ',' + data.loc[:, 'INTPTLONG'].astype(str)
    return list(data['coordinates'])

def load_library_coords():
    libraries = pd.read_csv('../libraries.csv', header=None)
    return list(libraries[0])

def get_distances(tract_coords, library_coords):
    distances = dict()
    tract_counter = 0
    for tract in tract_coords:
        distances[tract_counter] = dict()
        library_counter = 0
        for library in library_coords:
            gmaps = googlemaps.Client(key=gmaps_key)
            dm = gmaps.distance_matrix(tract, library, mode='driving', units='imperial')
            distance = dm['rows'][0]['elements'][0]['distance']['text'].split(' ')[0]
            distances[tract_counter][library_counter] = distance
            library_counter += 1
        tract_counter += 1
    return distances

def dump_to_json(distances):
    with open('../driving_distances.json', 'w') as file:
        json.dump(distances, file)

def main():
    t_coords = load_tract_coords()[:5] # for testing
    l_coords = load_library_coords()[:5] # for testing
    distances = get_distances(t_coords, l_coords)
    dump_to_json(distances)
    print('done!')

if __name__ == '__main__':
    main()