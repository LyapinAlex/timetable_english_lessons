
def full_all_groups(data, sol_1):
    max_students = data['maxNumber']
    groups = sol_1['groups']


    for group in groups:
        list_students = group[0]
        num_students = len(list_students)
        if num_students < max_students :
            full_group(group, data, sol_1)

    
    return None

def full_group(group, data, sol_1):
    max_students = data['maxNumber']
    J = data['J']
    course = data['course_of_students']
    num_students = len(group[0])
    course_group = group[2]
    # print(group)
    for _ in range(max_students  - num_students):
        for j in range(J):
            if course[j,course_group ] == 1 and sol_1['students'][j] == 0:
                if check_can_be_join(group, data, j):
                    sol_1['students'][j] = group[1]
                    group[0].append(j)
                    break

    return None

def check_can_be_join(group, data, j):

    work_times = group[3], group[4]

     
    info = studet_rec_info(data, j)

    d_1 = work_times[0][0]
    d_2 = work_times[1][0]


    if len(info[d_1]) == 0 or len(info[d_2]) == 0:
        return False
    
    first_time = work_times[0][1]
    second_time=work_times[1][1]
    if first_time in range(info[d_1][0]*4, info[d_1][-1]*4 ) and second_time in range(info[d_2][0]*4,info[d_2][-1]*4 ):
        return True



def studet_rec_info(data, j):
    D = data['D']
    T = data['T']
    timeslot_of_students = data['timeslot_of_students']


    days = []
    for d in range(D):
        times = []
        ind_interfal = False
        for t in range(T):
            if timeslot_of_students[j,d,t] :
                


                if not ind_interfal:
                    times.append(t)
                    ind_interfal = True
                elif t == T - 1:
                        times.append(T)

                else:
                    if ind_interfal:
                        times.append(t)
                        ind_interfal = False

        days.append(times)

    return days  