import numpy as np
import copy

def change_format_group(data, sol):
    """ Изменяет фортмат записи группы, к фторому этапу алгоритма. Заменяет sol['groups'] на новые группы.
        Принимает на вход: data, sol.
        data = входные данные 
        sol = решение из первого этапа

        Возращает groups.
        groups = отформированый список групп
     """

    groups = sol['groups']


    sort_group = []
    for course_group in groups:
        for group in course_group:
            sort_group.append(group)


    for group in sort_group:
        expand_timeslots(data, group)


    # Эвристиска для порядка групп
    # sort_group.sort(key = lambda x : len(x[0])*10000 + (44 - max(x[3][2] - x[3][1], x[4][2] - x[4][1]))*100 + (13 - x[2]))
    # sort_group.sort(key = lambda x : len(x[0]))
    sorting( sort_group)
    # sort_group.reverse()
    sol['groups'] = sort_group

    

    return sort_group

def sorting(list):

    for k_1 in range(len(list)):
        for k_2 in range(len(list)):

    # for k_1 in range(86):
    #     for k_2 in range(86):
            a = list[k_1]
            b = list[k_2]
            a_v = len(a[0])*10000 + (44 - max(a[3][2] - a[3][1], a[4][2] - a[4][1]))*100 + (13 - a[2])
            b_v = len(b[0])*10000 + (44 - max(b[3][2] - b[3][1], b[4][2] - b[4][1]))*100 + (13 - b[2])
            if a_v > b_v:
            # if len(a[0]) > len(b[0]):
                c = a
                list[k_1] = b
                list[k_2] = c



def expand_timeslots(data, group):

    timeslot_of_students = data['timeslot_of_students']
    students = group[0]
    days = group[3]
    expand_time_first_day = np.ones(data['T'], dtype = np.int8)
    expand_time_second_day = np.ones(data['T'], dtype = np.int8)
    for student in students:
        for time in range(data['T']):
            expand_time_first_day[time] *= timeslot_of_students[student, days[0], time] 
            expand_time_second_day[time] *= timeslot_of_students[student, days[1], time] 

    
    board_expand_time_first = [None, None]
    board_expand_time_second = [None, None]
    ind_1, ind_2 = True, True
    for time in range(data['T']):

        if expand_time_first_day[time] == 1 and ind_1:
            ind_1 = False
            board_expand_time_first[0] = time * 4
        elif  expand_time_first_day[time] == 0 and not ind_1:
            board_expand_time_first[1] = (time - 1) * 4
            ind_1 = True

        if expand_time_second_day[time] == 1 and ind_2:
            ind_2 = False
            board_expand_time_second[0] = time * 4
        elif  expand_time_second_day[time] == 0 and not ind_2:
            board_expand_time_second[1] = (time - 1) * 4
            ind_2 = True
            

    if board_expand_time_first[1] == None:
        board_expand_time_first[1] = data['T'] * 4
 
    if board_expand_time_second[1] == None:
        board_expand_time_second[1] = data['T'] * 4

    group.pop()
    group.pop()
    group.pop()

    group.append((days[0], board_expand_time_first[0],board_expand_time_first[1] ))
    group.append((days[1], board_expand_time_second[0],board_expand_time_second[1] ))



    return group

