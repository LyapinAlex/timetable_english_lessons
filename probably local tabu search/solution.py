import json
import numpy as np
from params import *
import matplotlib.pyplot as plt
from tabulate import tabulate
import pdb
# from sol_analys.params import *

class Solution:
    
    def __init__(self, filename ="sol"):
        """ иницализация решения и чтения его из JSON файла"""

       
        with open(filename + ".json",'r') as file:
            self.groups = json.load(file)

        self.recount_group()

        # self.init_vars_of_sol()

        # self.trans_sol_from_groups_to_vars()


    def init_vars_of_sol(self):
        self.y = np.zeros( (J, K), dtype = np.int8 )
        self.z = np.zeros( (K, L), dtype = np.int8 )
        self.s = np.zeros( (D, timeslotsInHour * T, K, L), dtype = np.int8 )
        self.c = np.zeros( (D, timeslotsInHour * T, K, L), dtype = np.int8 )
        self.p = np.zeros( (D, K, L), dtype = np.int8)

        self.u = np.zeros( (I, K, L), dtype = np.int8 )
        self.U = np.zeros( (I, D, timeslotsInHour * T, K, L), dtype = np.int8 )
        self.S = np.zeros( (I, D, timeslotsInHour * T), dtype = np.int8 )
        self.C = np.zeros( (I, D, timeslotsInHour * T), dtype = np.int8 )
        self.P = np.zeros( (I, D), dtype = np.int8 )

    def trans_sol_from_groups_to_vars(self):
        


        for group in self.groups:
            
            # print(group)


            list_students = group[0]
            k = group[1] - 1
            l = group[2]
            i = group[5]
            d_1 =group[3]
            d_2 = group[4]

            for j in list_students:
                self.y[j,k] = 1 

            self.z[k,l] = 1

            for t in range(timeslotsInHour * T):
                if t >= d_1[1]:
                    self.s[d_1[0], t , k, l] = 1
                if t >= d_2[1]:
                    self.s[d_2[0], t , k, l] = 1


            for t in range(timeslotsInHour * T):
                if t <= d_1[2]:
                    self.c[d_1[0], t , k, l] = 1
                if t <= d_2[2]:
                    self.c[d_2[0], t , k, l] = 1

            self.p[d_1[0], k, l] = 1
            self.p[d_2[0], k, l] = 1

            self.u[i, k, l] = 1
            
            self.P[i,d_1[0]] = 1
            self.P[i,d_2[0]] = 1

            for t in range(timeslotsInHour * T):
                if self.c[d_1[0], t , k, l] + self.s[d_1[0], t , k, l] == 2:
                    self.U[i,d_1[0], t, k, l] = 1

                if self.c[d_2[0], t , k, l] + self.s[d_2[0], t , k, l] == 2:
                    self.U[i,d_2[0], t, k, l] = 1

            for t in range(timeslotsInHour * T):
                if t >= d_1[1]:
                    self.S[i, d_1[0], t] = 1
                if t >= d_2[1]:
                    self.S[i, d_2[0], t] = 1


            for t in range(timeslotsInHour * T):
                if t <= d_1[2]:
                    self.C[i, d_1[0], t] = 1
                if t <= d_2[2]:
                    self.C[i, d_2[0], t] = 1 
        
    def recount_group(self):
        """Перенумерация номеров групп для каждого курса"""

        groups = self.groups

        couse_count = np.ones((L))
        for gr in groups:
            l = gr[2]
            gr[1] = int(couse_count[l])
            couse_count[l]+= 1

        self.init_vars_of_sol()

        self.trans_sol_from_groups_to_vars()

    def print_schedule(self, name = "schedule"):
        """создать txt файл с расписание формата таблицы"""

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
                    if d == work_time[0][0] and t in range(work_time[0][1], work_time[0][2] + 1):
                        lessons.append(f"G:{ group[1]},C:{ group[2]},T:{group[5]}")

                    if d == work_time[1][0] and t in range(work_time[1][1], work_time[1][2] + 1):
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
        """Распределение групп по комнатам"""

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

    def get_sol_val(self):
        """Возращает список вида:
                'num_st': количество студентов, 
                'num_gr': количество групп, 
                'obj_val': значение целевой функции}"""
        groups = self.groups

        num_st = 0
        num_gr = len(groups)

        for gr in groups:
            num_st+=len(gr[0])


        course_gr = [[] for __ in range(L)]

        objVal = num_st


        
        for gr in groups:
            course_gr[gr[2]].append(1)


        penalty = 0.0

        for l in range(L):
            penalty_l= len(course_gr[l])
            penalty+= np.sum(F[l,k] for k in range(penalty_l))


        objVal-=penalty



        return {'num_st': num_st, 
                'num_gr': num_gr, 
                'obj_val': objVal}

    def import_JSON(self, name = "sol"):
        """Создать json файл решенея"""
        list_gr = []

        for gr in self.groups:
            
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
        
    def timetable_from_sol(self, name= "schedule"): 
        """Создать png файл с таблицей расписания"""
        self.rooms_distribution()
    
        fig=plt.figure(figsize=(10,5.89))

        # Set Axis
        ax=fig.add_subplot(111)
        ax.yaxis.grid()
        ax.set_xlim(0.0,r * D)
        ax.set_ylim(20.1, 8.9)
        ax.set_xticks(range(2,r * D+2, r))
        ax.set_xticklabels(days)
        ax.set_ylabel('Time')

        # Set Second Axis
        ax2=ax.twiny().twinx()
        ax2.set_xlim(ax.get_xlim())
        ax2.set_ylim(ax.get_ylim())
        ax2.set_xticks(ax.get_xticks())
        ax2.set_xticklabels(days)
        ax2.set_ylabel('Time')

        for d in range(D):
            plt.axvline(r*d,color='black')
        
        for gr in self.groups:
            l = gr[2]
            k = gr[1]
            teacher = int(gr[5])
            room_1 = float(gr[6])
            room_2 = float(gr[7])
            day_first = (float(gr[3][0]),float(gr[3][1]),float(gr[3][2]))
            day_second = (float(gr[4][0]),float(gr[4][1]),float(gr[4][2]))



            
            plt.fill_between([day_first[0]*len(rooms) + room_1 - 1,day_first[0]*len(rooms) + room_1 ], [day_first[1]/4 + 9.0, day_first[1]/4 + 9.0], [day_first[2]/4 + 9.25,day_first[2]/4 + 9.25], color=colors[teacher], edgecolor='k', linewidth=0.5)
            plt.fill_between([day_second[0]*len(rooms) + room_2 - 1,day_second[0]*len(rooms) + room_2 ], [day_second[1]/4 + 9.0, day_second[1]/4 + 9.0], [day_second[2]/4 + 9.25,day_second[2]/4 + 9.25], color=colors[teacher], edgecolor='k', linewidth=0.5)

            plt.text(day_first[0]*len(rooms) + room_1 - 1+0.02,day_first[1]/4 + 9.0+0.05 ,f"L:{l}K:{k}", va='top', fontsize=5)
            plt.text(day_second[0]*len(rooms) + room_2 - 1+0.02,day_second[1]/4 + 9.0+0.05 ,f"L:{l}K:{k}", va='top', fontsize=5)  

    

        plt.title(name,y=1.07)
        plt.savefig('{0}.png'.format(name), dpi=200)


        return None

    def check_sol_math_model(self, data):
        

        # (2) Если студент в группе, то он может прийти, когда у этой группы занятие,
        for j in range(J):
            for k in range(K):
                for l in range(L):
                    if not np.sum((data.courseRec[j, l]*data.timeRec[j, d, t]*(self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l])) for d in range(D) for t in range(timeslotsInHour * T)) >= 2*data.courseRec[j, l]* data.timeL[l] * self.y[j, k]:
                        raise "ОШИБКА УСЛОВИЕ 2"
        


        #(3) В любой момент времени не может быть больше пар, чем число комнат 
        for d in range(D):
            for t in range(timeslotsInHour * T):
                if not np.sum((self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l])for k in range(K) for l in range(L)) <= r:
                    raise "ОШИБКА УСЛОВИЕ 3"

        #(4) Студент может быть только в одной группе
        for j in range(J):
           if not np.sum(self.y[j, k] for k in range(K)) <= 1:
               raise "ОШИБКА УСЛОВИЕ 4"

        #(5.1) Ограничения на максимальное количество студентов в группе
        for k in range(K):
            for l in range(L):
                if not np.sum(self.y[j, k]*data.courseRec[j, l] for j in range(J)) <= maxN:
                    raise "ОШИБКА УСЛОВИЕ 5.1"
        #(5.2) Ограничения на минимальное количество студентов в группе
        for k in range(K):
            for l in range(L):
                if not np.sum(self.y[j, k]*data.courseRec[j, l] for j in range(J)) >= minN * self.z[k,l]:
                    raise "ОШИБКА УСЛОВИЕ 5.2"

        #(6) Для любой группы в любой день количесво выделеных на нее таймслотов должно равняться продолжительности занятия
        for l in range(L):
            for k in range(K):
                for d in range(D):
                    if not np.sum((self.c[d, t, k, l] +  self.s[d, t, k, l])for t in range(timeslotsInHour * T)) == (timeslotsInHour * T + data.timeL[l])*self.p[d, k, l]:
                        raise "ОШИБКА УСЛОВИЕ 6" 

        #(7) Конкретные пары вместе не идут
        D_w = np.arange(0, D - 1, 1)
        for d in D_w:
            for k in range(K):
                for l in range(L):
                    if not self.p[d, k, l] + self.p[d + 1, k ,l] <= 1:
                        raise "ОШИБКА УСЛОВИЕ 7"
        #(8) Если нет группы, то и нет студента
        for j in range(J):
            for l in range(L):
                for k in range(K):
                    if not self.z[k,l] >= self.y[j,k]*data.courseRec[j,l]:
                        raise "ОШИБКА УСЛОВИЕ 8"
        #(9) Ограничения созданные против борьбы с симметрией
        K_l = np.arange(0, K - 1, 1)
        for l in range(L):
            for k in K_l:
                if not self.z[k,l] >= self.z[k + 1,l]:
                    raise "ОШИБКА УСЛОВИЕ 9"
        #(10) условие на непрерывность S
        T_1 = np.arange(0, timeslotsInHour * T - 1, 1) 
        for d in range(D):
            for t in T_1:
                for k in range(K):
                    for l in range(L):
                       if not self.s[d, t, k, l] <= self.s[d, t + 1, k, l]:
                        raise "ОШИБКА УСЛОВИЕ 10"

        #(11) условие на непрерывность C
        for d in range(D):
            for t in T_1:
                for k in range(K):
                    for l in range(L):
                        if not self.c[d, t, k, l] >= self.c[d, t + 1, k, l]:
                            raise "ОШИБКА УСЛОВИЕ 11"
        #(12) Для любой группы два рабочих дня
        for l in range(L):
            for k in range(K):
                if not np.sum((self.p[d, k, l]) for d in range(D)) == 2*self.z[k,l]:
                    raise "ОШИБКА УСЛОВИЕ 12"

        #(13) Для каждой сформированной группы есть преподаватель, руководящей ею
        for l in range(L):
            for k in range(K):
                if not np.sum((self.u[i, k, l]) for i in range(I)) == self.z[k,l]:
                    raise "ОШИБКА УСЛОВИЕ 13"
        #(14) Расписание преподавателя для каждой группы
        for i in range(I):
            for d in range(D):
                for t in range(timeslotsInHour * T):
                    for k in range(K):
                        for l in range(L):
                            if not self.U[i, d, t, k, l] <= self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l]:
                                raise "ОШИБКА УСЛОВИЕ 14"
                            if not self.U[i, d, t, k, l] <= self.u[i, k, l]:
                                raise "ОШИБКА УСЛОВИЕ 14"
                            if not self.c[d, t, k, l] +  self.s[d, t, k, l] - self.p[d, k, l] + self.u[i, k, l] - self.U[i, d, t, k, l] <= 1:
                                raise "ОШИБКА УСЛОВИЕ 14"
        #(15) Преподаватель в любой момент времени работает только с одной группой
        for i in range(I):
            for d in range(D):
                for t in range(timeslotsInHour * T):
                    if not np.sum(self.U[i, d, t, k, l] for k in range(K) for l in range(L)) <= 1:
                        raise "ОШИБКА УСЛОВИЕ 15"
        # (16) После занятия, у преподавателя идет перерыв 
        # for i in range(I):
        #     for d in range(D):
        #         for t in range(timeslotsInHour * T):
        #             for k in range(K):
        #                 for l in range(L):
        #                     if t >= timeslotsInHour * T - data.timeL[l] - 1:
        #                         continue
        #                     for k_1 in range(K):
        #                         for l_1 in range(L):
        #                             if not self.U[i, d, t + 1, k, l] - self.U[i, d, t, k, l] + self.U[i, d, t + data.timeL[l] + 1, k_1, l_1] <= 1:
        #                                 raise "ОШИБКА УСЛОВИЕ 16"
        for i in range(I):
            for d in range(D):
                for t in range(timeslotsInHour * T):
                    for k_1 in range(K):
                        for l_1 in range(L):
                            if t >= timeslotsInHour * T - 1:
                                continue
                            if not np.sum(self.U[i, d, t, k, l] for k in range(K) for l in range(L)) <= self.c[d, t, k_1, l_1] +  self.s[d, t, k_1, l_1] - self.p[d, k_1, l_1] + 1 - self.U[i, d, t + 1, k_1, l_1] :
                                raise "ОШИБКА УСЛОВИЕ 16"
        #(17) Если у преподователя занимается группа в день d, то и он должен работать в этот день
        for i in range(I):
            for k in range(K):
                for l in range(L):
                    for d in range(D):
                        if not self.p[d, k, l] + self.u[i, k, l] - self.P[i, d] <= 1:
                            raise "ОШИБКА УСЛОВИЕ 17"
        #(18) У всех преподавателей не больше пяти рабочих дней
        for i in range(I):
            if not np.sum(self.P[i, d] for d in range(D)) <= 5:
                raise "ОШИБКА УСЛОВИЕ 18"

        # #(19) Условия на задание рабочий таймслотов преподавателя
        for i in range(I):
            for d in range(D):
                for t in range(timeslotsInHour * T):
                    if not np.sum(self.U[i, d, t, k, l] for k in range(K) for l in range(L)) <= self.S[i, d, t]:
                        raise "ОШИБКА УСЛОВИЕ 19"
                    if not np.sum(self.U[i, d, t, k, l] for k in range(K) for l in range(L)) <= self.C[i, d, t]:
                        raise "ОШИБКА УСЛОВИЕ 19"
                    if t + 1 == timeslotsInHour * T:
                        continue
                    if not self.S[i, d, t] <= self.S[i, d, t + 1]:
                        raise "ОШИБКА УСЛОВИЕ 19"
                    if not self.C[i, d, t] >= self.C[i, d, t + 1]:
                        raise "ОШИБКА УСЛОВИЕ 19"
        #(20) Условия на продолжительность рабочего дня
         

        for i in range(I):
            for d in range(D):
                if not np.sum((self.C[i, d, t] +  self.S[i, d, t])for t in range(timeslotsInHour * T)) <= (timeslotsInHour * T + teacherLimit)*self.P[i, d]:
                    raise "ОШИБКА УСЛОВИЕ 20"

       
        return True

    def check_sol_alg(self, data):
        
        taken_students = np.zeros(J)
        create_groups = np.zeros((K,L))

        groups = self.groups
        for group in groups:
            # (1) Все студенты имеет курc группы
            list_st = group[0]
            if type(list_st) is not list:
                raise f"ОШИБКА ФОРМАТ РЕШЕНИЯ"

            k = group[1]
            if type(k) is not int:
                raise f"ОШИБКА ФОРМАТ РЕШЕНИЯ"
            if  k < 1 or k > K:
                raise f"ОШИБКА НОМЕРА ГРУППЫ" 

            l = group[2]
            if type(l) is not int:
                raise f"ОШИБКА ФОРМАТ РЕШЕНИЯ"
            if  l < 0 or l >= L:
                raise f"ОШИБКА КУРСА ГРУППЫ" 

            if create_groups[k - 1, l ] == 1:
                raise "ОШИБКА ГРУППЫ ОБЛАДАЮТ ОДНИМ НОМЕРОК К"
            
            create_groups[k - 1, l ] = 1

            for j in list_st:
                if type(j) is not int:
                    raise f"ОШИБКА ФОРМАТ РЕШЕНИЯ"

                if j < 0 or j >= J :

                    raise f"ОШИБКА НЕВЕРНО ЗАДАН НОМЕР СТУДЕНТА"


                if taken_students[j] == 1:
                    raise f"ОШИБКА СТУДЕНТ {j} ЧИСЛИТЬСЯ В НЕСКОЛЬКИ ГРУППАХ"
                else:
                    taken_students[j]+=1


       
                if data.courseRec[j, l] == 0:
                    raise f"ОШИБКА СТУДЕНТ В ГРУППЕ {k} {l} НЕ СВОЕГО КУРСА"

            num_st = len(list_st)
            if num_st < minN or num_st > maxN:
                raise f"ОШИБКА ЧИСЛЕНОСТЬ ГРУППЫ {k} {l} НЕ ПОДХОДИТ НАЧАЛЬНЫМ УСЛОВИЯМ"
            

            first_day = group[3]
            second_day = group[4]
            if type(first_day) is not list or  type(second_day) is not list:
                raise f"ОШИБКА ФОРМАТ РЕШЕНИЯ"
            if len(first_day) != 3 or len(second_day) != 3:          
                raise f"ОШИБКА ФОРМАТ РЕШЕНИЯ"
            for el in first_day:
                if type(el) is not int:
                    raise f"ОШИБКА ФОРМАТ РЕШЕНИЯ"
            for el in second_day:
                if type(el) is not int:
                    raise f"ОШИБКА ФОРМАТ РЕШЕНИЯ"
            if first_day[0] < 0 or first_day[0] >= D or second_day[0] < 0 or second_day[0] >= D:
                raise f"ОШИБКА ФОРМАТ РЕШЕНИЯ"
            if first_day[1] < 0 or first_day[1] >= timeslotsInHour * T or second_day[1] < 0 or second_day[1] >= timeslotsInHour * T:
                raise f"ОШИБКА ФОРМАТ РЕШЕНИЯ"
            if first_day[2] < 0 or first_day[2] >= timeslotsInHour * T or second_day[2] < 0 or second_day[2] >= timeslotsInHour * T:
                raise f"ОШИБКА ФОРМАТ РЕШЕНИЯ"

            if  abs(first_day[0] - second_day[0]) <= 1:
                raise f"ОШИБКА С РАБОЧИМИ ДНЯМИ ГРУППЫ {k} {l}"



            
            for j in list_st:
                for t_1 in range(first_day[1], first_day[2] + 1):
                    if data.timeRec[j, first_day[0], t_1] == 0:
                        raise f"ОШИБКА СТУДЕНТ {j} НЕ МОЖЕТ ЗАНИМАТЬСЯ  С ГРУППОЙ {k} {l}"
                    

                for t_2 in range(second_day[1], second_day[2] + 1):
                    if data.timeRec[j, second_day[0], t_2] == 0:
                        raise f"ОШИБКА СТУДЕНТ {j} НЕ МОЖЕТ ЗАНИМАТЬСЯ  С ГРУППОЙ {k} {l}"
                    

            if first_day[2] + 1 - first_day[1] != data.timeL[l] or second_day[2] + 1 - second_day[1] != data.timeL[l]:
                raise f"ОШИБКА ГРУППА {k} {l} ОБЛАДАЕТ НЕВЕРНОЙ ПРОДОЛЖИТЕЛЬНОСТЬ"

            if type(group[5]) is not int:
                raise f"ОШИБКА ФОРМАТ РЕШЕНИЯ"

            if not group[5] in range(I):
                raise f"ОШИБКА ГРУППЕ {k} {l} НЕПРАВИЛЬНО НАЗНАЧЕН ПРЕПОДАВАТЕЛЬ { group[5]}"
            
        teacher_worktimes = np.zeros((I, K, L, D, timeslotsInHour * T ))

        for group in groups:
            k = group[1]
            l = group[2]
            teacher = group[5] 
            first_day = group[3]
            second_day = group[4]
            for t_1 in range(first_day[1], first_day[2] + 1):
                teacher_worktimes[teacher, k, l, first_day[0], t_1]+=1
            for t_2 in range(second_day[1], second_day[2] + 1):
                teacher_worktimes[teacher, k, l, second_day[0], t_2]+=1

        max_room = 0
        for d in range(D):
            for t in range(timeslotsInHour * T):
                room_used = np.sum(teacher_worktimes[:, :, :, d, t])
                if room_used > max_room:
                    max_room = room_used
  
        if max_room > r:
            raise f"ОШИБКА РЕШЕНИЮ ТРЕБУЕТСЯ {max_room} КОМНАТ. У ШКОЛЫ ВСЕГО {r} КОМНАТ"
        
    


        for i in range(I):
            for d in range(D):
                for t in range(timeslotsInHour * T):
                    if np.sum(teacher_worktimes[i, :, :, d, t]) > 1:
                        raise f"ОШИБКА ПРЕПОДАВАТЕЛЬ {i} В ДЕНЬ {d} И ВРЕМЯ {t} РАБОТАЕТ С НЕСКОЛЬКИМИ ГРУППАМИ"

        for i in range(I):
            num_work_days = 0
            for d in range(D):
                if np.sum(teacher_worktimes[i, :, :, d, :]) > 0:
                    num_work_days+=1
            if num_work_days > D - 1:
                raise f"ОШИБКА ПРЕПОДАВАТЕЛЬ {i} НЕ ИМЕЕТ ВЫХОДНОГО"
        
        for i in range(I):
            for d in range(D):
                t_start = timeslotsInHour * T
                t_finish = 0
                for t in range(timeslotsInHour * T):
                    if np.sum(teacher_worktimes[i, :, :, d, t]) > 0:
                        t_start = t
                        break
                
                for t in range(timeslotsInHour * T - 1, -1, -1):
                    if np.sum(teacher_worktimes[i, :, :, d, t]) > 0:
                        t_finish = t
                        break
                
                if t_finish - t_start + 1 > teacherLimit:
                    raise f"ОШИБКА ПРЕПОДАВАТЕЛЬ {i} В ДЕНЬ {d} ПЕРЕРАБАТЫВАЕТ СВОИ ЧАСЫ"


        for group in groups:
            teacher = group[5] 
            first_day = group[3]
            second_day = group[4]

            if first_day[1]  != 0 and np.sum(teacher_worktimes[teacher, :, :, first_day[0], first_day[1] - 1]) > 0:
                raise f"ОШИБКА ПРЕПОДАВАТЕЛЬ {i} В ДЕНЬ {d} НЕ ОТДЫХАЕТ МЕЖДУ ПАРАМИ"

            if second_day[1]  != 0 and np.sum(teacher_worktimes[teacher, :, :, second_day[0], second_day[1] - 1]) > 0:
                raise f"ОШИБКА ПРЕПОДАВАТЕЛЬ {i} В ДЕНЬ {d} НЕ ОТДЫХАЕТ МЕЖДУ ПАРАМИ"

        return True

# Неиспользуемые функции
    def analysis(self, data, J):
        
        students_num = np.zeros((D, timeslotsInHour*T, L), dtype=np.uint8)

        for j in  J:
            for l in range(L):
                if data.courseRec[j,l] == 1:
                    for d in range(D):
                        for t in range(timeslotsInHour*T):
                            students_num[d,t,l] += int(data.timeRec[j,d,t])

        
        fig=plt.figure(figsize=(10,5.89))
        # fig=plt.figure(figsize=(5,5))
        # Set Axis
        ax=fig.add_subplot(111)
        ax.yaxis.grid()
        ax.set_xlim(0.5, D + 0.5)
        ax.set_ylim(20.1, 8.9)
        ax.set_xticks(range(1, D + 1))
        ax.set_xticklabels(days)
        ax.set_ylabel('Time')

        # Set Second Axis
        ax2=ax.twiny().twinx()
        ax2.set_xlim(ax.get_xlim())
        ax2.set_ylim(ax.get_ylim())
        ax2.set_xticks(ax.get_xticks())
        ax2.set_xticklabels(days)
        ax2.set_ylabel('Time')

        for d in range(D):
            plt.axvline(d + 0.5,color='black')
        
        
        for d in range(D):
            for t in range(timeslotsInHour*T):
                for l in range(L):


                # plt.fill_between([day_first[0] + room_1 - 1,day_first[0] + room_1 ], [day_first[1]/4 + 9.0, day_first[1]/4 + 9.0], [day_first[2]/4 + 9.25,day_first[2]/4 + 9.25], color=colors[teacher], edgecolor='k', linewidth=0.5)


                # plt.fill_between([day_second[0] + room_2 - 1,day_second[0] + room_2 ], [day_second[1]/4 + 9.0, day_second[1]/4 + 9.0], [day_second[2]/4 + 9.25,day_second[2]/4 + 9.25], color=colors[teacher], edgecolor='k', linewidth=0.5)

                # plt.text(day_first[0] + room_1 - 1+0.02,day_first[1]/4 + 9.0+0.05 ,f"L:{l}K:{k}", va='top', fontsize=5)
                    plt.text(d + l/13 + 0.5 , t/4 + 9.0 + 0.05 ,f"{students_num[d,t,l]}", va='top', fontsize=5)    

        name_schedule = 'cash'
        plt.title(name_schedule,y=1.07)
        plt.savefig('{0}.png'.format(name_schedule), dpi=200)

    def creat_output_schedule_txt(self, name):


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

        
