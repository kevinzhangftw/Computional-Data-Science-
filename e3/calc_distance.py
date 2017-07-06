from xml.dom.minidom import parse, parseString
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
import sys
from pykalman import KalmanFilter

def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)

    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)

    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)

    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')

# adapted from stackoverflow https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def distanceEachPt(lat1, lon1, lat2, lon2):
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def distance(data):
    df = pd.DataFrame()
    df['lat1']= data['lat']
    df['lon1']= data['lon']
    df['lat2']= df['lat1'].shift(1)
    df['lon2']= df['lon1'].shift(1)
    # df['lat2'].iloc[-1]= df['lat2'].iloc[-2]
    # df['lon2'].iloc[-1]= df['lon2'].iloc[-2]
    df['distance']=df.apply(lambda x: distanceEachPt(x['lat1'],x['lon1'],x['lat2'],x['lon2']), axis=1)
    return df['distance'].sum() * 1000

def get_data(data):
    gpx = open(data)
    dom = parse(gpx)
    trkpts = dom.getElementsByTagName("trkpt")
    lat = []
    lon = []
    for i in range(len(trkpts)):
        lat.append(trkpts[i].getAttribute("lat"))
        lon.append(trkpts[i].getAttribute("lon"))

    ddata= {'lat':lat, 'lon':lon}
    df =pd.DataFrame(data=ddata)
    df['lat']= pd.to_numeric(df['lat'])
    df['lon']= pd.to_numeric(df['lon'])
    # print(df)
    return df

def smooth(points):
    # print('points dataframe in smooth, %v', points.iloc[0])
    observation_stddev = 20e-5
    observation_covariance = [[observation_stddev ** 2, 0], [0, observation_stddev ** 2]]
    transition_stddev = 5.5e-5
    transition_covariance = [[transition_stddev ** 2, 0], [0, transition_stddev ** 2]]
    transition_matrices = [[1, 0], [0, 1]]
    initial_state = points.iloc[0]
    kf = KalmanFilter(
        initial_state_mean = initial_state,
        observation_covariance = observation_covariance,
        transition_matrices = transition_matrices,
        transition_covariance = transition_covariance)
    kalman_smoothed, _ = kf.smooth(points)
    kfs = pd.DataFrame(data=kalman_smoothed)
    kfs.columns = ['lat', 'lon']
    return kfs


def main():
    points = get_data(sys.argv[1])
    # print('points dataframe after get data, %v', points)
    print('Unfiltered distance: %0.2f' % (distance(points),))
    # print('points dataframe after distance, %v', points.iloc[0])
    # smooth(points)
    smoothed_points = smooth(points)
    # print('smoothed_points: %v', smoothed_points)
    print('Filtered distance: %0.2f' % (distance(smoothed_points),  ))
    output_gpx(smoothed_points, 'out.gpx')


if __name__ == '__main__':
    main()
