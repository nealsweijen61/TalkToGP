from sympy import symbols, lambdify, parse_expr, count_ops, preorder_traversal, Function, Pow, Mod, Symbol, simplify, expand
# expression = "((((x1+x9)+41.432000)/ ((x10/ (x2+1e-6) )+1e-6) )+(x8+x8))"
expression = "(57.700000/ (x10+1e-6))"
expression2 = "((57.700000/1) / (x10+1e-6))"
expression = "sin(2*x)"
expression2 = "2*sin(x)*cos(x)"

expression = "((((x1+x9)+41.432000)/ ((x10/ (x2+1e-6) )+1e-6) )+(x8+x8))"
expression2 = "(57.700000/ (x10+1e-6))"
expression3 = "x0+x1+x9"
expression4 = "((21.783000*56.278000)*x0)"
expression5 = "(((x1+(2.793000*x8))*(57.470000*(32.096000+x2)))+(((36.191000/ (x6+1e-6) )+(x0-19.821000))*((x4+x2)*4.235000)))"
symbols = symbols('x0 x1 x2 x3 x4 x5 x6 x7 x8 x9 x10')

expr = parse_expr(expression, evaluate=False)
expr2 = parse_expr(expression2, evaluate=False)
expr3 = parse_expr(expression3, evaluate=False)
expr4 = parse_expr(expression4, evaluate=False)
expr5 = parse_expr(expression5, evaluate=False)

exprs = [expr, expr3]

simple = simplify(expr)
simple2 = simplify(expr2)

subtrees = {}
print(expr3)
def addSubTrees(expr):
    for arg in preorder_traversal(expr):
        print(arg)
        if(arg.args != ()):
            found = False
            for key in subtrees:
                if simplify(key - arg) == 0:
                    print(key, arg)
                    subtrees[key] = subtrees.get(key, 0) + 1
                    found = True
            if not found:
                subtrees[arg] = subtrees.get(arg, 0) + 1

for expr in exprs:
    addSubTrees(expr)
sorted(subtrees.items(), key=lambda x:x[1], reverse=True)
print(subtrees)

func = lambdify(symbols, expr, 'numpy')
# symbols = symbols('x0 x1 x2 x3 x4 x5 x6 x7 x8 x9 x10')
# expr = parse_expr(expr, evaluate=False)
# print(expr)
# func = lambdify(symbols, expr, 'numpy')
# # X = [3,0,7,0,6,0,1,0.686667,0.638263,0.585,0.208342]
# X = [3,0,7,0,6,0,1,0.686667,0.638263,0.585,0.208342]
# res = func(*X)
# print(res)
# print(count_ops(expr))