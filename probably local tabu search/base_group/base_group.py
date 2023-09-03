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
        'students': np.zeros((data['J']),dtype = np.int32), 
        'groups': [ [] for __ in range(data['L'])]
        }
   
    if config == None:
        create_schedule(data, schedule)
    

    return schedule 


