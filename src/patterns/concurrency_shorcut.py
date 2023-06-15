import re


def pattern_handler(source: str) -> str:
    """
    ## Concurrency Shortcuts
    Provides shortcuts for using concurrency (threands & processes) in Python.

    ### Syntax
    ```
    concurrent::thread(function, *args, **kwargs)
    concurrent::process(function, *args, **kwargs)

    concurrent::thread!(function, *args, **kwargs) # Does not wait for the thread to finish
    concurrent::process!(function, *args, **kwargs) # Does not wait for the process to finish
    ```
    ### Example
    ```python
    def my_function():
        print("Hello World!")
        time.sleep(1)

    concurrent::thread(my_function) for _ in range(10)
    """

    pattern: re.Pattern = re.compile(
        r"""
        concurrent  # Keyword for syntax
        ::  # Separator token
        (thread|process) # Type
        (!)? # Mode (optional)
        \(([\w ,\+\-\_\{\}\(\)\|\]\[*\\\/@&!\"\']+)\) # Arguments
        """,
        re.VERBOSE,
    )

    while (match := pattern.search(source)) is not None:
        type, mode, args = match.groups()

        daemon = mode != "!"

        source = (
            source[: match.start()]
            + ("make_process" if type == 'process' else "make_thread") + f"({daemon}, {args})"
            + source[match.end() :]
        )

    return source
