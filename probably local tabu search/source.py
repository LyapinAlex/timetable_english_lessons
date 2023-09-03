from data import *
from solution import *
from params import *
from draw_timetable import *
from base_group.base_group import base_group
from base_schedule.base_schedule import base_schedule
from base_reconstruct.base_reconstruct import base_reconstruct
from func_with_data import *

# from sol_analys.data import *
# from sol_analys.solution import *
# from sol_analys.params import *
# from sol_analys.draw_timetable import *
# from sol_analys.base_group.base_group import base_group
# from sol_analys.base_schedule.base_schedule import base_schedule
# from sol_analys.base_reconstruct.base_reconstruct import base_reconstruct
# from sol_analys.func_with_data import *



import numpy as np
from tabulate import tabulate
import copy
import random
import pdb
import time
import json
import math


local_set = [[0,1],[0,2],[0,3],[0,4],
             [1,2],[1,3],[1,4],
             [2,3],[2,4],
             [3,4],
             [2,3,4],[1,3,4],[1,2,4],[1,2,3],
             [0,3,4],[0,2,4],[0,2,3],
             [0,1,4],[0,1,3],
             [0,1,2]]

def prob_loc(p):

    prob_loc = []
    for loc in local_set:
        if random.random() < p:
            prob_loc.append(loc)

    return prob_loc


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

def local_search(num_it, p ,data, sol, name = "history_sol"):

    sol_val = sol.get_sol_val()
    best_sol = copy.deepcopy(sol)
    best_objval = sol_val['obj_val']
    # best_objval = sol_val['num_st']
    best_it = 0
    last_loc = []
    rec_change = 0 
    # f = open( name + ".txt", "w" )
    # for it in range(num_it):
    it = 0 
    lose_it = 0
    while (it < 100 and lose_it < num_it):
        # val = (0,0)
        best_loc = []
        new_sol = copy.deepcopy(sol)
        loc_objval = 0
        pr_loc = prob_loc(p)
        # pr_loc = local_set
        if pr_loc == []:
            continue
        for loc in pr_loc:
            # if loc in last_loc:
            #     # print(loc)
            #     continue
            sol_copy = copy.deepcopy(sol)
            rebuild_timetable(loc, data, sol_copy)
            sol_val = sol_copy.get_sol_val()
            # f.write(f"it: {it} local {loc} sol st:{sol_val['num_st']} gr:{sol_val['num_gr']} objval:{sol_val['obj_val']} \n" )

            if [loc, sol_val] in last_loc:
                continue

            # if loc_objval < sol_val['num_st']:
            if loc_objval < sol_val['obj_val']:
                new_sol = sol_copy
                # loc_objval = sol_val['num_st']
                loc_objval = sol_val['obj_val']
                best_loc = loc
        
        sol = new_sol
        sol_val = sol.get_sol_val()
        # f.write(f" over it {it} best loc {best_loc}  sol st:{sol_val['num_st']} gr:{sol_val['num_gr']} objval:{sol_val['obj_val']}\n")
        if len(last_loc) == 3:
            last_loc.pop(0)
        last_loc.append([best_loc,sol_val])

        if best_objval < loc_objval:
            best_sol = new_sol
            # best_val = new_sol.get_sol()
            best_objval = loc_objval
            best_it = it
            if rec_change < lose_it:
                rec_change = lose_it
            lose_it = 0

            # print(it, lose_it, best_objval)
        else:
            lose_it+=1 

        it+=1
    print(it,lose_it, rec_change)
    sol_val = best_sol.get_sol_val()
    print(sol_val)
    # f.write(f" Best it{best_it} sol st:{sol_val['num_st']} gr:{sol_val['num_gr']} objval:{sol_val['obj_val']}\n")
    # f.close()
    return best_sol

def gradient_descent( data, sol, i):

    # best_val = sol.get_sol()
    best_objval = get_objVal(sol.groups)
    best_sol = copy.deepcopy(sol)
    it = 0
    # print("first",  best_objval)
    # f = open(f"history_sol_grad{i}.txt","w")
    for __ in range(1): 

        new_sol = copy.deepcopy(sol)
        loc_objval = 0
        for loc in local_set:

            sol_copy = copy.deepcopy(sol)
            objval = rebuild_timetable(loc,data, sol_copy)
            # print(objval, loc)
            # f.write(f"it: {it} local {loc} sol {sol_copy.get_sol()[0]} {sol_copy.get_sol()[1]}, objval{objval} \n" )
            if loc_objval < objval:
            # if loc_objval <sol_copy.get_sol()[0]:
                new_sol = sol_copy
                loc_objval = objval
                # loc_objval = sol_copy.get_sol()[0]
                best_loc = loc
        sol = new_sol
        # print(it, loc_objval)
        # f.write(f" over it {it} best loc {best_loc}  sol {new_sol.get_sol()[0]} {new_sol.get_sol()[1]}  objval {loc_objval} \n")
       

        if best_objval < loc_objval:
        # if best_objval < new_sol.get_sol()[0]:
            best_sol = new_sol
            best_objval = loc_objval
            # best_objval = new_sol.get_sol()[0]
            # print(it, best_objval)
            it+=1
        else:
            break

    # f.write(f" Best  sol {best_sol.get_sol()[0]} {best_sol.get_sol()[1]}, best_objval , {best_objval } it { it} \n")

    # f.close()
    return best_sol

def rebuild_timetable(set_update_teachers,data, sol):

    clear_group_teachers(set_update_teachers, sol)
    
    sol.recount_group()
    set_get_students = get_index_take_student(sol)
    set_dont_get_students = get_list_comp(range(J), set_get_students)


    new_data = get_new_input_data(data, sol, set_update_teachers )


    first_path_sol = base_group(new_data)

    groups = first_path_sol['groups'] 


    base_schedule(new_data, first_path_sol)
    

  

    groups = first_path_sol['groups'] 

    for gr in groups:

        # print(gr)
        if len(gr) == 5:
            continue
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
        g.append(d_1)
        g.append(d_2)
        g.append(new_data['Set_I'][int(gr[6])])
        sol.groups.append(g)

    sol.recount_group()

    return sol.get_sol_val()


def launch():
    prob_list = [[0.1, "01" ], [0.175, "0175" ], [0,25, "025"], [0.5, "05" ], [0.75, "075"], [0.825, "0825"], [0.9, "09" ]]


    data = Data(J, L, I, T , D, r, minN, maxN, timeL )

    for i in range(1,11):
        filename_data = f"examples_copy\\orders_2_{i}.txt"

        data.read_input(filename_data)

        filename_sol = f"sol_{i}"
        sol = Solution(filename_sol)
        print(sol.get_sol_val())
        # print(rebuild_timetable(range(I),data, sol))
        print(get_objVal(sol.groups))
\
        # print(data.timeRec[10][1])
        # print(data.timeRec[10][5])
        # if i == 6:
            # sol.check_sol(data)
        # return
        # sol = local_search(15, p[0], data, sol,  name = f"histity_{i}_{j}" )
        # sol.import_JSON(f"sol_{i}")
    
    # i = 1
    # for i in range(1,5 + 1):
    #     for p in prob_list:
    #         for j in range(3, 6):
    #             filename_data = f"examples_copy\\orders_2_{i}.txt"

    #             data.read_input(filename_data)

    #             filename_sol = f"sol_{i}"
    #             sol = Solution(filename_sol)
    #             sol = local_search(15, p[0], data, sol,  name = f"histity_{i}_{j}" )
    #             sol.import_JSON(f"sol_check__p_{p[1]}_loc_{i}_{j}")
    #             print(f"        experiment {j} compled")
    #         print(f"    prob {p[0]} compled")
    #     print(f"{i} compled")

    return


    

def get_num_var_and_constr():

    sum_var = int(0)
    var = 0
    sum_var+=J*K
    sum_var+=L*K
    sum_var+=D * J * K
    sum_var+=D * timeslotsInHour * T * K * L
    sum_var+=D * timeslotsInHour * T * K * L
    sum_var+=I *  K * L
    sum_var+= I * D
    sum_var+= I * D * timeslotsInHour * T
    sum_var+= I * D * timeslotsInHour * T   
    sum_var+= I * D * timeslotsInHour * T * K * L  
    print(f"y = {J*K}, \u03C9 = { round(J*K/ sum_var * 100, 3)} %")
    print(f"z = {L*K}, \u03C9 = { round(L*K/ sum_var * 100, 3)} %")
    print(f"p = {D*J*K}, \u03C9 = { round(D*J*K/ sum_var * 100, 3 )} %")
    print(f"c = {D * timeslotsInHour * T * K * L}, \u03C9 = { round(D * timeslotsInHour * T * K * L/ sum_var * 100, 3 )} %")
    print(f"s = {D * timeslotsInHour * T * K * L}, \u03C9 = { round(D * timeslotsInHour * T * K * L/ sum_var * 100, 3 )} %")
    print(f"u = {I *  K * L}, \u03C9 = { round(I *  K * L/ sum_var * 100, 3 )} %")
    print(f"P = {I * D}, \u03C9 = { round(I * D / sum_var * 100, 3 )} %")
    print(f"C = {I * D * timeslotsInHour * T}, \u03C9 = { round(I * D * timeslotsInHour * T/ sum_var * 100, 3 )} %")
    print(f"S = {I * D * timeslotsInHour * T}, \u03C9 = { round(I * D * timeslotsInHour * T/ sum_var * 100, 3 )} %")
    print(f"U = {I * D * timeslotsInHour * T * K * L}, \u03C9 = { round(I * D * timeslotsInHour * T * K * L/ sum_var * 100, 3 )} %")
    print(f" sum_var = {sum_var}")

    sum_constr = int(0)
    num_cons = 2

    sum_constr+=J*K*L
    sum_constr+=D*timeslotsInHour * T
    sum_constr+=J
    sum_constr+=2*K*L
    sum_constr+= K * L
    sum_constr+= L * K * D
    sum_constr+=D * K * L
    sum_constr+=J * L * K           
    sum_constr+=K * L
    sum_constr+=timeslotsInHour * T * D * K * L
    sum_constr+=timeslotsInHour * T * D * K * L
    sum_constr+=I * D * timeslotsInHour * T * K * L * 3
    sum_constr+=I * D * timeslotsInHour * T               
    sum_constr+=I * D * timeslotsInHour * T    
    sum_constr+=I * D * timeslotsInHour * T * K * L 
    sum_constr+=I * K * L * D
    sum_constr+=I     
    sum_constr+=I * D * timeslotsInHour * T  
    sum_constr+=K * L
    sum_constr+=I * D * timeslotsInHour * T   
    sum_constr+=I * D * timeslotsInHour * T    
    sum_constr+=I * D  
    # (2) Если студент в группе, то он может прийти, когда у этой группы занятие,
    cons = J*K*L
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1

    #(3) В любой момент времени не может быть больше пар, чем число комнат             
    cons = D*timeslotsInHour * T
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1

    #(4) Студент может быть только в одной группе
    cons = J
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1

    #(5) Ограничения на количество студентов в группе
    cons = 2*K*L
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1

    #(6) Ограничения на два рабочих дня
    cons =  K * L
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1


    #(7) Для любой группы в любой день количесво выделеных на нее таймслотов должно равняться продолжительности занятия
    cons = L * K * D
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1

    #(8) Занятия не располагаются в соседние дни
    cons = D * K * L
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1


    #(9) Если нет группы, то и нет студента
    cons = J * L * K
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1
    
    #(10) Ограничения созданные против борьбы с симметрией
    cons = K * L
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1
    
    #(11) Ограничения на непрерывность занятия С
    cons = timeslotsInHour * T * D * K * L
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1

    #(12) Ограничения на непрерывность занятия S
    cons = timeslotsInHour * T * D * K * L
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1

    #(13) Для каждой должен будет назначит преподаватель
    cons = K * L
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1

    #(14) Расписание преподавателя для каждой группы
    cons = I * D * timeslotsInHour * T * K * L * 3
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1

    #(15) Преподаватель в любой момент времени работает только с одной группой
    cons = I * D * timeslotsInHour * T 
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1

    #(16) После занятия, у преподавателя идет перерыв 
    cons = I * D * timeslotsInHour * T * K * L 
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1

    #(17) Если у преподователя занимается группа в день d, то и он должен работать в этот день
    cons = I * K * L * D
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1

    #(18) У всех преподавателей не больше пяти рабочих дней
    cons = I 
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1
    
    #(19) Условия на задание рабочий таймслотов преподавателе S_1
    cons = I * D * timeslotsInHour * T 
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1

    #(20) Условия на задание рабочий таймслотов преподавателе S_2
    cons = I * D * timeslotsInHour * T 
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1

    #(21) Условия на задание рабочий таймслотов преподавателе C_1
    cons = I * D * timeslotsInHour * T 
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1

    #(22) Условия на задание рабочий таймслотов преподавателе C_2
    cons = I * D * timeslotsInHour * T 
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1
    
    #(23) Условия на продолжительность рабочего длня педагога
    cons = I * D 
    print(f"{num_cons}: sum_constr ={ cons}, \u03C9 = {round(cons / sum_constr * 100, 3)} %")
    num_cons += 1

    print(f" sum all constr = {sum_constr}")


if __name__ == '__main__':
    # get_num_var_and_constr()
    launch()