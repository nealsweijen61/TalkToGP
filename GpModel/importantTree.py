import pickle
import array as arr
import ast
from sympy import parse_expr
from data.gpModel import GpModel
import csv
import pandas as pd
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.inspection import permutation_importance
import shap
from scipy.special import softmax
import numpy as np

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
    df = pd.read_csv('house_small_train_data.csv')
    row_slice = slice(0, df.shape[0])
    selected_row = df.iloc[row_slice, 1:9]
    y_true = df.iloc[row_slice, 9:10]
    y_pred = model.predict(selected_row)
    score = r2_score(y_true, y_pred)
    return score
    # print(score)

def print_feature_importances_shap_values(shap_values, features):
    '''
    Prints the feature importances based on SHAP values in an ordered way
    shap_values -> The SHAP values calculated from a shap.Explainer object
    features -> The name of the features, on the order presented to the explainer
    '''
    # Calculates the feature importance (mean absolute shap value) for each feature
    importances = []
    for i in range(shap_values.values.shape[1]):
        importances.append(np.mean(np.abs(shap_values.values[:, i])))
    # Calculates the normalized version
    # importances_norm = softmax(importances)
    # Organize the importances and columns in a dictionary
    # feature_importances = {fea: imp for imp, fea in zip(importances, features)}
    # feature_importances_norm = {fea: imp for imp, fea in zip(importances_norm, features)}
    # Sorts the dictionary
    # feature_importances = {k: v for k, v in sorted(feature_importances.items(), key=lambda item: item[1], reverse = True)}
    # feature_importances_norm= {k: v for k, v in sorted(feature_importances_norm.items(), key=lambda item: item[1], reverse = True)}
    # Prints the feature importances
    print(importances[7])

if __name__ == '__main__':
    X = [[-121.54,39.47,14.0,1724.0,315.0,939.0,302.0,2.4952]]
    model = load_sklearn_model("bikes_gp_4.pkl")
    df = pd.read_csv('house_small_train_data.csv')
    dfTest = pd.read_csv('house_small_test_data.csv')
    model.reInit()
    row_slice = slice(0, dfTest.shape[0])
    print(str(model.expr))

    # astExpr = ast.parse(str(model.expr))
    # print("astExpr", astExpr)
    # newTree = ast.fix_missing_locations(MyRemover(10, ast.parse("1")).visit(astExpr))
    # normal =  ast.unparse(newTree)
    # normal = normal.replace('\n', '')
    # print("normal", normal)
    # newModel = GpModel(normal, 0, 0, explain=True)
    # print(str(newModel.expr))

    # # Fits the explainer
    # explainer = shap.Explainer(model.predict, df.iloc[row_slice, 1:9])
    # shap_values = explainer(df.iloc[row_slice, 1:9])
    # print(shap_values)
    # print(len(shap_values), len(shap_values[0]))
    # print_feature_importances_shap_values(shap_values, ["longitude", "latitude", "housing_median_age", "total_rooms", "total_bedrooms", "population", "households", "median_income"])
    # shap.plots.bar(shap_values)
    # shap.summary_plot(shap_values, df.iloc[row_slice, 1:9])
    
    # result = permutation_importance(model, df.iloc[row_slice, 1:9], df.iloc[row_slice, 9:10], n_repeats=10, random_state=42, n_jobs=-1)

    # # Get mean importance
    # print(result.importances_mean)
    # importances = result.importances_mean

    # # Print feature importance
    # for i, importance in enumerate(importances):
    #     print(f'Feature {i}: {importance}')
    # model = GpModel("x0 - (-33431.155)*x7 - 1*(-62467.385)", 0, 0)
    # model.reInit()
    subtrees = model.subtrees
    print(type(subtrees[0]))
    print(subtrees)
    print("parents", model.nodeParents)
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
    # print(scores)

    # oldExpr = model.expr
    # astExpr = ast.parse(str(model.expr))
    # scores.append((getScore(model), 0))
    # exprs = []
    # for i in range(1, model.complexity):
    #     # oldPred = model.predict(X)
    #     astExpr = ast.parse(str(model.expr))
    #     newTree = ast.fix_missing_locations(MyRemover(i).visit(astExpr))
    #     normal =  ast.unparse(newTree)
    #     newModel = GpModel(normal, 0, 0)
    #     exprs.append(str(newModel.expr))
    #     scores.append((getScore(newModel), i))
    #     # print("expr", oldExpr)
    # scores = sorted(scores, key=lambda x: x[0], reverse=True)
    # print(scores)
    # print(exprs)
    # newPred = model.predict(X)
    # print("old", oldPred, "newPred", newPred, "differnce", oldPred-newPred, "part", (oldPred-newPred)/oldPred)





