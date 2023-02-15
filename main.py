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
from py_wake import BastankhahGaussian




## create a wtg class which is an instance of a pywake wind turinbe item setting turbine hub height, rotor diameter, neame, and power curve function

# clipper = GenericWindTurbine("clipper", 96,80, power_norm=10000, turbulence_intensity=.1)

data = pd.read_csv('wind_data_merged.csv')
wind_speed = data['WindSpeed (m/s)']
wind_speed = wind_speed.iloc[1:36]
wind_power = data['Wind Power (W)']
wind_power = wind_power.iloc[1:36]

# wind_speed = data(index=range(0,36), columns=['WindSpeed (m/s)'])
# wind_power = data(index=range(0,36), columns=['Wind Power (W)'])

ct = [.59]*len(wind_speed)
# print(ct[0:10])

clipper = WindTurbine(name='clipper',
                    diameter=96,
                    hub_height=80,
                    powerCtFunction=PowerCtTabular(wind_speed,wind_power,'kW',ct))



# windTurbines = clipper()
site = Hornsrev1Site()
noj = NOJ(site,clipper)
simulationResult = noj(wt16_x,wt16_y)
aep = simulationResult.aep()
total_aep = simulationResult.aep().sum()
total_aep = total_aep.item()
fm = simulationResult.flow_map()
# power = power.power_xylk()

plt.figure()
fm.plot(fm.power_xylk().sum(['wd', 'ws']) * 1e-3, "Power [kW]")
plt.show()
print("works")


wf_model = BastankhahGaussian(site, clipper)
sim_res = wf_model(type=0,   # Wind turbine types
                   wd=None,  # Wind direction
                   ws=wind_speed
                    )

# print(total_aep)
# print("Total annual energy production = "+str(total_aep) + " GWh")

# power = simulationResult

# plt.figure()
# aep.sum(['wt','wd']).plot()
# plt.xlabel("Wind speed [m/s]")
# plt.ylabel("AEP [GWh]")
# plt.title('AEP vs wind speed')
# plt.show()


# plt.figure()
# aep.sum(['wt','wd']).plot()
# plt.xlabel("Wind speed [m/s]")
# plt.ylabel("AEP [GWh]")
# plt.title('AEP vs wind speed')
# plt.show()

# plt.figure()
# aep = simulationResult.aep()
# c =plt.scatter(wt16_x, wt16_y, c=aep.sum(['wd','ws']))
# plt.colorbar(c, label='AEP [GWh]')
# plt.title('AEP of each turbine')
# plt.xlabel('x [m]')
# plt.ylabel('[m]')
# plt.show()



# plt.plot(wind_speed,power)