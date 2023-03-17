
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
from py_wake.wind_turbines import WindTurbine
from py_wake.site._site import UniformWeibullSite
from py_wake.wind_turbines.power_ct_functions import PowerCtTabular
from py_wake.site._site import UniformSite
from py_wake.site.xrsite import XRSite
from py_wake import BastankhahGaussian
from py_wake.examples.data.hornsrev1 import Hornsrev1Site
from py_wake.wind_turbines import WindTurbine
from py_wake.site import UniformSite
from py_wake.examples.data.hornsrev1 import Hornsrev1Site, V80, wt_x, wt_y, wt16_x, wt16_y





data = pd.read_csv('wind_data_merged.csv')
df2 = data.groupby('Turbines (Clipper)').apply(lambda x: x['WindSpeed (m/s)'].unique())
df3 = data.groupby('Turbines (Clipper)').apply(lambda x: x['Wind Power (W)'].unique())
df4 = data.groupby('Turbines (Clipper)').apply(lambda x: x['Wind Direction'].unique())


FO601_ws = df2['FO601']
FO601_pw = df3['FO601']
# FO601_wd = [270]*len(FO601_ws)
FO601_wd = df4['FO601']


ct = [.65]*len(FO601_ws)

# Test data:
xcoords = [0,1,2,3,4,5,6,7,8,9]
ycoords = [0,1,2,3,4,5,6,7,8,9]
wind_speed = [6.757998033, 6.695190991, 6.849339685,6.623479287,6.461867368,6.819221548,5.725604083,6.830237155,7.820850293,6.163569947,7.27172156]
wind_direction = [270]*len(wind_speed)

# Define the wind turbines (Vestas V80)
clipper = WindTurbine(name='clipper',
                    diameter=96,
                    hub_height=80,
                    powerCtFunction=PowerCtTabular(FO601_ws,FO601_pw,'kW',ct))

windTurbines = clipper

# Define the wind farm site (Horns Rev 1 offshore wind farm)
# site = UniformSite([0, 0], FO601_ws.mean())
# site = UniformSite()
site = Hornsrev1Site()

# Define the wind farm model using the Bastankhah-Gaussian wake model
wf_model = BastankhahGaussian(site, windTurbines)

# p = wf_model()
# Compute the power output of the turbine for a given wind direction and speed
# simulationResult = wf_model(xcoords, ycoords,[80]*10, wd=wind_direction, ws=wind_speed)
simulationResult = wf_model(xcoords, ycoords, ws=FO601_ws)

aep = simulationResult.aep()

print(simulationResult)
print(aep)

plt.figure()
aep.sum(['wt','wd']).plot()
plt.xlabel("Wind speed [m/s]")
plt.ylabel("AEP [GWh]")
plt.title('AEP vs wind speed')
plt.show()

