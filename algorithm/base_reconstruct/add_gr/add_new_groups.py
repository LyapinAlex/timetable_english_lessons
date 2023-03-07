from .add_in_timetable import add_new_group_in_timetable
import numpy as np
import math

def add_new_groups(data, sol_1, sol_2):
    
    L = data['L']
    timetable = get_timetable(data, sol_1, sol_2)
    

    for i in np.flip(get_list_teachers(sol_2)):
        for l in range(L):


            free_work_time_techers = get_free_work_time_techers(data, timetable, l , i)
            if free_work_time_techers == []:
                continue
            w = search_groups(data, sol_1,  free_work_time_techers, l)
            if w == []:
                continue
            add_new_group_in_timetable(data, sol_1, sol_2, w, free_work_time_techers, i)
            timetable = get_timetable(data, sol_1, sol_2)


def get_timetable(data, sol_1, sol_2):
    I = data['I']

    timetable = []
    for i in  range(I):
        timetable.append(get_teacher_period(data, sol_1, sol_2, i))

    return timetable


def get_list_teachers(schedule, day = None):
    schedule_of_teachers = schedule['schedule_of_teachers']
    I = np.shape(schedule_of_teachers)[0]

    if day == None:
        teacherLessonList  = np.array([np.sum(schedule_of_teachers[i]) for i in range(I)])
    else:
        teacherLessonList  = np.array([np.sum(schedule_of_teachers[i,day]) for i in range(I)])
    return np.flip(np.lexsort((range(I), teacherLessonList )))
    

def get_free_work_time_techers(data, timetable, l , i):

    list_days = data['couple_of_Days'] 

    days = reaserch_place(data, timetable, l , i)


    free_work_time_techers = []
    for d in list_days:
        if days[d[0]] != [] and days[d[1]] != []:
            
            free_work_time_techers.append((d, days[d[0]], days[d[1]]))
            

    return free_work_time_techers
        

def search_students(data, sol_1, d_1, d_2, t_1, t_2, l):
    J = data['J']
    max_number = data['maxNumber']
    min_number = data['minNumber']
    timeslot_of_students = data['timeslot_of_students']
    course_of_students = data['course_of_students'] 

    students = []
    for j in range(J):
        if len(students) == max_number:
            break
        if course_of_students[j,l] == 1 and  sol_1['students'][j] == 0:
            if timeslot_of_students[j, d_1, t_1] == 1.0 and timeslot_of_students[j, d_2, t_2] == 1.0:
                students.append(j)

    if len(students) >= min_number:
        return students
    else:
        return None
            

def search_groups(data, sol_1,  free_work_time_techers, l):

    
    groups = []
    for time in free_work_time_techers:
        d_1 = time[0][0]
        d_2 = time[0][1]

        t_1_begin =  int(time[1][0])//4
        t_2_begin =  int(time[2][0])//4
        t_1_end =  math.floor(int(time[1][-1])//4)
        t_2_end =  math.floor(int(time[2][-1])//4)

        time_d_1 = range(t_1_begin,  t_1_end + 1)
        time_d_2 = range(t_2_begin,  t_2_end + 1)

        for t_1 in time_d_1:
            for t_2 in time_d_2:
                students = search_students(data, sol_1, d_1, d_2, t_1, t_2, l)
                if students != None:
                    groups.append( [time[0], t_1, t_2, l, students])


    return groups




def get_teacher_period(data, sol_1, sol_2, i):

    D = data['D']
    real_time = sol_2['real_time']
    schedule_of_teachers = sol_2['schedule_of_teachers']
    real_time = sol_2['real_time']


    
    days_check = []
    for d in range(data['D']):
        day = []
        for t in range(real_time):
            if (np.sum(schedule_of_teachers[:,d,t]) == 4.0):
                day.append(t)

        days_check.append(day)


    list_day = []
    for d in range(D):

        list_lessons = []
        ind_interfal = False
        for t in range(real_time):
            
            if schedule_of_teachers[i,d,t] == 1.0 or np.sum(schedule_of_teachers[:,d,t]) == 4.0:

                if not ind_interfal:
                    list_lessons.append((t, 0))
                    ind_interfal = True
                elif t == real_time - 1:
                    list_lessons.append((real_time, 1))

            else:
                if ind_interfal:
                    list_lessons.append((t,1))
                    ind_interfal = False

        if list_lessons == []:
            list_day.append([])
            continue


        begin_work_time = list_lessons[0][0]
        end_work_time = list_lessons[-1][0]
        list_break = [begin_work_time]

        for id_el in range(int(len(list_lessons) / 2 - 1)):
            if list_lessons[2*id_el + 2][0] - list_lessons[2*id_el + 1][0]  > 2:
                list_break.append(list_lessons[2*id_el + 1][0])
                list_break.append(list_lessons[2*id_el + 2][0])
        
        list_break.append(end_work_time)
        list_day.append(list_break)   
    

    return list_day


def reaserch_place(data, timetable, l , i):
    D = data['D']
    timeLessons = data['timeLessons']
 
    duration = timeLessons[l]

    days = []
    for d in range(D):

        timeslots = []
        if len(timetable[i][d]) == 2:
            days.append([])
            continue
        for id_el in range(int(len(timetable[i][d]) / 2 - 1)):

            if timetable[i][d][2*id_el + 2] - timetable[i][d][2*id_el + 1] - 1 >  duration + 1:
                for  id_dur in range(timetable[i][d][2*id_el + 2] - timetable[i][d][2*id_el + 1] - 1 - duration):
                    timeslots.append(id_dur + timetable[i][d][2*id_el + 1] + 1)

        days.append(timeslots)

    return days