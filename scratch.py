import matplotlib.pyplot as plt
import numpy as np
from py_wake.examples.data.hornsrev1 import Hornsrev1Site
from py_wake.examples.data.hornsrev1 import HornsrevV80
from py_wake import NOJ
from py_wake.wind_farm_models.wind_farm_model import WindFarmModel

# Define the site (Horns Rev 1 offshore wind farm)
site = Hornsrev1Site()

# Define the wind turbines (Vestas V80)
turbines = HornsrevV80()

# Define the wind farm (multiple Vestas V80 turbines distributed on the site, NOJ wake model)
wind_turbines = turbines.create_layout(site, 3, 3)
wf_model = WindFarmModel(site, wind_turbines, NOJ())

# Define the wind speeds at which to calculate power output
wind_speeds = np.arange(4, 26, 2)

# Calculate the power output at each wind speed for the wind farm
p = wf_model.power(wind_speeds)

# Plot the power output against the wind speed
plt.plot(wind_speeds, p / 1000, '-o')
plt.xlabel('Wind speed (m/s)')
plt.ylabel('Power output (kW)')
plt.show()
