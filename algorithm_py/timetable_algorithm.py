import numpy as np
from base_group.base_group import base_group
from base_schedule.base_schedule import base_schedule
from base_reconstruct.base_reconstruct import base_reconstruct
from func_with_data import *
from tabulate import tabulate
import pdb
import time
import math


def algorithm(i, locationParams = None, solutionsFromDB = None):
    """ Запускает алгоритм.
        Получает на вход: locationParams, solutionsFromDB
        locationParams = Данные локации
        solutionsFromDB = заявки студентов

        Возращает sol
        sol = список групп, построенных в процессе
     """


    # data = sort_data(locationParams, solutionsFromDB)
    data = read_data(f"examples_copy\\orders_2_{i}.txt")

    Time = time.perf_counter()
    first_path_sol = base_group(data)
    second_path_sol = base_schedule(data, first_path_sol)
    Time = time.perf_counter() - Time 

    base_reconstruct(data, first_path_sol, second_path_sol)
    print_schedule(data, first_path_sol, second_path_sol, i)

    
    f=open(f"sol_alg_{i}.txt","w")
    f.write("sol = ")
    f.write(str(count_students(data, first_path_sol, second_path_sol)))
    f.write("\nobjVal = ")
    f.write(str(get_objVal(data, first_path_sol, second_path_sol)))
    f.close()


    # print(count_students(data, first_path_sol, second_path_sol), get_objVal(data, first_path_sol, second_path_sol))
    sol = get_solution( first_path_sol)
    # objVal = get_objVal(data, first_path_sol, second_path_sol)
    return sol

if __name__ == "__main__":

    for i in range(1,11):
        algorithm(i)
