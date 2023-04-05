import math
import numpy as np
import gurobipy as gr
from gurobipy import GRB
import time
import json
from tabulate import tabulate

data = {}
# data['J'] = 500# num of studetns
# data['L'] = 13# num of course
# data['D'] = 6# num of day
# data['T'] = 44# num of timslots in the day
# data['I'] = 5# num of teachers
# data['r'] = 4# num of rooms
# data['K'] = 15
# timeLessons = np.array([3, 3, 3, 3, 3, 4, 3, 4, 5, 5, 5, 6, 6])
data['J'] = 150
data['L'] = 3
data['K'] = 15
data['D'] = 6# num of day
data['T'] = 11# num of timslots in the 
data['I'] = 3# num of teachers
data['r'] = 2# num of rooms
data['minNumber'] = 2# min number of students in the group
data['maxNumber'] = 6# max number of students in the group
data['timeLessons']  = np.array([ 4, 5, 6])



def import_json_data():

    with open('sol.json') as f:
        sol = json.load(f)
    
    return sol

def get_gurobi_sol(sol):
    y = np.zeros( (data['J'], data['K']) )
    z = np.zeros( (data['K'], data['L']) )
    s = np.zeros( (data['D'], data['T'], data['K'], data['L']) )
    c = np.zeros( (data['D'], data['T'], data['K'], data['L']) )
    p = np.zeros( (data['D'], data['K'], data['L']))

    u = np.zeros( (data['I'], data['K'], data['L']) )
    U = np.zeros( (data['I'], data['D'], data['T'], data['K'], data['L']) )
    S = np.zeros( (data['I'], data['D'], data['T']) )
    C = np.zeros( (data['I'], data['D'], data['T']) )
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

        for t in range(data['T']):
            if t >= d_1[1]:
                s[d_1[0], t , k, l] = 1
            if t >= d_2[1]:
                s[d_2[0], t , k, l] = 1


        for t in range(data['T']):
            if t <= d_1[2]:
                c[d_1[0], t , k, l] = 1
            if t <= d_2[2]:
                c[d_2[0], t , k, l] = 1

        p[d_1[0], k, l] = 1
        p[d_2[0], k, l] = 1

        u[i, k, l] = 1
        
        P[i,d_1[0]] = 1
        P[i,d_2[0]] = 1

        for t in range(data['T']):
            if c[d_1[0], t , k, l] + s[d_1[0], t , k, l] == 2:
                U[i,d_1[0], t, k, l] = 1

            if c[d_2[0], t , k, l] + s[d_2[0], t , k, l] == 2:
                U[i,d_2[0], t, k, l] = 1

        for t in range(data['T']):
            if t >= d_1[1]:
                S[i, d_1[0], t] = 1
            if t >= d_2[1]:
                S[i, d_2[0], t] = 1


        for t in range(data['T']):
            if t <= d_1[2]:
                C[i, d_1[0], t] = 1
            if t <= d_2[2]:
                C[i, d_2[0], t] = 1 

    

def main():
    
    sol = import_json_data()
    
    y = np.zeros( (data['J'], data['K']) )
    z = np.zeros( (data['K'], data['L']) )
    s = np.zeros( (data['D'], data['T'], data['K'], data['L']) )
    c = np.zeros( (data['D'], data['T'], data['K'], data['L']) )
    p = np.zeros( (data['D'], data['K'], data['L']))

    u = np.zeros( (data['I'], data['K'], data['L']) )
    U = np.zeros( (data['I'], data['D'], data['T'], data['K'], data['L']) )
    S = np.zeros( (data['I'], data['D'], data['T']) )
    C = np.zeros( (data['I'], data['D'], data['T']) )
    P = np.zeros( (data['I'], data['D']) )

    for group in sol:
        print(group)

        list_students = group[0]
        k = group[1] - 1
        l = group[2]
        i = group[5]
        d_1 =group[3]
        d_2 = group[4]

        for j in list_students:
            y[j,k] = 1 

        z[k,l] = 1

        for t in range(data['T']):
            if t >= d_1[1]:
                s[d_1[0], t , k, l] = 1
            if t >= d_2[1]:
                s[d_2[0], t , k, l] = 1


        for t in range(data['T']):
            if t <= d_1[2]:
                c[d_1[0], t , k, l] = 1
            if t <= d_2[2]:
                c[d_2[0], t , k, l] = 1

        p[d_1[0], k, l] = 1
        p[d_2[0], k, l] = 1

        u[i, k, l] = 1
        
        P[i,d_1[0]] = 1
        P[i,d_2[0]] = 1

        for t in range(data['T']):
            if c[d_1[0], t , k, l] + s[d_1[0], t , k, l] == 2:
                U[i,d_1[0], t, k, l] = 1

            if c[d_2[0], t , k, l] + s[d_2[0], t , k, l] == 2:
                U[i,d_2[0], t, k, l] = 1

        for t in range(data['T']):
            if t >= d_1[1]:
                S[i, d_1[0], t] = 1
            if t >= d_2[1]:
                S[i, d_2[0], t] = 1


        for t in range(data['T']):
            if t <= d_1[2]:
                C[i, d_1[0], t] = 1
            if t <= d_2[2]:
                C[i, d_2[0], t] = 1 

    model = gr.read('C:\English_Lesson.lp')
    # model = gr.read('C:\gurobi950\win64\examples\data\coins.lp')

    # y_00 = model.getVarByName(f'y[{0},{0}]')
    # print(y_00)

    # self.y = self.model.addVars(J, K, vtype = gr.GRB.BINARY, name = "y")
    for j in range(data['J']):
        for k in range(data['K']):
            model.getVarByName(f'y[{j},{k}]').Start = int(y[j,k])

  

    # self.z = self.model.addVars(K, L, vtype = gr.GRB.BINARY, name = "z")
    for k in range(data['K']):
        for l in range(data['L']):
            model.getVarByName(f'z[{k},{l}]').Start = int(z[k,l])

    # self.c = self.model.addVars(D, T, K, L, vtype = gr.GRB.BINARY, name = "c")
    # self.s = self.model.addVars(D, T, K, L, vtype = gr.GRB.BINARY, name = "s")
    for d in range(data['D']):
        for t in range(data['T']):
            for k in range(data['K']):
                for l in range(data['L']):
                    model.getVarByName(f'c[{d},{t},{k},{l}]').Start = int(c[d,t,k,l])
                    model.getVarByName(f's[{d},{t},{k},{l}]').Start = int(s[d,t,k,l])
        
    
    # self.p = self.model.addVars(D, K, L, vtype = gr.GRB.BINARY, name = "p")
    for d in range(data['D']):
        for k in range(data['K']):
            for l in range(data['L']):
                model.getVarByName(f'p[{d},{k},{l}]').Start = int(p[d,k,l])
        


    # # Преводаватели

    # self.u = self.model.addVars(I, K, L, vtype = gr.GRB.BINARY, name = "u")
    for i in  range(data['I']):
        for k in range(data['K']):
            for l in range(data['L']):
                model.getVarByName(f'u[{i},{k},{l}]').Start = int(u[i,k,l])

    # self.P = self.model.addVars(I, D, vtype = gr.GRB.BINARY, name = "P")
    for i in range(data['I']):
        for d in range(data['D']):
            model.getVarByName(f'P[{i},{d}]').Start = int(P[i,d])


    # self.U = self.model.addVars(I, D, T, K, L, vtype = gr.GRB.BINARY, name = "U")
    for i in range(data['I']):
        for d in range(data['D']):
            for t in range(data['T']):
                for k in range(data['K']):
                    for l in range(data['L']):
                        model.getVarByName(f'U[{i},{d},{t},{k},{l}]').Start = int(U[i,d,t,k,l])

    # self.S = self.model.addVars(I, D, T, vtype = gr.GRB.BINARY, name = "S")
    # self.C = self.model.addVars(I, D, T, vtype = gr.GRB.BINARY, name = "C")
    for i in range(data['I']):
        for d in range(data['D']):
            for t in range(data['T']):
                model.getVarByName(f'S[{i},{d},{t}]').Start = int(S[i,d,t])
                model.getVarByName(f'C[{i},{d},{t}]').Start = int(C[i,d,t])

    model.update()
    model.params.TimeLimit = 600

    model.optimize()

if __name__ == "__main__":
    main()