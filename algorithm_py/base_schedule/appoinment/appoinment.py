import numpy as np
from params import *
import math
import time

from .check_func import check_in_timetable
from .add_func import add_group_in_timetable


def appointment(data, sol_1, schedule):
    """Заполняет расспиание по порядку группп"""

    I = data['I']
    groups = sol_1['groups']

    counter_groups = np.zeros((L), dtype=np.int32)
    
    cur_group = get_next_group(groups, counter_groups)

        
    assigned_groups = []
    
    while(cur_group != None):
        groups[cur_group[2]].remove(cur_group)
        
        group = cur_group
        cost_group = len(group[0]) - (F[group[2],counter_groups[group[2]]] if counter_groups[group[2]]< K else -2.5 )
        # print(cost_group)
        
        if cost_group < 0:
            group.append(False)
            group.append(None)
            assigned_groups.append(group)
            cur_group = get_next_group(groups, counter_groups)
            continue
        
        appropriate_times = []

        first_day = group[3]
        second_day = group[4]

        
        for t_1 in range(first_day[1], first_day[2]):
            for t_2 in range(second_day[1], second_day[2]):

                for i in range(I):
                    if check_in_timetable(t_1, t_2, group, i, data, schedule):
                        appropriate_times.append((t_1, t_2, i))



        if  appropriate_times == []:
            group.append(False)
            group.append(None)
            
        else:
            counter_groups[group[2]]+=1
          
            
            add_group_in_timetable(group, appropriate_times, data, schedule)
            
        
        assigned_groups.append(group)
        
        cur_group = get_next_group(groups, counter_groups)
        
        
    sol_1['groups'] = assigned_groups
    # print(sol_1['groups'])
    # for group in groups:

    #     cost_group = len(group[0]) - F[group[2],counter_groups[group[2]] ]
    #     if cost_group < 0:
    #         group.append(False)
    #         group.append(None)
    #         continue
        
    #     appropriate_times = []

    #     first_day = group[3]
    #     second_day = group[4]

        
    #     for t_1 in range(first_day[1], first_day[2]):
    #         for t_2 in range(second_day[1], second_day[2]):

    #             for i in range(I):
    #                 if check_in_timetable(t_1, t_2, group, i, data, schedule):
    #                     appropriate_times.append((t_1, t_2, i))



    #     if  appropriate_times == []:
    #         group.append(False)
    #         group.append(None)
            
            
            
    #     else:
    #         counter_groups[group[2]]+=1
    #         add_group_in_timetable(group, appropriate_times, data, schedule)

    
    # # print(groups)
    return None


def get_next_group(groups, counter_groups):
    
    applicant_group = []
    penalty_group = [ -F[l,counter_groups[l]] if counter_groups[l]< K else -2.5 for l in range(L)]
    for group_course in groups:
        if group_course == []:
            applicant_group.append([])
        else:
            applicant_group.append(group_course[0])
    


    # s = []
    # for gr in applicant_group:
    #     if gr == []:
    #         s.append(-float('inf'))
    #     else:
    #         s.append(len(gr[0]) - F[gr[2],counter_groups[gr[2]]])

    # print(s)
    # print(penalty_group)
    # l = []
    # for gr in applicant_group:
    #     if gr != []:
    #         l.append((gr[1],gr[2]))
    #     else:
    #         l.append((None,None))
    # print(l)
    sorting_groups( applicant_group, penalty_group)
    # l = []
    # for gr in applicant_group:
    #     if gr != []:
    #         l.append((gr[1],gr[2]))
    #     else:
    #         l.append((None,None))
    # print(l)
    if applicant_group[0] == []:
        return None 
    
    
    group = applicant_group[0]
    
    cost_group = len(group[0]) - penalty_group[group[2]] 
    
    return group if cost_group > 0 else None
    
    
    


def sorting_groups(list, list_coef = None):

    for k_1 in range(len(list)):
        for k_2 in range(len(list)):

            a = list[k_1]
            b = list[k_2]
            if (list_coef != None):
                c_1 = list_coef[k_1]
                c_2 = list_coef[k_2]


            if (list_coef == None):
                if greatest(a, b):
                    c = a
                    list[k_1] = b
                    list[k_2] = c
            else:
                if greatest(a, b, c_1, c_2):
                    c = a
                    list[k_1] = b
                    list[k_2] = c
                    
                    c = c_1
                    list_coef[k_1] = c_2
                    list_coef[k_2] = c


def greatest(a, b, coef_a = 0, coef_b = 0):
    if b == []:
        return True
    else:
        if a == []:
            return False
        else:
            if len(a[0]) + coef_a >  len(b[0]) + coef_b:
                return True
            if len(a[0]) + coef_a <  len(b[0]) + coef_b:
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