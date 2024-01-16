import ast
from graphviz import Digraph
from sympy import parse_expr, simplify

class MyVisitor(ast.NodeVisitor):
    def visit(self, node):
        stack = [node]

        while stack:
            current_node = stack.pop()
            print(f"Node type: {type(current_node).__name__}")

            # Add child nodes to the stack for further processing
            stack.extend(ast.iter_child_nodes(current_node))
def get_second_child_name(node):
    for i, child in enumerate(ast.iter_child_nodes(node)):
        if i == 1:
            return str(child.__class__.__name__)

def create_ast_graph(graph, node, parent_name, index=''):
    current_name = f'{parent_name}_{index}' if parent_name else 'Root'
    print(str(node.__class__.__name__))
    if isinstance(node, ast.BinOp):
        graph.node(current_name, label=get_second_child_name(node))
        for i, child in enumerate(ast.iter_child_nodes(node)):
            if i == 1:
                continue
            child_name = f'{current_name}_{i}'
            graph.edge(current_name, child_name)
            create_ast_graph(graph, child, current_name, i)
    elif isinstance(node, ast.Constant):
        graph.node(current_name, label=str(node.value))
    elif isinstance(node, ast.Name):
        graph.node(current_name, label=str(node.id))
    elif isinstance(node, ast.Module) or isinstance(node, ast.Expr):
        for i, child in enumerate(ast.iter_child_nodes(node)):
            child_name = f'{current_name}_{i}'
            create_ast_graph(graph, child, current_name, i)
    elif isinstance(node, ast.AST):
        graph.node(current_name, label=str(node.__class__.__name__))
        for i, child in enumerate(ast.iter_child_nodes(node)):
            child_name = f'{current_name}_{i}'
            graph.edge(current_name, child_name)
            create_ast_graph(graph, child, current_name, i)

def count_nodes(node):
    return sum(1 for _ in ast.walk(node))

def printSubTrees(node):
    if isinstance(node, ast.Module) or isinstance(node, ast.Expr) or count_nodes(node) < 3:
        for child_node in ast.iter_child_nodes(node):
            printSubTrees(child_node)
    else:
        subtrees.append(ast.unparse(node))
        for child_node in ast.iter_child_nodes(node):
            printSubTrees(child_node)


expr = "(57.700000/ (x10+1e-6))"
parsed = ast.parse(expr)

expr2 = "x0 * (x10+1e-6)"
parsed2 = ast.parse(expr2)

expr3= "(((x1+(2.793000*x8))*(57.470000*(32.096000+x2)))+(((36.191000/ (x6+1e-6) )+(x0-19.821000))*((x4+x2)*4.235000)))"
parsed3 = ast.parse(expr3)

subtrees = []
printSubTrees(parsed)
printSubTrees(parsed2)
printSubTrees(parsed3)
# print(subtrees)

subDic = {}
speedDic = {}
testExpr = "x0 * (x10+1e-6)"
for subtree in subtrees:
    symExpr = parse_expr(subtree)
    test = simplify(parse_expr(testExpr)- symExpr)
    speedDic[test] = speedDic.get(test, 0) + 1
    found = False
    if speedDic[test] > 1:
        for key in subDic:
            print("sym:", symExpr, "key:", key)
            if simplify(key - symExpr) == 0:
                subDic[key] = subDic.get(key, 0) + 1
                found = True
                break
    if not found:
        subDic[symExpr] = subDic.get(symExpr, 0) + 1
subDic = sorted(subDic.items(), key=lambda x:x[1], reverse=True)
print(subDic)
# Create the graph
# graph = Digraph(comment='AST Tree')
# create_ast_graph(graph, parsed, '')

# Render and save the graph
# graph.render('ast_tree', format='png', cleanup=True)

# normal = ast.unparse(parsed)
# print(normal)
# dump = ast.dump(parsed, annotate_fields=True)
# print(dump)
