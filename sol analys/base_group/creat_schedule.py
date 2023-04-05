import numpy as np
from random import shuffle

from .secondary_func import *


def create_schedule(data, schedule):
    """ Создает первичное рассписание"""

    r = data['r']
    number_working_rooms = data['number_working_rooms'] 
    I = data['I']
    T = data['T']
    maxPerson = data['maxNumber']
    minPerson = data['minNumber']
    B = sort_by_num_students_in_course(data)
    couple_of_days = data['couple_of_Days']
    numDays = len(couple_of_days)

    
    for l in B: 
    

        array_data = create_array_rec(l, data, schedule)
        print(array_data)
        cor = maxPerson
        while cor >= minPerson:
            ind = False 
            
            for t_1 in range(T):
                for t_2 in range(T):
                    for i in np.arange(numDays):
                        days = couple_of_days[i]
                        r_1 = min(r - number_working_rooms[days[0], 4*t_1], r - number_working_rooms[days[0], 4*t_1 + 1], r - number_working_rooms[days[0], 4*t_1 + 2], r - number_working_rooms[days[0], 4*t_1 + 3], I)
                        r_2 = min(r - number_working_rooms[days[1], 4*t_2], r - number_working_rooms[days[1], 4*t_2 + 1], r - number_working_rooms[days[1], 4*t_2 + 2], r - number_working_rooms[days[1], 4*t_2 + 3], I)
                        
                        if (schedule['rooms'][days[0], t_1] < r_1) and (schedule['rooms'][days[1], t_2] < r_2):
                            if array_data[t_1,t_2, i] >= cor:
                                list_students = create_group( i, t_1, t_2, l, cor, data, schedule)
                                for j in list_students:
                                    refresh_array(j , i, array_data, data)

                                ind = True


            if ind == False:
                cor -= 1
    
    return None

# def create_schedule_rand(data, schedule):
#     r = data['r']
#     T = data['T']
#     L = data['L']
#     maxPerson = data['maxNumber']
#     minPerson = data['minNumber']
#     couple_of_days = data['couple_of_Days']
#     numDays = len(couple_of_days)

#     course_order  = np.arange(L)
#     shuffle(course_order)

#     days_order = np.arange(numDays)
#     shuffle(days_order)

#     time_order = np.arange(T)
#     shuffle(time_order)

#     for l in course_order:
    

#         cor = maxPerson
#         while cor >= minPerson:
#             ind = False 
#             array_data = create_array_rec(l, data, schedule)
            
#             for t_1 in time_order:
#                 for t_2 in time_order:
#                     for i in days_order:
#                         days = couple_of_days[i]
#                         if (schedule['rooms'][days[0], t_1] < r - number_working_rooms) and (schedule['rooms'][days[1], t_2] < r - number_working_rooms):
#                             if array_data[t_1,t_2, i] >= cor:
#                                 list_students = create_group( i, t_1, t_2, l, cor, data, schedule)
#                                 for j in list_students:
#                                     refresh_array(j , i, array_data, data)

#                                 ind = True


#             if ind == False:
#                 cor -= 1
    
#     return None
