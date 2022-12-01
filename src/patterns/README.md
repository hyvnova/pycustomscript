
## Pattern File Format
-  Each pattern file must have a pattern_handler variable which should be function that takes a string (source code) ad returns the same string after it is modified if needed.

-  If a pattern file starts with `OP` means that file is a Optimization Pattern File; which finds a pattern ad replaces it with a more effiecient option


## Pattern File Template:
```py
import re

def pattern_handler(source: str) -> str:
    """
    Patter Name
    ```py
    sample pattern capture
    ```
    """

    pattern: re.Pattern = re.compile(
        r"""

        """,
        re.VERBOSE
    )

    for match in pattern.finditer(source):

        # match start & end
        start, end = match.start(),  match.end()


    return source
```