import numpy as np

# J = 150
# L = 3
# D = 6
# T = 11
# I = 3
# r = 2
# K = 15
# minN = 2
# maxN = 6
# timeL = np.array([ 4, 5, 6])
J = 500# num of studetns
L = 13# num of course
I = 5# num of teachers
r = 4# num of rooms
K = 25
D = 6# num of day
T = 11# num of timslots in the 
minN = 2# min number of students in the group
maxN = 8# max number of students in the group
timeL  = np.array([3, 3, 3, 3, 3, 4, 3, 4, 5, 5, 5, 6, 6])
timeslotsInHour = 4
teacherLimit = 32
teaherBreak = 1

filename_input = "examples_copy\\orders_2_1.txt"
filename_output = ""