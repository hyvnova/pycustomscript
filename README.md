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
    (n) => { n%2 == 0 },
    numbers
))
```
## Optimization
- To Cython Convertion. 
```toml
# config.toml
...

[ModuleImport]
# "package" module name
name = "tests/origin" # this file is where all files that use PyCS will be imported

# files which will be importar; they will be prepared
modules = [
  "tests/funcs.py",
]

to_cython = true # decides if convert the modules to cython
```
