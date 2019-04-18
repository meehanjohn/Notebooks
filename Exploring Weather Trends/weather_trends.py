
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize

def fit_func(x, a, b, c, d):
    return (a+b/(1+np.exp(-c*(x-d))))


city_data = pd.read_csv('city_data.csv')
city_data['rolling_avg'] = city_data['avg_temp'].rolling(window=15).mean()
city_data = city_data.dropna()
x1 = city_data['year'].values
y1 = city_data['rolling_avg'].values

global_data = pd.read_csv('global_data.csv')
global_data['rolling_avg'] = global_data['avg_temp'].rolling(window=15).mean()
global_data = global_data.dropna()
x2 = global_data['year'].values
y2 = global_data['rolling_avg'].values

popt1, pcov1 = optimize.curve_fit(fit_func, x1, y1, p0=[5,10,0.001,1800])
popt2, pcov2 = optimize.curve_fit(fit_func, x2, y2, p0=[5,10,0.001,1800])
print(popt1, popt2)

fig, axs = plt.subplots(2,1,figsize=(20,10))

axs[0].plot(x1, y1, 'g-')
axs[0].plot(range(x1[0],2050,1), fit_func(range(x1[0],2050,1), *popt1), 'y--')
axs[0].set_xlim(1800,2025)
axs[0].set_ylim(None,13)

axs[1].plot(x2, y2, 'g-')
axs[1].plot(range(x2[0],2050,1), fit_func(range(x2[0],2050,1), *popt2), 'y--')
axs[1].set_xlim(1800,2025)
axs[1].set_ylim(None,13)

axs[0].set_ylabel('Temp. (Celsius)')
axs[1].set_ylabel('Temp. (Celsius)')
axs[1].set_xlabel('Year')

fig.suptitle('Temperature (Rolling Average) by Year')
plt.show