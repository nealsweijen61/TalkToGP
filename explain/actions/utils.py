"""Util functions."""
import numpy as np
from sklearn.tree import _tree
import os
from graphviz import Digraph
import time
import ast

from explain.conversation import Conversation


def gen_parse_op_text(conversation):
    """Generates a piece of text summarizing the parse operation.

    Note that the first term in the parse op list is supposed to be an and or or
    which is stripped off here to make formatting that list in the operations easier.
    """
    ret_text = ""
    conv_parse_ops = conversation.parse_operation
    for i in range(1, len(conv_parse_ops)):
        ret_text += conv_parse_ops[i] + " "
    ret_text = ret_text[:-1]
    return ret_text


def convert_categorical_bools(data):
    if data == 'true':
        return 1
    elif data == 'false':
        return 0
    else:
        return data


def get_parse_filter_text(conversation: Conversation):
    """Gets the starting parse text."""
    parse_op = gen_parse_op_text(conversation)
    if len(parse_op) > 0:
        intro_text = f"For the data with <b>{parse_op}</b>,"
    else:
        intro_text = "For <b>all</b> the instances in the data,"
    return intro_text


def get_rules(tree, feature_names, class_names):
    # modified from https://mljar.com/blog/extract-rules-decision-tree/
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]

    paths = []
    path = []

    def recurse(node, path, paths):

        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            p1, p2 = list(path), list(path)
            p1 += [f"({name} <= {np.round(threshold, 3)})"]
            recurse(tree_.children_left[node], p1, paths)
            p2 += [f"({name} > {np.round(threshold, 3)})"]
            recurse(tree_.children_right[node], p2, paths)
        else:
            path += [(tree_.value[node], tree_.n_node_samples[node])]
            paths += [path]

    recurse(0, path, paths)

    # sort by samples count
    samples_count = [p[-1][1] for p in paths]
    ii = list(np.argsort(samples_count))
    paths = [paths[i] for i in reversed(ii)]

    rules = []
    for path in paths:
        incorrect_class = False

        rule = "if "

        for p in path[:-1]:
            if rule != "if ":
                rule += " and "
            rule += "<b>" + str(p) + "</b>"
        rule += " then "
        if class_names is None:
            rule += "response: " + str(np.round(path[-1][0][0][0], 3))
        else:
            classes = path[-1][0][0]
            largest = np.argmax(classes)
            if class_names[largest] == "incorrect":
                incorrect_class = True
            rule += f"then the model is incorrect <em>{np.round(100.0 * classes[largest] / np.sum(classes), 2)}%</em>"
        rule += f" over <em>{path[-1][1]:,}</em> samples"

        if incorrect_class:
            rules += [rule]
    return rules


def get_second_child_name(node):
    for i, child in enumerate(ast.iter_child_nodes(node)):
        if i == 1:
            return str(child.__class__.__name__)

def create_ast_graph(graph, node, parent_name, index='', num=-1):
    current_name = f'{parent_name}_{index}' if parent_name else 'Root'
    num += 1
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

def plot_tree(conversation, parse_text, i, model, **kwargs):
    # return_string = '<img src="https://upload.wikimedia.org/wikipedia/commons/7/70/2005-bandipur-tusker.jpg" alt="Girl in a jacket" width="500" height="600">'
    expr = ast.parse(str(model.expr))

    graph = Digraph(comment='AST Tree')
    create_ast_graph(graph, expr, '')

    output_directory = 'static/images/'
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)
    # Set the output directory
    timestamp = int(time.time())
    output_file = os.path.join(output_directory, f"expression_tree+{timestamp}")

    # Render and save the graph
    graph.render(output_file, format='png', cleanup=True)
    return_string = f'<img src="static/images/expression_tree+{timestamp}.png" alt="drawing" width="400"/>'
    return return_string, 1

def get_models(conversation):
    # get operatos of each model
    if conversation.temp_select == None:
        conversation.build_temp_select()
    models = conversation.temp_select.contents
    if len(conversation.temp_select.contents) == 0:
        return None
    return models