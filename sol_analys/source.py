# from data import *
# from solution import *
# from params import *
# from draw_timetable import *
# from base_group.base_group import base_group
# from base_schedule.base_schedule import base_schedule
# from base_reconstruct.base_reconstruct import base_reconstruct
# from func_with_data import *

from sol_analys.data import *
from sol_analys.solution import *
from sol_analys.params import *
from sol_analys.draw_timetable import *
from sol_analys.base_group.base_group import base_group
from sol_analys.base_schedule.base_schedule import base_schedule
from sol_analys.base_reconstruct.base_reconstruct import base_reconstruct
from sol_analys.func_with_data import *




import numpy as np
from tabulate import tabulate
import copy
import pdb
import time
import json




local_set = [[0],[1],[2],[3],[4],
             [0,1],[0,2],[0,3],[0,4],
             [1,2],[1,3],[1,4],
             [2,3],[2,4],
             [3,4],
             [2,3,4],[1,3,4],[1,2,4],[1,2,3],
             [0,3,4],[0,2,4],[0,2,3],
             [0,1,4],[0,1,3],
             [0,1,2]]




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

    time_rec = np.zeros((new_J, D, 4*T))
    course_rec = np.zeros((new_J, L))

    
    for j in range(len(set_dont_get_students)):
        new_j = set_dont_get_students[j]
        for d in range(D):
            for t in range(4*T):
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
    new_data['minNumber'] = minN# min number of students in the group
    new_data['maxNumber'] = maxN# max number of students in the group
    new_data['timeLessons']  = timeL 

    new_data['couple_of_Days'] =  get_list_of_couple_of_days(D)
    
    new_data['timeslot_of_students'] = time_rec
    new_data['course_of_students'] = course_rec


    return new_data

def local_search(num_it, data, sol, i):

    best_val = get_sol(sol)
    best_sol = copy.deepcopy(sol)
    best_it = 0
    last_loc = []

    f = open(f"history_sol_{i}.txt","w")
    for it in range(num_it): 
        val = (0,0)
        best_loc = []
        new_sol = copy.deepcopy(sol)
        for loc in local_set:
            if loc in last_loc:
                # print(loc)
                continue
            sol_copy = copy.deepcopy(sol)
            rebuild_timetable(loc,data, sol_copy)
            f.write(f"it: {it} local {loc} sol {get_sol(sol_copy)[0]} {get_sol(sol_copy)[1]} \n" )
            if val[0] < get_sol(sol_copy)[0]:
                new_sol = sol_copy
                val = get_sol(sol_copy)
                best_loc = loc
        sol = new_sol
        f.write(f" over it {it} best loc {best_loc}  sol {get_sol(new_sol)[0]} {get_sol(new_sol)[1]} \n")
        if len(last_loc) == 3:
            last_loc.pop(0)
        last_loc.append(best_loc)
        if get_sol(new_sol)[0] >best_val[0]:
            best_sol = new_sol
            best_val = get_sol(new_sol)
            best_it =it

    f.write(f" Best  sol {get_sol(best_sol)[0]} {get_sol(best_sol)[1]}, it { best_it} \n")
    f.close()
    return best_sol

def rebuild_timetable(set_update_teachers,data, sol):

    clear_group_teachers(set_update_teachers, sol)
    
    sol.rename_group()
    set_get_students = get_index_take_student(sol)
    set_dont_get_students = get_list_comp(range(J), set_get_students)

    new_data = get_new_input_data(data, sol, set_update_teachers )
    t = time.perf_counter()
    first_path_sol = base_group(new_data)
    print("first", time.perf_counter() - t)
    first_path_sol_copy = copy.deepcopy(first_path_sol)
    time_2 = time.perf_counter()
    second_path_sol = base_schedule(new_data, first_path_sol_copy)
    print("second", time.perf_counter() - time_2)

    # record = 0
    # for gr in first_path_sol_copy['groups']:
    #     if gr[5] == False:
    #         continue
    #     record+=len(gr[0])
    

    # for __ in  range(10):
    #     first_path_sol_copy_2 = copy.deepcopy(first_path_sol)
    #     second_path_sol = base_schedule(new_data, first_path_sol_copy_2, config="rand")

    #     rec = 0
    #     for gr in first_path_sol_copy_2['groups']:
    #         if gr[5] == False:
    #             continue
    #         rec+=len(gr[0])

    #     if rec > record:
    #         record = rec
    #         first_path_sol_copy =  first_path_sol_copy_2


    first_path_sol = first_path_sol_copy


    # base_reconstruct(new_data, first_path_sol, second_path_sol)



    groups = first_path_sol['groups'] 
    for gr in groups:
        if gr[5] == False:
            continue
        # print(gr)
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

    sol.rename_group()
    # print("Time ",time.perf_counter() - t)

def get_sol(sol):

    groups = sol.groups

    num_st = 0
    num_gr = len(groups)

    for gr in groups:
        num_st+=len(gr[0])

    return num_st, num_gr



def launch():
    data = Data(J, L, I, T, D, r, minN, maxN, timeL )

    # for i in range(1, 11):
    #     filename_data = f"examples_copy\\orders_2_{i}.txt"
    #     data.read_input(filename_data)

    #     filename_sol = f"sol_{i}.json"
    #     sol = Solution(filename_sol)
    #     t = time.perf_counter()
    #     print(get_sol(sol),"start") 
    #     # sol = local_search(1, data, sol, 1 )
    #     rebuild_timetable([1,3,2],data, sol)
    #     print(time.perf_counter() - t)
    #     print(get_sol(sol),"end")


    # sol.rooms_distribution()
    # sol.creat_output_schedule("data_schedule_out2.txt")
    # timetable_png("schedule2")
    # JSON_import(sol.groups, "sol_all")

    for i in range(1, 11):
        data = Data(J, L, I, T, D, r, minN, maxN, timeL )
        filename_data = f"examples_copy\\orders_2_{i}.txt"
        data.read_input(filename_data)
        filename_sol = f"sol_{i}.json"
        sol = Solution(filename_sol)
        print(get_sol(sol),f"start {i}")
        sol = local_search(15, data, sol, i )
        print(get_sol(sol),f"end {i}")
        JSON_import(sol.groups, f"local_prob_sol_{i}.json")
    
    

if __name__ == '__main__':
    launch()