"""
Run this file in Rhino Python Editor
"""

import os
import pickle
import time, datetime

try:
    import Rhino
    Grasshopper = Rhino.RhinoApp.GetPlugInObject("Grasshopper")
    import Grasshopper
except:
    #because the first try sometimes doesn't work after "Reset Script Engine"
    import clr
    clr.AddReference('Grasshopper')
    import Grasshopper

docServer = Grasshopper.GH_InstanceServer.DocumentServer
doc = docServer[0] # first opened document


def FindBatteryByNickname(docObjects, name):
    if docObjects is None: return None

    for obj in docObjects:
        attr = obj.Attributes
        
        if attr.PathName == name:
            print(type(obj))
            return obj
    raise Exception(name + " was not found in document")

def set_value(battery, val):
    battery.Script_ClearPersistentData()
    battery.AddPersistentData(val)
    battery.ExpireSolution(True) 

input_num = FindBatteryByNickname(doc.Objects, 'Input_Num')
output = FindBatteryByNickname(doc.Objects, 'Output_Data')

set_value(input_num, 77) #sets to 0=generator mode
print "retrieved:", output.VolatileData[0][0].Value