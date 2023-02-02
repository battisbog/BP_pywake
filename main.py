import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from scipy.stats import exponweib

# pywake packages

from py_wake.wind_turbines import WindTurbine
from py_wake.wind_turbines.power_ct_functions import PowerCtFunction as powerCtFunction
from py_wake.wind_turbines.power_ct_functions import PowerCtTabular
## create a wtg class which is an instance of a pywake wind turinbe item setting turbine hub height, rotor diameter, neame, and power curve function

# (class) WindTurbine(name: Any, diameter: Any, hub_height: Any, powerCtFunction: Any, **windTurbineFunctions: Any)

data = pd.read_csv('wind_data_merged.csv')

# for i in range(100):
#     wt = WindTurbine(name="wt", diameter=96, hub_height=80, powerCtFunction=powerCtFunction)
#     plt.plot(wt.power(ws, rho=r)/1000, label=f'Air density: {r}')
# plt.ylabel('Power [kW]')
# plt.xlabel('Wind speed [m/s]')
# plt.legend()
print(data)

