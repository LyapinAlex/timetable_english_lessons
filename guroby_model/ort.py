from ortools.sat.python import cp_model
import pandas as pd
import numpy as np
import pdb
import json

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

    # print(a[0])
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
    data['timeslot_of_students'] = np.fromstring(input_str_a, dtype = int, sep = ' ').reshape((data['J'], data['D'], data['T']))

    return data

J = np.arange(0, 500, 1) # Заявки
K = np.arange(0, 25, 1) # Количество групп
L = np.arange(0, 13, 1) # Множество курсов
D = np.arange(0, 6, 1) # Рабочие дни
T = np.arange(0, 44, 1) # Множество временных слотов
I = np.arange(0, 5, 1) # Множество преподователь 
r = 4 # Количество комнат

F = [] # Штрафы на создание каждой новой группы, созданно для борьбы с симметрией
for i in range(0, 13):
  F.append([])
for i in K:
  if ( i < 1):
    F[0].append(0)
    F[1].append(0)
    F[12].append(0)
    F[11].append(0)
  else:
    F[0].append(2.5)
    F[1].append(2.5)
    F[12].append(2.5)
    F[11].append(2.5)

for i in K:
  if ( i < 3):
    F[2].append(0)
    F[3].append(0)
    F[4].append(0)
    F[8].append(0)
    F[10].append(0)
    F[9].append(0)
  else:
    F[2].append(2.5)
    F[3].append(2.5)
    F[10].append(2.5)
    F[9].append(2.5)
    F[4].append(2.5)
    F[8].append(2.5)

for i in K:
  if ( i < 5):
    F[5].append(0)
    F[6].append(0)
    F[7].append(0)
    
  else:
    F[5].append(2.5)
    F[6].append(2.5)
    F[7].append(2.5)


F=np.array(F)

def get_index(list):
    return pd.MultiIndex.from_product(list)

def main(i, K):
    # Read input data
    data = read_data(f"examples_copy\\orders_2_{i}.txt")
    a = restruct(data['J'], data['D'], data['T'], data['L'], data['timeLessons'], data['timeslot_of_students'], data['course_of_students']  )
    b = data['course_of_students'] 
    lt = data['timeLessons']


    # Create the mip solver
    model = cp_model.CpModel()
    assert model
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 3600*24


    # Create variable

    y = model.NewBoolVarSeries(name = "y", index=get_index([J, K]))
    z = model.NewBoolVarSeries(name = "z", index=get_index([K, L]))
    c = model.NewBoolVarSeries(name = "c", index=get_index([D, T, K, L]))
    s = model.NewBoolVarSeries(name = "s", index=get_index([D, T, K, L]))
    p = model.NewBoolVarSeries(name = "p", index=get_index([D, K, L]))


    # u = model.NewBoolVarSeries(name = "u", index=get_index([I, K, L]))
    # P = model.NewBoolVarSeries(name = "P", index=get_index([I, D]))
    # U = model.NewBoolVarSeries(name = "U", index=get_index([I, D, T, K, L]))
    # S = model.NewBoolVarSeries(name = "S", index=get_index([I, D, T]))
    # C = model.NewBoolVarSeries(name = "C", index=get_index([I, D, T]))
   
    model.Maximize(sum(y[j, k] for k in K for j in J) - sum(F[l,k]*z[k, l] for k in K for l in L))



    for j in J:
        for k in K:
            model.Add(sum(b[j, l]*a[j, d, t]*(c[d, t, k, l] +  s[d, t, k, l] - p[d, k, l]) for d in D for t in T for l in L) >= sum(2*b[j, l]* lt[l] * y[j, k] for l in L ))
    for d in D:
        for t in T:
            model.Add(sum((c[d, t, k, l] +  s[d, t, k, l] - p[d, k, l])for k in K for l in L) <= r)

    for j in J:
        model.Add(sum(y[j, k] for k in K) <= 1)   
    
    for k in K:
        for l in L:
            model.Add(sum(y[j, k]*b[j, l] for j in J) <= 8)
    for k in K:
        for l in L:
            model.Add(sum(y[j, k]*b[j, l] for j in J) >= 2* z[k,l])
    for l in L:
        for k in K:
            for d in D:
                model.Add(sum((c[d, t, k, l] +  s[d, t, k, l])for t in T) == (len(T) + lt[l])*p[d, k, l])  
    D_w = np.arange(0, len(D) - 1, 1)
    for d in D_w:
        for k in K:
            for l in L:
                model.Add(p[d, k, l] + p[d + 1, k ,l] <= 1)       

    for j in J:
        for l in L:
            for k in K:
                model.Add(z[k,l] >= y[j,k]*b[j,l])

    K_l = np.arange(0, len(K) - 1, 1)
    for l in L:
        for k in K_l:
            model.Add(z[k,l] >= z[k + 1,l])

    T_1 = np.arange(0, len(T) - 1, 1) 
    for d in D:
        for t in T_1:
            for k in K:
                for l in L:
                    model.Add(s[d, t, k, l] <= s[d, t + 1, k, l])

    for d in D:
        for t in T_1:
            for k in K:
                for l in L:
                    model.Add(c[d, t, k, l] >= c[d, t + 1, k, l])

    for l in L:
        for k in K:
            model.Add(sum((p[d, k, l]) for d in D) == 2*z[k,l])

    res = read_sol("ortools_1")
        # y
    for key, val in res['y'].items():
        index = key[1:-1].split(',')
        j = int(index[0])
        k = int(index[1])
        model.AddHint(y[j,k], val)

    # z
    for key, val in res['z'].items():
        index = key[1:-1].split(',')
        k = int(index[0])
        l = int(index[1])
        model.AddHint(z[k,l], val)
    
    # s
    for key, val in res['s'].items():
        index = key[1:-1].split(',')
        d = int(index[0])
        t = int(index[1])
        k = int(index[2])
        l = int(index[3])
        model.AddHint(s[d,t,k,l], val)
    # c
    for key, val in res['c'].items():
        index = key[1:-1].split(',')
        d = int(index[0])
        t = int(index[1])
        k = int(index[2])
        l = int(index[3])
        model.AddHint(c[d,t,k,l], val)
    # p
    for key, val in res['p'].items():
        index = key[1:-1].split(',')
        d = int(index[0])
        k = int(index[1])
        l = int(index[2])
        model.AddHint(p[d,k,l], val)


    # for l in L:
    #     for k in K:
    #         model.Add(sum((u[i, k, l]) for i in I) == z[k,l])


    # for i in I:
    #     for d in D:
    #         for t in T:
    #             for k in K:
    #                 for l in L:
    #                     model.Add(U[i, d, t, k, l] <= c[d, t, k, l] +  s[d, t, k, l] - p[d, k, l])
    #                     model.Add(U[i, d, t, k, l] <= u[i, k, l])
    #                     model.Add(c[d, t, k, l] +  s[d, t, k, l] - p[d, k, l] + u[i, k, l] - U[i, d, t, k, l] <= 1)

  

    # for i in I:
    #     for d in D:
    #         for t in T:
    #             model.Add(sum(U[i, d, t, k, l] for k in K for l in L) <= 1)


    # for i in I:
    #     for d in D:
    #         for t in T:
    #             for k_1 in K:
    #                 for l_1 in L:
    #                     if t >= len(T) - 1:
    #                         continue
    #                     model.Add(sum(U[i, d, t, k, l] for k in K for l in L) <= c[d, t, k_1, l_1] +  s[d, t, k_1, l_1] - p[d, k_1, l_1] + 1 - U[i, d, t + 1, k_1, l_1] )
                        


    # for i in I:
    #     for k in K:
    #         for l in L:
    #             for d in D:
    #                 model.Add(p[d, k, l] + u[i, k, l] - P[i, d] <= 1)

    # for i in I:
    #     model.Add(sum( P[i, d] for d in D) <= 5)


    # for i in I:
    #     for d in D:
    #         for t in T:
    #             model.Add(sum(U[i, d, t, k, l] for k in K for l in L) <= S[i, d, t]  )

    #             model.Add(sum(U[i, d, t, k, l] for k in K for l in L) <= C[i, d, t]  )

    #             if t + 1 == len(T):
    #                 continue
    #             model.Add(S[i, d, t] <= S[i, d, t + 1])

    #             model.Add(C[i, d, t] >= C[i, d, t + 1])


    # for i in I:
    #     for d in D:
    #         model.Add(sum((C[i, d, t] +  S[i, d, t])for t in T) <= (len(T) + 32*P[i, d]))

    # solution_printer = cp_model.VarArrayAndObjectiveSolutionPrinter([y, z])
    solver.parameters.log_search_progress = True
    status = solver.Solve(model)



    # save sol
    dict_result = {}
    result_y = {}
    for key, val in y.items():
        sol = solver.Value(val)  # Достаем значение переменной
        result_y[str(key)] = sol
    dict_result['y'] = result_y

    result_z = {}
    for key, val in z.items():
        sol = solver.Value(val)  # Достаем значение переменной
        result_z[str(key)] = sol
    dict_result['z'] = result_z

    result_c = {}
    for key, val in c.items():
        sol = solver.Value(val)  # Достаем значение переменной
        result_c[str(key)] = sol
    dict_result['c'] = result_c

    result_s = {}
    for key, val in s.items():
        sol = solver.Value(val)  # Достаем значение переменной
        result_s[str(key)] = sol
    dict_result['s'] = result_s

    result_p = {}
    for key, val in p.items():
        sol = solver.Value(val)  # Достаем значение переменной
        result_p[str(key)] = sol
    dict_result['p'] = result_p


    save_sol(dict_result)

    print(solver.ObjectiveValue())

def setup_hint(model, res, y, z, s, c, p):
    # y
    for key, val in res['y'].items():
        index = key[1:-1].split(',')
        j = int(index[0])
        k = int(index[1])
        model.AddHint(y[j,k], val)

    # z
    for key, val in res['z'].items():
        index = key[1:-1].split(',')
        k = int(index[0])
        l = int(index[1])
        model.AddHint(z[k,l], val)
    
    # s
    for key, val in res['s'].items():
        index = key[1:-1].split(',')
        d = int(index[0])
        t = int(index[1])
        k = int(index[2])
        l = int(index[3])
        model.AddHint(s[d,t,k,l], val)
    # c
    for key, val in res['c'].items():
        index = key[1:-1].split(',')
        d = int(index[0])
        t = int(index[1])
        k = int(index[2])
        l = int(index[3])
        model.AddHint(c[d,t,k,l], val)
    # p
    for key, val in res['p'].items():
        index = key[1:-1].split(',')
        d = int(index[0])
        t = int(index[1])
        k = int(index[2])
        model.AddHint(p[d,k,l], val)


def read_sol(name):

    with open(name + '.json') as file:
        sol = json.load(file)
    return sol

def save_sol(res, name = "ortools_1"):

    with open(name+'.json','w') as file:
        json.dump(res, file, indent= 3)

if __name__ == "__main__":
    main(1, range(10))