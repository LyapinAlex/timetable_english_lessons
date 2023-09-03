import numpy as np

def restruct(J, D, T, L, tl, A, B ):
    
    k = 4

    a = np.zeros((J, D, k*T))

    for j in range(J):
        for l in range(L):
            if B[j,l] == 1:
                for d in range(D):
                    for t in range(T):
                        if A[j,d,t] == 1:
                            a[j,d,k*t] = 1
                            a[j,d,k*t+ 1] = 1
                            a[j,d,k*t + 2] = 1
                            a[j,d,k*t+ 3] = 1
                            for t_p in range(tl[l]):
                                if k*t+ k-1 + t_p == k*T:
                                    break
                                else:
                                     a[j,d,k*t+ k-1 + t_p] = 1

    return a

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
      

    def read_input(self, file_name = None):
        if file_name == None:
            return 0

        fileOrders = open(file_name)
        orders = fileOrders.readlines()
        input_str_a = orders[3]
        input_str_b = orders[1]
        fileOrders.close()

        a = np.fromstring(input_str_a, dtype = int, sep = ' ').reshape((self.J, self.D, self.T))
        self.courseRec = np.fromstring(input_str_b, dtype = int, sep = ' ').reshape((self.J, self.L))
        # self.timeRec = np.fromstring(input_str_a, dtype = int, sep = ' ').reshape((self.J, self.D, self.T))
        self.timeRec = restruct(self.J, self.D, self.T, self.L, self.timeL, a, self.courseRec )
        return 0



def get_list_of_couple_of_days(num_days):
    list = []

    for d_1 in np.arange(num_days):
        for d_2 in np.arange(d_1 + 2, num_days):
            list.append((d_1,d_2))

    return np.array(list)