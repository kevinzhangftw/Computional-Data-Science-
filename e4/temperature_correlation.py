import pandas as pd
import sys
import gzip
from math import radians, cos, sin, asin, sqrt
import matplotlib.pyplot as plt
import numpy as np

# adapted from stackoverflow https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def distanceEachPt(LatLon1, LatLon2):
    lat1 = LatLon1[0]
    lon1 = LatLon1[1]
    lat2 = LatLon2[0]
    lon2 = LatLon2[1]
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def distance(city, stations):
    LatLon1 = city.values
    s = stations.values
    oneCity = np.apply_along_axis(distanceEachPt, 1, s, LatLon1)
    return oneCity
    
def best_tmax(city, stns):
    aCity = distance(city, stns)
    bestindex = np.argmin(aCity)
    best = stations['avg_tmax/10'].iloc[bestindex]
    return best

stations_filename = sys.argv[1]
station_fh = gzip.open(stations_filename, 'rt', encoding='utf-8')
stations = pd.read_json(station_fh, lines=True)
stations['avg_tmax/10']=stations['avg_tmax']/10
stnLoc= pd.DataFrame()
stnLoc['lat'] = stations['latitude']
stnLoc['lon'] = stations['longitude']

city_data = pd.read_csv('city_data.csv')
city_data['area/km']=(city_data['area']/1000000).round(2)
city_data['density']=city_data['population']/city_data['area/km']
cityNnull = city_data[city_data.density.notnull()].reset_index()
cityLoc = pd.DataFrame()
cityLoc['lat'] = cityNnull['latitude']
cityLoc['lon'] = cityNnull['longitude']

# acity = distance(cityLoc.iloc[0], stnLoc)
# best_tmax(cityLoc.iloc[3], stnLoc)

cityTmax = cityLoc.apply(best_tmax, stns=stnLoc, axis=1)

plt.plot(cityTmax, cityNnull['density'], 'b.', alpha=0.5)
plt.title('Temperature vs Population Density')
plt.xlabel('Avg Max Temperature (\u00b0C)')
plt.ylabel('Population Density (people/km\u00b2)')

# plt.show()
plt.savefig(sys.argv[3])
