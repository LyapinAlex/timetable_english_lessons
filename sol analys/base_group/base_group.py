import numpy as np
import time

from .creat_schedule import *

def base_group(data, config = None):
    """Создает первое приблеженное решение, создавая группы и рапредиляя их по таймслотам.
        На фход принимает тип data, config.
        config = None, запускает одну иттерацию
        config = "heur", запускает одну иттерацию с эвристикой
        сonfis = "rand", запускает одну иттерацию с рандомизацией

        Возращает словарь schedule:
        students - массив в какой группе k находиться студент j.
        groups - список групп
        rooms - массив показывающий сколько групп занимается в день d, и время t
    """


    schedule = {
        'students': np.zeros((data['J'])), 
        'groups': [ [] for __ in range(data['L'])],
        'rooms': np.zeros((data['D'], 4*data['T']))  
        }
   
    if config == None:
        create_schedule(data, schedule)
    
    for l in range(data['L']):
        for gr in schedule['groups'][l]:
            print(gr)
    
    # if config == "rand":
    #     create_schedule_rand(data, schedule)

    return schedule 


