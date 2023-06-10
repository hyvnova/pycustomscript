
## Pattern File Format
-  Each pattern file must have a pattern_handler variable which should be function that takes a string (source code) ad returns the same string after it is modified if needed.

- Patter file are imported and use automatically.

-  If a pattern file starts with `OP` means that file is a Optimization Pattern File; which finds a pattern ad replaces it with a more effiecient option


### Syntax conventions
- for a pattern that affects directly a expression or a statement you should use the following syntax:
```py
# for a expression
(a + b)::name<parameter>

# or a statement
a = input()::name<parameter>

# Example
n = input()::to<int>

# Example - you can also have options like this
n = input()::to<int>?  
```


## Pattern File Template:
```py
import re

def pattern_handler(source: str) -> str:
    """
    ## Patter Name
    Description of the pattern

    ### Example
    Capure example 
    """

    pattern: re.Pattern = re.compile(
        r"""
        """,
        re.VERBOSE
    )

    while (match := pattern.search(source)) is not None:
        # Do something with the match

    return source
```