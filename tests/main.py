

# testing destruct

d = {
    "a": (x, y) => {x+y},
    "b": 2,
    "c": 3
}

{a, c} = d
print(a, c)