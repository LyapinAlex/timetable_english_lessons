from .reforming_groups import reforming_groups
from .fulling_groups import full_all_groups
from .add_gr.add_new_groups import add_new_groups
import numpy as np
import math
import pdb

def base_reconstruct(data, sol_1, sol_2):

    
    reforming_groups(sol_1)
    
    # add_new_groups( data, sol_1, sol_2)
    
    full_all_groups(data, sol_1)
    


