import numpy as np
import math
import pdb

from .reconstruct_group import change_format_group 
from .appoinment.appoinment import appointment


def base_schedule(data, sol_1):

    schedule = {
    'real_time': data['num_div'] * data['T'],
    'teachers': [[] for __ in range(data['I'])], 
    'teachers_work_days': np.zeros((data['D'], data['I'])),
    'schedule_of_teachers': np.zeros((data['I'], data['D'], data['num_div'] * data['T']))}

    # for x in (sol_1['groups'][7]):
    #     print(x)
    change_format_group(data, sol_1)
    # for x in (sol_1['groups'][7]):
    #     print(x)
    

    appointment(data, sol_1, schedule)

    return schedule

    
