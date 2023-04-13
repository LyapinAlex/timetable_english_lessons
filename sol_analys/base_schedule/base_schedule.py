import numpy as np
import math
import pdb

from .reconstruct_group import change_format_group 
from .appoinment.appoinment import appointment


def base_schedule(data, sol_1, config = None):

    schedule = {
    'real_time': 4 * data['T'],
    'teachers': [[] for __ in range(data['I'])], 
    'teachers_work_days': np.zeros((data['D'], data['I'])),
    'schedule_of_teachers': np.zeros((data['I'], data['D'], 4 * data['T']))}

    change_format_group(data, sol_1, config)

    appointment(data, sol_1, schedule)

    return schedule

    
