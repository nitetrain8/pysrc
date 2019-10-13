import numpy as np

myarray = np.array(range(10))
print(myarray)

print(myarray * 5)
print(myarray)


k_limit = 3*86400-86401
y = np.zeros(shape=k_limit)
for k in range(k_limit):
    yk = 0
    for i in range((k+1), (k+86400)):
        yk += data_set[i] * (2*(i-k)/(86400**2-1) - 1/(86400-1))
    y[k] = yk
