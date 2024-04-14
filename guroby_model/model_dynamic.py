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



class Problem:

    def __init__(self,i, K, course = None):
        self.i = i

        data = read_data(f"examples_copy\\orders_1_1.txt")

        self.a = restruct(data['J'], data['D'], data['T'], data['L'], data['timeLessons'], data['timeslot_of_students'], data['course_of_students']  )
        self.b = data['course_of_students'] 
        self.lt = data['timeLessons']


        capacity = np.sum(data['course_of_students'], axis=0)
       
        # K = []
        # for l in range(L):
        #     K.append(math.ceil(capacity[l]/ 4))
        K = [8,8,6]
            
        # Иницализация моедли
        # self.model = gr.Model("Schedule creating") 
        self.model = gr.Model("Schedule") 
        self.model.Params.logFile = f"consol_info_{i}"
        # Переменые 
        # print(K)
        # Группа

        J_index = []
        for j in range(J):
            for l in range(L):
                if self.b[j,l] == 1:
                    for k in range(K[l]):
                        J_index.append((j,k))


        
        self.y = self.model.addVars(J_index, vtype = gr.GRB.BINARY, name = "y")
        
        
        # self.z = self.model.addVars(range(L), range(L), vtype = gr.GRB.BINARY, name = "z")
        Z_index = []
        for l in range(L):
            for k in range(K[l]):
                Z_index.append((k,l))


        print(Z_index)
        self.z = self.model.addVars(Z_index, vtype = gr.GRB.BINARY, name = "z")

        Timsets_index = []
        for d in range(D):
            for t in range(timeslotsInHour*T):
                for l in range(L):
                    for k in range(K[l]):
                        Timsets_index.append((d,t,k,l))

        self.c = self.model.addVars(Timsets_index, vtype = gr.GRB.BINARY, name = "c")
        self.s = self.model.addVars(Timsets_index, vtype = gr.GRB.BINARY, name = "s")

        p_index = []
        for d in range(D):
            for l in range(L):
                for k in range(K[l]):
                    p_index.append((d,k,l))

        self.p = self.model.addVars(p_index, vtype = gr.GRB.BINARY, name = "p")

        # # Преводаватели

        u_index = []
        for i in range(I):
            for l in range(L):
                for k in range(K[l]):
                    u_index.append((i,k,l))
        
        self.u = self.model.addVars(u_index, vtype = gr.GRB.BINARY, name = "u")

        self.P = self.model.addVars([(i,d) for i in range(I) for d in range(D)], vtype = gr.GRB.BINARY, name = "P")

        U_index = []
        for i in range(J):
            for d in range(D):
                for t in range(timeslotsInHour*T):
                    for l in range(L):
                        for k in range(K[l]):
                            U_index.append((i,d,t,k,l))
                
        self.U = self.model.addVars(U_index , vtype = gr.GRB.BINARY, name = "U")
        self.S = self.model.addVars([(i,d,t) for i in range(I) for d in range(D) for t in range(timeslotsInHour*T) ], vtype = gr.GRB.BINARY, name = "S")
        self.C = self.model.addVars([(i,d,t) for i in range(I) for d in range(D) for t in range(timeslotsInHour*T) ], vtype = gr.GRB.BINARY, name = "C")
        
        # Целевая функция 
        # print(self.y)

        arc, kl_tupl = gr.multidict({(k,l): F[l,k] for k,l in Z_index})
        # print(arc)

        # raise
        F_coef = []
        for l in range(L):
            for k in range(K[l]):
                F_coef.append( ( (k,l), F[l,k] ) ) 
        F_coef = dict(F_coef)

        a_coef = []
        for j in range(J):
            for d in range(D):
                for t in range(T*timeslotsInHour):
                    a_coef.append( ( (j,d,t), self.a[j,d,t] ) )
        a_coef = dict(a_coef)
    
        b_coef = []
        for j in range(J):
            for l in range(L):
                b_coef.append( ( (j,l), self.b[j,l] ) )
        b_coef = dict(b_coef)

        ab_coef = []
        for j in range(J):
            for d in range(D):
                for t in range(T*timeslotsInHour):
                    ab_coef.append( ( (j,d,t),self.b[j, l]*self.a[j,d,t] ) )

        ab_coef = dict(ab_coef)

        ab_for_p_coef = []


        ltS_coef = []
        for j in range(J):
            for l in range(L):
                if self.b[j,l] == 1:
                    
                    ltS_coef.append( {'j': j,'l': l, 'lt': self.lt[l]})




     
        #(1)

        self.model.setObjective(gr.quicksum(self.y)-gr.quicksum(self.z[k,l]*kl_tupl[k,l] for k,l in arc), gr.GRB.MAXIMIZE)
        # Условия 
        # self.x[d, t, k, l]= self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l]
        # (2) Если студент в группе, то он может прийти, когда у этой группы занятие,
        for j in range(J):
            l = ltS_coef[j]['l']
            lt = ltS_coef[j]['lt']
            for k in range(K[l]):
                self.model.addLConstr( gr.quicksum(self.a[j,d,t]*(self.c[d,t,k,l] + self.s[d,t,k,l] - self.p[d,k,l]) 
                                                   for d in range(D) 
                                                   for t in range(timeslotsInHour*T)) 
                                                     >=  (2*lt)*self.y[j,k],
                                                     f"(2)_j_{j}_k_{k}")

      
        #(3) В любой момент времени не может быть больше пар, чем число комнат 
        for d in range(D):
            for t in range(timeslotsInHour*T):
                self.model.addLConstr(gr.quicksum((self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l])for k,l in arc ) 
                                      <= r, 
                                      f"(3)_d_{d}_t_{t}")


        #(4) Студент может быть только в одной группе
        for j in range(J):
            l = ltS_coef[j]['l']
            self.model.addLConstr(gr.quicksum(self.y[j, k] for k in range(K[l])) 
                                  <= 1, 
                                  f"(4)_j_{j}")

        #(5.1) Ограничения на максимальное количество студентов в группе
        for k,l in arc:
                J_l = [j for j in range(J) if self.b[j,l] == 1  ]
                self.model.addLConstr(gr.quicksum(self.y[j, k] for j in J_l) 
                                      <= data['maxNumber'] *self.z[k,l],
                                      f"(5.1)_k_{k}_l_{l}")
                
                self.model.addLConstr(gr.quicksum(self.y[j, k] for j in J_l) 
                                      >= data['minNumber'] * self.z[k,l],
                                      f"(5.2)_k_{k}_l_{l}")



        #(6) Для любой группы в любой день количесво выделеных на нее таймслотов должно равняться продолжительности занятия
        for k,l in arc:
            for d in range(D):
                self.model.addLConstr(gr.quicksum((self.c[d, t, k, l] +  self.s[d, t, k, l])for t in range(timeslotsInHour*T))
                                       == (len(range(timeslotsInHour*T)) + self.lt[l])*self.p[d, k, l],
                                       f"(6)_k_{k}_l_{l}_d_{d}")


        #(7) Конкретные пары вместе не идут
        D_w = np.arange(0, D - 1, 1)
        for d in D_w:
            for k,l in arc:
                self.model.addLConstr(self.p[d, k, l] + self.p[d + 1, k ,l] 
                                        <= 1,
                                        f"(7)_d_{d}_k_{k}_l_{l}")
        

        # #(8) Если нет группы, то и нет студента

        # for j in range(J):
        #     for l in range(L):
        #         for k in range(K):
        #             self.model.addLConstr(self.z[k,l] >= self.y[j,k]*self.b[j,l])
        
        # for l in range(L):
        #     for k in range(K):
        #         self.model.addLConstr(self.z[k,l] >= gr.quicksum((self.y[j,k]*self.b[j,l]) for j in range(J)))

        #(9) Ограничения созданные против борьбы с симметрией
   
        for k,l in arc:
            if k < K[l] - 1:
                self.model.addLConstr(self.z[k,l] 
                                      >= self.z[k + 1,l],
                                      f"(9)_k_{k}_l_{l}")

        #(10) условие на непрерывность S
        T_1 = np.arange(0, len(range(timeslotsInHour*T)) - 1, 1) 
        for d in range(D):
            for t in T_1:
                for k, l in arc:
                    self.model.addLConstr(self.s[d, t, k, l] 
                                          <= self.s[d, t + 1, k, l],
                                          f"(10)_d_{d}_t_{t}_k_{k}_l_{l}")
                    self.model.addLConstr(self.c[d, t, k, l] 
                                          >= self.c[d, t + 1, k, l],
                                          f"(11)_d_{d}_t_{t}_k_{k}_l_{l}")



        #(12) Для любой группы два рабочих дня
        for k, l in arc:
            self.model.addLConstr(gr.quicksum((self.p[d, k, l]) for d in range(D)) 
                                  == 2*self.z[k,l],
                                  f"(12)_k_{k}_l_{l}")


        #(13) Для каждой сформированной группы есть преподаватель, руководящей ею
        for k, l in arc:
            self.model.addLConstr(gr.quicksum((self.u[i, k, l]) for i in range(I)) 
                                  == self.z[k,l],
                                  f"(13)_k_{k}_l_{l}")

        # (14) Расписание преподавателя для каждой группы
        for i in range(I):
            for d in range(D):
                for t in range(timeslotsInHour*T):
                    for k,l in arc:
                        self.model.addLConstr(self.U[i, d, t, k, l] 
                                              <= self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l],
                                              f"(14.1)_i_{i}_d_{d}_t_{t}_k_{k}_l_{l}")
                        self.model.addLConstr(self.U[i, d, t, k, l] 
                                              <= self.u[i, k, l],
                                               f"(14.2)_i_{i}_d_{d}_t_{t}_k_{k}_l_{l}")
                        self.model.addLConstr(self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l] + self.u[i, k, l] - self.U[i, d, t, k, l] 
                                              <= 1,
                                               f"(14.3)_i_{i}_d_{d}_t_{t}_k_{k}_l_{l}")

        #(14.1) Расписание преподавателя для каждой группы
        # for i in range(I):
        #     self.model.addLConstr(gr.quicksum(self.U[i, d, t, k, l] for d in range(D) for t in range(timeslotsInHour*T) for k in range(K) for l in range(L)) == 2*(gr.quicksum(self.lt[l] * self.u[i, k, l] for k in range(K) for l in range(L))))


        #(15) Преподаватель в любой момент времени работает только с одной группой
        for i in range(I):
            for d in range(D):
                for t in range(timeslotsInHour*T):
                    self.model.addLConstr(gr.quicksum(self.U[i, d, t, k, l] for k,l in arc) 
                                          <= 1,
                                          f"(15)_i_{i}_d_{d}_t_{t}")

        #(16) После занятия, у преподавателя идет перерыв 
        for i in range(I):
            for d in range(D):
                for t in range(timeslotsInHour*T):
                    for k_1, l_1 in arc:
                            if t >= len(range(timeslotsInHour*T)) - 1:
                                continue
                            else:
                                self.model.addConstr(gr.quicksum(self.U[i, d, t, k, l] for k,l in arc) 
                                                    <= self.c[d, t, k_1, l_1] +  self.s[d, t, k_1, l_1] - self.p[d, k_1, l_1] + 1 - self.U[i, d, t + 1, k_1, l_1],
                                                    f"(16)_i_{i}_d_{d}_t_{t}_k_{k_1}_l_{l_1}" )
                            

        #(17) Если у преподователя занимается группа в день d, то и он должен работать в этот день
        for i in range(I):
            for k,l in arc:
                for d in range(D):
                    self.model.addLConstr(self.p[d, k, l] + self.u[i, k, l] - self.P[i, d] 
                                          <= 1,
                                          f"(17)_i_{i}_k_{k}_l_{l}_d_{d}")

        #(18) У всех преподавателей не больше пяти рабочих дней
        for i in range(I):
            self.model.addLConstr(gr.quicksum( self.P[i, d] for d in range(D)) 
                                  <= D - 1,
                                  f"(18)_i_{i}")


        # #(19) Условия на задание рабочий таймслотов преподавателя
        for i in range(I):
            for d in range(D):
                for t in range(timeslotsInHour*T):
                    self.model.addLConstr(gr.quicksum(self.U[i, d, t, k, l] for k,l in arc) 
                                          <= self.S[i, d, t],
                                          f"(19.1)_i_{i}_d_{d}_t_{t}")

                    self.model.addLConstr(gr.quicksum(self.U[i, d, t, k, l] for k,l in arc) 
                                          <= self.C[i, d, t],
                                          f"(19.2)_i_{i}_d_{d}_t_{t}")


                    if t + 1 == len(range(timeslotsInHour*T)):
                        continue
                    else:
                        self.model.addLConstr(self.S[i, d, t] 
                                            <= self.S[i, d, t + 1],
                                            f"(19.3)_i_{i}_d_{d}_t_{t}")


                        self.model.addLConstr(self.C[i, d, t] 
                                            >= self.C[i, d, t + 1],
                                            f"(19.4)_i_{i}_d_{d}_t_{t}")


        #(20) Условия на продолжительность рабочего дня

        for i in range(I):
            for d in range(D):
                self.model.addLConstr(gr.quicksum((self.C[i, d, t] +  self.S[i, d, t])for t in range(timeslotsInHour*T)) 
                                      <= ((len(range(timeslotsInHour*T)) + teacherLimit )*self.P[i, d]),
                                      f"(20)_i_{i}_d_{d}_t")


        self.model.write(f"test.lp")  

        

def launch():
 
    p = Problem(5,  5)

if __name__ == "__main__":
    launch()