from data import *
from solution import *
from params import *
import numpy as np
from base_group.base_group import base_group
from base_schedule.base_schedule import base_schedule
from base_reconstruct.base_reconstruct import base_reconstruct
from func_with_data import *
from tabulate import tabulate
import pdb
import time
import math


# def analys(data, sol):

#     all_teachers_time = []
#     for i in range(I):
#         teacher_time = []
#         for d in range(D):
#             time_in_day =[]
#             for t in range(4*T):
#                 if np.sum(sol.U[i,d,t]) == 0:
#                     time_in_day.append(t)
#             teacher_time.append(time_in_day)
#         all_teachers_time.append(teacher_time)


#     all_teachers_time = np.array(all_teachers_time)

#     print(all_teachers_time[0])
#     for l in range(L):
#         print(l)
#         map_rec_distr = np.zeros((4*T, D))

#         for j in range(J):
#             if np.sum(sol.y[j]) == 0 and data.courseRec[j,l] == 1: 
#                 # for t in range(4*T):
#                 for d in range(D):
#                     for t in all_teachers_time[0,d]:
#                         map_rec_distr[t,d]+=data.timeRec[j,d,t]

#         print(map_rec_distr)   

        # map_gr_sidtr = np.zeros((4*T, D))

        # for j in range(J):
        #     if np.sum(sol.y[j]) == 0 and data.courseRec[j,l] == 1: 
        #         for t in range(4*T):
        #             for d in range(D):
        #                 map_rec_distr[t,d]+=data.timeRec[j,d,t]


def get_list_comp(A, B):
    set = []
    for a in A:
        if a not in B:
            set.append(a)
    return set

def clear_group_teachers(set_update_teachers, sol):
    groups = sol.groups  

    i = 0
    while i < len(groups):
        if groups[i][5] in set_update_teachers:
            print(groups[i])
            del groups[i]
        else:
            i += 1

    return 0

def get_index_take_student(sol):
    index_st = []
    for gr in sol.groups:
        for st in gr[0]:
            index_st.append(st)
    
    return index_st 


def get_new_input_data(data, sol, set_update_teachers):
    

    set_immutable_teachers = get_list_comp(range(I), set_update_teachers)
    set_get_students = get_index_take_student(sol)
    set_dont_get_students = get_list_comp(range(J), set_get_students)

    new_J = len(set_dont_get_students)

    time_rec = np.zeros((new_J, D, T))
    course_rec = np.zeros((new_J, L))

    
    for j in range(len(set_dont_get_students)):
        new_j = set_dont_get_students[j]
        for d in range(D):
            for t in range(T):
                time_rec[j,d,t] = data.timeRec[new_j ,d,t]

        for l in range(L):
            course_rec[j,l] = data.courseRec[new_j, l]


    number_working_rooms = np.zeros((D, 4*T))
    for i in set_immutable_teachers:
        for d in range(D):
            for t in range(4*T):
                if np.sum(sol.U[i,d,t]) != 0:
                    number_working_rooms[d,t]+=1





    new_data = {}
    new_data['J'] = new_J
    new_data['L'] = L
    new_data['D'] = D# num of day
    new_data['T'] = T# num of timslots in the 
    new_data['I'] = len(set_update_teachers)# num of teachers
    new_data['Set_I'] = set_update_teachers
    new_data['r'] = r # num of rooms
    new_data['number_working_rooms'] = number_working_rooms# num of rooms
    new_data['minNumber'] = 2# min number of students in the group
    new_data['maxNumber'] = 6# max number of students in the group
    new_data['timeLessons']  = np.array([ 4, 5, 6])

    new_data['couple_of_Days'] =  get_list_of_couple_of_days(D)
    
    new_data['timeslot_of_students'] = time_rec
    new_data['course_of_students'] = course_rec

    return new_data

def rebuild_timetable(set_update_teachers,data, sol):

    clear_group_teachers(set_update_teachers, sol)

    sol.rename_group()
    print_sol(sol)

    set_get_students = get_index_take_student(sol)
    set_dont_get_students = get_list_comp(range(J), set_get_students)

    new_data = get_new_input_data(data, sol, set_update_teachers )



    first_path_sol = base_group(new_data)
    second_path_sol = base_schedule(new_data, first_path_sol)



    groups = first_path_sol['groups'] 
    
    for gr in groups:
        # print(gr)
        if gr[5] == False:
            continue
        g = []
        set_st = []
        for j in gr[0]:
            set_st.append(set_dont_get_students[j])
        g.append(set_st)
        g.append(int(gr[1]))
        d_1 = [int(gr[3][0]), int(gr[3][1]), int(gr[3][2])]
        d_2 = [int(gr[4][0]), int(gr[4][1]), int(gr[4][2])]
        g.append(int(gr[2]))
        g.append( d_1)
        g.append( d_2)
        g.append(new_data['Set_I'][int(gr[6])])
        sol.groups.append(g)


def print_sol(sol):

    groups = sol.groups

    num_st = 0
    num_gr = len(groups)

    for gr in groups:
        num_st+=len(gr[0])

    print("st :", num_st, "gr :", num_gr)

def launch():

    data = Data(J, L, I, T, D, r, minN, maxN, timeL )
    data.read_input(filename_input)
    
    sol = Solution()
    # print("Start solution")
    # print(sol.groups)
    print_sol(sol)
    # print("------------------")

    rebuild_timetable([0],data, sol)
    sol.rename_group()
    print_sol(sol)
    # print("Rebuild solution")
    # print(sol.groups)
    # print("------------------")
    # sol.print_schedule("rebuild_schedule")
    

if __name__ == '__main__':
    launch()