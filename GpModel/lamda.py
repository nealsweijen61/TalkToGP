from sympy import symbols, lambdify, parse_expr, count_ops

expr = "((((x1+x9)+41.432000)/ ((x10/ (x2+1e-6) )+1e-6) )+(x8+x8))"

symbols = symbols('x0 x1 x2 x3 x4 x5 x6 x7 x8 x9 x10')
expr = parse_expr(expr, evaluate=False)
print(expr)
func = lambdify(symbols, expr, 'numpy')
# X = [3,0,7,0,6,0,1,0.686667,0.638263,0.585,0.208342]
X = [3,0,7,0,6,0,1,0.686667,0.638263,0.585,0.208342]
res = func(*X)
print(res)
print(count_ops(expr))