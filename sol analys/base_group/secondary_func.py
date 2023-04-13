import numpy as np

def info_array_rec(array_data):

    print(np.shape(array_data))
    print(array_data[:,:,0])
    print(np.max(array_data[:,:,0]))
    print(np.argmax(array_data[:,:,0]))

    for t in range(44):
        print(array_data[:,t,0])
    return None

def time_for_begin(timeslots, T , D, timeL):


    load_days = [[] for __ in range(D)]

    for d in range(D):
        t = 0
        ind = False
        while( t <= T - timeL):
            if int(timeslots[d,t]) == 1.0:
                if ind:
                    if int(timeslots[d,t + timeL - 1] )== 1:
                        load_days[d].append(t)
                        t+=1
                    else:
                        ind = False
                        t+=timeL
                else:
                    if int(np.sum(timeslots[d,t: t + timeL])) == timeL:
                        ind = True
                        load_days[d].append(t)
                        t+=1
                    else:
                        t+=timeL
            else:
                t+=1


    return load_days
    
            


def get_list_of__student( data):

    list_set_J = [[] for __ in  range(data['L'])]
    for j in range(data['J']):
        for l in range(data['L']):
            if data['course_of_students'][j,l] == 1:
                list_set_J[l].append(j)
                break

    return list_set_J


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




def create_array_rec( data, time_begin_for_st, set_id_students):
    """ Создает массив записи студентов"""

    couple_days = data['couple_of_Days']
    numDays = len(data['couple_of_Days'])
    T = 4*data['T']
    A = np.zeros((T, T, numDays))
    for j in set_id_students:

        list_time = time_begin_for_st[j]
        for i in range(numDays):
            d_1 = couple_days[i][0]
            d_2 = couple_days[i][1]
            if list_time[d_1] == [] or list_time[d_2] == []:
                continue
            for t_1 in list_time[d_1]:
                for t_2 in list_time[d_2]:
                        A[t_1, t_2, i]+= 1




    return A

def check_lengh(l, data, t_1, t_2, j, i):

    couple_of_days = data['couple_of_Days']
    timeSlots = data['timeslot_of_students']
    time_lesson = data['timeLessons'][l]

    for t in range(time_lesson):
        if t_1 + t >= 44 or t_2 + t >= 44:
            return False
    

        if timeSlots[j, couple_of_days[i][0],t_1 + t] != 1 or timeSlots[j, couple_of_days[i][1],t_2 + t] != 1:
            return False

    return True

def check(t_1, t_2, timeL, number_working_rooms, d_1, d_2):

    
    
    for t in range(timeL):
        if t_1 + t >= 44 or t_2 + t >= 44:
            return False

        if number_working_rooms[d_1, t_1 + t] == 0 or number_working_rooms[d_2, t_2 + t] == 0:
            return False
        
        
                        
    return True
    



def refresh_array(i, array_data, data, list_time):
    """ Обновляет массив заявок, убирая занятых студентов"""

    couple_of_days = data['couple_of_Days']


    for i in np.arange(len(couple_of_days)):
        d_1 = couple_of_days[i][0]
        d_2 = couple_of_days[i][1]
        if list_time[d_1] == [] or list_time[d_2] == []:
            continue
        for t_1 in list_time[d_1]:
            for t_2 in list_time[d_2]:
                array_data[t_1, t_2, i]-= 1
             

    return array_data



def create_group( i, t_1, t_2, l, cor, data, shedule, J ):
    """ Создает группу по заданным параметрам времени"""

    maxPerson = data['maxNumber']
    students = shedule['students']
    groups =  shedule['groups']
    couple_of_days = data['couple_of_Days']
    timeSlots = data['timeslot_of_students']
    d_1, d_2 = couple_of_days[i]
    k = len(groups[l]) + 1


    ind = 0
    list_students = []
    while ( ind < cor ):
        
        for j in J:
            if (ind == maxPerson):
                break
            
            
            if check_lengh(l, data, t_1, t_2, j, i):
            # if timeSlots[j,d_1,t_1] == 1 and timeSlots[j,d_2,t_2] == 1:
         

                students[j] = k
                list_students.append(j)
            
                ind+= 1
                continue
        

    groups[l].append([list_students, k, l, data['couple_of_Days'][i], t_1, t_2])
    
    return  list_students


