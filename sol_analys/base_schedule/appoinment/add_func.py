import numpy as np
import math

def add_group_in_timetable(group, appropriate_times, data, schedule, teacher = None):
    """ Добавляет группу в рассписание"""

    real_time = schedule['real_time']
    schedule_of_teachers = schedule['schedule_of_teachers']

    work_time = group[3], group[4]

    first_day = work_time[0]
    second_day = work_time[1]
    course = group[2]

    if teacher == None:
        teacher = get_list_teachers(schedule)
    else:
        teacher = [teacher]
    for i in teacher:

        best_time_1 = None
        best_time_2 = None
        place_timetable_for_i = []
        for t in appropriate_times:

            if t[2] == i:
                place_timetable_for_i.append((t[0], t[1])) 

        if  place_timetable_for_i == []:
            continue
        else:
            if np.sum(schedule_of_teachers[i, first_day[0]]) == 0:
        
                distance_to_mid_day = real_time
                for time in place_timetable_for_i:
                    if math.fabs( real_time /2 - time[0] ) < distance_to_mid_day:
                        distance_to_mid_day  =  math.fabs( real_time /2 - time[0] )
                        best_time_1 = time[0]
            else:

                time_first_day = []
                for t in place_timetable_for_i:
                    time_first_day.append(t[0])
                best_time_1 = choose_best_time_for_teachers(course, first_day[0], time_first_day, i, data, schedule)

            

            if np.sum(schedule_of_teachers[i, second_day[0]]) == 0:
            
                distance_to_mid_day = real_time
                for time in place_timetable_for_i:
                    if math.fabs( real_time /2- time[1] ) < distance_to_mid_day:
                        distance_to_mid_day  =  math.fabs( real_time /2 - time[1] )
                        best_time_2 = time[1]
            else:
        
                time_second_day = []
                for t in place_timetable_for_i:
                    time_second_day.append(t[1])
                best_time_2 = choose_best_time_for_teachers(course, second_day[0], time_second_day, i, data, schedule)
        
        marker_days(i, group, best_time_1, best_time_2, data, schedule)
        break


    return None


def get_list_teachers(schedule, day = None):
    schedule_of_teachers = schedule['schedule_of_teachers']
    I = np.shape(schedule_of_teachers)[0]

    if day == None:
        teacherLessonList  = np.array([np.sum(schedule_of_teachers[i]) for i in range(I)])
    else:
        teacherLessonList  = np.array([np.sum(schedule_of_teachers[i,day]) for i in range(I)])
    return np.flip(np.lexsort((range(I), teacherLessonList )))


def choose_best_time_for_teachers( l, day, appropriate_times, i, data, schedule):
    

    timeLessons = data['timeLessons']
    best_time = None
    real_time = schedule['real_time']
    distance = real_time
    schedule_of_teachers = schedule['schedule_of_teachers']
    for t in appropriate_times:
        dis_metr_up = 0

        for pointer_up in range(t + timeLessons[l] + 2, real_time):
            if schedule_of_teachers[i, day,pointer_up] != 0:
                dis_metr_up=pointer_up -( t + timeLessons[l] + 2)
                continue
        
        dis_metr_down = 0
        for pointer_down in range(t, 0, - 1 ):
            if schedule_of_teachers[i, day, pointer_down] != 0:
                dis_metr_down = t - pointer_down 
                continue

        if dis_metr_up <=  dis_metr_down:
            if  dis_metr_up < distance:
                distance = dis_metr_up
                best_time = t
        else:
            if  dis_metr_down < distance:
                distance = dis_metr_down
                best_time = t
    
    return best_time 



def marker_days(i, group, t_1, t_2, data, schedule):
    teachers_work_days = schedule['teachers_work_days']
    teachers_groups = schedule['teachers']
    schedule_of_teachers = schedule['schedule_of_teachers']
    timeLessons = data['timeLessons']

    
    course = group[2]
    num_of_group = group[1]

    teachers_groups[i].append((num_of_group, course))

    work_time = group[3], group[4]


    for tReal in range(timeLessons[course]):
        schedule_of_teachers[i, work_time[0][0], t_1 + tReal] = 1
        schedule_of_teachers[i, work_time[1][0], t_2 + tReal] = 1


    teachers_work_days[work_time[0][0], i] = 1
    teachers_work_days[work_time[1][0], i] = 1

    d_1 = work_time[0][0]
    d_2 = work_time[1][0]

    group.pop()
    group.pop()
    group.append((d_1, t_1, t_1 + timeLessons[course] - 1))
    group.append((d_2, t_2, t_2 + timeLessons[course] - 1))
    group.append(True)
    group.append(i)

    
    return None
        