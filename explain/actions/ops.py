import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from flask import Flask, render_template 
import os
import base64
from data.customClassifier import CustomClassifier
from io import BytesIO
from graphviz import Digraph
import ast
from sympy import dotprint, simplify, parse_expr
from explain.actions.utils import plot_tree
from explain.actions.utils import get_models, feature_to_name, map_strings
import time

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
    models = get_models(conversation)
    # compose the return string
    return_string = f"The number of operators in each model is"
    for model in models:
        return_string += "<br>"
        return_string += f'model <b>{str(model.id+1)}</b>) '
        return_string += str(model.numOperators())
    # return the string and 1, indicating success
    return return_string, 1

def get_ops_operation(conversation, parse_text, i, **kwargs):
    """Gives the operations"""
    # get operatos of each model
    models = get_models(conversation)
    # compose the return string
    return_string = f"The operators in each model is"
    for model in models:
        return_string += "<br>"
        return_string += f'model <b>{str(model.id+1)}</b>) '
        return_string += str(model.getOperators())
    # return the string and 1, indicating success
    return return_string, 1

def num_nodes_operation(conversation, parse_text, i, **kwargs):
    """Gives the number of nodes"""
    # get operatos values of each model
    models = get_models(conversation)
    return_string = f"The number of nodes in each model is"
    for model in models:
        return_string += "<br>"
        return_string += f'model <b>{str(model.id+1)}</b>) '
        return_string += str(model.numNodes())
    # compose the return string
    # return the string and 1, indicating success
    return return_string, 1

def get_features_operation(conversation, parse_text, i, **kwargs):
    """Gives the features"""
    # get operatos of each model
    models = get_models(conversation)
    features = []
    for model in models:
        features.append(model.getFeatures())
    # compose the return string
    features_names = []
    for feature in features:
        feats = []
        for feat in feature:
            feats.append(feature_to_name(conversation, feat))
        features_names.append(feats)
    return_string = f"The features in each model are {features_names}"
    # return the string and 1, indicating success
    return return_string, 1
    
def num_features_operation(conversation, parse_text, i, **kwargs):
    """Gives the number of features"""
    # get operatos of each model
    models = get_models(conversation)
    # compose the return string
    return_string = f"The features in each model are"
    for model in models:
        return_string += "<br>"
        return_string += f'model <b>{str(model.id+1)}</b>) '
        return_string += str(model.numFeatures())

    # return the string and 1, indicating success
    return return_string, 1

def most_common_features_operation(conversation, parse_text, i, **kwargs):
    models = get_models(conversation)
    features = []
    for model in models:
        features.append(model.getFeatures())
    
    features_count = {}
    for feature_set in features:
        for feature in feature_set:
            feature = feature_to_name(conversation, feature)
            features_count[feature] = features_count.get(feature, 0) + 1
    features_count = sorted(features_count.items(), key=lambda x:x[1], reverse=True)
    return_string = f"Most common features are {features_count}"
    return return_string, 1
    

def get_expr_operation(conversation, parse_text, i, **kwargs):
    """Gives the expressions of each model"""
    # get operatos of each model
    print("parse_text", parse_text)
    models = get_models(conversation)
    expressions = []
    return_string = f"The expressions off each model are:"
    return_string += "<br><br>"
    features = set()
    for i, model in enumerate(models):
        return_string += f'model <b>{str(model.id+1)}</b>) '
        print("expr", model.expr)
        mapped_string = map_strings(conversation, str(model.expr))
        return_string += mapped_string
        return_string += "<br><br>"
        features.update(model.getFeatures())
    print("features", features)
    # return_string += "<br><br>"
    # return_string += "The following are the mapping of the variables"
    # for feature in features:
    #     return_string += "<br><br>"
    #     name = feature_to_name(conversation, feature)
    #     return_string += f"{feature} = {name}"
    
        # expressions.append(model.getExpr())
    # compose the return string
    # return_string = f"The features in each model are {expressions}"
    # return the string and 1, indicating success
    
    return return_string, 1

def plot_operation(conversation, parse_text, i, **kwargs):
    # return_string = '<img src="https://upload.wikimedia.org/wikipedia/commons/7/70/2005-bandipur-tusker.jpg" alt="Girl in a jacket" width="500" height="600">'
    models = get_models(conversation)
    x = []
    y = []
    expr = "(57.700000/ (x10+1e-6))"
    classifier = CustomClassifier(expr, 5, 6)
    print(classifier.accuracy)
    data = conversation.temp_dataset.contents['X']
    y_true = conversation.temp_dataset.contents['y']
    plot_colors = ['hotpink','darkviolet','mediumblue']
    explain_string = ""
    colors = ["red", "blue", "green", "magenta", "cyan", "black", "yellow", "darkred", "lime", "indigo", "grey", "pink"]
    print(colors)
    plot_colors = []
    for i, model in enumerate(models):
        color = colors[i%len(colors)]
        plot_colors.append(color)
        y_pred = model.predict(data)
        print("model number:", model.id)
        score = conversation.describe.get_score_text(y_true,y_pred,'mse',conversation.rounding_precision,'', True)
        score = float(score)
        x.append(score)
        y.append(model.complexity)
        explain_string += f'<p style="color:{color};">{model.id+1}) {str(model.expr)}</p>'
    plt.scatter(x, y, c=plot_colors, alpha=0.5) 
    plt.xlabel("Accurracy (MSE)")
    plt.ylabel("Complexity (size)")
    timestamp = int(time.time())
    plt.savefig(os.path.join('static', 'images', f'plot{timestamp}.png'))
    plt.close()
    # render = render_template('matplotlib-plot1.html') 
    # return_string = "<img src='{{ url_for('static', filename='istatic/images/plot.png') }}'>"
    return_string = f'<img src="static/images/plot{timestamp}.png" alt="drawing" width="400"/>'
    return_string += explain_string
    return return_string, 1

# def most_common_features_operation(conversation, parse_text, i, **kwargs):
#     models = conversation.get_var('models').contents
#     for model in models:
#         model.getFeatures()

#     return "kloenk", 1

def plot_tree_operation(conversation, parse_text, i, **kwargs):
    # return_string = '<img src="https://upload.wikimedia.org/wikipedia/commons/7/70/2005-bandipur-tusker.jpg" alt="Girl in a jacket" width="500" height="600">'
    models = get_models(conversation)
    model = models[0]
    # return_string = ""
    # for model in models:
    #     tree_text, i = plot_tree(conversation, parse_text, i, model, **kwargs)
    #     return_string += tree_text

    # model = models[0]
    # return return_string, 1
    return plot_tree(conversation, parse_text, i, model, **kwargs)

def most_common_trees_operation(conversation, parse_text, i, **kwargs):
    models = get_models(conversation)
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
                # print("sym:", symExpr, "key:", key)
                if simplify(key - symExpr) == 0:
                    subDic[key] = subDic.get(key, 0) + 1
                    found = True
                    break
        if not found:
            subDic[symExpr] = subDic.get(symExpr, 0) + 1
    subDic = sorted(subDic.items(), key=lambda x:x[1], reverse=True)
    return_string = f"Most common subtrees are {subDic}"
    return return_string, 1