import numpy as np


def  num_students_in_course(l, data):
    """ Считает сколько студентов на курсе l"""

    num = 0
    for j in range(data['J']):
        num+=data['course_of_students'][j,l]
    

    return num

def sort_by_num_students_in_course(data):
    """ Возращает список курсов, отсортированный по количеству студентов"""
    
    B = list(range(data['L']))    
    B.sort(key = lambda x: num_students_in_course(x, data) )


    return np.array(B)


def create_array_rec(l, data, schedule):
    """ Создает массив записи студентов"""

    couple_of_days = data['couple_of_Days']
    numDays = len(data['couple_of_Days'])
    T = data['T']
    J = data['J']
    timeSlots = data['timeslot_of_students']
    A = np.zeros((data['T'], data['T'], numDays))
    for j in range(J):
        if data['course_of_students'][j,l] == 1 and schedule['students'][j] == 0:
            for t_1 in range(T):
                for t_2 in range(T):
                    for i in range(numDays):
                        if timeSlots[j, couple_of_days[i][0],t_1] == 1 and timeSlots[j, couple_of_days[i][1],t_2] == 1:
                            A[t_1, t_2, i]+= 1


    return A


def refresh_array(j , i, array_data, data):
    """ Обновляет массив заявок, убирая занятых студентов"""

    timeSlots = data['timeslot_of_students']
    T = data['T']
    couple_of_days = data['couple_of_Days']
    for i in np.arange(len(couple_of_days)):
        d_1, d_2 = couple_of_days[i]
        for t_1 in range(T):
            for t_2 in range(T):
                if timeSlots[j,d_1,t_1] and timeSlots[j,d_2,t_2]:
                    array_data[t_1, t_2, i] -= 1


    return array_data

def create_group( i, t_1, t_2, l, cor, data, shedule):
    """ Создает группу по заданным параметрам времени"""

    d_1, d_2 = data['couple_of_Days'][i]
    timeSlots = data['timeslot_of_students']
    maxPerson = data['maxNumber']
    course = data['course_of_students']
    J = data['J']
    students = shedule['students']
    groups =  shedule['groups']
    rooms = shedule['rooms']

    k = len(groups[l]) + 1

    rooms[d_1, t_1] += 1
    rooms[d_2, t_2] += 1

    ind = 0
    list_students = []
    while ( ind < cor ):
        
        for j in range(J):
            if (ind == maxPerson):
                break
            if students[j] != 0:
                continue
            
            if course[j,l] == 1:
                # print(j)
                if timeSlots[j,d_1,t_1] == 1 and timeSlots[j,d_2,t_2] == 1:


                    students[j] = k
                    list_students.append(j)
                
                    ind+= 1
                    continue
            

    groups[l].append([list_students, k, l, data['couple_of_Days'][i], t_1, t_2])
    
    return  list_students