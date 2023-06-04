import re

def pattern_handler(source: str) -> str:
    """
    ## Ranges
    Syntax support for ranges just like in Rust. Underneath the hood, this uses the `range` function in Python.
    Note: There cannot be any whitespace between the range operator `..` and the start/end of the range.
    
    ### Examples
    ```py
    for i in <1..10>:
        print(i)

    <a..z>.map((x) => x * 2;) # <- returns a `Iterator` object not a list 
    
    <..10> # <- start is omitted

    # List slicing 
    some_list[<1..10>] # <- returns a list since the range is being used as a slice

    ### Invalid Examples
    ```py
    """

    range_pattern: re.Pattern = re.compile(
        r"""
        \<  # opening arrow - syntax for start of range
        (?P<start>[a-zA-Z0-9._\[\]\"\'\(\)\{\}]+)? # start
        \.\. # range operator seperator ".."
        (?P<inclusive>\=)? # inclusive
        (?P<end>[a-zA-Z0-9._\[\]\"\'\(\)\{\}]+)? # end
        \> # closing arrow - syntax for end of range
        """,
        re.VERBOSE
    )

    slice_range_pattern: re.Pattern = re.compile(
        r"""
        \[ # opening bracket
        \< # opening arrow - syntax for start of range
        (?P<start>[a-zA-Z0-9._\[\]\"\'\(\)\{\}]+)? # start
        \.\. # range operator seperator ".."
        (?P<inclusive>\=)? # inclusive
        (?P<end>[a-zA-Z0-9._\[\]\"\'\(\)\{\}]+)? # end
        \> # closing arrow - syntax for end of range
        \] # closing bracket
        """,
        re.VERBOSE
    )

    # HANDLE SLICE RANGES FIRST TO AVOID OVERLAP WITH NORMAL RANGES
    for match in slice_range_pattern.finditer(source):
        # match start & end
        start, end = match.start(), match.end()

        # get start & end of range
        range_start, range_end, inclusive = match.group("start"), match.group("end"), match.group("inclusive")

        inclusive = "+1" if inclusive else ""
        
        # replace range with slice
        source = source[:start] + f"{range_start}:{range_end}{inclusive}" + source[end:]

    # HANDLE NORMAL RANGES
    for match in range_pattern.finditer(source):
        # match start & end
        start, end = match.start(), match.end()

        # get start & end of range
        range_start, range_end, inclusive = match.group("start"), match.group("end"), match.group("inclusive")

        inclusive = "+1" if inclusive else ""

        # replace range with slice | Note: Iterator should be already imported as a custom builtin
        source = source[:start] + f"Iterator(range({range_start}, {range_end}{inclusive}))" + source[end:] 

    return source