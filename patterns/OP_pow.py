import re


def pattern_handler(source: str) -> str:
    """
    Pow Replacement (Optimization Pattern)
    ```py
    # match these cases
    n = x * x # -> n = pow(x, 2)
    num = 10 * 10 # -> num = pow(10, 2)
    
    ```
    """

    pattern: re.Pattern = re.compile(
        r"""
        ([0-9a-z-A-Z]+) 
        \s?\*\s?\1
        """,
        re.VERBOSE
    )

    for match in pattern.finditer(source):

        # match start & end
        start, end = match.start(),  match.end()

        qu


    return source
