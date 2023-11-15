import numpy as np
import pdb
import math
import time
import copy

from params import *
from .check_func import *
from .add_func import add_group_in_timetable

def appointment(data, sol_1, schedule):
    """Заполняет расспиание по порядку группп"""

    I = data['I']
    groups = sol_1['groups']

    sorting_new(groups)

    # groups_course = sort_course_group(groups)

    # for list_groups_course in groups_course:
    #     sorting_new(list_groups_course)
    


    # blank_groups = [0 for __ in range(L)]
    # next_group = get_next_group(groups_course, blank_groups)

    # while(next_group != None):
    for group in groups:
        # group = get_next_group(groups_course, blank_groups)
        # groups_course[group[2]].pop(0)
        # next_group = get_next_group(groups_course, blank_groups)

        appropriate_times = []

        first_day = group[3]
        second_day = group[4]
        for i in range(I):

            if not check_limit_working_days(i, first_day[0], second_day[0], data, schedule):
                continue

            # for t_1 in range(first_day[1], 4 + first_day[2]):
            for t_1 in range(first_day[1], first_day[2] + 1 - data['timeLessons'][group[2]] + 1 ):
                if not check_rooms(group, t_1, first_day[0], data, schedule):
                    continue

                if not check_teachers_break(i, group, t_1, first_day[0] , data, schedule):
                    continue

                if not check_time_teachers(i, group, t_1, first_day[0], data, schedule):
                    continue

                if not check_limit_work_time(i, group, t_1, first_day[0], data, schedule):
                    continue


                # for t_2 in range(second_day[1], 4 + second_day[2]):
                for t_2 in range(second_day[1], second_day[2] + 1  - data['timeLessons'][group[2]] + 1):
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
            # blank_groups[group[2]] += 1

    return None


def sort_course_group(groups):

    groups_course = [[] for l in range(L)]
    
    for gr in groups:
        l = gr[2]
        groups_course[l].append(gr)

    return groups_course

def sorting(list):

    for k_1 in range(len(list)):
        for k_2 in range(len(list)):

            a = list[k_1]
            b = list[k_2]
            a_v = len(a[0])*10000 + (T * timeslotsInHour - max(a[3][2] - a[3][1], a[4][2] - a[4][1]))*100 + (L - a[2])
            b_v = len(b[0])*10000 + (T * timeslotsInHour - max(b[3][2] - b[3][1], b[4][2] - b[4][1]))*100 + (L - b[2])


            if a_v > b_v:
            # if greatest(a, b):
                c = a
                list[k_1] = b
                list[k_2] = c

def sorting_new(list):

    for k_1 in range(len(list)):
        for k_2 in range(len(list)):

            a = list[k_1]
            b = list[k_2]


            if greatest(a, b):
                c = a
                list[k_1] = b
                list[k_2] = c


def greatest(a, b):
    if b == []:
        return True
    else:
        if a == []:
            return False
        else:
            if len(a[0]) >  len(b[0]):
                return True
            if len(a[0]) <  len(b[0]):
                return False

            else:

                a_2 = T * timeslotsInHour - max(a[3][2] + 1 - timeL[a[2]] + 1 - a[3][1], a[4][2] + 1 - timeL[a[2]] + 1 - a[4][1])
                b_2 = T * timeslotsInHour - max(b[3][2] + 1 - timeL[b[2]] + 1 - b[3][1], b[4][2] + 1 - timeL[b[2]] + 1 - b[4][1])
                if a_2 > b_2:
                    return True
                if a_2 < b_2:
                    return False        


                else:
                    a_3 = L - a[2]
                    b_3 = L - b[2]
                    if a_3 > b_3:
                        return True
                    else:
                        return False

def get_next_group(groups_course, blank_groups):


    list_choosen_group = []
    list_cost = []

    for l in range(L):
        if groups_course[l] != []:
            gr = groups_course[l][0]
            list_choosen_group.append(gr)
            list_cost.append(len(gr[0]) - F[l, blank_groups[l]])
        else:
            list_choosen_group.append([])
            list_cost.append(float('-inf'))

    
    max_value = 0
    for l in range(L):
        if list_cost[l] > max_value:
            max_value = list_cost[l]
  

    list_max_gr = []
    for group in list_choosen_group:
        if group == []:
            continue
        if list_cost[group[2]] == max_value:
            list_max_gr.append(group)

    sorting_new(list_max_gr)
    
    group = list_max_gr[0] if list_max_gr != [] else None
    return group