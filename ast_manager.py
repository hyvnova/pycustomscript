import ast  
from typing import List


# Creating AST  
code = ast.parse("""
1 * 2 * 3 * 4
""")  

# get expr
for expr in filter(
        lambda i: isinstance(i.value, ast.BinOp), 
        code.body
    ):

    # type hint
    expr: ast.Expr = expr.value

    numbers: List[int] = []

    # if expression has a value
    
    if "value" in expr._fields:
        print(dir(expr.value))
        numbers.append(expr.value)

    while (isinstance(expr, ast.BinOp)):

        # check that operation is *
        if not isinstance(expr.op, ast.Mult):
            break

        # right is always a value
        print(dir(expr.right))
    




# Printing AST
# print(ast.dump(code))
