"""
Example to show/test how solution updates are scheduled in Grasshopper if some parts required a lot of computation time.
"""

import os
import time

t = time.time()
def dt(message):
    global t
    dt = time.time()-t
    print(f"{message}: dt = {int(dt*1000)} [ms]")
    t=time.time()


from utils import (TYPES, get_ghdoc, get_values, set_input, runcount)

dt("Imports")

ghdoc = get_ghdoc(
    filepath = os.path.dirname(__file__), 
    filename = "delay.ghx")

dt("Load ghdoc")

"""
InputA - no delay
InputB - delay 1s
Calc - delay 5s

Expected behaviour: one iteration/solution takes approx. 6s
"""

for i in range(5):
    set_input(ghdoc,component_nickname="InputB", parameter_nickname="b", value=i*2, ghtype=TYPES['Number'])
    set_input(ghdoc,component_nickname="InputA", parameter_nickname="a", value=i, ghtype=TYPES['Number'])

    # new_solution(ghdoc) doesn't seem to do anything
    print(f"\t\t expected result: {-i-i*2}")
    data_collected = get_values(ghdoc, component_nickname="ResultC")
    dt(f"iter {i}")
    print("\n")
