import numpy as np
from base_group.base_group import base_group
from base_schedule.base_schedule import base_schedule
from base_reconstruct.base_reconstruct import base_reconstruct
from func_with_data import *
from data import *
from solution import *
import pdb
import time



def algorithm(i, locationParams = None, solutionsFromDB = None):
    """ Запускает алгоритм.
        Получает на вход: locationParams, solutionsFromDB
        locationParams = Данные локации
        solutionsFromDB = заявки студентов

        Возращает sol
        sol = список групп, построенных в процессе
     """


    # data = sort_data(locationParams, solutionsFromDB)
    data = read_data(f"examples_copy\\orders_4_{i}.txt")

    Time = time.perf_counter()
    first_path_sol = base_group(data)

    second_path_sol = base_schedule(data, first_path_sol)
    base_reconstruct(data, first_path_sol, second_path_sol)
    Time = time.perf_counter() - Time 
    
    


    JSON_import( first_path_sol, f"sol_ex_{i}_dim_{2}" )

    return get_objVal(data, first_path_sol, second_path_sol)
    # sol = get_solution( first_path_sol)
    # sol_export_gurobi(data, first_path_sol, second_path_sol)
    # return sol

if __name__ == "__main__":

    # algorithm(1)
    
    # s = 0.0
    # for i in range(1,11):
    #     a = algorithm(i)['obj_val']
    #     s+=a
    #     print(a)
    # print('\n')
    # print(s/10)

    
    for i in range(1,11):
        data = Data(J, L, I, T , D, r, minN, maxN, timeL )
        filename_data = f"examples_copy\\orders_4_{i}.txt"
        data.read_input(filename_data)

        data.up_bound()
        

        # filename_sol = f"sol_ex_{i}_dim_3.json"
        # sol = Solution(filename_sol)
        # print(sol.get_sol_val())