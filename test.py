# DO NOT RUN THIS FILE DIRECTLY; run run.py
import time


s = time.time()
for i in range(9000000):
    x = i * i * i 
    num = x * x
    
e = time.time()
print("TIME:", e-s)