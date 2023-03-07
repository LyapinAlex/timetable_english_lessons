def reforming_groups(sol_1):
    students = sol_1['students']
    groups = sol_1['groups']    


    for group in groups:
        if group[5] == False:
            list_students = group[0]

            for st in list_students: 
                students[st] = 0

    i = 0
    while i < len(groups):
        if groups[i][5] == False:
            del groups[i]
        else:
            i += 1

    return None