import json
import numpy as np
# from params import *
from tabulate import tabulate

from sol_analys.params import *

class Solution:

    def __init__(self, filename ="sol.json"):
        
        
        with open(filename,'r') as file:
            self.groups = json.load(file)


        self.y = np.zeros( (J, K) )
        self.z = np.zeros( (K,L) )
        self.s = np.zeros( (D, 4*T, K, L) )
        self.c = np.zeros( (D, 4*T, K, L) )
        self.p = np.zeros( (D, K, L))

        self.u = np.zeros( (I, K, L) )
        self.U = np.zeros( (I, D, 4*T, K, L) )
        self.S = np.zeros( (I, D, 4*T) )
        self.C = np.zeros( (I, D, 4*T) )
        self.P = np.zeros( (I, D) )

        for group in self.groups:
  

            list_students = group[0]
            k = group[1] - 1
            l = group[2]
            i = group[5]
            d_1 =group[3]
            d_2 = group[4]

            for j in list_students:
                self.y[j,k] = 1 

            self.z[k,l] = 1

            for t in range(4*T):
                if t >= d_1[1]:
                    self.s[d_1[0], t , k, l] = 1
                if t >= d_2[1]:
                    self.s[d_2[0], t , k, l] = 1


            for t in range(4*T):
                if t <= d_1[2]:
                    self.c[d_1[0], t , k, l] = 1
                if t <= d_2[2]:
                    self.c[d_2[0], t , k, l] = 1

            self.p[d_1[0], k, l] = 1
            self.p[d_2[0], k, l] = 1

            self.u[i, k, l] = 1
            
            self.P[i,d_1[0]] = 1
            self.P[i,d_2[0]] = 1

            for t in range(4*T):
                if self.c[d_1[0], t , k, l] + self.s[d_1[0], t , k, l] == 2:
                    self.U[i,d_1[0], t, k, l] = 1

                if self.c[d_2[0], t , k, l] + self.s[d_2[0], t , k, l] == 2:
                    self.U[i,d_2[0], t, k, l] = 1

            for t in range(4*T):
                if t >= d_1[1]:
                    self.S[i, d_1[0], t] = 1
                if t >= d_2[1]:
                    self.S[i, d_2[0], t] = 1


            for t in range(4*T):
                if t <= d_1[2]:
                    self.C[i, d_1[0], t] = 1
                if t <= d_2[2]:
                    self.C[i, d_2[0], t] = 1 

    def rename_group(self):
        groups =self.groups

        couse_count = np.ones((L))
        for gr in groups:
            l = gr[2]
            gr[1] = int(couse_count[l])
            couse_count[l]+= 1

        self.y = np.zeros( (J, K) )
        self.z = np.zeros( (K,L) )
        self.s = np.zeros( (D, 4*T, K, L) )
        self.c = np.zeros( (D, 4*T, K, L) )
        self.p = np.zeros( (D, K, L))

        self.u = np.zeros( (I, K, L) )
        self.U = np.zeros( (I, D, 4*T, K, L) )
        self.S = np.zeros( (I, D, 4*T) )
        self.C = np.zeros( (I, D, 4*T) )
        self.P = np.zeros( (I, D) )

        for group in self.groups:
  

            list_students = group[0]
            k = group[1] - 1
            l = group[2]
            i = group[5]
            d_1 =group[3]
            d_2 = group[4]

            for j in list_students:
                self.y[j,k] = 1 

            self.z[k,l] = 1

            for t in range(4*T):
                if t >= d_1[1]:
                    self.s[d_1[0], t , k, l] = 1
                if t >= d_2[1]:
                    self.s[d_2[0], t , k, l] = 1


            for t in range(4*T):
                if t <= d_1[2]:
                    self.c[d_1[0], t , k, l] = 1
                if t <= d_2[2]:
                    self.c[d_2[0], t , k, l] = 1

            self.p[d_1[0], k, l] = 1
            self.p[d_2[0], k, l] = 1

            self.u[i, k, l] = 1
            
            self.P[i,d_1[0]] = 1
            self.P[i,d_2[0]] = 1

            for t in range(4*T):
                if self.c[d_1[0], t , k, l] + self.s[d_1[0], t , k, l] == 2:
                    self.U[i,d_1[0], t, k, l] = 1

                if self.c[d_2[0], t , k, l] + self.s[d_2[0], t , k, l] == 2:
                    self.U[i,d_2[0], t, k, l] = 1

            for t in range(4*T):
                if t >= d_1[1]:
                    self.S[i, d_1[0], t] = 1
                if t >= d_2[1]:
                    self.S[i, d_2[0], t] = 1


            for t in range(4*T):
                if t <= d_1[2]:
                    self.C[i, d_1[0], t] = 1
                if t <= d_2[2]:
                    self.C[i, d_2[0], t] = 1 


    def print_schedule(self, name = "schedule"):


        groups = self.groups

        file_name_all_groups = name + "_all_groups.txt"
        f=open(file_name_all_groups ,"w")


        column_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        value_list = []
        for t in range(timeslotsInHour*T):
            week = []
            for d in range(D):
                lessons = []
                for group in groups:
                    work_time = group[3], group[4]
                    if d == work_time[0][0] and  t in range(work_time[0][1],work_time[0][2] + 1):
                        lessons.append(f"G:{ group[1]},C:{ group[2]},T:{group[5]}")

                    if d == work_time[1][0] and t in range(work_time[1][1],work_time[1][2] + 1):
                        lessons.append(f"G:{ group[1]},C:{ group[2]},T:{group[5]}")
                week.append(lessons)
            value_list.append(week)

        f.write(tabulate(value_list, column_list, tablefmt="grid"))
        f.write('\n')

        f.close()

        file_name_teachers = name + "_teachers.txt"
        f=open(file_name_teachers,"w")

        for i in range(I):
            column_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
            value_list = []
            f.write(str(i))
            f.write("\n")
            for t in range(timeslotsInHour*T):
                week = []
                for d in range(D):
                    lessons = []
                    for group in groups:
                        if group[5] == i:
                            work_time = group[3], group[4]
                            if d == work_time[0][0] and  t in range(work_time[0][1],work_time[0][2] + 1):
                                lessons.append(f"G:{ group[1]},C:{ group[2]},T:{i}")

                            if d == work_time[1][0] and t in range(work_time[1][1],work_time[1][2] + 1):
                                lessons.append(f"G:{ group[1]},C:{ group[2]},T:{i}")
                    
                    
                    week.append(lessons)
                value_list.append(week)

            f.write(tabulate(value_list, column_list, tablefmt="grid"))
            f.write('\n')

        f.close()

    def rooms_distribution(self):

        groups = self.groups 

        rooms_number = np.zeros((timeslotsInHour*T, D, r)) 

        for gr in groups:
            gr.append(0)
            gr.append(0)


        for t in range(timeslotsInHour*T):

            for gr in groups:
                
                
                day_first = gr[3]
                day_second = gr[4]

                if day_first[1] != t and day_second[1] != t:
                    continue
                
                l = gr[2]

                if  day_first[1] == t:
                    room = 0  
                    for r_1 in range(r):
                        if np.sum(rooms_number[day_first[1] + t_point, day_first[0],r_1] for t_point in range(timeL[l])) == 0:
                            for t_point in range(timeL[l]):
                                rooms_number[day_first[1] + t_point, day_first[0],r_1]=1
                                
                            room = r_1+1
                            break
                    
                    gr[6] = room


                if day_second[1] == t:


                    room = 0


                    for r_2 in range(r):
                        if np.sum( rooms_number[day_second[1] + t_point, day_second[0],r_2] for t_point in range(timeL[l])) == 0:
                            for t_point in range(timeL[l]):
                                rooms_number[day_second[1] + t_point, day_second[0],r_2]=1
                                
                            room = r_2+1
                            break

                    gr[7] = room

 
        return None

    def creat_output_schedule(self, name):


        groups = self.groups
        
        f = open(name, 'w')
        for gr in groups:
            day_first = gr[3]
            day_second = gr[4]
            l = gr[2]
            k = gr[1]
            
            i = gr[5]
            room_1 = gr[6]
            room_2 = gr[7]
            f.write(f"{k}\t{l}\t{i}\t{room_1}\t{day_first[0]}\t{day_first[1]}\t{day_first[2]}\t{room_2}\t{day_second[0]}\t{day_second[1]}\t{day_second[2]}\n")
        f.close()

        return None