
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
## create a wtg class which is an instance of a pywake wind turinbe item setting turbine hub height, rotor diameter, neame, and power curve function

class WTG(WindTurbine):
    def __init__(self,name,RD,HH,WS,PC,Ct):
        WindTurbine.__init__(self,
                             name=name,
                             diameter=RD,
                             hub_height=HH,
                             powerCtFunction=PowerCtTabular(WS, PC, 'kW', Ct))
        
## sets up a PyWake site - this assumes the same wind resource across the entire site - this is a simplification and a XRSite taking account of wind speed and direction variations              
class SimpleSite(UniformWeibullSite):
    def __init__(self,f,a,k,ti,X,Y):
        UniformWeibullSite.__init__(self,f,a,k,ti)
        #self.initial_position = np.array([X,Y]).T
## create a wind farm object setting the turinbe type, wind farm name and power curve info
## this could be linked to a central OneMap Feature Class
class wind_farm_site(object):
    def __init__(self):
        self.Site_Name = None
        self.X = None
        self.Y = None
        self.Lat = None
        self.Long = None
        # power curve info
        self.WS = None
        self.PC = None
        self.Ct = None
        self.TurbineName = None
        self.RD = None
        self.Hub_Height = None
        self.Ti = None
        self.ERA5_WindData = None
    def get_era5_WindData(self): 
       
        ## local ERA5 net CDF for 2013 only 
        dataset = "Era5 Data\\*.nc"
        ds = xr.open_mfdataset(dataset)

        df = (ds.sel(longitude=self.Long, latitude=self.Lat)).to_dataframe()
        
        df ['ws_10m']= np.sqrt((df['u10'] ** 2) + (df['v10'] ** 2))
        df ['wd_10m']=(180 + (np.degrees(np.arctan2(df['u10'], df['v10'])))) % 360
                
        df ['ws_100m']= np.sqrt((df['u100'] ** 2) + (df['v100'] ** 2))
        df ['wd_100m']=(180 + (np.degrees(np.arctan2(df['u100'], df['v100'])))) % 360

        df['power_alpha'] = np.log(df ['ws_100m'] / df ['ws_10m']) / np.log(100 / 10)
        df[f"ws_{self.Hub_Height}m"] = df ['ws_100m'] * ((self.Hub_Height / 100 ) ** df['power_alpha'])
        
        df.rename(columns={'p140209': 'air_dens', 'wd_100m': 'wd', f"ws_{self.Hub_Height}m":'ws'}, inplace=True)

        return (df[['air_dens','wd','ws']])
## define a new site
FlatRidge2 = wind_farm_site()

## set the turibine locations
FlatRidge2.X = [1426361,1422584,1423524,1421371,1420322,1420262,1421811,1419258,1428648,1427342]#,1431791,1429189,1428146,1434778,1433486,1431937,1430743,1428707,1427307,1425749,1421713,1422778,1422864,1420242,1430682,1429647,1427922,1426829,1425621,1422174,1419578,1420632,1420513,1418975,1417726,1416351,1415123,1426458,1425496,1421628,1408528,1409600,1416201,1415044,1414209,1413207,1412130,1411020,1406982,1408600,1409709,1411296,1412741,1416038,1414936,1413862,1393327,1394478,1395475,1396492,1397727]#,1398757,1400155,1401822,1402734,1405788,1404008,1401724,1403483,1404647,1412011,1413115,1378181,1379527,1380597,1382104,1383788,1385260,1393857,1393010,1394454,1395513,1397771,1399818,1400829,1402077,1393822,1395957,1375765,1379698,1380890,1381873,1383283,1384625,1385775,1387065,1385731,1386560,1388726,1397492,1399013,1396441,1400295,1401342,1399486,1400662,1401846,1397907,1399139,1400994,1402396,1403116,1404292,1414940,1403164,1404582,1407325,1408410,1409564,1410925,1412769,1412129,1411190,1410161,1405694,1404683,1405350,1407122,1405708,1406647,1407867,1410095,1411487,1412726,1413764,1417622,1413744,1415148,1417334,1416211,1418263,1412428,1417847,1416364,1337029,1338716,1339944,1340989,1342249,1343402,1344699,1346026,1347022,1348049,1350243,1351219,1352361,1353816,1355524,1356611,1357870,1344139,1346376,1347480,1348551,1349651,1352597,1359698,1360684,1349160,1350295,1351392,1352476,1353502,1354493,1355514,1356922,1358103,1333987,1335520,1336523,1339604,1340976,1342466,1344909,1346210,1347310,1348436,1349611,1350662,1354511,1355622,1356635,1357721,1362777,1361566,1357726,1359932,1358961,1356982,1357853,1360752,1359647,1371469,1370346,1369124,1368191,1367178,1364533,1362220,1373842,1372739,1371405,1369656,1365557,1364328,1363142,1362179,1375049,1369967,1371252,1376400,1376137,1375006,1374066,1372836,1370322,1369484,1368139,1367151,1365701,1381494,1381768,1376634,1375329,1373602,1372681,1370588,1368105,1367115,1365691,1364560,1363469,1391790,1390798,1389562,1388195,1387479,1385931,1392214,1390258,1388420,1387012,1385475,1384120,1383115,1374292,1373309,1372311,1371202,1384163,1383165,1380738,1379782,1378776,1377804,1371842,1372800,1377559,1376274,1374612,1373552,1371032,1369996,1369009,1368059,1367078,1339399,1340386,1341354,1342385,1343634,1344795,1345786,1346797,1347911,1349276,1358957,1360472,1365862,1364788,1363698,1362769,1361754]
FlatRidge2.Y = [1560454,1561413,1562520,1562647,1562642,1558601,1559379,1562336,1560517,1561174]#,1561376,1564162,1564159,1565095,1565456,1565695,1566331,1567628,1567749,1567464,1566150,1566544,1570413,1570200,1577904,1577745,1577298,1577236,1580684,1580450,1580699,1580195,1576241,1575103,1575060,1573192,1573019,1572976,1573328,1570538,1582543,1582909,1582006,1582348,1581515,1581146,1580963,1581048,1579745,1576268,1576321,1575833,1575783,1578053,1576757,1575734,1583358,1581475,1581949,1582731,1582747]#,1581928,1582680,1581945,1581255,1583423,1581336,1575712,1575698,1576236,1572521,1572494,1574256,1576136,1575673,1575035,1575709,1575501,1578691,1576198,1575731,1575864,1575412,1572208,1573018,1572272,1571710,1571858,1571980,1571865,1572045,1571683,1571607,1572716,1572876,1572833,1569438,1568998,1572775,1570419,1570739,1567799,1569157,1569870,1562642,1562332,1561033,1566351,1566591,1566728,1566303,1569087,1569802,1569676,1572457,1572873,1573061,1572641,1572583,1572349,1561665,1564257,1565474,1565492,1561104,1561631,1564558,1565273,1570031,1570087,1569323,1569400,1569245,1569259,1568046,1569436,1560362,1561032,1561092,1562184,1562197,1558903,1566197,1566821,1567171,1565842,1565968,1566198,1566647,1567048,1567744,1567206,1567547,1567572,1572185,1571023,1569954,1570039,1569684,1569620,1569228,1564809,1563356,1562990,1563125,1563097,1562504,1564714,1564925,1567182,1566962,1567141,1566152,1565928,1566320,1565966,1565848,1565946,1561640,1562227,1562021,1560577,1561200,1561819,1561512,1558263,1558600,1558679,1558629,1558832,1560990,1561230,1561162,1561287,1554107,1554183,1553784,1554860,1556939,1558151,1557917,1559119,1559938,1558769,1558967,1558684,1558791,1558603,1560878,1565383,1551892,1551808,1551504,1551606,1551670,1551361,1550972,1550282,1551796,1554541,1554856,1551495,1556092,1557043,1556438,1557238,1563687,1562535,1562497,1562243,1561969,1564510,1567253,1567162,1567843,1566600,1567048,1567503,1566748,1566597,1566255,1565991,1565985,1561463,1560874,1560995,1562532,1559825,1561324,1567956,1566398,1566936,1565322,1565205,1565205,1565152,1572324,1571430,1571300,1571267,1582239,1582375,1582253,1581314,1580744,1579987,1579592,1578492,1576804,1576071,1576428,1575786,1575350,1572378,1572552,1571667,1571445,1570485,1570333,1570062,1570766,1571714,1572199,1572684,1572833,1573056,1573033,1569142,1568851,1570897,1570699,1570581,1569896,1569074]


## ERA5 node - this could be taken as center of the turbine X and Ys
FlatRidge2.Lat = 37.5
FlatRidge2.Long = -98.25

# site WTG data
FlatRidge2.WS = [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,13.5,14,14.5,15,15.5,16,16.5,17,17.5,18,18.5,19,19.5,20,20.5,21,21.5,22,22.5,23,23.5,24,24.5,25,25.5,26,26.5,27,27.5,28,28.5,29,29.5,30]
FlatRidge2.PC = [0,0,0,0,0,0,13,49,99,164,243,338,449,582,737,913,1094,1273,1438,1566,1620,1620,1620,1620,1620,1620,1620,1620,1620,1620,1620,1620,1620,1620,1620,1620,1620,1620,1620,1620,1620,1620,1620,1620,1620,1620,1620,1620,1620,1458,1296,1134,972,972,972,972,972,972,972,972,972]
FlatRidge2.Ct = [0,0,0,0,0,0,0.818,0.815,0.813,0.811,0.809,0.806,0.804,0.803,0.801,0.798,0.762,0.702,0.631,0.555,0.471,0.392,0.333,0.288,0.25,0.22,0.195,0.174,0.156,0.14,0.127,0.115,0.105,0.095,0.087,0.08,0.073,0.068,0.062,0.058,0.054,0.05,0.046,0.043,0.04,0.038,0.035,0.033,0.031,0.026,0.022,0.018,0.015,0.014,0.013,0.012,0.012,0.011,0.011,0.01,0.01]
FlatRidge2.TurbineName = 'GE 100 1.65 MW'
FlatRidge2.RD = 100
FlatRidge2.Hub_Height = 80
FlatRidge2.Ti = 0.06

FlatRidge2.ERA5_WindData = FlatRidge2.get_era5_WindData()
## function to run an energy analysis on a time series approach
def Run_PyWake_TimeSeries(year,wind_farm_site):

    windTurbines = WTG(wind_farm_site.TurbineName,wind_farm_site.RD,wind_farm_site.Hub_Height,wind_farm_site.WS,wind_farm_site.PC,wind_farm_site.Ct)
    
    
    
    wind_DF = wind_farm_site.ERA5_WindData
    wind_DF = wind_DF[wind_DF.index.year == year]
    
    directions = np.array('N NNE NE ENE E ESE SE SSE S SSW SW WSW W WNW NW NNW N'.split())
    bins = np.arange(11.25, 372, 22.5)
    wind_DF['bins'] = directions[np.digitize(wind_DF['wd'], bins)]
    
    statsDF = pd.DataFrame(columns=["f","a","K"])
    for d in directions:
        ws =  (wind_DF.loc[wind_DF['bins'] == d,"ws"]).values
        f = len(ws)/wind_DF["ws"].count()
        dummy,k,dummy,A = exponweib.fit(ws, floc=0, fa=1)
        statsDF = statsDF.append(pd.DataFrame({'f':f, 'a':A, 'K': k}, index=[0]), ignore_index=True)


    site = SimpleSite(statsDF.f,statsDF.a,statsDF.K,wind_farm_site.Ti,wind_farm_site.X,wind_farm_site.Y)
    
    # # define wind farm model with no blockage 
    wfm_no_blockage = PropagateDownwind(site, 
                            windTurbines,
                            wake_deficitModel=TurboNOJDeficit(),
                            rotorAvgModel=RotorCenter(),
                            superpositionModel=LinearSum(),
                            turbulenceModel=CrespoHernandez())
    
    sim_res_time = wfm_no_blockage(wind_farm_site.X, wind_farm_site.Y, # wind turbine positions
                            wd=wind_DF["wd"], # Wind direction time series
                            ws=wind_DF["ws"], # Wind speed time series
                            time=wind_DF.index, # time stamps
                            #TI=ti, # turbulence intensity time series
                            #operating=operating # time dependent operating variable
                      )
    
    return(sim_res_time)

def Run_PyWake_WithDeflection(list_of_random_wake_deflection_angles,wind_farm_site):

    windTurbines = WTG(wind_farm_site.TurbineName,wind_farm_site.RD,wind_farm_site.Hub_Height,wind_farm_site.WS,wind_farm_site.PC,wind_farm_site.Ct)

    wind_DF = wind_farm_site.ERA5_WindData
    
    directions = np.array('N NNE NE ENE E ESE SE SSE S SSW SW WSW W WNW NW NNW N'.split())
    bins = np.arange(11.25, 372, 22.5)
    wind_DF['bins'] = directions[np.digitize(wind_DF['wd'], bins)]
    
    statsDF = pd.DataFrame(columns=["f","a","K"])
    for d in directions:
        ws =  (wind_DF.loc[wind_DF['bins'] == d,"ws"]).values
        f = len(ws)/wind_DF["ws"].count()
        dummy,k,dummy,A = exponweib.fit(ws, floc=0, fa=1)
        statsDF = statsDF.append(pd.DataFrame({'f':f, 'a':A, 'K': k}, index=[0]), ignore_index=True)


    site = SimpleSite(statsDF.f,statsDF.a,statsDF.K,wind_farm_site.Ti,wind_farm_site.X,wind_farm_site.Y)
    
    # # define wind farm model with no blockage 
    wfm_no_blockage = PropagateDownwind(site, 
                            windTurbines,
                            wake_deficitModel=TurboNOJDeficit(),
                            rotorAvgModel=RotorCenter(),
                            superpositionModel=LinearSum(),
                            turbulenceModel=CrespoHernandez(),
                            deflectionModel=JimenezWakeDeflection())

    
    
    
    
    sim_res_yaw_offset = wfm_no_blockage(
                            wind_farm_site.X, 
                            wind_farm_site.Y, # wind turbine positions
                            yaw=np.reshape(list_of_random_wake_deflection_angles,(len(wind_farm_site.X),1,1)),
                            wd=180, # Wind direction time series
                            ws=10, # Wind speed time series
                      )
    
    return(sim_res_yaw_offset)

