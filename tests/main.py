
from concurrent.futures import ThreadPoolExecutor
from origin import funcs as ofuncs
import funcs 
import time

n = 10

def test(n, *funcs):
    for fn in funcs:
        start = time.time()
        
        for i in range(n):
                fn(i*n**2)
                
        end = time.time()

        print(f"{fn.__module__}.{fn.__name__} Took: {end - start}")

with ThreadPoolExecutor() as exe:
    
    exe.submit(test, n, funcs.fibonacci, funcs.is_prime)
    exe.submit(test, n, ofuncs.fibonacci, ofuncs.is_prime)
    
    
