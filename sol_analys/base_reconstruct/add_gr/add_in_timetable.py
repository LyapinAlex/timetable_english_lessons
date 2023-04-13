
def add_new_group_in_timetable(data, sol_1, sol_2,  groups, times_techer, i):
    students = sol_1['students']
    

    groups.sort(key = lambda x: len(x[4]))
    groups.reverse()
    group = groups[0]

    time_for_record = None
    for t in times_techer:
        if t[0][0] == group[0][0] and t[0][1] == group[0][1]:
            time_for_record = t
            break


    d_1, d_2 = group[0]
    t_1 = 4*group[1]
    t_2 = 4*group[2]
    while t_1 not in time_for_record[1]:
        t_1+=1
    while t_2 not in time_for_record[2]:
        t_2+=1
    
    l = group[3]
    k = get_num_group(sol_1 , l)
    



    for j in group[4]:
        students[j] = k

    group = [group[4], k, l, d_1, d_2]


    marker_days(i, group, t_1, t_2, data, sol_1, sol_2)

def marker_days(i, group, t_1, t_2, data, sol_1, sol_2):
    teachers_work_days = sol_2['teachers_work_days']
    teachers_groups = sol_2['teachers']
    schedule_of_teachers = sol_2['schedule_of_teachers']
    timeLessons = data['timeLessons']

    
    course = group[2]
    num_of_group = group[1]

    teachers_groups[i].append((num_of_group, course))

    work_time = group[3], group[4]


    for tReal in range(timeLessons[course]):
        schedule_of_teachers[i, work_time[0], t_1 + tReal] = 1
        schedule_of_teachers[i, work_time[1], t_2 + tReal] = 1


    teachers_work_days[work_time[0], i] = 1
    teachers_work_days[work_time[1], i] = 1

    d_1 = work_time[0]
    d_2 = work_time[1]

    group.pop()
    group.pop()
    group.append((d_1, t_1, t_1 + timeLessons[course] - 1))
    group.append((d_2, t_2, t_2 + timeLessons[course] - 1))
    group.append(True)
    group.append(i)

    sol_1['groups'].append(group)
    
    return None

def get_num_group(sol_1 , l):
    groups = sol_1['groups']
    k = 1
    for group in groups:
        if group[2] == l:
            if group[1] >= k:
                k =  group[1] + 1

    return k