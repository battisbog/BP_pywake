
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import numpy as np
import random
import xarray as xr
import matplotlib.pyplot as plt
from scipy.stats import exponweib
import streamlit as st

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

data = pd.read_csv('wind_data_merged.csv')
wind_speed = data['WindSpeed (m/s)']
wind_speed = wind_speed.iloc[1:36]
wind_power = data['Wind Power (W)']
wind_power = wind_power.iloc[1:36]
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

plt.figure()
aep.sum(['wt','wd']).plot()
plt.xlabel("Wind speed [m/s]")
plt.ylabel("AEP [GWh]")
plt.title('AEP vs wind speed')
plt.show()

fig = plt.figure()
aep = simulationResult.aep()
c =plt.scatter(x_coord, y_coord)
# new_point = plt.scatter(44.47376462, -99.15023877, marker='o', label="met tower") # Plot the new point in magenta
plt.colorbar( label='AEP [GWh]')
plt.title('AEP of each turbine')
plt.xlabel('Longitude [degrees]')
plt.ylabel('Latitude [degrees]')
plt.show()

st.pyplot(fig=fig)

# plt.plot(wind_speed,power)

# plt.plot(wind_rose)
import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(go.Barpolar(
    r=[0, 0, 0, 0, 0, 0, 0.003805175, 0.013318113],
    name='20-22.5 m/s',
    marker_color='#131413'
))
fig.add_trace(go.Barpolar(
    r=[0, 0, 0, 0.057077626, 0, 0.005707763, 0.064687976, 0.1065449015],
    name='17.5-20 m/s',
    marker_color='#323D32'
))
fig.add_trace(go.Barpolar(
    r=[0.003805175, 0, 0, 0.188356164, 0.020928463, 0.024733638, 0.195966514, 0.340563166],
    name='15-17.5 m/s',
    marker_color='#385238'
))
fig.add_trace(go.Barpolar(
    r=[0.019025875, 0.00761035, 0.043759513, 1.065449011, 0.060882801, 0.070395738, 0.496575342, 0.755327245],
    name='12.5-15 m/s',
    marker_color='#3F6F3F'
))
fig.add_trace(go.Barpolar(
    r=[0.053272451, 0.083713851, 1.168188737, 2.747336377, 0.226407915, 0.203576865, 1.267123288, 1.25],
    name='10-12.5 m/s',
    marker_color='#3B833B'
))
fig.add_trace(go.Barpolar(
    r=[0.363394216, 0.351978691, 3.175418569, 4.24847793, 0.637366819, 0.72108067, 1.835996956, 1.48782344],
    name='7.5-10 m/s',
    marker_color='#33A033'
))
fig.add_trace(go.Barpolar(
    r=[1.023592085, 1.175799087, 2.517123288, 3.706240487, 1.445966514, 1.084474886, 2.566590563, 1.659056317],
    name='5-7.5 m/s',
    marker_color='#23B723'
))
fig.add_trace(go.Barpolar(
    r=[0.742009132, 0.903729072, 1.504946728, 2.077625571, 1.263318113, 1.057838661, 1.411719939, 0.939878234],
    name='2.5-5 m/s',
    marker_color='#14D414'
))
fig.add_trace(go.Barpolar(
    r=[0.081811263, 0.117960426, 0.25304414,	0.374809741, 0.319634703, 0.21499239, 0.209284627, 0.106544901],
    name='< 2.5 m/s',
    marker_color='#03F903'
))

fig.update_traces(text=['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W'])
fig.update_layout(
    title='Wind Speed Distribution at Titan BP Asset',
    font_size=16,
    legend_font_size=16,
    polar_radialaxis_ticksuffix='%',
    polar_angularaxis_rotation=90,
    

)
fig.show()