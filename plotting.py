import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np
import random
import xarray as xr
import matplotlib.pyplot as plt
from scipy.stats import exponweib

data = pd.read_csv('wind_data_merged.csv')

df1 = data.loc[data['Turbines (Clipper)'] == "FO601"]
df1 = df1[["DateTime","WindSpeed (m/s)"]]
df1["DateTime"] = pd.to_datetime(df1["DateTime"])
# df2 = data.loc[data['Turbines (Clipper)'] == "FO601","DateTime"]

df1.plot.line(x="DateTime", y="WindSpeed (m/s)")
plt.title('Windspeed vs time')
plt.ylabel('WindSpeed (m/s)')
plt.xlabel('Time (hh:mm:yy)')
plt.show()

print(df1.head())

