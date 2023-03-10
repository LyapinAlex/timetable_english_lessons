import math
import numpy as np
import gurobipy as gr
from gurobipy import GRB
import time
from tabulate import tabulate
import gurobipy as gr

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
    data['r'] = 1# num of rooms
    data['minNumber'] = 2# min number of students in the group
    data['maxNumber'] = 8# max number of students in the group
    data['timeLessons']  = np.array([3, 3, 3, 3, 3, 4, 3, 4, 5, 5, 5, 6, 6])
        
    data['timeslot_of_students'] = np.fromstring(input_str_a, dtype = int, sep = ' ').reshape((data['J'], data['D'], data['T']))
    data['course_of_students'] = np.fromstring(input_str_b, dtype = int, sep = ' ').reshape((data['J'], data['L']))

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

J = np.arange(0, 100, 1) # ????????????
K = np.arange(0, 5, 1) # ???????????????????? ??????????
L = np.arange(0, 13, 1) # ?????????????????? ????????????
D = np.arange(0, 6, 1) # ?????????????? ??????
T = np.arange(0, 44, 1) # ?????????????????? ?????????????????? ????????????
I = np.arange(0, 5, 1) # ?????????????????? ?????????????????????????? 
r = 4 # ???????????????????? ????????????
# J = np.arange(0, 500, 1) # ????????????
# K = np.arange(0, 15, 1) # ???????????????????? ??????????
# L = np.arange(0, 13, 1) # ?????????????????? ????????????
# D = np.arange(0, 6, 1) # ?????????????? ??????
# T = np.arange(0, 44, 1) # ?????????????????? ?????????????????? ????????????
# I = np.arange(0, 5, 1) # ?????????????????? ?????????????????????????? 
# r = 4 # ???????????????????? ????????????

F = [] # ???????????? ???? ???????????????? ???????????? ?????????? ????????????, ???????????????? ?????? ???????????? ?? ????????????????????
for i in range(0, len(L)):
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



class Problem:

    def __init__(self,i):
        self.i = i
        # str = f"C:/Users/??????????????????/source/vscode_project/Operation research/examples_copy/orders_2_{i}.txt"
        # f"examples_copy\\orders_hand_make.txt"
        # data = read_data(f"examples_copy\\orders_3_{i}.txt")
        data = read_data(f"examples_copy\\orders_2_{i}.txt")
        self.a =restruct(data['J'], data['D'], data['T'], data['L'], data['timeLessons'], data['timeslot_of_students'], data['course_of_students']  )
        self.b = data['course_of_students'] 
        self.lt = data['timeLessons']
        # ???????????????????????? ????????????
        self.model = gr.Model("Schedule creating") 
        self.model.Params.logFile = f"consol_info_{i}"
        # ?????????????????? 

        # ????????????
        self.y = self.model.addVars(J, K, vtype = gr.GRB.BINARY, name = "y")
        self.z = self.model.addVars(K, L, vtype = gr.GRB.BINARY, name = "z")
        self.c = self.model.addVars(D, T, K, L, vtype = gr.GRB.BINARY, name = "c")
        self.s = self.model.addVars(D, T, K, L, vtype = gr.GRB.BINARY, name = "s")
        self.p = self.model.addVars(D, K, L, vtype = gr.GRB.BINARY, name = "p")

        # ??????????????????????????

        self.u = self.model.addVars(I, K, L, vtype = gr.GRB.BINARY, name = "u")
        self.P = self.model.addVars(I, D, vtype = gr.GRB.BINARY, name = "P")
        self.U = self.model.addVars(I, D, T, K, L, vtype = gr.GRB.BINARY, name = "U")
        self.S = self.model.addVars(I, D, T, vtype = gr.GRB.BINARY, name = "S")
        self.C = self.model.addVars(I, D, T, vtype = gr.GRB.BINARY, name = "C")
        
        # ?????????????? ?????????????? 

        #(1)
        self.model.setObjective(gr.quicksum(self.y[j, k] for k in K for j in J) - gr.quicksum( F[l,k]*self.z[k, l] for k in K for l in L), gr.GRB.MAXIMIZE)

        # ?????????????? 
        # self.x[d, t, k, l]= self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l]



        # (2) ???????? ?????????????? ?? ????????????, ???? ???? ?????????? ????????????, ?????????? ?? ???????? ???????????? ??????????????,
        for j in J:
            for k in K:
                for l in L:
                    self.model.addLConstr(gr.quicksum((self.b[j, l]*self.a[j, d, t]*(self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l])) for d in D for t in T) >= 2*self.b[j, l]* self.lt[l] * self.y[j, k])

   
        #(3) ?? ?????????? ???????????? ?????????????? ???? ?????????? ???????? ???????????? ??????, ?????? ?????????? ???????????? 
        for d in D:
            for t in T:
                self.model.addLConstr(gr.quicksum((self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l])for k in K for l in L) <= r)

        #(4) ?????????????? ?????????? ???????? ???????????? ?? ?????????? ????????????
        for j in J:
            self.model.addLConstr(gr.quicksum(self.y[j, k] for k in K) <= 1)

        #(5.1) ?????????????????????? ???? ???????????????????????? ???????????????????? ?????????????????? ?? ????????????
        for k in K:
            for l in L:
                self.model.addLConstr(gr.quicksum(self.y[j, k]*self.b[j, l] for j in J) <= 8)

        #(5.2) ?????????????????????? ???? ?????????????????????? ???????????????????? ?????????????????? ?? ????????????
        for k in K:
            for l in L:
                self.model.addLConstr(gr.quicksum(self.y[j, k]*self.b[j, l] for j in J) >= 2* self.z[k,l])


        #(6) ?????? ?????????? ???????????? ?? ?????????? ???????? ?????????????????? ?????????????????? ???? ?????? ???????????????????? ???????????? ?????????????????? ?????????????????????????????????? ??????????????
        for l in L:
            for k in K:
                for d in D:
                    self.model.addLConstr(gr.quicksum((self.c[d, t, k, l] +  self.s[d, t, k, l])for t in T) == (len(T) + self.lt[l])*self.p[d, k, l])


        #(7) ???????????????????? ???????? ???????????? ???? ????????
        D_w = np.arange(0, len(D) - 1, 1)
        for d in D_w:
            for k in K:
                for l in L:
                    self.model.addLConstr(self.p[d, k, l] + self.p[d + 1, k ,l] <= 1)

        # #(8) ???????? ?????? ????????????, ???? ?? ?????? ????????????????
        for j in J:
            for l in L:
                for k in K:
                    self.model.addLConstr(self.z[k,l] >= self.y[j,k]*self.b[j,l])

        #(9) ?????????????????????? ?????????????????? ???????????? ???????????? ?? ????????????????????
        K_l = np.arange(0, len(K) - 1, 1)
        for l in L:
                for k in K_l:
                    self.model.addLConstr(self.z[k,l] >= self.z[k + 1,l])

        #(10) ?????????????? ???? ?????????????????????????? S
        T_1 = np.arange(0, len(T) - 1, 1) 
        for d in D:
            for t in T_1:
                for k in K:
                    for l in L:
                        self.model.addLConstr(self.s[d, t, k, l] <= self.s[d, t + 1, k, l])


        #(11) ?????????????? ???? ?????????????????????????? C
        for d in D:
            for t in T_1:
                for k in K:
                    for l in L:
                        self.model.addLConstr(self.c[d, t, k, l] >= self.c[d, t + 1, k, l])

        #(12) ?????? ?????????? ???????????? ?????? ?????????????? ??????
        for l in L:
            for k in K:
                self.model.addLConstr(gr.quicksum((self.p[d, k, l]) for d in D) == 2*self.z[k,l])


        #(13) ?????? ???????????? ???????????????????????????? ???????????? ???????? ??????????????????????????, ?????????????????????? ????
        for l in L:
            for k in K:
                self.model.addLConstr(gr.quicksum((self.u[i, k, l]) for i in I) == self.z[k,l])

        #(14) ???????????????????? ?????????????????????????? ?????? ???????????? ????????????
        for i in I:
            for d in D:
                for t in T:
                    for k in K:
                        for l in L:
                            # self.model.addLConstr(self.U[i, d, t, k, l] <= self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l])
                            # self.model.addLConstr(self.U[i, d, t, k, l] <= self.u[i, k, l])
                            self.model.addLConstr(self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l] + self.u[i, k, l] - self.U[i, d, t, k, l] <= 1)

        #(15) ?????????????????????????? ?? ?????????? ???????????? ?????????????? ???????????????? ???????????? ?? ?????????? ??????????????
        for i in I:
            for d in D:
                for t in T:
                    self.model.addLConstr(gr.quicksum(self.U[i, d, t, k, l] for k in K for l in L) <= 1)

        #(16) ?????????? ??????????????, ?? ?????????????????????????? ???????? ?????????????? 
        for i in I:
            for d in D:
                for t in T:
                    for k in K:
                        for l in L:
                            if t >= len(T) - self.lt[l] - 1:
                                continue
                            for k_1 in K:
                                for l_1 in L:
                                    self.model.addLConstr(1 - self.U[i, d, t, k, l] + self.U[i, d, t + 1, k, l]   - 1 + self.U[i, d, t + self.lt[l] + 1, k_1, l_1] <= 1)

        #(17) ???????? ?? ?????????????????????????? ???????????????????? ???????????? ?? ???????? d, ???? ?? ???? ???????????? ???????????????? ?? ???????? ????????
        for i in I:
            for k in K:
                for l in L:
                    for d in D:
                        self.model.addLConstr(self.p[d, k, l] + self.u[i, k, l] - self.P[i, d] <= 1)

        #(18) ?? ???????? ???????????????????????????? ???? ???????????? ???????? ?????????????? ????????
        for i in I:
            self.model.addLConstr(gr.quicksum( self.P[i, d] for d in D) <= 5)


        #(19) ?????????????? ???? ?????????????? ?????????????? ???????????????????? ??????????????????????????
        for i in I:
            for d in D:
                for t in T:
                    self.model.addLConstr(gr.quicksum(self.U[i, d, t, k, l] for k in K for l in L) <= self.S[i, d, t]  )

                    self.model.addLConstr(gr.quicksum(self.U[i, d, t, k, l] for k in K for l in L) <= self.C[i, d, t]  )

                    if t + 1 == len(T):
                        continue
                    self.model.addLConstr(self.S[i, d, t] <= self.S[i, d, t + 1])

                    self.model.addLConstr(self.C[i, d, t] >= self.C[i, d, t + 1])

        #(20) ?????????????? ???? ?????????????????????????????????? ???????????????? ?????? 
        for i in I:
            for d in D:
                self.model.addLConstr(gr.quicksum((self.C[i, d, t] +  self.S[i, d, t])for t in T) <= (len(T) + 32)*self.P[i, d])




    def calculate(self, time):
        self.model.reset()
        # model._cur_obj = float('inf')
        # model._time = time.time()
        self.model.params.TimeLimit = time
        self.model.update()
        self.model.optimize()

        
        # f=open(f"gurobiSchedule_hm.txt","w")
        # f.write("\ny\n")
        # for j in J:
        #     for k in K:
        #         f.write(f"{int(self.y[j, k].X) } ")
        # f.write("\n")
        # f.write("x\n")
        # for d in D:
        #     for k in K:
        #         for l in L:
        #             for t in T:
        #                 f.write(f"{int(self.c[d, t, k, l].X) + int(self.s[d, t, k, l].X) - int(self.p[d, k, l].X)} ")
        # f.write("\n")
        # f.write("z\n")
        # for k in K:
        #     for l in L:
        #         f.write(f"{int(self.z[k, l].X)} ")
        # f.write("\n")

        # f.write("p\n")
        # for l in L:
        #     for k in K:
        #         for d in D:
        #             f.write(f"{ int(self.p[d, k, l].X)} ")


        # f.close()


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
        f.write(f"gap : {self.model.gap}")   
        f.close()




i = 1 
p = Problem(i)
p.calculate(600)
