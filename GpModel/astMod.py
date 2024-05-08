import ast
from graphviz import Digraph
from sympy import parse_expr, simplify
import pickle
import time
import os

def get_second_child_name(node, number=1):
    for i, child in enumerate(ast.iter_child_nodes(node)):
        if i == number:
            return str(child.__class__.__name__)
def get_grand_child(node, number=0):
    for i, child in enumerate(ast.iter_child_nodes(node)):
        if i == number:
            for j, ch in enumerate(ast.iter_child_nodes(child)):
                if j == number:
                    return str(ch.__class__.__name__)

def create_ast_graph(graph, node, parent_name, index='', num=-1):
    current_name = f'{parent_name}_{index}' if parent_name else 'Root'
    num += 1
    print(type(node))
    if isinstance(node, ast.BinOp):
        print("binop", node.__class__)
        graph.node(current_name, label=f'{get_second_child_name(node)}_{num}')
        for i, child in enumerate(ast.iter_child_nodes(node)):
            if i == 1:
                continue
            child_name = f'{current_name}_{i}'
            graph.edge(current_name, child_name)
            num = create_ast_graph(graph, child, current_name, i, num)
    elif isinstance(node, ast.Constant):
        graph.node(current_name, label=f'{node.value}_{num}')
    elif isinstance(node, ast.Name): 
        graph.node(current_name, label=f'{node.id}_{num}')
    elif isinstance(node, ast.Module) or isinstance(node, ast.Expr):
        num -= 1
        for i, child in enumerate(ast.iter_child_nodes(node)):
            child_name = f'{current_name}_{i}'
            num = create_ast_graph(graph, child, current_name, i, num)
    elif isinstance(node, ast.Call):
        graph.node(current_name, label=f'{node.func.id}_{num}')
        for i, child in enumerate(ast.iter_child_nodes(node)):
            if i == 0:
                continue
            child_name = f'{current_name}_{i}'
            graph.edge(current_name, child_name)
            num = create_ast_graph(graph, child, current_name, i, num)
    elif isinstance(node, ast.AST):
        graph.node(current_name, label=f'{node.__class__.__name__}_{num}')
        for i, child in enumerate(ast.iter_child_nodes(node)):
            child_name = f'{current_name}_{i}'
            graph.edge(current_name, child_name)
            num = create_ast_graph(graph, child, current_name, i, num)
    return num

def plot_tree(model, output):
    # return_string = '<img src="https://upload.wikimedia.org/wikipedia/commons/7/70/2005-bandipur-tusker.jpg" alt="Girl in a jacket" width="500" height="600">'
    print("plotexpr", str(model.expr))
    print("plotparse", parse_expr(model.expression, evaluate=False))
    print("plotexpression", str(model.expression))
    expr = ast.parse(str(model.expr))

    graph = Digraph(comment='AST Tree')
    create_ast_graph(graph, expr, '')

    output_directory = output
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    # Set the output directory
    # timestamp = int(time.time())
    output_file = os.path.join(output_directory, f"expression_tree")

    # Render and save the graph
    graph.render(output_file, format='png', cleanup=True)

class MyRemover(ast.NodeTransformer):
    def __init__(self, modIndex, newNode=None):
        # self.node_number = node_number
        self.modIndex = modIndex
        self.newNode = newNode
        self.index = 0
        self.nodes = []
        self.parent = None

    # def visit(self, node):
    #     # set parent attribute for this node
    #     node.parent = self.parent
    #     # This node becomes the new parent
    #     self.parent = node
    #     if isinstance(node, ast.BinOp) or isinstance(node, ast.Name) or isinstance(node, ast.Constant):
    #         if isinstance(node, ast.BinOp):
    #             print(node.__class__.__name__, "parent:", node.parent.__class__.__name__, "index", self.index, "left", get_second_child_name(node))
    #         elif isinstance(node, ast.Constant):
    #             print(node.__class__.__name__, "parent:", node.parent.__class__.__name__, "index", self.index, "left", node.value)
    #         else:
    #             # print(node.__class__.__name__, "parent:", node.parent.__class__.__name__, "index", self.index)
    #             print(node.__class__.__name__, "parent:", node.parent.__class__.__name__, "index", self.index, "left", node.id)
    #         node.index = self.index
    #         self.index += 1
    #     # Do any work required by super class 
    #     # print("visit super", node, node.__class__.left)
    #     node = super().visit(node)
    #     # print("visit after super")
    #     # If we have a valid node (ie. node not being removed)
    #     if isinstance(node, ast.AST):
    #         # update the parent, since this may have been transformed 
    #         # to a different node by super
    #         self.parent = node.parent
    #     return node

    def generic_visit(self, node):
        node.parent = self.parent
        # This node becomes the new parent
        self.parent = node
        if isinstance(node, ast.BinOp) or isinstance(node, ast.Name) or isinstance(node, ast.Constant):
            if isinstance(node, ast.BinOp):
                print(node.__class__.__name__, "parent:", node.parent.__class__.__name__, "index", self.index, "left", get_grand_child(node), get_second_child_name(node, 1), get_grand_child(node, 2))
            elif isinstance(node, ast.Constant):
                print(node.__class__.__name__, "parent:", node.parent.__class__.__name__, "index", self.index, "left", node.value)
            else:
                # print(node.__class__.__name__, "parent:", node.parent.__class__.__name__, "index", self.index)
                print(node.__class__.__name__, "parent:", node.parent.__class__.__name__, "index", self.index, "left", node.id)
            node.index = self.index
            self.index += 1
        
        result = super().generic_visit(node)
        
        if hasattr(node, 'index'):
            print("index", node.index)
        if hasattr(node, 'index') and self.modIndex == node.index:
            print("ALTERING", node.__class__.__name__)
            if self.newNode is not None:
                newNode = self.newNode
            else:
                num = 0
                if isinstance(node.parent, ast.BinOp):
                    op = node.parent.op
                    if isinstance(op, ast.Mult) or isinstance(op, ast.Div):
                        num = 1
                newNode = ast.Constant(num)
            newNode.parent = node.parent
            return newNode
        return result
        

def load_sklearn_model(filepath):
    """Loads a sklearn model."""
    with open(filepath, 'rb') as file:
        model = pickle.load(file)
    return model


model = load_sklearn_model("bikes_gp_6.pkl")
model.reInit()
plot_tree(model, "og")
# print(str(model.expr))
# astModel = model.ast
# # astModel = ast.parse(str(model.expr))
# print("ast", astModel)
# add = ast.BinOp(left = ast.Constant(2), right= ast.Constant(2), op= ast.Add())
# # newTree = ast.fix_missing_locations(MyRemover(1, add).visit(astModel))
# newTree = ast.fix_missing_locations(MyRemover(1).visit(astModel))

# normal = ast.unparse(newTree)
# normal = normal.replace('\n', '')
# model.changeModel(normal)
# plot_tree(model, "newTree")

# print(model.expression)

# astModel = model.ast
# newTree = ast.fix_missing_locations(MyRemover(4, add).visit(astModel))

# normal = ast.unparse(newTree)
# model.changeModel(normal)

# X = [[3,0,7,0,6,0,1,0.686667,0.638263,0.585,0.208342]]
# pred = model.predict(X)
# print(pred)
# print(model.expression)