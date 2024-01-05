import numpy as np
import copy
import time
from params import *
from random import shuffle
import pdb

from .secondary_func import *


def create_schedule(data, schedule):
    """ Создает первичное рассписание"""

    timeL = data['timeLessons']
    r = data['r']
    I = data['I']

    number_working_rooms = copy.copy(data['number_working_rooms'])
    for d in range(data['D']):
        for t in range(timeslotsInHour*data['T']):
            number_working_rooms[d,t] = min(r - number_working_rooms[d,t], I)

    T = 4*data['T']
    maxPerson = data['maxNumber']
    minPerson = data['minNumber']
    B = sort_by_num_students_in_course(data)

    couple_of_days = data['couple_of_Days']
    numDays = len(couple_of_days)
    
    timeSlots = data['timeslot_of_students']
    

    time_begin_for_st = []
    for j in np.arange(data['J']):
        for l in np.arange(data['L']):
            if data['course_of_students'][j,l] == 1:
                time_begin_for_st.append(time_for_begin(timeSlots[j], T , data['D'], timeL[l]))
                break
            

    list_set_students = get_list_of__student(data)

    
    for l in B: 
        # print('l', l)
        # time_list_creat = time.perf_counter()

        set_id_students = list_set_students[l]
        # print(len(set_id_students))

        array_data = create_array_rec(data, time_begin_for_st, set_id_students)
        cor = maxPerson
        # print(array_data)
        # print(l, np.max(array_data))
        while cor >= minPerson:
            ind = False 
            max_rec = 0
            for t_1 in range(T):
                for t_2 in range(T):
                    for i in np.arange(numDays):
                        days = couple_of_days[i]

                        if array_data[t_1,t_2, i] >= cor:
                            if check(t_1, t_2, timeL[l], number_working_rooms, days[0], days[1]):

                                list_students = create_group( i, t_1, t_2, l, cor, data, schedule, set_id_students)
                                for j in list_students:
                                    refresh_array( i, array_data, data, time_begin_for_st[j])
                                    set_id_students.remove(j)
                                

                                for t in range(timeL[l]):
                                    number_working_rooms[days[0], t_1 + t]-=1
                                    number_working_rooms[days[1], t_2 + t]-=1

                               
                                ind = True
                            else: 
                                array_data[t_1,t_2, i] = 0

                        if array_data[t_1,t_2, i] > max_rec:
                            max_rec = array_data[t_1,t_2, i]

            if ind == False:
                cor -= 1
                if cor > max_rec:
                    cor= max_rec

        # print(len(set_id_students))
        # print(l, time.perf_counter() - time_list_creat)
    return None
