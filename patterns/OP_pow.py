import ast
from typing import TypeVar, List
from dataclasses import dataclass

# type hint
Number = TypeVar("Number", int, float)


@dataclass
class ExprData:
    base: Number | str = None
    exponent: int = 1
    end: int = None


def find_mult_pattern_at(expr: ast.Expr, source: str, data: ExprData, passed_right_value: Number = None):
    """
    Gets an epression and tries to find patterns as:
    ```py
    10 * 10
    x * x * x
    ```
    Replaces the matched expression with `pow(base, exponent)`, returns source code modified
    """

    # check operation type, if is not Mult then continue:
    if not isinstance(expr.op, ast.Mult):

        # if left is a BinOp then try to find a mult in it
        if isinstance(expr.left, ast.BinOp):
            return find_mult_pattern_at(expr.left, source, data)

        # if left is not a Expr, then theres nothing more to do
        else:
            return source

    right = expr.right

    # right must be a gettable value here
    if isinstance(right, ast.Constant):
        right_value = right.value

    elif isinstance(right, ast.Name):
        right_value = right.id

    # if a passed right value is given then compare to it
    if passed_right_value == right_value:

        # set base
        data.base = right_value
        # add 1 to exponent
        data.exponent += 1

    else:
        # set end; because passed it not right
        data.end = expr.end_col_offset

    # if left is an Operation then give the "process" to that side
    if isinstance(expr.left, ast.BinOp):

        # set end; end is the offset of chars where the code is located line[:end]
        data.end = expr.end_col_offset

        return find_mult_pattern_at(expr.left, source, data, right_value)

    # if left is not an operation then it is has a value
    else:
        # get left value
        left = expr.left

        if isinstance(left, ast.Constant):
            left_value = left.value

        elif isinstance(left, ast.Name):
            left_value = left.id

        # compare values
        if right_value == left_value:
            start = expr.col_offset

            # set base
            data.base = right_value
            # add 1 to exponent
            data.exponent += 1

        # if not equal then start is on the right
        else:
            start = expr.right.col_offset

    # replace expr in source with pow
    code = source.split("\n")
    line = code[expr.lineno-1]
    code[expr.lineno-1] = line[:start] + \
        f"pow({data.base}, {data.exponent})" + line[data.end:]

    return "\n".join(code)


def find_all_binOp(body: ast.Module | List[ast.Expr]) -> List[ast.BinOp]:
    """
    Finds all `ast.BinOp` inside all properties of all members of the given `body`
    """

    found: List[ast.BinOp] = []

    for item in body:

        if isinstance(item, ast.BinOp):
            found.append(item)
            continue

        if not isinstance(item, (
            ast.Assign,
            ast.Expr,
            ast.AnnAssign,
            ast.For,
            ast.FunctionDef,
            ast.comprehension,
            ast.ClassDef,
            ast.AsyncFunctionDef,
            ast.AsyncFor,
            ast.With,
            ast.AsyncWith
        )) or not getattr(item, "__dict__", None):
            continue
        
        print()
        for k, value in vars(item).items():
            print(k)

            if isinstance(value, ast.BinOp):
                found.append(value)
                continue

            else:
                if getattr(value, "__dict__", None):
                    found.extend(find_all_binOp([value]))

    return found


def pattern_handler(source: str) -> str:
    """
    Pow Replacement (Optimization Pattern)
    ```py
    # match these cases
    n = x * x # -> n = pow(x, 2)
    num = 10 * 10 * 10 # -> num = pow(10, 3)
    3 + 4 * 4 * 2 - 3 # -> 3 + pow(4,2) * 2 -3
    ```
    """
    parsed_source = ast.parse(source)

    # iterate throught BinOp (arithmetic operations) and see if can find any multiplication valid pattern to replace

    f = find_all_binOp(parsed_source.body)
    print(f)
    for expr in f:

        expr: ast.Expr = expr.value

        source = find_mult_pattern_at(expr, source, ExprData())

    return source
