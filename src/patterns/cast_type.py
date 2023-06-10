import re

def pattern_handler(source: str) -> str:
    """
    ## Patter Name
    Cast A Expression or Variable to a Type. Only works in in-line expressions.
    ### Example
    ```py
    n = input("Enter a number: ")::to<int>

    # The code above is equivalent to:
    n = int(input("Enter a number: "))

    # If you the casting can fail you can use the following syntax to get a Option:
    n = input("Enter a number: ")::to<int>? \
        .expect("The input is not a number") \
        .unwrap() 

    # The code above is equivalent to:
    n = cast_type(input("Enter a number: "), int) # This returns a Option (Some or None)
    ```
    """

    pattern: re.Pattern = re.compile(
        r"""
        ([\w \+\-\_\{\}\(\)\|\]\[*\\\/@&!\"\']*?) # The expression or variable to cast
        ::to<([a-zA-Z_][a-zA-Z0-9_]*)> # The type to cast to
        (\?)? # If the casting can fail
        """,
        re.VERBOSE
    )

    while (match := pattern.search(source)) is not None:

        expr, type_name, can_fail = match.groups()

        expr = expr.strip()

        # convert can_fail to bool
        can_fail = bool(can_fail)

        # if the casting can fail
        if can_fail:
            source = source[:match.start()] + f"cast_to({expr}, {type_name})" + source[match.end():]
        
        # if the casting can't fail
        else:
            source = source[:match.start()] + f" {type_name}({expr})" + source[match.end():]

    return source