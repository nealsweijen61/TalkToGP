from sympy import symbols, parse_expr

operator = "MUL"
# operator = parse_expr(operator, evaluate=False)
operator = symbols(operator)

print(operator, type(operator))