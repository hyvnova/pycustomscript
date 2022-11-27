# PyCustomScript

## Custom Sintax

- Dictionary Destructuration
```py
obj = {
    "name" : "Jonh",
    "age" : 21,
    "email" : "jonh@sample-email.com",
    "role" : "Developer"
}

{name, role} = obj

print(name, role) # Jonh Developer
```
- JS-like Anonimous Functions
```py
even_numbers: List[int] = list(filter(
    (n) = { n%2=0 },
    numbers
))
```
## Optimization Patterns
- Exponent to Pow
```py
# Original
n = x * x * x + 23 * 5

# Turns  into
n = pow(x,3) + 23 * 5
```
