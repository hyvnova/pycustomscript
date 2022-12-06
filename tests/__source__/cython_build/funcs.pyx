cdef get_name(obj):
    name = obj.get("name", None)
    return  name
cdef fibonacci(n):
    a, b = 0, 1
    for i in range(n):
        a, b = a+b, a
    return a
