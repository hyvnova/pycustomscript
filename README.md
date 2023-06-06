# PyCustomScript (1.4.1)

## Custom Sintax
- Ranges
Similar to Rust's ranges, provides a way to iterate over a range of numbers. 
```py
# Range from 1 to 10
for i in <1..11>:
    print(i)

# Using ranges as slices
numbers = [1, 2, 3, 4, 5]
print(numbers[<0..=3>]) # [1, 2, 3, 4]
```


- Dictionary Destructuration
Similar to JS's destructuration, provides a way to get values from a dictionary.
```py
user = {
    "name" : "Jonh",
    "age" : 21,
    "email" : "jonh@sample-email.com",
    "role" : "Developer"
}

{name, role} = user

print(name, role) # Jonh Developer
```

- JS-like Functions Arrow functions
Inspired by JS's arrow functions, are a more clean way to write anonymous functions.
```py
even_numbers = <1..n+1>.filter((x) => x % 2 == 0;)

# they can be async too
async (data) => await fetch(data);
```
