import numpy as np

class Data:
    
    def __init__(self, J, L, I, T, D, r, minN, maxN, timeL ):
        self.J = J
        self.L = L
        self.D = D
        self.T = T
        self.I = I
        self.r = r
        self.minN = minN
        self.maxN = maxN
        self.timeL = timeL
        self.listCoupleDays = get_list_of_couple_of_days(D)
        self.timeRec = None
        self.courseRec = None
        return 0

    def read_input(self, file_name = None):
        if file_name == None:
            return 0

        fileOrders = open(file_name)
        orders = fileOrders.readlines()
        input_str_a = orders[3]
        input_str_b = orders[1]
        fileOrders.close()

        self.timeRec = np.fromstring(input_str_a, dtype = int, sep = ' ').reshape((self.J, self.D, self.T))
        self.listCoupleDays = np.fromstring(input_str_b, dtype = int, sep = ' ').reshape((self.J, self.L))
        return 0



def get_list_of_couple_of_days(num_days):
    list = []

    for d_1 in np.arange(num_days):
        for d_2 in np.arange(d_1 + 2, num_days):
            list.append((d_1,d_2))

    return np.array(list)