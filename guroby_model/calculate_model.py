import math
import numpy as np
import gurobipy as gr
from gurobipy import GRB
import time
import json
from tabulate import tabulate
from model_schedule import *
from solution import *
from data import *



# data = {}
# data['J'] = 500# num of studetns
# data['L'] = 13# num of course
# data['D'] = 6# num of day
# data['T'] = 44# num of timslots in the day
# data['I'] = 5# num of teachers
# data['r'] = 4# num of rooms
# data['K'] = 10
# timeLessons = np.array([3, 3, 3, 3, 3, 4, 3, 4, 5, 5, 5, 6, 6])
# data['J'] = 150
# data['L'] = 3
# data['K'] = 15
# data['D'] = 6# num of day
# data['T'] = 11# num of timslots in the 
# data['I'] = 3# num of teachers
# data['r'] = 2# num of rooms
# data['minNumber'] = 2# min number of students in the group
# data['maxNumber'] = 6# max number of students in the group
# data['timeLessons']  = np.array([ 4, 5, 6])

timeslotsInHour = 4

def import_JSON(groups, name = "sol"):
    """Создать json файл решенея"""
    list_gr = []

    for gr in groups:
        
        g = []
        g.append(gr[0])
        g.append(int(gr[1]))
        d_1 = [int(gr[3][0]), int(gr[3][1]), int(gr[3][2])]
        d_2 = [int(gr[4][0]), int(gr[4][1]), int(gr[4][2])]
        g.append(int(gr[2]))
        g.append( d_1)
        g.append( d_2)
        g.append(int(gr[5]))
        list_gr.append(g)


    with open(name+'.json','w') as file:
        json.dump(list_gr, file, indent= 3)

def restruct(J, D, T, L, tl, A, B ):
    
    k = 4

    a = np.zeros((J, D, k*T))

    for j in range(J):
        for l in range(L):
            if B[j,l] == 1:
                for d in range(D):
                    for t in range(T):
                        if A[j,d,t] == 1:
                            a[j,d,k*t] = 1
                            a[j,d,k*t+ 1] = 1
                            a[j,d,k*t + 2] = 1
                            a[j,d,k*t+ 3] = 1
                            for t_p in range(tl[l]):
                                if k*t+ k-1 + t_p == k*T:
                                    break
                                else:
                                     a[j,d,k*t+ k-1 + t_p] = 1

    return a


def read_data(name = None, k = 10, i = 0):
    if name == None:
        return 0
    file_name = name
    #     data = read_data("examples_copy\\orders_2_1.txt")

    # file_nam e = f"examples_copy\\orders_2_{i}.txt"
    fileOrders = open(file_name)
    orders = fileOrders.readlines()
    input_str_a = orders[3]
    input_str_b = orders[1]

    fileOrders.close()

    data = {}
    # data['J'] = 500# num of studetns
    # data['L'] = 13# num of course
    # data['D'] = 6# num of day
    # data['T'] = 11# num of timslots in the day
    # data['I'] = 5# num of teachers
    # data['r'] = 4# num of rooms
    # data['minNumber'] = 2# min number of students in the group
    # data['maxNumber'] = 8# max number of students in the group
    # data['timeLessons']  = np.array([3, 3, 3, 3, 3, 4, 3, 4, 5, 5, 5, 6, 6])
    data['K'] = k
    data['J'] = 150
    data['L'] = 3
    data['D'] = 6# num of day
    data['T'] = 11# num of timslots in the 
    data['I'] = 3# num of teachers
    data['r'] = 2# num of rooms
    data['minNumber'] = 2# min number of students in the group
    data['maxNumber'] = 6# max number of students in the group
    data['timeLessons']  = np.array([ 4, 5, 6])

       
    # data['J'] = 300# num of studetns
    # data['L'] = 8# num of course
    # data['D'] = 6# num of day
    # data['T'] = 11# num of timslots in the day
    # data['I'] = 4# num of teachers
    # data['r'] = 3# num of rooms
    # data['minNumber'] = 2# min number of students in the group
    # data['maxNumber'] = 6# max number of students in the group
    # data['timeLessons']  = np.array([3, 3, 4, 4, 5 ,5, 6, 6])



    data['course_of_students'] = np.fromstring(input_str_b, dtype = int, sep = ' ').reshape((data['J'], data['L']))
    # data['timeslot_of_students'] = np.fromstring(input_str_a, dtype = int, sep = ' ').reshape((data['J'], data['D'], data['T']))


    a = np.fromstring(input_str_a, dtype = int, sep = ' ').reshape((data['J'], data['D'], data['T']))
    data['timeslot_of_students'] = restruct(data['J'], data['D'], data['T'], data['L'], data['timeLessons'], a, data['course_of_students'] )

    return data


def import_json_data(filename = 'sol'):

    with open(filename + '.json') as f:
        sol = json.load(f)
    
    return sol

def get_gurobi_sol(sol, data):
    y = np.zeros( (data['J'], data['K']) )
    z = np.zeros( (data['K'], data['L']) )
    s = np.zeros( (data['D'], timeslotsInHour * data['T'], data['K'], data['L']) )
    c = np.zeros( (data['D'], timeslotsInHour * data['T'], data['K'], data['L']) )
    p = np.zeros( (data['D'], data['K'], data['L']))

    u = np.zeros( (data['I'], data['K'], data['L']) )
    U = np.zeros( (data['I'], data['D'], timeslotsInHour * data['T'], data['K'], data['L']) )
    S = np.zeros( (data['I'], data['D'], timeslotsInHour * data['T']) )
    C = np.zeros( (data['I'], data['D'], timeslotsInHour * data['T']) )
    P = np.zeros( (data['I'], data['D']) )

    for group in sol:

        list_students = group[0]
        k = group[1] - 1
        l = group[2]
        i = group[5]
        d_1 =group[3]
        d_2 = group[4]

        for j in list_students:
            y[j,k] = 1 

        z[k,l] = 1

        for t in range(timeslotsInHour * data['T']):
            if t >= d_1[1]:
                s[d_1[0], t , k, l] = 1
            if t >= d_2[1]:
                s[d_2[0], t , k, l] = 1


        for t in range(timeslotsInHour * data['T']):
            if t <= d_1[2]:
                c[d_1[0], t , k, l] = 1
            if t <= d_2[2]:
                c[d_2[0], t , k, l] = 1

        p[d_1[0], k, l] = 1
        p[d_2[0], k, l] = 1

        u[i, k, l] = 1
        
        P[i,d_1[0]] = 1
        P[i,d_2[0]] = 1

        for t in range(timeslotsInHour * data['T']):
            if c[d_1[0], t , k, l] + s[d_1[0], t , k, l] == 2:
                U[i,d_1[0], t, k, l] = 1

            if c[d_2[0], t , k, l] + s[d_2[0], t , k, l] == 2:
                U[i,d_2[0], t, k, l] = 1

        for t in range(timeslotsInHour * data['T']):
            if t >= d_1[1]:
                S[i, d_1[0], t] = 1
            if t >= d_2[1]:
                S[i, d_2[0], t] = 1


        for t in range(timeslotsInHour * data['T']):
            if t <= d_1[2]:
                C[i, d_1[0], t] = 1
            if t <= d_2[2]:
                C[i, d_2[0], t] = 1 

def get_alg_sol(model, data):

    groups = []

    for k in  range(data['K']):
        for l in range(data['L']):
            z = model.getVarByName(f'z[{k},{l}]').X
            if z == 1:
                # group = []

                list_students = []
                for j in range(data['J']):
                    y = model.getVarByName(f'y[{j},{k}]').X
                    course = data['course_of_students'][j][l]

                    if y == 1 and course == 1:
                        list_students.append(j)

                teacher = None
                for i in range(data['I']):
                    u = model.getVarByName(f'u[{i},{k},{l}]').X
                    if u == 1:
                        teacher = i

                day_1 = None
                day_2 = None

                for d in range(data['D']):
                    p = model.getVarByName(f'p[{d},{k},{l}]').X
                    if p == 1:
                        if day_1 == None:
                            day_1 = d
                        else:
                            day_2 = d

                
                day_1_time_begin = None
                day_2_time_begin = None
                # day_1_time_end = None
                # day_2_time_end = None

                for t in range( timeslotsInHour * data['T']):
                    x_1 = int(model.getVarByName(f'c[{day_1},{t},{k},{l}]').X) + int(model.getVarByName(f's[{day_1},{t},{k},{l}]').X) - int(model.getVarByName(f'p[{day_1},{k},{l}]').X)
                    if x_1 == 1:
                        day_1_time_begin = t
                        break
                    

                for t in range(timeslotsInHour * data['T']):
                    x_2 = int(model.getVarByName(f'c[{day_2},{t},{k},{l}]').X) + int(model.getVarByName(f's[{day_2},{t},{k},{l}]').X) - int(model.getVarByName(f'p[{day_2},{k},{l}]').X)
                    if x_2 == 1:
                        day_2_time_begin = t
                        break

                dur_lesson = data['timeLessons'][l]


                group = [list_students, k + 1, l, [day_1, day_1_time_begin, day_1_time_begin + dur_lesson - 1], [day_2, day_2_time_begin, day_2_time_begin + dur_lesson - 1], teacher]

                groups.append(group)

                # print(group)

    return groups


def main(i_num, k_num, time = 3600):
    
    # i_num = 1
    # dim = 1
    data = Data(J, L, I, T , D, r, minN, maxN, timeL )
    # filename_data = f"examples_copy\\orders_2_{i_num}.txt"
    filename_data = f"examples_copy\\orders_4_{i_num}.txt"
    data.read_input(filename_data)
    # file_name = f"sol_ex_{i_num}_dim_{dim}.json"

    # sol = Solution(file_name)

    # print(sol.check_sol_alg(data))
    # print(sol.check_sol_math_model(data))

    # K = np.zeros(L)
    # for group in sol.groups:
    #     K[group[2]]+=1

    # print(K)

    # # data = read_data(f"examples_copy\\orders_1_{i_num}.txt", k=k_num)
    

    model_name = f"English_Lesson_K_{k_num}_EX_{i_num}_ver4.lp"

    # model_name= "English_Lesson_K_7_EX_1_ver4.lp"
    # model_name = "test.lp"

    # model_name = f"English_Lesson_L_{str(k_num)}_EX_{i_num}_ver5.lp"
    model = gr.read(model_name)


    # sol_name = f"S_K_{k_num}_EX_{i_num}_ver4.1.sol"
    # sol_name = "S_K_6_EX_1_ver4.1.sol"
    # sol_name = "alg_1_dim_1.sol"
    # sol_name = "test_sol.sol"
    # # # Чтение решения
    # model.read(sol_name)
    # model.update()



    # # self.y = self.model.addVars(J, K, vtype = gr.GRB.BINARY, name = "y")
    # for j in range(data.J):
    #     for k in range( k_num):
    #         model.getVarByName(f'y[{j},{k}]').Start = int(sol.y[j,k])

  

    # # self.z = self.model.addVars(K, L, vtype = gr.GRB.BINARY, name = "z")
    # for k in range( k_num):
    #     for l in range(data.L):
    #         model.getVarByName(f'z[{k},{l}]').Start = int(sol.z[k,l])

    # # self.c = self.model.addVars(D, T, K, L, vtype = gr.GRB.BINARY, name = "c")
    # # self.s = self.model.addVars(D, T, K, L, vtype = gr.GRB.BINARY, name = "s")
    # for d in range(data.D):
    #     for t in range(timeslotsInHour * data.T):
    #         for k in range( k_num):
    #             for l in range(data.L):
    #                 model.getVarByName(f'c[{d},{t},{k},{l}]').Start = int(sol.c[d,t,k,l])
    #                 model.getVarByName(f's[{d},{t},{k},{l}]').Start = int(sol.s[d,t,k,l])
        
    
    # # self.p = self.model.addVars(D, K, L, vtype = gr.GRB.BINARY, name = "p")
    # for d in range(data.D):
    #     for k in range( k_num):
    #         for l in range(data.L):
    #             model.getVarByName(f'p[{d},{k},{l}]').Start = int(sol.p[d,k,l])
        


    # # # Преводаватели

    # # self.u = self.model.addVars(I, K, L, vtype = gr.GRB.BINARY, name = "u")
    # for i in  range(data.I):
    #     for k in range( k_num):
    #         for l in range(data.L):
    #             model.getVarByName(f'u[{i},{k},{l}]').Start = int(sol.u[i,k,l])

    # # self.P = self.model.addVars(I, D, vtype = gr.GRB.BINARY, name = "P")
    # for i in range(data.I):
    #     for d in range(data.D):
    #         model.getVarByName(f'P[{i},{d}]').Start = int(sol.P[i,d])


    # # self.U = self.model.addVars(I, D, T, K, L, vtype = gr.GRB.BINARY, name = "U")
    # for i in range(data.I):
    #     for d in range(data.D):
    #         for t in range(timeslotsInHour * data.T):
    #             for k in range( k_num):
    #                 for l in range(data.L):
    #                     model.getVarByName(f'U[{i},{d},{t},{k},{l}]').Start = int(sol.U[i,d,t,k,l])


    # for i in range(data.I):
    #     for d in range(data.D):
    #         for t in range(timeslotsInHour * data.T):
    #             model.getVarByName(f'S[{i},{d},{t}]').Start = int(sol.S[i,d,t])
    #             model.getVarByName(f'C[{i},{d},{t}]').Start = int(sol.C[i,d,t])



    # model.update()

    model.Params.logFile = f"consol_sol_{i_num}_time_{time}_K_{str(k_num)}_EX_{i_num}_ver4.1.txt"
    model.Params.logFile = "test_info.txt"
    model.params.TimeLimit = time
    # model.setParam("Method", 2)
    # model.setParam("MIPFocus", 3)
    model.update()
    # for l in range(5):
    #     # model.params.TimeLimit = 60*60
    #     # model.update()
    model.optimize()
    
    # model.write(f"English_Lesson_K_{k_num}_EX_{i_num}_ver4.1.sol")  
    model.write(f"test_sol1.sol") 


    groups = get_gurobi_sol_in_alg_sol(model, data)
    sol = Solution(group=groups)
    # if not sol.check_sol_alg(data):
    #     raise
    # if not sol.check_sol_math_model(data):
    #     raise
    # print(k_num, i_num)
    print(sol.check_sol_alg(data))
    print(sol.check_sol_math_model(data))

    # K = np.zeros(L)
    # for group in groups:
    #     K[group[2]]+=1

    # print(K)






def get_gurobi_sol_in_alg_sol(model, data):

    groups = []
    groups_id = []
    for k in range(K):
        for l in range(L):
            try:
                z = int(model.getVarByName(f'z[{k},{l}]').X)
                # print(z)
                if z == 0:
                    break
                else:
                    groups_id.append([k,l])

            except:
                break
    
    for id in groups_id:
        gr = []
        k = id[0]
        l = id[1]

        st_list = []

        for j in range(J):
            course_st = data.courseRec[j][l]
            if course_st == 0:
                continue
            else:
                y = int(model.getVarByName(f'y[{j},{k}]').X)
                if y == 1:
                   st_list.append(j)

        gr.append(st_list)
        gr.append(k+1)
        gr.append(l)

        d_1 = []
        d_2 = []

        for d in range(D):
            p = int(model.getVarByName(f'p[{d},{k},{l}]').X)
            if p == 1:
                if d_1 == []:
                    d_1.append(d)
                else:
                    d_2.append(d)
                    break
        
            
        d = d_1[0]
        t_1 = None
        t_2 = None
        for t in range(timeslotsInHour*T):
            if (  int(model.getVarByName(f'c[{d},{t},{k},{l}]').X) + int(model.getVarByName(f's[{d},{t},{k},{l}]').X) - int(model.getVarByName(f'p[{d},{k},{l}]').X)) == 1:
                if t_1 == None:
                    t_1 = t

            if (  int(model.getVarByName(f'c[{d},{t},{k},{l}]').X) + int(model.getVarByName(f's[{d},{t},{k},{l}]').X) - int(model.getVarByName(f'p[{d},{k},{l}]').X)) == 0:
                if t_1 != None:
                    t_2 = t
                    break
        d_1.append(t_1)
        if t_2 == None:
            t_2 = timeslotsInHour*T
        d_1.append(t_2 - 1)

        d = d_2[0]
        t_1 = None
        t_2 = None
        for t in range(timeslotsInHour*T):
            if (  int(model.getVarByName(f'c[{d},{t},{k},{l}]').X) + int(model.getVarByName(f's[{d},{t},{k},{l}]').X) - int(model.getVarByName(f'p[{d},{k},{l}]').X)) == 1:
                if t_1 == None:
                    t_1 = t

            if (  int(model.getVarByName(f'c[{d},{t},{k},{l}]').X) + int(model.getVarByName(f's[{d},{t},{k},{l}]').X) - int(model.getVarByName(f'p[{d},{k},{l}]').X)) == 0:
                if t_1 != None:
                    t_2 = t
                    break
        d_2.append(t_1)
        if t_2 == None:
            t_2 = timeslotsInHour*T
        d_2.append(t_2 - 1)


        gr.append(d_1)
        gr.append(d_2)

        for i in range(I):
            u = int(model.getVarByName(f'u[{i},{k},{l}]').X)
            if u == 1:
                gr.append(i)
                break
        
        groups.append(gr)
        
    
    return groups





if __name__ == "__main__":
    
    
    # main(1,1,3600)
    # for k in range(2,10):
    # k = 6

    # main(1, 6, 10)
    # for i in range(1, 11):
    # for k in range(4,5):
    # for i in range(1,4):
    #     for k in range(7,11):
    #     # k = 8
    #         main(i, k, 3600)

    for i in range(3):
        for k in range(6,10):
            main(i + 1 , k + 1, 3600)
    