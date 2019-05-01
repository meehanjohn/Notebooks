
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize


# Define a sigmoid function to fit the temperature data to
def fit_func(x, a, b, c, d):
    # a: vertical offset
    # b: max value
    # c: growth factor
    # d: s-curve mid-point
    return (a+b/(1+np.exp(-c*(x-d))))

# define rolling average window size
rolling_window = 25
    
# load city data into dataframe
city_data = pd.read_csv('city_data.csv')

# add rolling average dataframe with the pre-defined window size
city_data['rolling_avg'] = city_data['avg_temp'].rolling(window=rolling_window).mean()

# drop rows with empty values
city_data = city_data.dropna()

# define local temperature input/output datasets
x1 = city_data['year'].values
y1 = city_data['rolling_avg'].values

# load global data into dataframe
global_data = pd.read_csv('global_data.csv')

# add rolling average dataframe with the pre-defined window size
global_data['rolling_avg'] = global_data['avg_temp'].rolling(window=rolling_window).mean()

# drop rows with empty values
global_data = global_data.dropna()

# define global temperature input/ouput datasets
x2 = global_data['year'].values
y2 = global_data['rolling_avg'].values

# fit local and global datasets to sigmoid curve with set of beginning guesses as defined
popt1, pcov1 = optimize.curve_fit(fit_func, x1, y1, p0=[5,10,0.001,1800])
popt2, pcov2 = optimize.curve_fit(fit_func, x2, y2, p0=[5,10,0.001,1800])

# inner join the datasets where yearly temperature data is available for both
result = pd.merge(city_data, global_data, how='inner', on='year', suffixes=('_local','_global'))
# determine correlation coefficent of merged dataset
corr_coef = np.corrcoef(result['rolling_avg_local'].values, result['rolling_avg_global'].values, rowvar=False)

plt.figure(figsize=(20,10))

# plot local raw data in blue
plt.plot(x1, y1, 'b-',label="Philadelphia")
# plot fit data in cyan; extend projection into future
plt.plot(range(x1[0],2100,1), fit_func(range(x1[0],2100,1), *popt1), 'c--',label="Phila. Sigmoid Fit")

# plot global raw data in red
plt.plot(x2, y2, 'r-',label="Global")
# plot fit data in yellow; extend projection into future
plt.plot(range(x2[0],2100,1), fit_func(range(x2[0],2100,1), *popt2), 'y--',label="Global Sigmoid Fit")
plt.legend(fontsize=12)

plt.ylabel('Temp. (Celsius)')
plt.xlabel('Year')

plt.suptitle('Temperature by Year (Rolling Average, Window = {} years)'.format(rolling_window),fontsize=24)
plt.show