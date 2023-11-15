import math
import json
import numpy as np
import gurobipy as gr
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

    # print(a[0])
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
    # data['J'] = 150
    # data['L'] = 3
    # data['D'] = 6# num of day
    # data['T'] = 11# num of timslots in the 
    # data['I'] = 3# num of teachers
    # data['r'] = 2# num of rooms
    # data['minNumber'] = 2# min number of students in the group
    # data['maxNumber'] = 6# max number of students in the group
    # data['timeLessons']  = np.array([ 4, 5, 6])

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
    data['J'] = 300# num of studetns
    data['L'] = 4# num of course
    data['D'] = 6# num of day
    data['T'] = 8# num of timslots in the day
    data['I'] = 4# num of teachers
    data['r'] = 3# num of rooms
    data['minNumber'] = 2# min number of students in the group
    data['maxNumber'] = 6# max number of students in the group
    data['timeLessons']  = np.array([3, 4, 5 , 6])



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
# K = np.arange(0, 15, 1) # Количество групп
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
J = np.arange(0, 300, 1) # Заявки
K = np.arange(0, 10, 1) # Количество групп
L = np.arange(0, 4, 1) # Множество курсов
D = np.arange(0, 6, 1) # Рабочие дни
T = np.arange(0, 4*8, 1) # Множество временных слотов
I = np.arange(0, 3, 1) # Множество преподователь 
r = 2 # Количество комнат
# I = np.arange(0, 4, 1) # Множество преподователь 
# r = 3 # Количество комнат



F = [] # Штрафы на создание каждой новой группы, созданно для борьбы с симметрией
# old penalty
# for i in L:
#   F.append([])
# for i in K:
#   if ( i < 1):
#     F[0].append(0)
#     F[1].append(0)
#     F[12].append(0)
#     F[11].append(0)
#   else:
#     F[0].append(2.5)
#     F[1].append(2.5)
#     F[12].append(2.5)
#     F[11].append(2.5)

# for i in K:
#   if ( i < 3):
#     F[2].append(0)
#     F[3].append(0)
#     F[4].append(0)
#     F[8].append(0)
#     F[10].append(0)
#     F[9].append(0)
#   else:
#     F[2].append(2.5)
#     F[3].append(2.5)
#     F[10].append(2.5)
#     F[9].append(2.5)
#     F[4].append(2.5)
#     F[8].append(2.5)

# for i in K:
#   if ( i < 5):
#     F[5].append(0)
#     F[6].append(0)
#     F[7].append(0)
    
#   else:
#     F[5].append(2.5)
#     F[6].append(2.5)
#     F[7].append(2.5)




# F=np.array(F)
F = np.array([[0,0,0,2.5,2.5,2.5,2.5,2.5,2.5,2.5],
              [0,0,0,0,2.5,2.5,2.5,2.5,2.5,2.5],
              [0,0,0,0,2.5,2.5,2.5,2.5,2.5,2.5],
              [0,0,0,2.5,2.5,2.5,2.5,2.5,2.5,2.5]])



class Problem:

    def __init__(self,i, K):
        self.i = i
        # str = f"C:/Users/Александр/source/vscode_project/Operation research/examples_copy/orders_2_{i}.txt"
        # f"examples_copy\\orders_hand_make.txt"
        # data = read_data("examples_copy\\orders_hm.txt")
        data = read_data(f"examples_copy\\orders_3_{i}.txt")
        self.a =restruct(data['J'], data['D'], data['T'], data['L'], data['timeLessons'], data['timeslot_of_students'], data['course_of_students']  )
        self.b = data['course_of_students'] 
        self.lt = data['timeLessons']
        # Иницализация моедли
        # self.model = gr.Model("Schedule creating") 
        self.model = gr.Model("Schedule without teachers") 
        self.model.Params.logFile = f"consol_info_{i}"
        # Переменые 
        # print(K)
        # Группа
        self.y = self.model.addVars(J, K, vtype = gr.GRB.BINARY, name = "y")
        self.z = self.model.addVars(K, L, vtype = gr.GRB.BINARY, name = "z")
        self.c = self.model.addVars(D, T, K, L, vtype = gr.GRB.BINARY, name = "c")
        self.s = self.model.addVars(D, T, K, L, vtype = gr.GRB.BINARY, name = "s")
        self.p = self.model.addVars(D, K, L, vtype = gr.GRB.BINARY, name = "p")

        # Преводаватели

        self.u = self.model.addVars(I, K, L, vtype = gr.GRB.BINARY, name = "u")
        self.P = self.model.addVars(I, D, vtype = gr.GRB.BINARY, name = "P")
        self.U = self.model.addVars(I, D, T, K, L, vtype = gr.GRB.BINARY, name = "U")
        self.S = self.model.addVars(I, D, T, vtype = gr.GRB.BINARY, name = "S")
        self.C = self.model.addVars(I, D, T, vtype = gr.GRB.BINARY, name = "C")
        
        # Целевая функция 



        #(1)
        # self.model.setObjective(gr.quicksum(self.y[j, k] for k in K for j in J), gr.GRB.MAXIMIZE)
        self.model.setObjective(gr.quicksum(self.y[j, k] for k in K for j in J) - gr.quicksum( F[l,k]*self.z[k, l] for k in K for l in L), gr.GRB.MAXIMIZE)
        # Условия 
        # self.x[d, t, k, l]= self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l]



        # (2) Если студент в группе, то он может прийти, когда у этой группы занятие,
        for j in J:
            for k in K:
                for l in L:
                    self.model.addLConstr(gr.quicksum((self.b[j, l]*self.a[j, d, t]*(self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l])) for d in D for t in T) >= 2*self.b[j, l]* self.lt[l] * self.y[j, k])


        #(3) В любой момент времени не может быть больше пар, чем число комнат 
        for d in D:
            for t in T:
                self.model.addLConstr(gr.quicksum((self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l])for k in K for l in L) <= r)

        #(4) Студент может быть только в одной группе
        for j in J:
            self.model.addLConstr(gr.quicksum(self.y[j, k] for k in K) <= 1)

        #(5.1) Ограничения на максимальное количество студентов в группе
        for k in K:
            for l in L:
                self.model.addLConstr(gr.quicksum(self.y[j, k]*self.b[j, l] for j in J) <= data['maxNumber'] )

        #(5.2) Ограничения на минимальное количество студентов в группе
        for k in K:
            for l in L:
                self.model.addLConstr(gr.quicksum(self.y[j, k]*self.b[j, l] for j in J) >= data['minNumber'] * self.z[k,l])


        #(6) Для любой группы в любой день количесво выделеных на нее таймслотов должно равняться продолжительности занятия
        for l in L:
            for k in K:
                for d in D:
                    self.model.addLConstr(gr.quicksum((self.c[d, t, k, l] +  self.s[d, t, k, l])for t in T) == (len(T) + self.lt[l])*self.p[d, k, l])


        #(7) Конкретные пары вместе не идут
        D_w = np.arange(0, len(D) - 1, 1)
        for d in D_w:
            for k in K:
                for l in L:
                    self.model.addLConstr(self.p[d, k, l] + self.p[d + 1, k ,l] <= 1)

        # #(8) Если нет группы, то и нет студента
        for j in J:
            for l in L:
                for k in K:
                    self.model.addLConstr(self.z[k,l] >= self.y[j,k]*self.b[j,l])

        #(9) Ограничения созданные против борьбы с симметрией
        K_l = np.arange(0, len(K) - 1, 1)
        for l in L:
                for k in K_l:
                    self.model.addLConstr(self.z[k,l] >= self.z[k + 1,l])

        #(10) условие на непрерывность S
        T_1 = np.arange(0, len(T) - 1, 1) 
        for d in D:
            for t in T_1:
                for k in K:
                    for l in L:
                        self.model.addLConstr(self.s[d, t, k, l] <= self.s[d, t + 1, k, l])


        #(11) условие на непрерывность C
        for d in D:
            for t in T_1:
                for k in K:
                    for l in L:
                        self.model.addLConstr(self.c[d, t, k, l] >= self.c[d, t + 1, k, l])

        #(12) Для любой группы два рабочих дня
        for l in L:
            for k in K:
                self.model.addLConstr(gr.quicksum((self.p[d, k, l]) for d in D) == 2*self.z[k,l])


        #(13) Для каждой сформированной группы есть преподаватель, руководящей ею
        for l in L:
            for k in K:
                self.model.addLConstr(gr.quicksum((self.u[i, k, l]) for i in I) == self.z[k,l])

        # (14) Расписание преподавателя для каждой группы
        for i in I:
            for d in D:
                for t in T:
                    for k in K:
                        for l in L:
                            self.model.addLConstr(self.U[i, d, t, k, l] <= self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l])
                            self.model.addLConstr(self.U[i, d, t, k, l] <= self.u[i, k, l])
                            self.model.addLConstr(self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l] + self.u[i, k, l] - self.U[i, d, t, k, l] <= 1)

        #(14.1) Расписание преподавателя для каждой группы
        # for i in I:
            # self.model.addLConstr(gr.quicksum(self.U[i, d, t, k, l] for d in D for t in T for k in K for l in L) <= 2*(gr.quicksum(self.lt[l] * self.u[i, k, l] for k in K for l in L)))


        #(15) Преподаватель в любой момент времени работает только с одной группой
        for i in I:
            for d in D:
                for t in T:
                    self.model.addLConstr(gr.quicksum(self.U[i, d, t, k, l] for k in K for l in L) <= 1)

        #(16) После занятия, у преподавателя идет перерыв 
        for i in I:
            for d in D:
                for t in T:
                    for k_1 in K:
                        for l_1 in L:
                            if t >= len(T) - 1:
                                continue
                            self.model.addConstr(gr.quicksum(self.U[i, d, t, k, l] for k in K for l in L) <= self.c[d, t, k_1, l_1] +  self.s[d, t, k_1, l_1] - self.p[d, k_1, l_1] + 1 - self.U[i, d, t + 1, k_1, l_1] )
                            

        #(17) Если у преподователя занимается группа в день d, то и он должен работать в этот день
        for i in I:
            for k in K:
                for l in L:
                    for d in D:
                        self.model.addLConstr(self.p[d, k, l] + self.u[i, k, l] - self.P[i, d] <= 1)

        #(18) У всех преподавателей не больше пяти рабочих дней
        for i in I:
            self.model.addLConstr(gr.quicksum( self.P[i, d] for d in D) <= 5)


        # #(19) Условия на задание рабочий таймслотов преподавателя
        for i in I:
            for d in D:
                for t in T:
                    self.model.addLConstr(gr.quicksum(self.U[i, d, t, k, l] for k in K for l in L) <= self.S[i, d, t]  )

                    self.model.addLConstr(gr.quicksum(self.U[i, d, t, k, l] for k in K for l in L) <= self.C[i, d, t]  )

                    if t + 1 == len(T):
                        continue
                    self.model.addLConstr(self.S[i, d, t] <= self.S[i, d, t + 1])

                    self.model.addLConstr(self.C[i, d, t] >= self.C[i, d, t + 1])

        #(20) Условия на продолжительность рабочего дня

        for i in I:
            for d in D:
                self.model.addLConstr(gr.quicksum((self.C[i, d, t] +  self.S[i, d, t])for t in T) <= (len(T) + 24*self.P[i, d]))


        self.model.write(f"English_Lesson_I_3_{self.i}_K_{len(K)}_ver2.1.lp")  

        # self.model.write(f"English_Lesson_WT_{self.i}_K_{len(K)}_ver1.1.lp")
        

    def calculate(self, time):
        self.model.reset()
        # model._cur_obj = float('inf')
        # model._time = time.time()
        self.model.params.TimeLimit = time
        # self.model.setParam("MIPFocus", 2)
        # self.model.setParam("Presolve", 2)
    #     MIPFocus 2
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
        for t in T:
            week = []
            for d in D:
                lessons = []
                for k in K:
                    for l in L:
                        if (  int(self.c[d, t, k, l].X) + int(self.s[d, t, k, l].X) - int(self.p[d, k, l].X) == 1):
                            lessons.append(f"Gr{k}, Cr{l}")
                            # for i in I:
                            #     if int(self.u[i,k,l].X) == 1:
                            #         lessons.append(f"Gr{k}, Cr{l}")
                week.append(lessons)
            value_list.append(week)

        f.write(tabulate(value_list, column_list, tablefmt="grid"))
            
        f.close()

        f=open(f"sol_gr_{self.i}.txt","w")

        sm_st = 0
        sm_gr =0
        for j in J:
            for k in K:
                if int(self.y[j,k].X) == 1:
                    sm_st+=1

        for l in L:
            for k in K:
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


def launch():
    i = 1 
    for i in range(1,11):
        p = Problem(i, range(10))
        # tuning_models(i)
    # p.calculate(60*30)

if __name__ == "__main__":
    launch()