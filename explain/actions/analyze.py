import pandas as pd
from sklearn.metrics import r2_score
from sklearn.inspection import permutation_importance
from explain.actions.utils import get_models
from data.gpModel import GpModel
import ast

class SubTree(ast.NodeVisitor):
    def __init__(self):
        self.index = 0
        self.mapping = []
        self.parent = None

    def generic_visit(self, node):
        node.parent = self.parent
        self.parent = node
        if isinstance(node, ast.BinOp) or isinstance(node, ast.Name) or isinstance(node, ast.Constant) or isinstance(node, ast.Call) or isinstance(node, ast.UnaryOp):
            print("visit", self.index, type(node))
            if isinstance(node, ast.Constant) == False and isinstance(node, ast.Name) == False:
                self.mapping.append(self.index)
            if isinstance(node, ast.Name) and isinstance(node.parent, ast.Call):
                self.index -= 1
            self.index += 1
        ast.NodeVisitor.generic_visit(self, node)
        if isinstance(node, ast.AST):
            # update the parent, since this may have been transformed 
            # to a different node by super
            self.parent = node.parent
        return node

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
    
def getScore(conversation, model):
    data = conversation.temp_dataset.contents['X']
    y_true = conversation.temp_dataset.contents['y']
    y_pred = model.predict(data)
    score = r2_score(y_true, y_pred)
    return score

def analyze_operation(conversation, parse_text, i, **kwargs):
    models = get_models(conversation)
    model = models[0]
    data = conversation.temp_dataset.contents['X']
    trueOutput = conversation.temp_dataset.contents['y']
    result = permutation_importance(model, data, trueOutput, n_repeats=10, random_state=42, n_jobs=-1)

    subtrees = model.subtrees
    scores = []
    return_string = "The scores of all subtrees are:"
    for i, subtree in enumerate(subtrees):
        #make new model from subtree
        newModel = GpModel(subtree, 0, 0)

        preds = newModel.predict(data)
        adjustedData = data.copy()
        #add predictions to last column of data
        adjustedData[f"node{1}"] = preds

        #look which index this subtree is add
        subT = SubTree()
        subT.visit(model.ast)
        mapping = subT.mapping
        print("mapping", mapping)
        num = mapping[i]
        print(num)

        astExpr = ast.parse(str(model.expr))
        print("astExpr", astExpr)
        newTree = ast.fix_missing_locations(MyRemover(num, ast.parse("x8")).visit(astExpr))
        normal =  ast.unparse(newTree)
        normal = normal.replace('\n', '')
        print(normal)
        newModel = GpModel(normal, 0, 0, explain=True)
        print(str(newModel.expr))

        # explainer = shap.Explainer(newModel.predict, selected_row)
        # shap_values = explainer(selected_row)
        # score = print_feature_importances_shap_values(shap_values)
        # scores.append(score)
        result = permutation_importance(newModel, adjustedData, trueOutput, n_repeats=10, random_state=42, n_jobs=-1)
        importances = result.importances_mean
        print("Last feature", importances[8])
        scores.append(importances[8])
        return_string += "<br>"
        return_string += f"Subtree {num} has score {importances[8]}"
        for i, importance in enumerate(importances):
            print(f'Feature {i}: {importance}')
    
    print(scores)
    print("mapping", mapping)
    return return_string, 1

def bad_operation(conversation, parse_text, i, **kwargs):
    models = get_models(conversation)
    model = models[0]
    scores = []
    score0 = getScore(conversation, model)
    for i in range(1, model.complexity+1):
        # oldPred = model.predict(X)
        astExpr = ast.parse(str(model.expr))
        newTree = ast.fix_missing_locations(MyRemover(i).visit(astExpr))
        normal =  ast.unparse(newTree)
        newModel = GpModel(normal, 0, 0)
        scores.append((getScore(conversation, newModel), i))
    scores = sorted(scores, key=lambda x: x[0], reverse=True)
    return_string = f"The original model scores {score0}"
    return_string += "<br>"
    return_string += "Removing the following nodes results in a score:"
    for score, node in scores:
        return_string += "<br>"
        return_string += f"Node {node} scores {score}"
    return return_string, 1