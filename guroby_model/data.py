import numpy as np
from params import *

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

class Data:
    
    def __init__(self, J, L, I, T, D, r, minN, maxN, timeL ):
        self.J = J
        self.L = L
        self.D = D
        self.T = T
        self.I = I
        self.r = r
        self.minN = minN
        self.maxN = maxN
        self.timeL = timeL
        self.listCoupleDays = get_list_of_couple_of_days(D)
        self.timeRec = None
        self.courseRec = None
      

    def read_input(self, file_name = None):
        if file_name == None:
            return 0

        fileOrders = open(file_name)
        orders = fileOrders.readlines()
        input_str_a = orders[3]
        input_str_b = orders[1]
        fileOrders.close()

        a = np.fromstring(input_str_a, dtype = int, sep = ' ').reshape((self.J, self.D, self.T))
        self.courseRec = np.fromstring(input_str_b, dtype = int, sep = ' ').reshape((self.J, self.L))
        # self.timeRec = np.fromstring(input_str_a, dtype = int, sep = ' ').reshape((self.J, self.D, self.T))
        self.timeRec = restruct(self.J, self.D, self.T, self.L, self.timeL, a, self.courseRec )
        return 0

    
    
    def students_stats(self):
        
        num_st_of_course = np.sum(self.courseRec, axis=0)

        num_gr_of_course = np.ceil(np.divide(num_st_of_course, 8))
        
        
        print(num_st_of_course)


    
    def school_power(self):
        
        return self.D * self.r * teacherLimit 
    
    def get_dict_form(self):
        
        
        new_data = {}
        new_data['J'] = J
        new_data['L'] = L
        new_data['D'] = D# num of day
        new_data['T'] = T# num of timslots in the 
        new_data['I'] = I# num of teachers
        new_data['r'] = r # num of rooms
        new_data['number_working_rooms'] = r # num of rooms
        new_data['minNumber'] = minN# min number of students in the group
        new_data['maxNumber'] = maxN# max number of students in the group
        new_data['timeLessons']  = timeL 

        new_data['couple_of_Days'] =  get_list_of_couple_of_days(D)

        new_data['timeslot_of_students'] = self.time_rec
        new_data['course_of_students'] = self.course_rec
        
        return new_data
            
    
    def up_bound(self):
        
        num_gr_of_course = np.floor(np.divide(np.sum(self.courseRec, axis=0), self.maxN))
        rem_st_of_course = np.mod(np.sum(self.courseRec, axis=0), self.maxN)
        # print(np.sum(self.courseRec, axis=0))
        # print(num_gr_of_course)
        # print(rem_st_of_course)
        count_gr = np.zeros((self.L))
        
        objval = 0.0
        
        P = self.school_power()
        R = 0
        
 
        
        while(True): 
            
            # print(P,R)
            gr_course = None
            gr_R = 0.0 
            gr_objval = 0.0
            
            
            for l in range(self.L):
                k = int(count_gr[l])
                
                if k >= K:
                    break
                
                if k == num_gr_of_course[l] + 1:
                    continue
                
                value =  self.maxN  if k < num_gr_of_course[l] else rem_st_of_course[l]
                value-=F[l,k]
                if value <= 0:
                    continue
                
                if  gr_objval < value and R + 2*timeL[l] <= P:
                    gr_objval = value
                    gr_course = l
                    gr_R = 2*timeL[l]
            
            if gr_course == None:
                break
            
            
            count_gr[gr_course]+=1
            R+= gr_R
            objval+=gr_objval
        
        
        # print(R, objval)
        # print(count_gr)
        return objval
            
                
                
            
        
        
        
        
            
            
            
        
        
        
        


def get_list_of_couple_of_days(num_days):
    list = []

    for d_1 in np.arange(num_days):
        for d_2 in np.arange(d_1 + 2, num_days):
            list.append((d_1,d_2))

    return np.array(list)

    