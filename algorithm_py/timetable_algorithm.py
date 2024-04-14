import numpy as np
from base_group.base_group import base_group
from base_schedule.base_schedule import base_schedule
from base_reconstruct.base_reconstruct import base_reconstruct
from func_with_data import *
from data import *
from solution import *
import pdb
import time

def stat_print(sch, data):

    gr = sch['groups']
    
    st_sum = 0
    gr_sum = 0
    
    if len(gr) == data['L']:
        for l in range(data['L']):
            gr_list = gr[l]
            gr_sum+=len(gr_list)
            
            for g in gr_list:
                st_sum+=len(g[0])
    else:
        gr_sum = 0
        for g in gr:
            if g[5] == True:
                st_sum+=len(g[0])
                gr_sum+=1
        
    
    print('st: ', st_sum,' gr: ', gr_sum)
    print()

    

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
    # stat
    stat_print(first_path_sol, data)

    second_path_sol = base_schedule(data, first_path_sol)
    # stat
    stat_print(first_path_sol, data)
    
    
    # base_reconstruct(data, first_path_sol, second_path_sol)
    Time = time.perf_counter() - Time 
    
    


    # JSON_import( first_path_sol, f"sol_ex_{i}_dim_{2}" )

    return get_objVal(data, first_path_sol, second_path_sol)


if __name__ == "__main__":

    # print(algorithm(3)['obj_val'])

    
    # s = 0.0
    for i in range(1,11):
        a = algorithm(i)['obj_val']
    #     s+=a
        print(a)
    # print('\n')
    # print(s/10)

    
    # for i in range(1,11):
    #     data = Data(J, L, I, T , D, r, minN, maxN, timeL )
    #     filename_data = f"examples_copy\\orders_4_{i}.txt"
    #     data.read_input(filename_data)

    #     data.up_bound()
        

    #     # filename_sol = f"sol_ex_{i}_dim_3.json"
        # sol = Solution(filename_sol)
        # print(sol.get_sol_val())
    for i in range(1,11):
        data = Data(J, L, I, T , D, r, minN, maxN, timeL )
        filename_data = f"examples_copy\\orders_1_{i}.txt"
        data.read_input(filename_data)
        filename_sol = f"sol_ex_{i}_dim_1.json"
        sol = Solution(filename_sol)
        sol.import_sol_format(name = f'alg_{i}_dim_1')
        break
        print(sol.get_sol_val())
