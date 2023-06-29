import re


def pattern_handler(source: str) -> str:
    """
    ## Patter Name
    Distribute a single or multiple parameters into a multiple function calls

    ### Syntax
    ```
    | <args> -> <funcs>;        # Distribute as parameter
    |> <args> -> <funcs>;       # Distribute iterable arguments
    ```

    ### Example
    ```py
    # Distrubute as parameter
    @Derive(| "items" -> Iter, Get;)

    # You can  get the result of the functions
    res = | 3.14 -> Dist, Trayectory;

    # Distribute iterable arguments
    |> inputs, outputs -> test1, test2, test3; (Note: the result is a tuple of tuples, a tuple the results of each function)
    """

    pattern: re.Pattern = re.compile(
        r"""
        \| # Distribute operator start token
        (?P<iter_mode>\>)? # If the distribute is using iteration (|>)
        \s? # Optional Whitespace
        (?P<args>[\w ,\+\-\_\{\}\(\)\|\]\[*\\\/@&!\"\']*?) # The arguments to distribute
        \s?
        -> # Distribute operator separation token
        \s?
        (?P<funcs>[\w ,\+\-\_\{\}\(\)\|\]\[*\\\/@&!\"\']*?) # The functions to distribute the arguments to
        ; # end token
        """,
        re.VERBOSE,
    )

    while (match := pattern.search(source)) is not None:
        args, funcs, call_mode, iter_mode = (
            match.group("args"),
            match.group("funcs"),
            match.group("call_mode"),
            match.group("iter_mode"),
        )

        # clean args
        args = args.strip()

        # clean funcs
        funcs = [*map(lambda x: x.strip(), funcs.split(","))]

        # create new source
        new_source = ""

        # if the distribute is a iteration (args are iterables)
        if iter_mode:
            new_source += (
                "tuple((tuple(map(lambda args: func(*args), zip("
                + args
                + ")))) for func in ["
                + ", ".join(funcs)
                + "])"
            )

        else:
            new_source += "[" + ", ".join([f"{func}({args})" for func in funcs]) + "]"

        # replace sintax with new source
        source = source[: match.start()] + new_source + source[match.end() :]

    return source
