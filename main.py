import matplotlib.pyplot as plt
import numpy as np
from py_wake.examples.data.hornsrev1 import Hornsrev1Site
from py_wake.examples.data.hornsrev1 import HornsrevV80
from py_wake import NOJ
from py_wake.wind_farm_models.wind_farm_model import WindFarmModel

# Define the site (Horns Rev 1 offshore wind farm)
site = Hornsrev1Site()

# Define the wind turbines (Vestas V80)
clipper = WindTurbine(name='clipper',
                    diameter=96,
                    hub_height=80,
                    powerCtFunction=PowerCtTabular(FO601_ws,FO601_pw,'kW',ct))
