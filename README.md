# RICH - Rhino.Inside.Cpython.Helpers

This small tool makes it easier to interact with **Grasshopper** through **cpython** using Rhino.Inside.  
It contains wrappers for setting and collecting data from selected component types.  
See examples files.    

## Installation

```bash
pip install --user rhinoinside
```
See also: https://github.com/mcneel/rhino.inside-cpython 

Developed and tested using Rhino 7 on Windows 10 and Python 3.8.


## Comments

* It runs a Grasshopper in a headless mode (without Rhino/Grasshopper GUI), and it creates an _invisible_ instance of the Grasshopper file. 
Even the Grasshopper file is open, the changes done by the cpython script will not be visible and will not be saved.

* Through this interface, the state of the objects (e.g. disabled) seems to be ignored. This means that values from disabled sources will be collected!
