import re

def pattern_handler(source: str) -> str:
    """
    Dict Destructuration
    ```py
    obj = {"name": "Jonh", "level" : 2, "other" : "other value"}
    {name, level} = obj
    ```
    """


    pattern: re.Pattern = re.compile(
        r"""
        \{                      # Start of dict
        \s?                     # Optional WhiteSpace
        ([a-zA-Z_0-9,\s]+)      # Dict values
        \s?                     
        \}                      # Dict end
        \s?         
        =                       # assigment token
        \s?         
        (.+)                    # Object which will be destructured
        """,
        re.VERBOSE
    )

    for match in pattern.finditer(source):
        s, e = match.start(),  match.end()

        key, obj = match.groups()
        sentence = ''

        if not key or not obj:
            return

        key, obj = key.strip(), obj.strip()

        # multiple assingments
        if "," in key:
            keys = [*map(lambda x: x.strip(), key.split(","))]

            sentence = ", ".join(keys)
            sentence += " = "

            for key in keys:
                sentence += f"{obj}['{key}'], "

        # one assing
        else:
            sentence = f'{key} = {obj}["{key}"]'

        source = source[:s] + "\n" + sentence + "\n" + source[e:]


    return source
