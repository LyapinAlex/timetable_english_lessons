import numpy as np
import math
import time

from .check_func import *
from .add_func import add_group_in_timetable

def appointment(data, sol_1, schedule):
    """Заполняет расспиание по порядку группп"""

    I = data['I']
    groups = sol_1['groups']


    for group in groups:
        # Time = time.perf_counter() 
        appropriate_times = []

        first_day = group[3]
        second_day = group[4]
        for i in range(I):

            if not check_limit_working_days(i, first_day[0], second_day[0], data, schedule):
                continue

            for t_1 in range(first_day[1], 4 + first_day[2]):

                if not check_rooms(group, t_1, first_day[0], data, schedule):
                    continue

                if not check_teachers_break(i, group, t_1, first_day[0] , data, schedule):
                    continue

                if not check_time_teachers(i, group, t_1, first_day[0], data, schedule):
                    continue

                if not check_limit_work_time(i, group, t_1, first_day[0], data, schedule):
                    continue


                for t_2 in range(second_day[1], 4 + second_day[2]):
                    
                    if not check_rooms(group, t_2, second_day[0], data, schedule):
                        continue
                    
                    if not check_teachers_break(i, group, t_2, second_day[0] , data, schedule):
                        continue

                    if not check_time_teachers(i, group, t_2, second_day[0], data, schedule):
                        continue

                    if not check_limit_work_time(i, group, t_2, second_day[0], data, schedule):
                        continue



                    # if check_in_timetable(t_1, t_2, group, i, data, schedule):
                    appropriate_times.append((t_1, t_2, i))
            

        # Time = time.perf_counter() - Time
        # print(Time, group[2], group[1])
        if  appropriate_times == []:
            # print("Fail ", "l",group[2],"k", group[1])
            group.append(False)
            group.append(None)
            continue
        else:
            # print("Sucsecc ", "l",group[2],"k", group[1])
            add_group_in_timetable(group, appropriate_times, data, schedule)

    return None


