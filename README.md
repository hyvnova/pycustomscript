# PyCustomScript (1.6)

## Syntax

### Distribution Operator
Provides a way to distribute a single or multiple arguents into multiple funcions.
```py
res = | PI, Coords -> Direction, Distance; # Distribute PI and Coords into the Direction and Distance functions

# Make direct call
|| test_data -> Fn1, Fn2, Fn3;
``` 

### Type Casting 
Provides a way to cast a variable to a specific type. Inspired by Rust's type casting.
```py
# Casting to int
n = "10"::to<int>

# Error handling
n = "10"::to<int>?.expect("Expected a number")
```

### Ranges
Similar to Rust's ranges, provides a way to iterate over a range of numbers. 
```py
# Range from 1 to 10
for i in <1..11>:
    print(i)

# Using ranges as slices
numbers = [1, 2, 3, 4, 5]
print(numbers[<0..=3>]) # [1, 2, 3, 4]
```


### Dictionary Destructuration
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

### Arrow functions
Inspired by JS's arrow functions, are a more clean way to write anonymous functions.
```py
even_numbers = <1..n+1>.filter((x) => x % 2 == 0;)

# they can be async too
async (data) => await fetch(data);
```
## Built-ins

### Iterator 
A cleaner and more readable way to interact with iterators.
Under the hood `Ranges` use `Iterators`.
```py
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Iterator(numbers).filter((n) => n <= 7;).map((n) => n * 2;) 
```

### Magic Methods Shortcuts
A set of decorators that made it easy to "derive" behavior into a class.


```py
# Making a class iterable
@Iter("items")
class MyClass:
    def __init__(self, items):
        self.items = items
    ...

obj = MyClass([1, 2, 3, 4, 5])
for item in obj:
    print(item)

# deriving multiple behaviors
@Derive(| "items" -> Iter, Get, Set;)
class MyClass:
    def __init__(self, items):
        self.items = items
    ...

obj = MyClass([1, 2, 3, 4, 5])

n = obj[0] # Get
obj[0] = 10 # Set

for item in obj: # Iter
    print(item)
``` 
#### Available decorators
1. Dependent decorators (require a field in the class)
    - `Iter`: Makes a class iterable.
    - `Get`: Makes a class subscriptable.
    - `Set`: Makes a class subscriptable.
    - `Len`: Makes a class have a length.
    - `Call`: Makes a class callable.

2. Independent decorators (don't require a field in the class)
    - `Str`: Makes a class printable.


### Option type
A type that represents a value that can be `Some` or `Nothing`. Inspired by Rust's `Option` type.
```py
def get_user() -> Option:
    user = fetch_user()
    if user:
        return Some(user)
    return Nothing

user = get_user().expect("User not found") # throws an error if the value is Nothing

# Or you could use a default value
user = get_user().unwrap_or(DEFAULT_USER)
```