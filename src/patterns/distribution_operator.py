import re

def pattern_handler(source: str) -> str:
    """
    ## Patter Name
    Distribute a single or multiple parameters into a multiple function calls

    ### Syntax
    ```
    | <args> -> <funcs>;        # Distribute as parameter
    || <args> -> <funcs>;       # Distribute as call
    ```

    ### Example
    ```py
    # Distrubute as parameter
    @Derive(| "items" -> Iter, Get;)    

    # You can also get the result of the functions
    res = (| 3.14 -> Dist, Trajectory) 

    # Distribute as call
    x = [1, 2, 3]
    || x -> Func1, Func2; # Note that for calls we use double pipes (||)

    Note: the main difference between the two is that using parameter distribution (|) you can get the result of the functions, while using call distribution (||) you can't, since the are only being called. Basicly one acts as a `expression` and the other as a `statement`.
    """


    pattern: re.Pattern = re.compile(
        r"""
        \| # Distribute operator start token
        (?P<call_mode>\|)? # If the distribute is a direct call (||)
        \s? # Optional Whitespace
        (?P<args>[\w ,\+\-\_\{\}\(\)\|\]\[*\\\/@&!\"\']*?) # The arguments to distribute
        \s?
        -> # Distribute operator separation token
        \s?
        (?P<funcs>[\w ,\+\-\_\{\}\(\)\|\]\[*\\\/@&!\"\']*?) # The functions to distribute the arguments to
        ; # end token
        """,
        re.VERBOSE
    )

    while (match := pattern.search(source)) is not None:

        args, funcs, call_mode = match.group("args"), match.group("funcs"), match.group("call_mode")

        # clean args
        args = args.strip()

        # clean funcs
        funcs = [*map(lambda x: x.strip(), funcs.split(","))]

        # create new source
        new_source = ""

        # if the distribute is a direct call
        if call_mode:
            new_source += "\n".join([f"{func}({args})" for func in funcs])
        else:
            new_source += ", ".join([f"{func}({args})" for func in funcs])

        # replace sintax with new source
        source = source[:match.start()] + new_source + source[match.end():] 

    return source