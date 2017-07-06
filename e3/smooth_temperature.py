import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pykalman import KalmanFilter
lowess = sm.nonparametric.lowess

def to_timestamp(datetime):
    return datetime.timestamp()

cpu_data = pd.read_csv('sysinfo.csv')
cpu_data['timestamp'] = pd.to_datetime(cpu_data['timestamp']).apply(to_timestamp)

loess_smoothed = lowess(cpu_data['temperature'].values, cpu_data['timestamp'].values, frac=0.08)

kalman_data = cpu_data[['temperature', 'cpu_percent']]
observation_stddev = 3
transition_stddev = 2

initial_state = kalman_data.iloc[0]
observation_covariance = [[observation_stddev ** 2, 0], [0, 2 ** 2]]
transition_covariance = [[transition_stddev ** 2, 0], [0, 80 ** 2]]
transition_matrices = transition_matrices = [[1, 0], [0, 1]]

kf = KalmanFilter(
    initial_state_mean = initial_state,
    observation_covariance = observation_covariance,
    initial_state_covariance = observation_covariance,
    transition_matrices = transition_matrices,
    transition_covariance = transition_covariance)

kalman_smoothed, _ = kf.smooth(kalman_data)
plt.figure(figsize=(12, 4))
plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5)
plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-')
plt.plot(cpu_data['timestamp'], kalman_smoothed[:, 0], 'g-')
# plt.show()
plt.savefig('cpu.svg')
