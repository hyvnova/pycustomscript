import time
s = time.time()
for i in range(9000000):
    x = pow(i, 3) 
    num = pow(x, 2)
e = time.time()
print("TIME:", e-s)
