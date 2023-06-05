
## Pattern File Format
-  Each pattern file must have a pattern_handler variable which should be function that takes a string (source code) ad returns the same string after it is modified if needed.

- Patter file are imported and use automatically.

-  If a pattern file starts with `OP` means that file is a Optimization Pattern File; which finds a pattern ad replaces it with a more effiecient option



## Pattern File Template:
```py
import re

def pattern_handler(source: str) -> str:
    """
    ## Patter Name
    Description of the pattern

    ```py
    sample pattern capture
    ```
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