import json
import math
import pprint
import collections
from skyfield.api import Star, Topos, Loader
from skyfield.api import load
from copy import deepcopy
import os
import time
from datetime import datetime
from collections import OrderedDict

###################
# Space object
###################
class space_obj:
  def __init__(self,cfg):    

    self.cfg = cfg 
    with open(self.cfg.spacecraft_file_j,"r") as json_file:
      self.sp_data = json.load(json_file) # load space objects

    self.obj_data=[]
   
    self.od = {
      "dispname":"",
      "name":"",
      "az":0.0,           # azimut
      "el":0.0,           # elevation
      "sat_qrg":0.0,      # Tx qrg
      "doppler":0.0,      # doppler
      "rx_qrg":0.0,       # rx qrg after doppler correction
      "delot":0.0,        # delot
      "dist_km":0.0,      # distance in km       
      "dist_au":0.0,      # distance in AU
      "l_min":0.0,        # distance in light Minutes
      "l_y":0.0,          # distance in light Years 
      "ts":0.0            # time for observation  
    }

  # calc dummy
  def calc(self, leo_obj):   
    pass
  
  # returns all 
  def calc_all(self):
    o1=[]
    for d in self.list:
      ee=deepcopy(self.calc(d))
      if ee != 0:
        o1.append(ee)
    return o1    

  # returns by name
  def calc_by_name(self,name):
    for x in self.list:
      if x["name"] == name:
        return self.calc(x)

###################
# LEOs
###################
class Leos(space_obj):
  def __init__(self,cfg):  
    super().__init__(cfg)
    self.load = Loader(self.cfg.skyfield_loader_path)
    self.list = self.sp_data['leos']
    
  # calc leo
  def calc(self, leo_obj):  
    if leo_obj["disp"]==0:
      return 0
    sat_list          = leo_obj["datafile"]                  # tle data list
    stations_url      = self.cfg.celestrack_url              # url for sat data source
    satellites        = self.load.tle(stations_url+sat_list) # get TLE
    ts_               = self.load.timescale()
    t                 = ts_.now()
    
    #days              = t - satellite.epoch
    # #print('{:.3f} days away from epoch'.format(days))
    # #if abs(days) > 14: satellites = self.load.tle(stations_url+sat_list,reload=True)  #  self.load.tle(stations_url, reload=True)

    dss_qth            = Topos(self.cfg.lat_s, self.cfg.lon_s)
    relative_postion   = satellites[leo_obj["name"]] - dss_qth
    topocentric        = relative_postion.at(t)
    alt, az, distance  = topocentric.altaz()
    range_velocity     = topocentric.velocity.km_per_s
    range_speed        = math.sqrt(range_velocity[0]**2 + range_velocity[1]**2+range_velocity[2]**2)
    
    self.od["sat_qrg"] = float(leo_obj["qrg"])
    self.od["name"]    = leo_obj["name"]
    self.od["dispname"]    = leo_obj["dispname"]
    self.od["az"]      = az.degrees                # azimut
    self.od["el"]      = alt.degrees               # elevation
    self.od["delot"]   = range_speed               # [km/s]   # delot
    self.od["dist_km"] = distance.km               # [km]     # distance in mkm       
    self.od["dist_au"] = distance.au               # [AU]     # distance in AU
    self.od["l_min"]   = distance.km / 1.799e+7    # [l_min]  # distance in light Minutes
    self.od["l_y"]     = distance.km / 9.461e+12   # [LY]     # distance in distance in light Years 
    self.od["ts"]      = "0" #t                                                         # observation time 
    self.od["doppler"] = (1 + range_speed * 1e3 / 299792458)  * self.od["sat_qrg"] - self.od["sat_qrg"]     # dopper shift
    self.od["rx_qrg"]  = self.od["sat_qrg"] + self.od["doppler"]       # rx qrg after doppler correction
    return(self.od)

