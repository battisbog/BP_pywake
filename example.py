import matplotlib.pyplot as plt
import numpy as np
from py_wake.examples.data.hornsrev1 import Hornsrev1Site
from py_wake.examples.data.hornsrev1 import HornsrevV80
# from py_wake.deficit_models.floris import FLORIS
from py_wake.deficit_models.noj import NOJDeficit, NOJ
from py_wake.wind_farm_models.wind_farm_model import WindFarmModel

# Define the site (Horns Rev 1 offshore wind farm)
site = Hornsrev1Site()

# Define the wind turbine (Vestas V80)
v80 = HornsrevV80()

# Define the wind farm (single Vestas V80 turbine at origin, FLORIS wake model)
wf_model = WindFarmModel(site, [v80])

# Define the wind speeds at which to calculate power output
wind_speeds = np.arange(4, 26, 2)

# Calculate the power output at each wind speed for the single turbine
p = wf_model.power(wind_speeds)

# Plot the power output against the wind speed
plt.plot(wind_speeds, p / 1000, '-o')
plt.xlabel('Wind speed (m/s)')
plt.ylabel('Power output (kW)')
plt.show()
