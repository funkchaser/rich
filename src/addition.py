
import os

from utils import (TYPES, get_ghdoc, get_values, new_solution,
                   runcount, set_input)

ghdoc = get_ghdoc(
    filepath = os.path.dirname(__file__), 
    filename = "addition.gh")


runcount(ghdoc, "Add")
runcount(ghdoc, "A+B")
runcount(ghdoc, "TimesTwo")

set_input(ghdoc,component_nickname="Add", parameter_nickname="A", value=111, ghtype=TYPES['Number'])
set_input(ghdoc,component_nickname="Add", parameter_nickname="B", value=222, ghtype=TYPES['Number'])
# new_solution(ghdoc) doesn't seem to do anything

data_collected = get_values(ghdoc, component_nickname="Result")

runcount(ghdoc, "Add")
runcount(ghdoc, "A+B")
runcount(ghdoc, "TimesTwo")

print("---")

set_input(ghdoc,component_nickname="A+B", parameter_nickname="A", value=5, ghtype=TYPES['Number'])
set_input(ghdoc,component_nickname="A+B", parameter_nickname="B", value=7, ghtype=TYPES['Number'])
set_input(ghdoc,component_nickname="A+B", parameter_nickname="B", value=1, ghtype=TYPES['Number'])
new_solution(ghdoc)
data_collected = get_values(ghdoc, component_nickname="Result") #-> does not update result


runcount(ghdoc, "Add")
runcount(ghdoc, "A+B")
runcount(ghdoc, "TimesTwo")