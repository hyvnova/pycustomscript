from patterns import patterns

def run(raw_source: str) -> None:
    """
    Runs the code given using CustomScript Sintax
    """

    source = ""

    # clean lines
    for line in raw_source.split("\n"):

        # skip empty lines or comments
        if not line.strip() or line.startswith("#"):
            continue

        # remove commet
        if "#" in line:
            line = line.split("#")[0]

        source += line + "\n"


    for pattern_handler in patterns:
        source = pattern_handler(source)

    # save source
    with open("__source.py", "w") as f:
        f.write(source)

    exec(source)
        
            