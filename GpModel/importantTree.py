import pickle
import array as arr
import ast
from sympy import parse_expr
from data.gpModel import GpModel
import csv
import pandas as pd
from sklearn.metrics import r2_score, mean_squared_error

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
        
        if isinstance(node, ast.BinOp) or isinstance(node, ast.Name) or isinstance(node, ast.Constant) or isinstance(node, ast.Call) or isinstance(node, ast.UnaryOp):
            print(node.__class__.__name__, "parent:", node.parent.__class__.__name__, "index", self.index)
            node.index = self.index
            self.index += 1
            if isinstance(node, ast.Call):
                print("Call node", get_second_child_name(node, 0), get_second_child_name(node, 1))
            if isinstance(node, ast.UnaryOp):
                print("Unary node", get_second_child_name(node, 0), get_second_child_name(node, 1))
        # Do any work required by super class 
        node = super().visit(node)
        # If we have a valid node (ie. node not being removed)
        if isinstance(node, ast.AST):
            # update the parent, since this may have been transformed 
            # to a different node by super
            self.parent = node.parent
        return node

    def generic_visit(self, node):
        result = super().generic_visit(node)

        if isinstance(node.parent, ast.Call) and isinstance(node, ast.Name):
            self.index -= 1
            return result
        if hasattr(node, 'index') and self.modIndex == node.index:
            if self.newNode is not None:
                newNode = self.newNode
            else:
                print("node type", type(node))
                num = 0
                if isinstance(node.parent, ast.Call):
                    node2 = get_second_child(node.parent, 0)
                    if node2.id == "sin":
                        num = 1
                if isinstance(node.parent, ast.BinOp):
                    op = node.parent.op
                    if isinstance(op, ast.Mult) or isinstance(op, ast.Div):
                        num = 1
                newNode = ast.Constant(num)
            newNode.parent = node.parent    
            return newNode
        return result
    
def get_second_child_name(node, number=1):
    for i, child in enumerate(ast.iter_child_nodes(node)):
        if i == number:
            return str(child.__class__.__name__)
def get_second_child(node, number=1):
    for i, child in enumerate(ast.iter_child_nodes(node)):
        if i == number:
            return child
def load_sklearn_model(filepath):
    """Loads a sklearn model."""
    with open(filepath, 'rb') as file:
        model = pickle.load(file)
    return model

def getScore(model):
    df = pd.read_csv('house_small_test_data.csv')
    row_slice = slice(0, df.shape[0])
    selected_row = df.iloc[row_slice, 1:9]
    y_true = df.iloc[row_slice, 9:10]
    y_pred = model.predict(selected_row)
    score = r2_score(y_true, y_pred)
    return score
    # print(score)

if __name__ == '__main__':
    X = [[-121.54,39.47,14.0,1724.0,315.0,939.0,302.0,2.4952]]
    model = load_sklearn_model("bikes_gp_4.pkl")
    model.reInit()
    print(str(model.expr))
    # model = GpModel("x0 - (-33431.155)*x7 - 1*(-62467.385)", 0, 0)
    # model.reInit()
    # subtrees = model.subtrees
    # print(type(subtrees[0]))
    # print(subtrees)
    scores = []
    # for subtree in subtrees:
    #     newModel = GpModel(subtree, 0, 0)
    #     pred = newModel.predict(X)

    #     df = pd.read_csv('house_small_test_data.csv')
    #     row_slice = slice(0, df.shape[0])
    #     selected_row = df.iloc[row_slice, 1:9]
    #     y_true = df.iloc[row_slice, 9:10]
    #     y_pred = newModel.predict(selected_row)
    #     score = r2_score(y_true, y_pred)
    #     # print(score)
    #     scores.append(score)
    oldExpr = model.expr
    astExpr = ast.parse(str(model.expr))
    scores.append(getScore(model))
    exprs = []
    for i in range(1, model.complexity):
        # oldPred = model.predict(X)
        astExpr = ast.parse(str(model.expr))
        newTree = ast.fix_missing_locations(MyRemover(i).visit(astExpr))
        normal =  ast.unparse(newTree)
        newModel = GpModel(normal, 0, 0)
        exprs.append(str(newModel.expr))
        scores.append(getScore(newModel))
        # print("expr", oldExpr)
    print(scores)
    print(exprs)
    # newPred = model.predict(X)
    # print("old", oldPred, "newPred", newPred, "differnce", oldPred-newPred, "part", (oldPred-newPred)/oldPred)





