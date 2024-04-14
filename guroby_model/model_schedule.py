import math
import json
import numpy as np
import gurobipy as gr
from params import *
from gurobipy import GRB
import time
from tabulate import tabulate

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

def import_json_data(filename = 'sol'):

    with open(filename + '.json') as f:
        sol = json.load(f)
    
    return sol

def read_data(name = None, i = 0):
    if name == None:
        return 0
    file_name = name
    #     data = read_data("examples_copy\\orders_2_1.txt")

    # file_name = f"examples_copy\\orders_2_{i}.txt"
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
    data['J'] = J
    data['L'] = L
    data['D'] = D# num of day
    data['T'] = T# num of timslots in the 
    data['I'] = I# num of teachers
    data['r'] = r# num of rooms
    data['minNumber'] = minN# min number of students in the group
    data['maxNumber'] = maxN# max number of students in the group
    data['timeLessons']  = timeL



    # новая яразмерность
   
    # data['J'] = 300# num of studetns
    # data['L'] = 4# num of course
    # data['D'] = 6# num of day
    # data['T'] = 8# num of timslots in the day
    # data['I'] = 3# num of teachers
    # data['r'] = 2# num of rooms
    # data['minNumber'] = 2# min number of students in the group
    # data['maxNumber'] = 6# max number of students in the group
    # data['timeLessons']  = np.array([3, 4, 5 , 6])



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
    data['timeslot_of_students'] = np.fromstring(input_str_a, dtype = int, sep = ' ').reshape((data['J'], data['D'], data['T']))

    return data




def cb(model, where):
    if where == GRB.Callback.MIPNODE:
        # Get model objective
        obj = model.cbGet(GRB.Callback.MIPNODE_OBJBST)

        # Has objective changed?
        if abs(obj - model._cur_obj) > 1e-8:
            # If so, update incumbent and time
            model._cur_obj = obj
            model._time = time.time()

    # Terminate if objective has not improved in 20s
    if time.time() - model._time > 60*30:
        model.terminate()


# J = np.arange(0, 150, 1) # Заявки
# # K = np.arange(0, 6, 1) # Количество групп
# L = np.arange(0, 3, 1) # Множество курсов
# D = np.arange(0, 6, 1) # Рабочие дни
# T = np.arange(0, 44, 1) # Множество временных слотов
# I = np.arange(0, 3, 1) # Множество преподователь 
# r = 2 # Количество комнат
# J = np.arange(0, 500, 1) # Заявки
# K = np.arange(0, 25, 1) # Количество групп
# L = np.arange(0, 13, 1) # Множество курсов
# D = np.arange(0, 6, 1) # Рабочие дни
# T = np.arange(0, 44, 1) # Множество временных слотов
# I = np.arange(0, 5, 1) # Множество преподователь 
# r = 4 # Количество комнат


# новая яразмерность
# J = np.arange(0, 300, 1) # Заявки
# K = np.arange(0, 10, 1) # Количество групп
# L = np.arange(0, 8, 1) # Множество курсов
# D = np.arange(0, 6, 1) # Рабочие дни
# T = np.arange(0, 4*11, 1) # Множество временных слотов
# I = np.arange(0, 4, 1) # Множество преподователь 
# r = 3 # Количество комнат


# F=np.array(F)
# # ДЛЯ РАЗМЕРНОСТИ(150  ЛЮДЕЙ)
# F = np.array([[0,0,0,0,2.5,2.5,2.5,2.5,2.5,2.5],
#               [0,0,0,0,0,2.5,2.5,2.5,2.5,2.5],
#               [0,0,0,0,2.5,2.5,2.5,2.5,2.5,2.5]])



# ДЛЯ НОВОЙ РАЗМЕРНОСТИ(300 ЛЮДЕЙ)
# F = np.array([[0,0,0,2.5,2.5,2.5,2.5,2.5,2.5,2.5],
#               [0,0,0,0,2.5,2.5,2.5,2.5,2.5,2.5],
#               [0,0,0,0,2.5,2.5,2.5,2.5,2.5,2.5],
#               [0,0,0,0,0,2.5,2.5,2.5,2.5,2.5],
#               [0,0,0,0,0,2.5,2.5,2.5,2.5,2.5],
#               [0,0,0,0,2.5,2.5,2.5,2.5,2.5,2.5],
#               [0,0,0,0,2.5,2.5,2.5,2.5,2.5,2.5],
#               [0,0,0,2.5,2.5,2.5,2.5,2.5,2.5,2.5]])

# ДЛЯ НОВОЙ РАЗМЕРНОСТИ(500 ЛЮДЕЙ)
# F = np.array([[0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5],
#               [0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5],
#               [0,   0,   0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5],
#               [0,   0,   0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5],
#               [0,   0,   0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5],
#               [0,   0,   0,   0,   0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5],
#               [0,   0,   0,   0,   0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5],
#               [0,   0,   0,   0,   0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5],
#               [0,   0,   0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5],
#               [0,   0,   0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5],
#               [0,   0,   0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5],
#               [0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5],
#               [0, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5]])

class Problem:

    def __init__(self,i, K, course = None):
        self.i = i
        # str = f"C:/Users/Александр/source/vscode_project/Operation research/examples_copy/orders_2_{i}.txt"
        # f"examples_copy\\orders_hand_make.txt"
        # data = read_data("examples_copy\\orders_hm.txt")
        data = read_data(f"examples_copy\\orders_2_{i}.txt")
        if course == None:
            self.a =restruct(data['J'], data['D'], data['T'], data['L'], data['timeLessons'], data['timeslot_of_students'], data['course_of_students']  )
            self.b = data['course_of_students'] 
            self.lt = data['timeLessons']


        capacity = np.sum(data['course_of_students'], axis=0)
       
        Z = []
        for l in range(L):
            Z.append(math.ceil(capacity[l]/ 4))
   

        # else:
        #     A = restruct(data['J'], data['D'], data['T'], data['L'], data['timeLessons'], data['timeslot_of_students'], data['course_of_students']  )

        #     data['L'] = len(course)
        #     L = len(course)


        #     st_list = []
        #     for j in range(data['J']):
        #         for l in course:
        #             if data['course_of_students'][j][l] == 1:
        #                 st_list.append(j)


        #     data['J'] = len(st_list)
        #     J = len(st_list)


        #     self.b = np.zeros((J, L ), dtype=np.int8)
        #     for j in range(J):
        #         for l in range(L):
        #             if data['course_of_students'][st_list[j]][course[l]] == 1:
        #                 self.b[j,l] = 1 

        #     tl = []
        #     for l in course:
        #         tl.append(data['timeLessons'][l])
        #     data['timeLessons'] = tl
        #     self.lt = tl

        #     self.a = np.zeros((J, D, timeslotsInHour*T))
        #     for j in range(J):
        #         for d in range(D):
        #             for t in range(timeslotsInHour*T):
        #                 self.a[j,d,t] = A[st_list[j],d,t]
            
        # Иницализация моедли
        # self.model = gr.Model("Schedule creating") 
        self.model = gr.Model("Schedule") 
        self.model.Params.logFile = f"consol_info_{i}"
        # Переменые 
        # print(K)
        # Группа
        self.y = self.model.addVars(range(J), range(K), vtype = gr.GRB.BINARY, name = "y")
        self.z = self.model.addVars(range(K), range(L), vtype = gr.GRB.BINARY, name = "z")
        self.c = self.model.addVars(range(D), range(timeslotsInHour*T), range(K), range(L), vtype = gr.GRB.BINARY, name = "c")
        self.s = self.model.addVars(range(D), range(timeslotsInHour*T), range(K), range(L), vtype = gr.GRB.BINARY, name = "s")
        self.p = self.model.addVars(range(D), range(K), range(L), vtype = gr.GRB.BINARY, name = "p")

        # Преводаватели

        self.u = self.model.addVars(range(I), range(K), range(L), vtype = gr.GRB.BINARY, name = "u")
        self.P = self.model.addVars(range(I), range(D), vtype = gr.GRB.BINARY, name = "P")
        self.U = self.model.addVars(range(I), range(D), range(timeslotsInHour*T), range(K), range(L), vtype = gr.GRB.BINARY, name = "U")
        self.S = self.model.addVars(range(I), range(D), range(timeslotsInHour*T), vtype = gr.GRB.BINARY, name = "S")
        self.C = self.model.addVars(range(I), range(D), range(timeslotsInHour*T), vtype = gr.GRB.BINARY, name = "C")
        
        # Целевая функция 



        #(1)
        # self.model.setObjective(gr.quicksum(self.y[j, k] for k in range(K) for j in J), gr.GRB.MAXIMIZE)
        if course == None:
            self.model.setObjective(gr.quicksum(self.y[j, k] for k in range(K) for j in range(J)) - gr.quicksum( F[l,k]*self.z[k, l] for k in range(K) for l in range(L)), gr.GRB.MAXIMIZE)
        else:
            self.model.setObjective(gr.quicksum(self.y[j, k] for k in range(K) for j in range(J)) - gr.quicksum( F[course[l],k]*self.z[k, l] for k in range(K) for l in range(L)), gr.GRB.MAXIMIZE)
        # Условия 
        # self.x[d, t, k, l]= self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l]



        # (2) Если студент в группе, то он может прийти, когда у этой группы занятие,
        # for j in range(J):
        #     for k in range(K):
        #         for l in range(L):
        #             self.model.addLConstr(gr.quicksum((self.b[j, l]*self.a[j, d, t]*(self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l])) for d in range(D) for t in range(timeslotsInHour*T)) >= 2*self.b[j, l]* self.lt[l] * self.y[j, k])

        for j in range(J):
            for k in range(K):
                self.model.addLConstr(gr.quicksum((self.b[j, l]*self.a[j, d, t]*(self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l])) for d in range(D) for t in range(timeslotsInHour*T) for l in range(L)) >= gr.quicksum((2*self.b[j, l]* self.lt[l] * self.y[j, k]) for l in range(L) ))


        #(3) В любой момент времени не может быть больше пар, чем число комнат 
        for d in range(D):
            for t in range(timeslotsInHour*T):
                self.model.addLConstr(gr.quicksum((self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l])for k in range(K) for l in range(L)) <= r)

        #(4) Студент может быть только в одной группе
        for j in range(J):
            self.model.addLConstr(gr.quicksum(self.y[j, k] for k in range(K)) <= 1)

        #(5.1) Ограничения на максимальное количество студентов в группе
        for k in range(K):
            for l in range(L):
                self.model.addLConstr(gr.quicksum(self.y[j, k]*self.b[j, l] for j in range(J)) <= data['maxNumber'] *self.z[k,l])
        # for k in range(K):
        #     for l in range(L):
        #         self.model.addLConstr(gr.quicksum(self.y[j, k]*self.b[j, l] for j in range(J)) <= data['maxNumber'] )

        #(5.2) Ограничения на минимальное количество студентов в группе
        for k in range(K):
            for l in range(L):
                self.model.addLConstr(gr.quicksum(self.y[j, k]*self.b[j, l] for j in range(J)) >= data['minNumber'] * self.z[k,l])


        #(6) Для любой группы в любой день количесво выделеных на нее таймслотов должно равняться продолжительности занятия
        for l in range(L):
            for k in range(K):
                for d in range(D):
                    self.model.addLConstr(gr.quicksum((self.c[d, t, k, l] +  self.s[d, t, k, l])for t in range(timeslotsInHour*T)) == (len(range(timeslotsInHour*T)) + self.lt[l])*self.p[d, k, l])


        #(7) Конкретные пары вместе не идут
        D_w = np.arange(0, D - 1, 1)
        for d in D_w:
            for k in range(K):
                for l in range(L):
                    self.model.addLConstr(self.p[d, k, l] + self.p[d + 1, k ,l] <= 1)

        # #(8) Если нет группы, то и нет студента

        # for j in range(J):
        #     for l in range(L):
        #         for k in range(K):
        #             self.model.addLConstr(self.z[k,l] >= self.y[j,k]*self.b[j,l])
        
        # for l in range(L):
        #     for k in range(K):
        #         self.model.addLConstr(self.z[k,l] >= gr.quicksum((self.y[j,k]*self.b[j,l]) for j in range(J)))

        #(9) Ограничения созданные против борьбы с симметрией
        K_l = np.arange(0,K - 1, 1)
        for l in range(L):
            for k in K_l:
                self.model.addLConstr(self.z[k,l] >= self.z[k + 1,l])

        #(10) условие на непрерывность S
        T_1 = np.arange(0, len(range(timeslotsInHour*T)) - 1, 1) 
        for d in range(D):
            for t in T_1:
                for k in range(K):
                    for l in range(L):
                        self.model.addLConstr(self.s[d, t, k, l] <= self.s[d, t + 1, k, l])


        #(11) условие на непрерывность C
        for d in range(D):
            for t in T_1:
                for k in range(K):
                    for l in range(L):
                        self.model.addLConstr(self.c[d, t, k, l] >= self.c[d, t + 1, k, l])

        #(12) Для любой группы два рабочих дня
        for l in range(L):
            for k in range(K):
                self.model.addLConstr(gr.quicksum((self.p[d, k, l]) for d in range(D)) == 2*self.z[k,l])


        #(13) Для каждой сформированной группы есть преподаватель, руководящей ею
        for l in range(L):
            for k in range(K):
                self.model.addLConstr(gr.quicksum((self.u[i, k, l]) for i in range(I)) == self.z[k,l])

        # (14) Расписание преподавателя для каждой группы
        for i in range(I):
            for d in range(D):
                for t in range(timeslotsInHour*T):
                    for k in range(K):
                        for l in range(L):
                            self.model.addLConstr(self.U[i, d, t, k, l] <= self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l])
                            self.model.addLConstr(self.U[i, d, t, k, l] <= self.u[i, k, l])
                            self.model.addLConstr(self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l] + self.u[i, k, l] - self.U[i, d, t, k, l] <= 1)

        #(14.1) Расписание преподавателя для каждой группы
        # for i in range(I):
        #     self.model.addLConstr(gr.quicksum(self.U[i, d, t, k, l] for d in range(D) for t in range(timeslotsInHour*T) for k in range(K) for l in range(L)) == 2*(gr.quicksum(self.lt[l] * self.u[i, k, l] for k in range(K) for l in range(L))))


        #(15) Преподаватель в любой момент времени работает только с одной группой
        for i in range(I):
            for d in range(D):
                for t in range(timeslotsInHour*T):
                    self.model.addLConstr(gr.quicksum(self.U[i, d, t, k, l] for k in range(K) for l in range(L)) <= 1)

        #(16) После занятия, у преподавателя идет перерыв 
        for i in range(I):
            for d in range(D):
                for t in range(timeslotsInHour*T):
                    for k_1 in range(K):
                        for l_1 in range(L):
                            if t >= len(range(timeslotsInHour*T)) - 1:
                                continue
                            self.model.addConstr(gr.quicksum(self.U[i, d, t, k, l] for k in range(K) for l in range(L)) <= self.c[d, t, k_1, l_1] +  self.s[d, t, k_1, l_1] - self.p[d, k_1, l_1] + 1 - self.U[i, d, t + 1, k_1, l_1] )
                            

        #(17) Если у преподователя занимается группа в день d, то и он должен работать в этот день
        for i in range(I):
            for k in range(K):
                for l in range(L):
                    for d in range(D):
                        self.model.addLConstr(self.p[d, k, l] + self.u[i, k, l] - self.P[i, d] <= 1)

        #(18) У всех преподавателей не больше пяти рабочих дней
        for i in range(I):
            self.model.addLConstr(gr.quicksum( self.P[i, d] for d in range(D)) <= D - 1)


        # #(19) Условия на задание рабочий таймслотов преподавателя
        for i in range(I):
            for d in range(D):
                for t in range(timeslotsInHour*T):
                    self.model.addLConstr(gr.quicksum(self.U[i, d, t, k, l] for k in range(K) for l in range(L)) <= self.S[i, d, t]  )

                    self.model.addLConstr(gr.quicksum(self.U[i, d, t, k, l] for k in range(K) for l in range(L)) <= self.C[i, d, t]  )

                    if t + 1 == len(range(timeslotsInHour*T)):
                        continue
                    self.model.addLConstr(self.S[i, d, t] <= self.S[i, d, t + 1])

                    self.model.addLConstr(self.C[i, d, t] >= self.C[i, d, t + 1])

        #(20) Условия на продолжительность рабочего дня

        for i in range(I):
            for d in range(D):
                self.model.addLConstr(gr.quicksum((self.C[i, d, t] +  self.S[i, d, t])for t in range(timeslotsInHour*T)) <= ((len(range(timeslotsInHour*T)) + teacherLimit )*self.P[i, d]))


        for l in range(L):
            capacity = math.floor(np.sum(data['course_of_students'][l]) / 4) + 1
            self.mode


        self.model.write(f"English_Lesson_K_{K}_EX_{self.i}_ver4.lp")  
        
        # self.model.write(f"English_Lesson_L_{str(course)}_EX_{self.i}_ver5.lp")  
        # self.model.write(f"English_Lesson_WT_{self.i}_K_{len(K)}_ver1.1.lp")
        

    def calculate(self, time, K):
        self.model.reset()
        # model._cur_obj = float('inf')
        # model._time = time.time()
        self.model.params.TimeLimit = time
        # self.model.setParam("MIPFocus", 2)
        # self.model.setParam("Presolve", 2)
    # MIPFocus 2
	# Presolve 2
        self.model.update()

        self.model.write("English_Lesson.lp")
        # return 0
        # self.model.write("English_Lesson.sol")
        # self.model.tune()
        self.model.optimize()

        f=open(f"schedule_gr_{self.i}.txt","w")

       
        column_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        value_list = []
        f.write("\n")
        for t in range(timeslotsInHour*T):
            week = []
            for d in range(D):
                lessons = []
                for k in range(K):
                    for l in range(L):
                        if (  int(self.c[d, t, k, l].X) + int(self.s[d, t, k, l].X) - int(self.p[d, k, l].X) == 1):
                            lessons.append(f"Gr{k}, Cr{l}")
                            # for i in range(I):
                            #     if int(self.u[i,k,l].X) == 1:
                            #         lessons.append(f"Gr{k}, Cr{l}")
                week.append(lessons)
            value_list.append(week)

        f.write(tabulate(value_list, column_list, tablefmt="grid"))
            
        f.close()

        f=open(f"sol_gr_{self.i}.txt","w")

        sm_st = 0
        sm_gr =0
        for j in range(J):
            for k in range(K):
                if int(self.y[j,k].X) == 1:
                    sm_st+=1

        for l in range(L):
            for k in range(K):
                if int(self.z[k,l].X) == 1:
                    sm_gr+=1

        f.write(f"sum students: {sm_st}\n")
        f.write(f"sum groups: {sm_gr}\n")
        f.write(f"ObjVal : {self.model.objVal}\n")
        f.close()


def tuning_models(i_num):
    # model_name = f'C:\cyrillic_characters\English_Lesson_WT_{i_num}_K_10_ver1.0.lp'
    model_name = f"English_Lesson_WT_tuning_{i_num}_K_{10}_ver1.0.lp"
    model = gr.read(model_name)
    print(model.getParamInfo("Method"))
    model.setParam("Method", 2)
    model.setParam("MIPFocus", 3)
    print(model.getParamInfo("Method"))

    # model.tune()
    # for i in range(model.tuneResultCount):
    #     model.getTuneResult(i)
    #     model.write(f'tune_m_{i_num}'+str(i)+'.prm')
    #     break
    # model.write(f"English_Lesson_WT_tuning_{i_num}_K_{10}_ver1.0.lp")

def creat_subsets_course_problem(list_L):

    for el in list_L:
        p = Problem(1,  10, course=el)


def launch():
 

    # K_list = [[3, 3, 4, 4, 3, 8, 6, 4, 6, 5, 5, 4, 2],
    #         [3, 3, 4, 6, 4, 6, 5, 7, 5, 4, 4, 2, 3],
    #         [4, 4, 4, 4, 6, 5, 5, 4, 5, 5, 4, 4, 3],
    #         [4, 4, 4, 5, 4, 5, 4, 4, 6, 4, 5, 4, 5],
    #         [4, 4, 4, 5, 4, 6, 7, 5, 4, 5, 4, 4, 2],
    #         [2, 4, 3, 5, 6, 3, 5, 5, 6, 5, 5, 4, 3],
    #         [2, 3, 3, 6, 7, 5, 4, 6, 6, 5, 4, 3, 3],
    #         [3, 4, 5, 4, 4, 6, 6, 5, 5, 4, 3, 4, 3],
    #         [3, 3, 4, 4, 6, 7, 5, 5, 6, 4, 4, 4, 3],
    #         [3, 4, 4, 5, 4, 6, 5, 7, 4, 5, 5, 3, 3]]

    # K_list = [ [7.0, 10.0, 7.0],
    #         [6.0, 10.0, 8.0],
    #         [6.0, 12.0, 5.0],
    #         [8.0, 9.0, 7.0],
    #         [6.0, 11.0, 6.0],
    #         [6.0, 13.0, 5.0],
    #         [5.0, 13.0, 5.0],
    #         [6.0, 10.0, 7.0],
    #         [6.0, 12.0, 6.0],
    #         [6.0, 11.0, 6.0]]

    # # for k in range(2,4):
    # for i in range(1, 11):
    #     for l in range(3):
    #         p = Problem(i,  int(K_list[i-1][l]) + 1, course=l)
            
    # creat_subsets_course_problem([[0,1],[2]])

    # for i in range(1,11):
        
    #     for k in range(9,11):
    #         p = Problem(i,  k)



    p = Problem(5,  5)
if __name__ == "__main__":
    launch()