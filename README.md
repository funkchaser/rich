# RICH - Rhino.Inside.Cpython.Helpers

This small tool makes it easier to interact with **Grasshopper** through **cpython** using Rhino.Inside.  
It contains wrappers for setting and collecting data from selected component types.  
See examples files.    

## Installation
Developed and tested using Rhino 7 on Windows 10 and Python 3.8.  
Requires [rhinoinside](https://github.com/mcneel/rhino.inside-cpython ):

```bash
pip install --user rhinoinside
```

## Contents
The `src` folder contains:
* a module with helper functions `util.py`
* three demos/examples (_addition_, _delay_, _inputs_) consisting of a python file (to be run in cpython, e.g. in terminal, VSCode or another IDE) and a corresponding Grasshopper file (does not have to be open). Additionally,  `inputs_rhinoscript.py` shows an alternative way of interacting with a Grasshopper file from RhinoPythonEditor.   

## Features & Comments
* Finds components and inputs by nickname, in a Grasshopper file given by the path.

* Set values to:
    * "Primitive Param" components (`Int`, `Num`, `Text`, `Bool`): `set_value()`
    * components that have inputs, incl. ghpython components:  `set_input()`
    * single value or a 1D list
* Read values from:
    * "Param" components, e.g. `Data`: `get_values()`
    * The collected data is flattened (no tree structure preserved).
    * Returns Rhino.Geometry object types, not only primitives.

* It runs a Grasshopper in a headless mode (without Rhino/Grasshopper GUI), and it creates an _invisible_ instance of the Grasshopper file. 
Even the Grasshopper file is open, the changes done by the cpython script will not be visible and will not be saved.

* Through this interface, the state of the objects (e.g. disabled) seems to be ignored. This means that values from disabled sources will be collected!
