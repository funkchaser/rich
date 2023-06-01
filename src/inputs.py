"""
Demonstrating how to set SINGLE values (no lists, no trees) to different types of components in Grasshopper.

/!\ 
Through this interface, the state of the objects (e.g. disabled) seems to be ignored! 
This means that values from diabled sources will be collected!

"""

import os

from utils import (TYPES, get_ghdoc, get_param_component, new_solution,
                   runcount, set_input, set_value, set_slider)

ghdoc = get_ghdoc(
    filepath = os.path.dirname(__file__), 
    filename = "inputs.ghx")

# #set input to components that have input and output parameters, incl. ghPython components
set_input(ghdoc, component_nickname="Input_Python", parameter_nickname="x", value=7, ghtype=TYPES['Integer'])


# # set input to Params Primitive components (Num, Int, Bool, Text)
set_value(ghdoc, component_nickname="Input_Num", value=3.141592)
set_value(ghdoc, component_nickname="Input_Int", value=123)
set_value(ghdoc, component_nickname="Input_Txt", value="Hello")
set_value(ghdoc, component_nickname="Input_Bool", value=True)

# set input to a slider 
#   /!\ slider is treated as a Param component of type GH_Number, this ignores the pre-set range of the slider!
set_value(ghdoc, component_nickname="Input_Slider", value=123.456)


data_collected = get_param_component(ghdoc, component_nickname="Output_Data")