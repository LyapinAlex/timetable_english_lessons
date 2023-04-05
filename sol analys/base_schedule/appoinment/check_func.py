import numpy as np

def check_in_timetable(t_1, t_2, group, i, data, schedule):
    """ Соверашет проверку может ли быть группа добавлена в рассписание"""

    if not check_rooms(group, t_1, t_2, data, schedule):
        return  False
    elif not check_teacher(i, group, t_1, t_2, data, schedule):
        return False
    else:
        return True



def check_rooms(group, t_1, t_2, data, schedule):
    r = data['r']
    number_working_rooms = data['number_working_rooms'] 
    I = data['I']
    l =  group[2]
    real_time = schedule['real_time']
    schedule_of_teachers = schedule['schedule_of_teachers']
    timeLessons = data['timeLessons']

    work_time = group[3], group[4]

    
    for tReal in range(timeLessons[l]):
        if (t_1 + tReal >= real_time) or (t_2 + tReal  >= real_time):
            return False

        if np.sum([ schedule_of_teachers[i, work_time[0][0], t_1 + tReal] for i in range(I) ]) >= r - number_working_rooms[work_time[0][0], t_1 + tReal] :
            # print("l",group[2],"k", group[1],"room ",work_time[0][0] ," day t:" ,t_1 + tReal )
            return False

        if np.sum([ schedule_of_teachers[i, work_time[1][0], t_2 + tReal] for i in range(I) ]) >= r - number_working_rooms[ work_time[1][0], t_2 + tReal]:
            # print("l",group[2],"k", group[1],"room ", work_time[1][0]," day t:" ,t_2 + tReal )
            return False

    return True



def check_teacher(i, group, t_1, t_2, data, schedule):
    
    if not check_limit_working_days(i, group, data, schedule):
        # print("l",group[2],"k", group[1]," limit days" )
        return False

    if  not check_teachers_break(i, group, t_1, t_2, data, schedule):
        return False

    if not check_time_teachers(i, group, t_1, t_2, data, schedule):
        # print("l",group[2],"k", group[1],"time closed :" ,t_1, t_2 )
        return False

    if not check_limit_work_time(i, group, t_1, t_2, data, schedule):
        # print("l",group[2],"k", group[1],"time limit:" ,t_1, t_2 )
        return False
    

    return True



def check_limit_working_days(i, group, data, schedule):

    teachers_work_days = schedule['teachers_work_days']


    D = data['D']

    work_time = group[3], group[4]

    if teachers_work_days[work_time[0][0], i] == 1 and teachers_work_days[work_time[1][0], i] == 1:

        return  True

    s = 0
    for d in range(D):
        s+=teachers_work_days[d, i]
    

    if D - 1 == s  and (teachers_work_days[work_time[0][0], i] == 0 or teachers_work_days[work_time[1][0], i] == 0):
        return False


    if  D - 2 == s  and teachers_work_days[work_time[0][0], i] == 0 and teachers_work_days[work_time[1][0], i] == 0 :
        return False
    

    return True



def check_teachers_break(i, group, t_1, t_2, data, schedule):
    timeLessons = data['timeLessons']
    real_time = schedule['real_time']
    schedule_of_teachers =  schedule['schedule_of_teachers']
    l = group[2]
 
    work_time = group[3], group[4]
    
    

    for k in range(1):
        
        if t_1 - (1 + k) >= 0:
            if ( schedule_of_teachers[i, work_time[0][0], t_1 - (1 +k)] == 1) :
                # print("l",group[2],"k", group[1]," teacher break 1 day first time" , t_1 )
                return False
            
        if t_1 + timeLessons[l] - 1 + (1 + k) < real_time :
            if (schedule_of_teachers[i, work_time[0][0], t_1 + timeLessons[l] - 1 + (1 + k)] == 1):
                # print("l",group[2],"k", group[1]," teacher break 1 day last time" , t_1 + timeLessons[l] )
                return False


        if t_2 - (1 + k) >= 0:
            if ( schedule_of_teachers[i, work_time[1][0], t_2 - (1 +k)] == 1) :
                # print("l",group[2],"k", group[1]," teacher break 2 day first time" , t_2 )
                return False
            
        if t_2 + timeLessons[l] - 1+ (1 + k) < real_time :
            if (schedule_of_teachers[i, work_time[1][0], t_2 + timeLessons[l] - 1+ (1 + k)] == 1):
                # print("l",group[2],"k", group[1]," teacher break 2 day last time" , t_2 + timeLessons[l] )
                return False

    

    return True

def check_time_teachers(i, group, t_1, t_2, data, schedule):

    l =  group[2]

    schedule_of_teachers = schedule['schedule_of_teachers']
    timeLessons = data['timeLessons']


    work_time = group[3], group[4]


    for tReal in range(timeLessons[l]):
        
        if schedule_of_teachers[i, work_time[0][0], t_1 + tReal] != 0:
            return False

        if schedule_of_teachers[i, work_time[1][0], t_2 + tReal] != 0:
            return False
    
    
    return True



def check_limit_work_time(i, group, t_1, t_2, data, schedule):


    l =  group[2]
    real_time = schedule['real_time']
    schedule_of_teachers = schedule['schedule_of_teachers']
    timeLessons = data['timeLessons']

    work_time = group[3], group[4]


    lesson_begin_in_first_day = t_1
    lesson_end_in_first_day = t_1 + timeLessons[l] - 1
    # first day
    s_1 = real_time
    s_2 = 0
    for t in range(real_time):
        if (schedule_of_teachers[i, work_time[0][0], t] == 1):
            s_1 = t
            break
    
    for t in reversed(range(real_time)):
        if (schedule_of_teachers[i, work_time[0][0], t] == 1):
            s_2 = t
            break
    
    if s_1 > lesson_begin_in_first_day:
        s_1 = lesson_begin_in_first_day
    if s_2 < lesson_end_in_first_day :
        s_2 = lesson_end_in_first_day 

    S_1 = s_2 - s_1 
    #  second day
    s_1 = real_time
    s_2 = 0
    lesson_begin_in_second_day = t_2
    lesson_end_in_second_day = t_2 + timeLessons[l] - 1
    for t in range(real_time):
        if (schedule_of_teachers[i, work_time[1][0], t] == 1):
            s_1 = t
            break
    
    for t in reversed(range(real_time)):
        if (schedule_of_teachers[i, work_time[1][0], t] == 1):
            s_2 = t
            break
    

    if s_1 > lesson_begin_in_second_day:
        s_1 = lesson_begin_in_second_day
    if s_2 < lesson_end_in_second_day :
        s_2 = lesson_end_in_second_day
    
    S_2 = s_2 - s_1 

    if ( S_1  >=  8*4 ) or ( S_2  >=  8*4 ):
    
        return False
    
    return True       

