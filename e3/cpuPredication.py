import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pykalman import KalmanFilter
lowess = sm.nonparametric.lowess

def to_timestamp(datetime):
    return datetime.timestamp()

cpu_data = pd.read_csv('sysinfo.csv')
cpu_data['timestamp'] = pd.to_datetime(cpu_data['timestamp']).apply(to_timestamp)
