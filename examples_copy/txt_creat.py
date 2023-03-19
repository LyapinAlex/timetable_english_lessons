J = 100
K = 5
L = 2
I = 2
D = 6
T = 6
t_w = 5

f=open("orders_hm.txt","w")

f.write('\n')

for j in range(J):
    if j < 50:
        f.write('1 0 ')
    else:
        f.write('0 1 ')

f.write('\n')
f.write('\n')

for j in range(J):
    for d in range(D):
        for t in range(T):
            f.write('1 ')


f.close()