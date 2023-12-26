import numpy as np
import json
from params  import *
from tabulate import tabulate

# def sol_export_gurobi(data, first_path_sol, second_path_sol):


def get_list_of_couple_of_days(num_days):
    list = []

    for d_1 in np.arange(num_days):
        for d_2 in np.arange(d_1 + 2, num_days):
            list.append((d_1,d_2))

    return np.array(list)

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
    
     
    data['J'] = J# num of studetns
    data['L'] = L# num of course
    data['I'] = I# num of teachers
    data['r'] = r# num of rooms
    data['D'] = D# num of day
    data['T'] = T# num of timslots in the 
    data['minNumber'] = minN# min number of students in the group
    data['maxNumber'] = maxN# max number of students in the group
    data['timeLessons']  = timeL
    data['num_div'] = timeslotsInHour
    


    data['couple_of_Days'] =  get_list_of_couple_of_days(data['D'])
    
    data['timeslot_of_students'] = np.fromstring(input_str_a, dtype = int, sep = ' ').reshape((data['J'], data['D'], data['T']))
    data['course_of_students'] = np.fromstring(input_str_b, dtype = int, sep = ' ').reshape((data['J'], data['L']))

    return data


def print_schedule(data, first_path_sol, second_path_sol, ind = 0):
    
   
    I = data['I']
    D = data['D']
    L = data['L']
    real_time = second_path_sol['real_time']
    teachers_groups = second_path_sol['teachers']
    schedule_of_teachers = second_path_sol['schedule_of_teachers']
    groups = first_path_sol['groups']


    f=open(f"scheduleOfAllGroups_{ind}.txt","w")


    column_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    value_list = []
    for t in range(real_time):
        week = []
        for d in range(D):
            lessons = []
            for i in range(I):
                if ( schedule_of_teachers[i,d,t] == 1):
                    for t_gt in teachers_groups[i]:
                        for group in groups:
                            if t_gt[0] == group[1] and t_gt[1] == group[2]:
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


    f=open(f"scheduleOfTeachers_{ind}.txt","w")

    for i in range(I):
        column_list = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        value_list = []
        f.write(str(i))
        f.write("\n")
        for t in range(real_time):
            week = []
            for d in range(D):
                lessons = []
                if ( schedule_of_teachers[i,d,t] == 1):
                    for t_gt in teachers_groups[i]:
                        for group in groups:
                            if t_gt[0] == group[1] and t_gt[1] == group[2]:
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



    
    return None


def get_solution( first_path_sol ):


    groups = first_path_sol['groups'] 

    solution = {}
    it = 0
    for group in groups:
        if group[5] == False:
            continue


        gr = {}
        gr['num_in_location'] = str(group[1])
        gr['id_teacher'] = str(group[6])
        gr['id_course'] = str(group[2])
        gr['first_day'] = str(group[3][0]) +',' + str(group[3][1])
        gr['second_day'] = str(group[4][0]) +',' + str(group[4][1])
        groupComposition = ''
        for student in group[0]:
            groupComposition+= str(student)
            groupComposition+= ','
        gr['compositionGroup'] = groupComposition
        gr['working_group'] = True
        
        solution[str(it)] = gr
        it+= 1
        

    return solution


def count_students(data, first_path_sol, second_path_sol):
    teachers = second_path_sol['teachers']
    groups = 0
    students = 0

    for group  in first_path_sol['groups']:
        if group[5] == True:
            groups+=1
    

    for i in  range(data['I']):

        for t in teachers[i]:
            for group  in first_path_sol['groups']:

                if group[1] == t[0] and group[2] == t[1]:
                    students+=len(group[0])


    return (students, groups, format(students/groups, '.3f') )

def c_s(first_path_sol):
    students = first_path_sol["students"]
    sm_st = 0
    for j in range(500):
        if students[j] != 0:
            sm_st+= 1

    return sm_st
    # groups = first_path_sol[]

def sort_data(locationParams, solutionsFromDB):


    lastCourses = solutionsFromDB['lastCourses'] 


    timeLessons = []
    for course in lastCourses:
        timeLessons.append(course[1])



    input_str_a = solutionsFromDB['input_str_a']
    input_str_b = solutionsFromDB['input_str_b']


    data = {}
    data['J'] = locationParams['num_students']# num of studetns
    data['L'] = locationParams['num_courses']# num of course
    data['D'] = locationParams['num_work_days']# num of day
    data['T'] = locationParams['num_timeslots']# num of timslots in the day
    data['I'] = locationParams['num_teachers']# num of teachers
    data['r'] = locationParams['num_classes']# num of rooms
    data['minNumber'] = locationParams['min_num_students']# min number of students in the group
    data['maxNumber'] = locationParams['max_num_students'] # max number of students in the group
    data['timeLessons']  = np.array(timeLessons)

    
    data['couple_of_Days'] =  get_list_of_couple_of_days(data['D'])
    
    data['timeslot_of_students'] = np.fromstring(input_str_a, dtype = int, sep = ' ').reshape((data['J'], data['D'], data['T']))
    data['course_of_students'] = np.fromstring(input_str_b, dtype = int, sep = ' ').reshape((data['J'], data['L']))

    return data

def get_objVal(data, first_path_sol, second_path_sol):
    
    groups = first_path_sol["groups"]
    
    num_st = 0
    num_gr = 0
    for gr in groups:
        if gr[5] == True:
            num_gr+=1
    for gr in groups:
        if gr[5] == True:
        
            num_st+=len(gr[0])


    course_gr = [[] for __ in range(L)]

    objVal = num_st
    
    
    for gr in groups:
        if gr[5] == True:
            course_gr[gr[2]].append(1)


    penalty = 0.0

    for l in range(L):
        penalty_l= len(course_gr[l])
        penalty+= np.sum(F[l,k] for k in range(penalty_l))


    objVal-=penalty



    return {'num_st': num_st, 
            'num_gr': num_gr, 
            'obj_val': objVal}

def JSON_import( first_path_sol , filename):


    groups = first_path_sol['groups'] 


    list_gr = []

    for gr in groups:
        
        if gr[5] == False:
            continue
        g = []
        g.append(gr[0])
        g.append(int(gr[1]))
        d_1 = [int(gr[3][0]), int(gr[3][1]), int(gr[3][2])]
        d_2 = [int(gr[4][0]), int(gr[4][1]), int(gr[4][2])]
        g.append(int(gr[2]))
        g.append( d_1)
        g.append( d_2)
        g.append(int(gr[6]))
        list_gr.append(g)


    with open(filename,'w') as file:
        json.dump(list_gr, file, indent= 3)
