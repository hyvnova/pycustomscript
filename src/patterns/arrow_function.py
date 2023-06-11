import re
from uuid import uuid4

def pattern_handler(source: str) -> str:
    """
    ## Anonimous Functions
    Create anonimous functions similar to JavaScript.

    ### Syntax
    ```
    (param1, ...) => <body>;
    ```
    
    ### Examples
    ```py
    (param1, ...) => 
        x = do_something(param1)
        x * 2 # <- last expression is returned (unless it ends with ";")
        ; # <- this indicates the end of the function

    # You can also have 1 line functions
    (param1, ...) => x = do_something(param1);  # <- as long as it ends with ";"

    # They can also be async
    async (param1, ...) => ...;
    ```
    """

    pattern: re.Pattern = re.compile(
        r"""
        (?P<async>async\s)?     # async keyword
        \s?                     # Optional Whitespace
        \(                      # Function Arguments Start Parenthesis
        (?P<args>[\w ,\+\-\_\{\}\(\)\|\]\[*\\\/@&!\"\']*?)      # Function Arguments
        \)                      # Function Arguments End Parenthesis
        \s?                     # Optional Whitespace
        =>                      # Arrow token (only used for sintax)
        \s?                     
        (?P<body>[-!$%^&*()_+|~=`\[\]:";'<>?,.\/a-zA-Z0-9\s]+) # function Body
        ;                      # End of function
        """,
        re.VERBOSE
    ) 

    while (match := pattern.search(source)) is not None:
        is_async, params, func_content = match.group("async"), match.group("args"), match.group("body")

        # fo cases when a comma get into function content
        func_end = ""

        func_content = func_content.strip()

        if "," in func_content:
            func_content, *func_end = func_content.split(",", maxsplit=1)
            func_end.insert(0, ",")

            func_end = "".join(func_end)

        # func creation
        func_name = "__func_" + str(uuid4())[4:12].replace("-", "")

        func = f'def {func_name}({params}):\n\t'
        if is_async:
            func = "async " + func

        func_sentences  = [*map(lambda x: x.strip(), func_content.split("\n"))]

        if len(func_sentences) == 1:
            func += f"return {func_sentences[0]}"

        else:
            # if last sentence is doesnt end with ";" add return
            if not func_sentences[-1].endswith(";"):
                func_sentences[-1] = "return " + func_sentences[-1]

            func += "\n\t".join(func_sentences)

        # replace sintax with func name
        source = source[:match.start()] + func_name + func_end + source[match.end():]

        # append func at source (this happens after because start and end world change)
        source = func + "\n" + source

    return source
