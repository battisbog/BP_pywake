
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
from py_wake.site._site import UniformSite
from py_wake.site.xrsite import XRSite
from py_wake import BastankhahGaussian
from py_wake.examples.data.hornsrev1 import Hornsrev1Site
from py_wake.wind_turbines import WindTurbine
from py_wake.site import UniformSite




data = pd.read_csv('wind_data_merged.csv')
wind_speed = data['WindSpeed (m/s)']
wind_speed = wind_speed.iloc[1:36]
wind_power = data['Wind Power (W)']
wind_power = wind_power.iloc[1:36]
df2 = data.groupby('Turbines (Clipper)').apply(lambda x: x['WindSpeed (m/s)'].unique())
df3 = data.groupby('Turbines (Clipper)').apply(lambda x: x['Wind Power (W)'].unique())

FO601_ws = df2['FO601']
FO601_pw = df3['FO601']

ct = [.65]*len(FO601_ws)
# Define the site (Horns Rev 1 offshore wind farm)
# site = XRSite(ws)
windspeeds = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
# site = UniformSite([0, 0], windspeeds)


# Define the wind turbines (Vestas V80)
clipper = WindTurbine(name='clipper',
                    diameter=96,
                    hub_height=80,
                    powerCtFunction=PowerCtTabular(FO601_ws,FO601_pw,'kW',ct))

# Define the wind farm site (Horns Rev 1 offshore wind farm)
site = UniformSite([0, 0], FO601_ws.mean())

# Define the wind farm model using the Bastankhah-Gaussian wake model
wf_model = BastankhahGaussian(site, clipper)

# p = wf_model()
# Compute the power output of the turbine for a given wind direction and speed
simulationResult = wf_model([0,1,2,3,4,5,6,7,8,9], [0,1,2,3,4,5,6,7,8,9],[80]*10, wd=270, ws=FO601_ws)

print(simulationResult)

plt.figure()
aep = simulationResult.aep()
aep.sum(['wt','wd']).plot()
plt.xlabel("Wind speed [m/s]")
plt.ylabel("AEP [GWh]")
plt.title('AEP vs wind speed')
plt.show()
