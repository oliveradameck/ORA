from amplpy import AMPL, Environment, DataFrame
import pandas as pd
import numpy as np
import sys
import os

from ampl_modules.amplcode import AmplCode
import ascii_table

# Days per Week
DpW = 3

# Timeslots per day
TpD = 4

# Weeks for the schedule
weeks = 2

# Number Of Rooms
# room_count = 3 not in use anymore
buildings = 2
rooms_per_building = 2
rooms = sum([list(range(i * 1000 + 1, i * 1000 + rooms_per_building + 1)) for i in range(1, buildings + 1)], [])

# department HQ
departmentHQ = {1: 1000, 2: 2000}

print(rooms)
# capacity
capacity = {}
for r in rooms:
    capacity[r] = [10, 20, 40, 50, 100][r % 5]

# Number of Courses
course_count = 5

# course frequency
course_frequency = {}
for c in range(1, course_count + 1):
    course_frequency[c] = [1, 0.5][c % 2]

# department assign
department_assign = {}
for c in range(1, course_count + 1):
    department_assign[c] = (c + 1) % 2 + 1

# Distance matrix
distance_matrix = {}
for d, base in departmentHQ.items():
    for r in rooms:
        distance_matrix[(d, r)] = abs(r - base)

# sys.exit()
print("Optimized Room Assignment Tool")

print("Setup")
print("Expected Number of Courses: ", sum(list(course_frequency.values())))

# pro_environment = "/Users/oliveradameck/Desktop/ampl-pro/ampl_linux-intel64"
# low_environment = "/User/oliveradameck/Desktopampl/ampl.linux64"
pro_environment = os.environ.get("AMPL_PATH", "ampl")
# low_environment = "/User/oliveradameck/Desktopampl/ampl.linux64"
# path = os.path.join(os.path.expanduser('~'), 'ora')
ampl = AMPL(Environment(pro_environment))
ampl.setOption('solver', 'cplex')

amplcode = AmplCode.from_file('room_assignment.txt')

# print("Parameters from AMPL Code:")
# print(amplcode.get_params())

amplcode.set_param("DpW", data=DpW)
amplcode.set_param("TpD", data=TpD)
amplcode.set_param("weeks", data=weeks)

# amplcode.set_set('rooms', '{' + ','.join(map(str, rooms)) + '}')
amplcode.set_set('rooms', '{' + ','.join(map(str, rooms)) + '}')
amplcode.set_set('courses', '{1..%i}' % course_count)
amplcode.set_set('departments', list(departmentHQ.keys()))

amplcode.set_param_data("capacity", data=capacity.items())
amplcode.set_param_data("courseFrequency", data=course_frequency.items())
amplcode.set_param_data("departmentHQ", departmentHQ.items())
amplcode.set_param_data("departmentAssign", department_assign.items())
amplcode.set_param_data_3d("distance", distance_matrix.items())

amplcode.export("ora_export.txt")

ampl.eval(amplcode.code)

### transform output
print("Values from Ampl (where x[c, r, t] = 1)")
print("c,  r,    t")
values = ampl.getVariable('x').getValues().toPandas()
data = []
for key, value in zip(values.index.tolist(), values.values.tolist()):
    if value[0] == 1:
        print(key)
        data.append(key)

print("Number of Entries", len(data))

all_days = DpW * weeks
arranged_data = []
for day in range(all_days):
    arranged_data.append([])
    for slot in range(TpD):
        arranged_data[-1].append(list(filter(lambda crt: crt[2] // TpD == day and crt[2] % TpD == slot, data)))

print("arranged data")

for day in arranged_data:
    print("Day:")
    for slot in day:
        print(slot)
    print()

lines = np.array(arranged_data).T

rows = []
for line in lines:
    rows.append([])
    for cell in line:
        if len(cell) > 0:
            rows[-1].append('; '.join(["C{}(R{})".format(int(c), int(r)) for c, r, t in cell]))
        else:
            rows[-1].append('')

for week in range(weeks):
    print(f"Week {week+1}")
    ascii_table.print_table(header=[f"Day {i}" for i in range(1, DpW + 1)],
                            rows=list(map(lambda a: a[week * DpW:(week + 1) * DpW], rows)),
                            spacing=2,
                            min_width=30)
