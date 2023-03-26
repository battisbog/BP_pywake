
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np
import random
import xarray as xr
import matplotlib.pyplot as plt
from scipy.stats import exponweib

# pywake packages
from py_wake.wind_farm_models.engineering_models import PropagateDownwind
from py_wake.deficit_models import TurboNOJDeficit
from py_wake.rotor_avg_models import RotorCenter
from py_wake.superposition_models import LinearSum
from py_wake.turbulence_models import CrespoHernandez
from py_wake.deflection_models.jimenez import JimenezWakeDeflection
from py_wake.wind_turbines import WindTurbine
from py_wake.site._site import UniformWeibullSite
from py_wake.wind_turbines.power_ct_functions import PowerCtTabular
from py_wake.examples.data.hornsrev1 import Hornsrev1Site, V80, wt_x, wt_y, wt16_x, wt16_y
from py_wake import NOJ
from py_wake.wind_turbines.generic_wind_turbines import GenericWindTurbine

## create a wtg class which is an instance of a pywake wind turinbe item setting turbine hub height, rotor diameter, neame, and power curve function

# clipper = GenericWindTurbine("clipper", 96,80, power_norm=10000, turbulence_intensity=.1)

data = pd.read_csv('titan_data.csv')
wind_speed = data['WS']
# wind_speed = wind_speed.iloc[1:36]
wind_power = data['Power']
# wind_power = wind_power.iloc[1:36]
ct = [.65]*len(wind_speed)

x_coord = [-99.163365,
-99.159478,
-99.148998,
-99.144288,
-99.139698,
-99.133815,
-99.128011,
-99.122527,
-99.11286,
-99.107977]

y_coord = [44.469055,
44.468935,
44.475188,
44.47658,
44.477594,
44.477952,
44.480515,
44.480035,
44.480819,
44.479672]

met_x = 44.47376462
met_y = -99.15023877

turbines = []

# ct = np.linspace()

clipper = WindTurbine(name='clipper',
                    diameter=96,
                    hub_height=80,
                    powerCtFunction=PowerCtTabular(wind_speed,wind_power,'kW',ct))

# new_site = 

# windTurbines = clipper()
site = Hornsrev1Site()
noj = NOJ(site,clipper)
simulationResult = noj(x_coord,y_coord)
aep = simulationResult.aep()
total_aep = simulationResult.aep().sum()
total_aep = total_aep.item()
# print(total_aep)
print("Total annual energy production = "+str(total_aep) + " GWh")

site_wind_speeds = site.local_wind(x=x_coord, y=y_coord).ws
ws = xr.DataArray(site_wind_speeds, dims=['ws'], name='ws')
wd = site.local_wind(x=x_coord, y=y_coord).wd

simulationResult_given_ws = noj(x_coord, y_coord, ws=ws, wd=wd)
aep_given_ws = simulationResult_given_ws.aep()

aep_given_ws_sum = aep_given_ws.sum(dim='wd').values.T

fig, ax = plt.subplots()
for i in range(len(x_coord)):
    ax.plot(site_wind_speeds, aep_given_ws_sum[i], label=f'Turbine {i+1}')

ax.set_xlabel('Wind speed [m/s]')
ax.set_ylabel('AEP [GWh]')
ax.set_title('AEP of each turbine vs wind speed')
ax.legend()
plt.show()
