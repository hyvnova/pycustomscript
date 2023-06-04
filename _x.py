from ezstools.iterator import Iterator


it = Iterator(range(1, 5))

print(it.map(lambda x: x * 2))