import pickle
from data.gpModel import GpModel
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
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

def load_sklearn_model(filepath):
    """Loads a sklearn model."""
    with open(filepath, 'rb') as file:
        model = pickle.load(file)
    return model

if __name__ == '__main__':
    X = [[-121.54,39.47,14.0,1724.0,315.0,939.0,302.0,2.4952]]
    # model = load_sklearn_model("bikes_gp_4.pkl")
    # model.reInit()
    # print(str(model.expr))

    model = GpModel("(x3 + x7*55001 + 24423.635)*sin(cos(sin(x0)))", 0, 0 )
    model.reInit()
    print(str(model.expr))

    #Variables
    FEATURE_NAME = "longitude"
    SUBTREE_NUM = 8

    # Get Subtree mapping
    subTree = SubTree()
    subTree.visit(model.ast)
    mapping = subTree.mapping
    print("mapping", mapping)

    df = pd.read_csv('house_small_test_data.csv')
    row_slice = slice(0, df.shape[0])
    selected_row = df.iloc[row_slice, 1:9]
    print(selected_row.iloc[:, 0].mean())

    subtrees = model.subtrees
    print("amount", len(subtrees))
    print(subtrees)

    minValue = selected_row[FEATURE_NAME].min()
    maxValue = selected_row[FEATURE_NAME].max()
    column_num = df.columns.get_loc(FEATURE_NAME)
    print("column num", column_num)

    num = mapping.index(SUBTREE_NUM) if SUBTREE_NUM in mapping else -1
    model = GpModel(subtrees[num], 0, 0)  

    # Generate a range of values for the 8th feature
    feature_values = np.linspace(minValue, maxValue, num=100)  # Adjust num as needed for smoother plot

    default_values = []
    for i in range(8):
        default_values.append(selected_row.iloc[:, i].mean())

    input_values = []
    for feat in feature_values:
        input = default_values.copy()
        input[column_num-1] = feat
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
    plt.show()