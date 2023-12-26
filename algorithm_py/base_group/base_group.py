import numpy as np
import time

from .creat_schedule import *

def base_group(data, config = None):
    """Создает первое приблеженное решение, создавая группы и рапредиляя их по таймслотам.
        На фход принимает тип data, config.
        config = None, запускает одну иттерацию
        config = "heur", запускает одну иттерацию с эвристикой
        сonfis = "rand", запускает одну иттерацию с рандомизацией

        Возращает словарь schedule:
        students - массив в какой группе k находиться студент j.
        groups - список групп
        rooms - массив показывающий сколько групп занимается в день d, и время t
    """


    schedule = {
        'students': np.zeros((data['J'])), 
        'groups': [ [] for __ in range(data['L'])],
        'rooms': np.zeros((data['D'], data['T']))  
        }
   
    if config == None:
        create_schedule(data, schedule)
    if config == "rand":
        raise "Launch dont finish method"
        create_schedule_rand(data, schedule)

    return schedule 



# def  num_students_in_course(l, data):

#     num = 0
#     for j in range(data['J']):
#         num+=data['course_of_students'][j,l]
    
#     return num

# def sort_by_num_students_in_course(data):
    
#     B = list(range(data['L']))    
#     B.sort(key = lambda x: num_students_in_course(x, data) )

#     return np.array(B)


# def create_array_rec(l, data, schedule):

#     couple_of_days = data['couple_of_Days']
#     numDays = len(data['couple_of_Days'])
#     T = data['T']
#     J = data['J']
#     timeSlots = data['timeslot_of_students']
#     A = np.zeros((data['T'], data['T'], numDays))
#     for j in range(J):
#         if data['course_of_students'][j,l] == 1 and schedule['students'][j] == 0:
#             for t_1 in range(T):
#                 for t_2 in range(T):
#                     for i in range(numDays):
#                         if timeSlots[j, couple_of_days[i][0],t_1] == 1 and timeSlots[j, couple_of_days[i][1],t_2] == 1:
#                             A[t_1, t_2, i]+= 1

#     return A


# def refresh_array(j , i, array_data, data):

#     timeSlots = data['timeslot_of_students']
#     T = data['T']
#     couple_of_days = data['couple_of_Days']
#     for i in np.arange(len(couple_of_days)):
#         d_1, d_2 = couple_of_days[i]
#         for t_1 in range(T):
#             for t_2 in range(T):
#                 if timeSlots[j,d_1,t_1] and timeSlots[j,d_2,t_2]:
#                     array_data[t_1, t_2, i] -= 1


#     return array_data

# def create_group( i, t_1, t_2, l, cor, data, shedule):

#     d_1, d_2 = data['couple_of_Days'][i]
#     timeSlots = data['timeslot_of_students']
#     maxPerson = data['maxNumber']
#     course = data['course_of_students']
#     J = data['J']
#     students = shedule['students']
#     groups =  shedule['groups']
#     rooms = shedule['rooms']

#     k = len(groups[l]) + 1

#     rooms[d_1, t_1] += 1
#     rooms[d_2, t_2] += 1

#     ind = 0
#     list_students = []
#     while ( ind < cor ):
        
#         for j in range(J):
#             if (ind == maxPerson):
#                 break
#             if students[j] != 0:
#                 continue
            
#             if course[j,l] == 1:
#                 # print(j)
#                 if timeSlots[j,d_1,t_1] == 1 and timeSlots[j,d_2,t_2] == 1:
#                     students[j] = k
#                     list_students.append(j)
#                     # print(j, "suc")
                
#                     ind+= 1
#                     continue
            
        
#     groups[l].append([list_students, k, l, data['couple_of_Days'][i], t_1, t_2])
    
#     return  list_students

# def create_schedule(data, schedule):
#     r = data['r']
#     T = data['T']
#     maxPerson = data['maxNumber']
#     minPerson = data['minNumber']
#     B = sort_by_num_students_in_course(data)
#     couple_of_days = data['couple_of_Days']
#     numDays = len(couple_of_days)


#     for l in B:
    

#         cor = maxPerson
#         while cor >= minPerson:
#             ind = False 
#             array_data = create_array_rec(l, data, schedule)
            
#             for t_1 in range(T):
#                 for t_2 in range(T):
#                     for i in np.arange(numDays):
#                         days = couple_of_days[i]
#                         if (schedule['rooms'][days[0], t_1] < r) and (schedule['rooms'][days[1], t_2] < r):
#                             if array_data[t_1,t_2, i] >= cor:
#                                 list_students = create_group( i, t_1, t_2, l, cor, data, schedule)
#                                 for j in list_students:
#                                     refresh_array(j , i, array_data, data)

#                                 ind = True


#             if ind == False:
#                 cor -= 1
    
#     return None

# def create_schedule_rand(data, schedule):
#     r = data['r']
#     T = data['T']
#     L = data['L']
#     maxPerson = data['maxNumber']
#     minPerson = data['minNumber']
#     couple_of_days = data['couple_of_Days']
#     numDays = len(couple_of_days)

#     course_order  = np.arange(L)
#     shuffle(course_order)

#     days_order = np.arange(numDays)
#     shuffle(days_order)

#     time_order = np.arange(T)
#     shuffle(time_order)

#     for l in course_order:
    

#         cor = maxPerson
#         while cor >= minPerson:
#             ind = False 
#             array_data = create_array_rec(l, data, schedule)
            
#             for t_1 in time_order:
#                 for t_2 in time_order:
#                     for i in days_order:
#                         days = couple_of_days[i]
#                         if (schedule['rooms'][days[0], t_1] < r) and (schedule['rooms'][days[1], t_2] < r):
#                             if array_data[t_1,t_2, i] >= cor:
#                                 list_students = create_group( i, t_1, t_2, l, cor, data, schedule)
#                                 for j in list_students:
#                                     refresh_array(j , i, array_data, data)

#                                 ind = True


#             if ind == False:
#                 cor -= 1
    
#     return None





if __name__ == "__main__":
    print("!")