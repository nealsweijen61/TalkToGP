import matplotlib.pyplot as plt
from flask import Flask, render_template 
import os
import base64
from data.customClassifier import CustomClassifier
from io import BytesIO
from graphviz import Digraph
import ast
from sympy import dotprint, simplify, parse_expr

# def ops_operation(conversation, parse_text, i, **kwargs):
#     """Gives the number of operations"""
#     # get the max value
#     model = conversation.get_var('model').contents
#     number = model.operators()
#     # compose the return string
#     return_string = f"The number of operators is {number}"
#     # return the string and 1, indicating success
#     return return_string, 1

def num_ops_operation(conversation, parse_text, i, **kwargs):
    """Gives the number of operations"""
    # get operatos values of each model
    models = conversation.get_var('models').contents
    operators = []
    for model in models:
        operators.append(model.numOperators())
    # compose the return string
    return_string = f"The number of operators in each model is {operators}"
    # return the string and 1, indicating success
    return return_string, 1

def get_ops_operation(conversation, parse_text, i, **kwargs):
    """Gives the operations"""
    # get operatos of each model
    models = conversation.get_var('models').contents
    operators = []
    for model in models:
        operators.append(model.getOperators())
    # compose the return string
    return_string = f"The operators in each model is {operators}"
    # return the string and 1, indicating success
    return return_string, 1

def num_nodes_operation(conversation, parse_text, i, **kwargs):
    """Gives the number of nodes"""
    # get operatos values of each model
    models = conversation.get_var('models').contents
    operators = []
    for model in models:
        operators.append(model.numNodes())
    # compose the return string
    return_string = f"The number of nodes in each model is {operators}"
    # return the string and 1, indicating success
    return return_string, 1

def get_features_operation(conversation, parse_text, i, **kwargs):
    """Gives the features"""
    # get operatos of each model
    models = conversation.get_var('models').contents
    features = []
    for model in models:
        features.append(model.getFeatures())
    # compose the return string
    definitions = conversation.feature_definitions
    features_names = []
    for feature in features:
        feats = []
        for feat in feature:
            feats.append(feature_to_name(feat, definitions))
        features_names.append(feats)
    return_string = f"The features in each model are {features_names}"
    # return the string and 1, indicating success
    return return_string, 1

def feature_to_name(variable_name, definitions):
    print("Varaialbe_name", variable_name)
    variable_number = int(str(variable_name)[1:])
    keys = list(definitions.keys())
    if 0 <= variable_number <= len(keys):
        return keys[variable_number]
    else:
        return None
    
def num_features_operation(conversation, parse_text, i, **kwargs):
    """Gives the number of features"""
    # get operatos of each model
    models = conversation.get_var('models').contents
    features = []
    for model in models:
        features.append(model.numFeatures())
    # compose the return string
    return_string = f"The features in each model are {features}"
    # return the string and 1, indicating success
    return return_string, 1

def most_common_features_operation(conversation, parse_text, i, **kwargs):
    models = conversation.get_var('models').contents
    features = []
    definitions = conversation.feature_definitions
    for model in models:
        features.append(model.getFeatures())
    
    features_count = {}
    for feature_set in features:
        for feature in feature_set:
            feature = feature_to_name(feature, definitions)
            features_count[feature] = features_count.get(feature, 0) + 1
    features_count = sorted(features_count.items(), key=lambda x:x[1], reverse=True)
    return_string = f"Most common features are {features_count}"
    return return_string, 1
    

def get_expr_operation(conversation, parse_text, i, **kwargs):
    """Gives the expressions of each model"""
    # get operatos of each model
    models = conversation.get_var('models').contents
    expressions = []
    return_string = f"The features in each model are: "
    for model in models:
        return_string += str(model.getExpr())
        return_string += "<br><br>"
        # expressions.append(model.getExpr())
    # compose the return string
    # return_string = f"The features in each model are {expressions}"
    # return the string and 1, indicating success
    
    return return_string, 1

def plot_operation(conversation, parse_text, i, **kwargs):
    # return_string = '<img src="https://upload.wikimedia.org/wikipedia/commons/7/70/2005-bandipur-tusker.jpg" alt="Girl in a jacket" width="500" height="600">'
    models = conversation.get_var('models').contents
    x = []
    y = []
    expr = "(57.700000/ (x10+1e-6))"
    classifier = CustomClassifier(expr, 5, 6)
    print(classifier.accuracy)
    for model in models:
        x.append(model.accuracy)
        y.append(model.complexity)
    plt.scatter(x, y, alpha=0.5) 
    plt.savefig(os.path.join('static', 'images', 'plot.png'))
    plt.close()
    # render = render_template('matplotlib-plot1.html') 
    # return_string = "<img src='{{ url_for('static', filename='istatic/images/plot.png') }}'>"
    return_string = '<img src="static/images/plot.png" alt="drawing" width="400"/>'
    return return_string, 1

# def most_common_features_operation(conversation, parse_text, i, **kwargs):
#     models = conversation.get_var('models').contents
#     for model in models:
#         model.getFeatures()

#     return "kloenk", 1
def get_second_child_name(node):
    for i, child in enumerate(ast.iter_child_nodes(node)):
        if i == 1:
            return str(child.__class__.__name__)

def create_ast_graph(graph, node, parent_name, index='', num=-1):
    current_name = f'{parent_name}_{index}' if parent_name else 'Root'
    num += 1
    print(str(node.__class__.__name__))
    if isinstance(node, ast.BinOp):
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
    elif isinstance(node, ast.AST):
        graph.node(current_name, label=f'{node.__class__.__name__}_{num}')
        for i, child in enumerate(ast.iter_child_nodes(node)):
            child_name = f'{current_name}_{i}'
            graph.edge(current_name, child_name)
            num = create_ast_graph(graph, child, current_name, i, num)
    return num

def plot_tree_operation(conversation, parse_text, i, **kwargs):
    # return_string = '<img src="https://upload.wikimedia.org/wikipedia/commons/7/70/2005-bandipur-tusker.jpg" alt="Girl in a jacket" width="500" height="600">'
    models = conversation.get_var('models').contents
    model = models[0]
    expr = ast.parse(model.expression)

    graph = Digraph(comment='AST Tree')
    create_ast_graph(graph, expr, '')

    output_directory = 'static/images/'
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    # Set the output directory
    output_file = os.path.join(output_directory, "expression_tree")

    # Render and save the graph
    graph.render(output_file, format='png', cleanup=True)

    return_string = '<img src="static/images/expression_tree.png" alt="drawing" width="400"/>'
    return return_string, 1

def most_common_trees_operation(conversation, parse_text, i, **kwargs):
    models = conversation.get_var('models').contents
    subtrees = []
    for model in models:
        subtrees = subtrees + model.subtrees
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
    return_string = f"Most common subtrees are {subDic}"
    return return_string, 1