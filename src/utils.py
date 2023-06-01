import os
import rhinoinside
rhinoinside.load()

import Rhino 
# Start grasshopper in "headless" mode
pluginObject = Rhino.RhinoApp.GetPlugInObject("Grasshopper")
if pluginObject:
    pluginObject.RunHeadless()

from System import Decimal

import Grasshopper
from Grasshopper.Kernel.Data import GH_Path
from Grasshopper.Kernel import GH_SolutionMode


TYPES = {
    "Arc": Grasshopper.Kernel.Types.GH_Arc,
    "Boolean": Grasshopper.Kernel.Types.GH_Boolean,
    "Box": Grasshopper.Kernel.Types.GH_Box,
    "Brep": Grasshopper.Kernel.Types.GH_Brep,
    "Circle": Grasshopper.Kernel.Types.GH_Circle,
    "ComplexNumber": Grasshopper.Kernel.Types.GH_ComplexNumber,
    "Curve": Grasshopper.Kernel.Types.GH_Curve,
    "Guid": Grasshopper.Kernel.Types.GH_Guid,
    "Integer": Grasshopper.Kernel.Types.GH_Integer,
    "Interval": Grasshopper.Kernel.Types.GH_Interval,
    "Interval2D": Grasshopper.Kernel.Types.GH_Interval2D,
    "Line": Grasshopper.Kernel.Types.GH_Line,
    "Mesh": Grasshopper.Kernel.Types.GH_Mesh,
    "Number": Grasshopper.Kernel.Types.GH_Number,
    "Plane": Grasshopper.Kernel.Types.GH_Plane,
    "Point": Grasshopper.Kernel.Types.GH_Point,
    "Rectangle": Grasshopper.Kernel.Types.GH_Rectangle,
    "String": Grasshopper.Kernel.Types.GH_String,
    "SubD": Grasshopper.Kernel.Types.GH_SubD,
    "Surface": Grasshopper.Kernel.Types.GH_Surface,
    "Vector": Grasshopper.Kernel.Types.GH_Vector,
    "Text": Grasshopper.Kernel.Types.GH_String
    }

def cast_gh_type_to_python(x):
    if type(x) in (float, int, str, bool):
        return x
    if type(x) is Grasshopper.Kernel.Types.GH_Boolean:
        return bool(x.Value)
    if type(x) is Grasshopper.Kernel.Types.GH_Number:
        return float(x.Value)
    if type(x) is Grasshopper.Kernel.Types.GH_Integer:
        return int(x.Value)
    if type(x) is Grasshopper.Kernel.Types.GH_String:
        return str(x.Value)
    if isinstance(x, Decimal):
        return float(x)
    print("Not implemented: cast {} of type {} to python types.".format(x, type(x)))



def get_ghdoc(filepath, filename):

    ghfile = os.path.join(filepath, filename)
    if not os.path.exists(ghfile):
        print("This file does not exists:", ghfile)

    ghdocIO = Grasshopper.Kernel.GH_DocumentIO()
    ghdocIO.Open(ghfile)
    ghdoc = ghdocIO.Document
    return ghdoc

def cast(item):
    success, cast_item = item.CastTo[TYPES[item.TypeName]](item)
    return success, cast_item.Value


def runcount(ghdoc, component_nickname):
    for obj in ghdoc.Objects:
        if obj.NickName == component_nickname: 
            component = Grasshopper.Kernel.IGH_Component(obj)
            n = component.RunCount
            print(f"  gh_component run {n:>3} times: '{component_nickname}'")

def set_input(ghdoc, component_nickname, parameter_nickname, value, ghtype):
    assert not isinstance(value, list), "Value parameter cannot be a list. Please provide a single value"
    obj = find_component_by_nickname(ghdoc,component_nickname)
    if not obj: 
        print("Could not set value.")
        return

    component = Grasshopper.Kernel.IGH_Component(obj)
    for param in component.Params.Input:
        if param.NickName == parameter_nickname:
            param.VolatileData.Clear()
            param.AddVolatileData(GH_Path(0), 0, ghtype(value))
            print(f"'{obj.NickName}' -> input '{param.NickName}' set to {param.VolatileData[0][0]}")
    component.ExpireSolution(True)


def set_value(ghdoc, component_nickname, value):
    obj = find_component_by_nickname(ghdoc, component_nickname)

    if not obj: 
        print("Could not set value.")
        return
    print(obj, type(obj))
    component = Grasshopper.Kernel.IGH_Param(obj)
    ghtype = TYPES[component.TypeName] 
    component.AddVolatileData(GH_Path(0),0, ghtype(value))

    print(f"'{obj.NickName}' -> value set to {component.VolatileData[0][0]}")
    # DO NOT component.ExpireSolution(True)! It will erase the volatile data!

def set_slider(ghdoc, component_nickname, value):
    raise NotImplementedError("Use set_value() method instead")



def get_param_component(ghdoc, component_nickname):
    obj = find_component_by_nickname(ghdoc, component_nickname)
    if not obj: 
        print("Could not set value.")
        return
    
    values = []
    param = Grasshopper.Kernel.IGH_Param(obj)
    param.CollectData()
    param.ComputeData()
    for item in param.VolatileData.AllData(True):
        success, cast_item = cast(item)
        values.append(cast_item)
        # print(f"\titem of type: '{item.TypeName}'")
        # print("\t    -->", success, "|", cast_item, type(cast_item))

    if not values: 
        print(f"'{component_nickname}' collected no values.")
        return None
    if len(values)==1: 
        value = values[0]
        print(f"'{component_nickname}' collected one value: {value}({type(value)})")
        return value
    else:
        print(f"'{component_nickname}' collected {len(values)} values: ")
        for value in values: print(f"\t{value} {type(value)}")
        return values

def find_component_by_nickname(ghdoc, component_nickname):
    found = []
    for obj in ghdoc.Objects:
        # if obj.Attributes.PathName == component_nickname:
        if obj.NickName == component_nickname:
            found.append(obj)
    
    if not found:
        print(f"No ghcomponent found with a nickname {component_nickname}.")
        return
    if len(found)>1:
        print(f"{len(found)} ghcomponents found with the nickname {component_nickname} - will return None.")
        return
    return found[0]




def new_solution(ghdoc):
    ghdoc.NewSolution(True, GH_SolutionMode.Silent)