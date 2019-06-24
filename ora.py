from amplpy import AMPL, Environment, DataFrame
import pandas as pd
import numpy as np

from ampl_modules.amplcode import AmplCode

# Days per Week
DpW = 5

# Timeslots per day
TpD = 4

# Number Of Rooms
room_count = 10

# capacity
capacity = {}
for r in range(1, room_count+1):
    capacity[r] = [10, 20, 40, 50, 100][r%5]

# Number of Courses
course_count = 50

print("Optimized Room Assignment Tool")

ampl = AMPL(Environment("/home/paszin/ampl/ampl.linux64"))
ampl.setOption('solver', 'cplex')

amplcode = AmplCode.from_file('room_assignment.txt')

amplcode.set_param("DpW", data=DpW)
amplcode.set_param("TpD", data=TpD)

amplcode.set_set('rooms', '{1..%i}' % room_count)
amplcode.set_set('courses', '{1..%i}' % course_count)

amplcode.set_param_data("capacity", data=capacity.items())

amplcode.export("ora_export.txt")

ampl.eval(amplcode.code)

### transform output

values = ampl.getVariable('x').getValues().toPandas()
data = []
for key, value in zip(values.index.tolist(), values.values.tolist()):
    if value[0] == 1:
        print(key)
        data.append(key)

print("Number of Entries", len(data))

arranged_data = []
for day in range(DpW):
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

colTemplate = '{:26}|'
colWidth = int(colTemplate[2:4]) + 1
print(DpW * colWidth * '-' + '-')
print('|' + (DpW * colTemplate).format(*[f"Day {i}" for i in range(1, DpW + 1)]))
print(DpW * colWidth * '-' + '-')
for line in lines:
    print('|', end='')
    for d in line:
        print(colTemplate.format('; '.join(["C{}(R{})".format(int(c), int(r)) for c, r, t in d])), end='')
    print('\n' + (DpW * colWidth) * '-' + '-')
