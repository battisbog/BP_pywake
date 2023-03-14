import pandas as pd
import numpy as np
import xarray as xr
import py_wake
import py_wake.examples.data as wd
import matplotlib.pyplot as plt
from py_wake.wind_turbines import WindTurbine
from py_wake.wind_turbines.power_ct_functions import PowerCtTabular

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



# Define the turbine and wind farm specifications
# Define the wind turbines (Vestas V80)
turbine = WindTurbine(name='clipper',
                    diameter=96,
                    hub_height=80,
                    powerCtFunction=PowerCtTabular(FO601_ws,FO601_pw,'kW',ct))
wind_farm = wd.WindFarmFromDict({'type': 'WindFarm', 'windTurbines': {turbine.name: turbine.to_dict()}})
# Create a wind farm model
model = py_wake.GaussianWindFarmModel(windTurbines=[turbine], windFarmModel=wind_farm)

# Define the wind direction and speed conditions
wind_dir = 270
wind_speed = 8

# Run the simulation
sim_res = model([0, 0], wd.uniform([0, 0], [1000, 0], [1000, 1000], [0, 1000]), wd.uniform([wind_speed], [wind_dir]))

# Visualize the results
fig, ax = plt.subplots()
sim_res.flow_map(wd.site_x(site_y=0), ax=ax)
ax.set_title('Wind Farm Simulation')
plt.show()
