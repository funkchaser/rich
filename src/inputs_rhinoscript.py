"""
Run this file in Rhino Python Editor.
The Grasshopper file must be the first active file. (Close all other Grasshopper files to avoid confusion.)
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


def find_component_by_nickname(docObjects, name):
    if docObjects is None: return None

    for obj in docObjects:
        attr = obj.Attributes
        
        if attr.PathName == name:
            return obj
    raise Exception(name + " was not found in document")

def set_value(component, val):
    component.Script_ClearPersistentData()
    component.AddPersistentData(val)
    component.ExpireSolution(True) 

input_num = find_component_by_nickname(doc.Objects, 'Input_Num')
output = find_component_by_nickname(doc.Objects, 'Output_Data')

set_value(input_num, '-1')
print "Collected Data:", output.VolatileData[0][0].Value