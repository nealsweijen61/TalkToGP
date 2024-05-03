import ast
from graphviz import Digraph
from sympy import parse_expr, simplify
import pickle

class MyRemover(ast.NodeTransformer):
    def __init__(self, modIndex, newNode=None):
        # self.node_number = node_number
        self.modIndex = modIndex
        self.newNode = newNode
        self.index = 0
        self.nodes = []
        self.parent = None

    def visit(self, node):
        # set parent attribute for this node
        node.parent = self.parent
        # This node becomes the new parent
        self.parent = node
        if isinstance(node, ast.BinOp) or isinstance(node, ast.Name) or isinstance(node, ast.Constant):
            print(node.__class__.__name__, "parent:", node.parent.__class__.__name__, "index", self.index)
            node.index = self.index
            self.index += 1
        # Do any work required by super class 
        print("visit super", node)
        node = super().visit(node)
        print("visit after super")
        # If we have a valid node (ie. node not being removed)
        if isinstance(node, ast.AST):
            # update the parent, since this may have been transformed 
            # to a different node by super
            self.parent = node.parent
        return node

    def generic_visit(self, node):
        print("generic visit", node)
        
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


model = load_sklearn_model("bikes_gp_1.pkl")
print(str(model.expr))
astModel = model.ast
print(astModel)
add = ast.BinOp(left = ast.Constant(2), right= ast.Constant(2), op= ast.Add())
# newTree = ast.fix_missing_locations(MyRemover(1, add).visit(astModel))
newTree = ast.fix_missing_locations(MyRemover(1).visit(astModel))

normal = ast.unparse(newTree)
normal = normal.replace('\n', '')
model.changeModel(normal)

print(model.expression)

# astModel = model.ast
# newTree = ast.fix_missing_locations(MyRemover(4, add).visit(astModel))

# normal = ast.unparse(newTree)
# model.changeModel(normal)

# X = [[3,0,7,0,6,0,1,0.686667,0.638263,0.585,0.208342]]
# pred = model.predict(X)
# print(pred)
# print(model.expression)