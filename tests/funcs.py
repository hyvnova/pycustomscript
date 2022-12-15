
def fibonacci(n: int) -> int:
    a, b = 0, 1
    for i in range(n):
        a, b = a+b, a
    return a


def is_prime(n: int) -> bool:
    for i in range(2, n):
        if (n % i) == 0:
            return False
    return True


print(list((1,2,3,4,3,2,1)).split(3))
