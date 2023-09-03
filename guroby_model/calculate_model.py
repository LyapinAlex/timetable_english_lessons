import math
import numpy as np
import gurobipy as gr
from gurobipy import GRB
import time
import json
from tabulate import tabulate

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


def read_data(name = None, i = 0):
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
    data['J'] = 500# num of studetns
    data['L'] = 13# num of course
    data['D'] = 6# num of day
    data['T'] = 11# num of timslots in the day
    data['I'] = 5# num of teachers
    data['r'] = 4# num of rooms
    data['minNumber'] = 2# min number of students in the group
    data['maxNumber'] = 8# max number of students in the group
    data['timeLessons']  = np.array([3, 3, 3, 3, 3, 4, 3, 4, 5, 5, 5, 6, 6])
    data['K'] = 10
    # data['J'] = 150
    # data['L'] = 3
    # data['D'] = 6# num of day
    # data['T'] = 11# num of timslots in the 
    # data['I'] = 3# num of teachers
    # data['r'] = 2# num of rooms
    # data['minNumber'] = 2# min number of students in the group
    # data['maxNumber'] = 6# max number of students in the group
    # data['timeLessons']  = np.array([ 4, 5, 6])


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


def main(i_num, time):
    
    # i = 1
    file_name = f"sol_{i_num}"
    # file_name = f"sol_gurobi_ex_{i_num}_time_10800"
    sol = import_json_data(file_name)

    data = read_data(f"examples_copy\\orders_2_{i_num}.txt")
    
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
            if c[d_1[0], t , k, l] + s[d_1[0], t , k, l] - p[d_1[0], k, l] == 1:
                U[i,d_1[0], t, k, l] = 1

            if c[d_2[0], t , k, l] + s[d_2[0], t , k, l] - p[d_2[0], k, l] == 1:
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


    # print(f'C:\cyrillic_characters\English_Lesson_I_{i}_K_10.lp')
    model = gr.read(f'C:\cyrillic_characters\English_Lesson_I_{i_num}_K_10_ver1.1.lp')
    # English_lesson_exp_4_time_600.sol
    # model = gr.read("C:\cyrillic_characters\English_lesson_exp_1_time_600.lp")
    model.update()

   

    # # self.y = self.model.addVars(J, K, vtype = gr.GRB.BINARY, name = "y")
    # for j in range(data['J']):
    #     for k in range(data['K']):
    #         model.getVarByName(f'y[{j},{k}]').Start = int(y[j,k])

  

    # # self.z = self.model.addVars(K, L, vtype = gr.GRB.BINARY, name = "z")
    # for k in range(data['K']):
    #     for l in range(data['L']):
    #         model.getVarByName(f'z[{k},{l}]').Start = int(z[k,l])

    # # self.c = self.model.addVars(D, T, K, L, vtype = gr.GRB.BINARY, name = "c")
    # # self.s = self.model.addVars(D, T, K, L, vtype = gr.GRB.BINARY, name = "s")
    # for d in range(data['D']):
    #     for t in range(timeslotsInHour * data['T']):
    #         for k in range(data['K']):
    #             for l in range(data['L']):
    #                 model.getVarByName(f'c[{d},{t},{k},{l}]').Start = int(c[d,t,k,l])
    #                 model.getVarByName(f's[{d},{t},{k},{l}]').Start = int(s[d,t,k,l])
        
    
    # # self.p = self.model.addVars(D, K, L, vtype = gr.GRB.BINARY, name = "p")
    # for d in range(data['D']):
    #     for k in range(data['K']):
    #         for l in range(data['L']):
    #             model.getVarByName(f'p[{d},{k},{l}]').Start = int(p[d,k,l])
        


    # # # Преводаватели

    # # self.u = self.model.addVars(I, K, L, vtype = gr.GRB.BINARY, name = "u")
    # for i in  range(data['I']):
    #     for k in range(data['K']):
    #         for l in range(data['L']):
    #             model.getVarByName(f'u[{i},{k},{l}]').Start = int(u[i,k,l])

    # # self.P = self.model.addVars(I, D, vtype = gr.GRB.BINARY, name = "P")
    # for i in range(data['I']):
    #     for d in range(data['D']):
    #         model.getVarByName(f'P[{i},{d}]').Start = int(P[i,d])


    # # self.U = self.model.addVars(I, D, T, K, L, vtype = gr.GRB.BINARY, name = "U")
    # for i in range(data['I']):
    #     for d in range(data['D']):
    #         for t in range(timeslotsInHour * data['T']):
    #             for k in range(data['K']):
    #                 for l in range(data['L']):
    #                     model.getVarByName(f'U[{i},{d},{t},{k},{l}]').Start = int(U[i,d,t,k,l])

    # # self.S = self.model.addVars(I, D, T, vtype = gr.GRB.BINARY, name = "S")
    # # self.C = self.model.addVars(I, D, T, vtype = gr.GRB.BINARY, name = "C")
    # for i in range(data['I']):
    #     for d in range(data['D']):
    #         for t in range(timeslotsInHour * data['T']):
    #             model.getVarByName(f'S[{i},{d},{t}]').Start = int(S[i,d,t])
    #             model.getVarByName(f'C[{i},{d},{t}]').Start = int(C[i,d,t])

    # model.update()
    model.Params.logFile = f"consol_pure_sol_{i_num}_time_{time}_ver1.1.txt"
    model.params.TimeLimit = time
    model.update()
    # for l in range(5):
    #     # model.params.TimeLimit = 60*60
    #     # model.update()
    model.optimize()
    groups = get_alg_sol(model, data)
    import_JSON(groups, name = f"pure_sol_gurobi_ex_{i_num}_time_{time}_ver1.1")
    # model.write(f"English_lesson_exp_{i_num}_time_{2*60*10}.lp")







if __name__ == "__main__":
    
    time_work = 60*60
    for i in range(1, 6):
        main(i, time_work)
    time_work = 60*60*2
    for i in range(1, 6):
        main(i, time_work)

    