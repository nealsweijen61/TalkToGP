from explain.actions.utils import get_models
import ast
from data.gpModel import GpModel
import numpy as np
import matplotlib.pyplot as plt
import time
import os

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
    
def effect_operation(conversation, parse_text, i, **kwargs):
    models = get_models(conversation)
    model = models[0]
    data = conversation.temp_dataset.contents['X']

    FEATURE_NAME = parse_text[i+1]
    SUBTREE_NUM = int(parse_text[i+2])
    print("FEATURE NAME", FEATURE_NAME, "SUBTREE_NUM", SUBTREE_NUM)

    # Get Subtree mapping
    subTree = SubTree()
    subTree.visit(model.ast)
    mapping = subTree.mapping
    print("mapping", mapping)

    #find subtrees
    subtrees = model.subtrees
    print("amount", len(subtrees))
    print(subtrees)

    minValue = data[FEATURE_NAME].min()
    maxValue = data[FEATURE_NAME].max()
    column_num = data.columns.get_loc(FEATURE_NAME)
    print("column num", column_num)

    num = mapping.index(SUBTREE_NUM) if SUBTREE_NUM in mapping else -1
    model = GpModel(subtrees[num], 0, 0)  

    # Generate a range of values for the 8th feature
    feature_values = np.linspace(minValue, maxValue, num=100)  # Adjust num as needed for smoother plot

    default_values = []
    features = conversation.get_var('features').contents
    definitions = conversation.feature_definitions
    keys = list(definitions.keys())
    for i in range(8):
        if keys[i] in features:
            default_values.append(features[keys[i]])
        else:
            default_values.append(data.iloc[:, i].mean())
    print("default_values", default_values)
    input_values = []
    for feat in feature_values:
        input = default_values.copy()
        input[column_num] = feat
        input_values.append(input)

        # Obtain predictions for each feature value
    predictions = model.predict(input_values)
    # print(predictions)
    
    # Plot the graph
    plt.plot(feature_values, predictions, label='Predictions')
    plt.xlabel(f'{FEATURE_NAME}')
    plt.ylabel('Predicted Value')
    plt.title(f'Effect of {FEATURE_NAME} on Prediction of subtree {str(model.expr)}')
    plt.legend()
    plt.grid(True)
    timestamp = int(time.time())
    plt.savefig(os.path.join('static', 'images', f'plot{timestamp}.png'))
    plt.close()
    return_string = f'<img src="static/images/plot{timestamp}.png" alt="drawing" width="400"/>'
    return return_string, 1