import ast
import os
from graphviz import Digraph

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

def plot_tree_operation(conversation, parse_text, i, model, **kwargs):
    # return_string = '<img src="https://upload.wikimedia.org/wikipedia/commons/7/70/2005-bandipur-tusker.jpg" alt="Girl in a jacket" width="500" height="600">'
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

def modification_operation(conversation, parse_text, i, **kwargs):
    models = conversation.get_var('models').contents
    model = models[0]
    astModel = model.ast
    operation = parse_text[i]
    node = parse_text[i+1]
    print("here", operation, node)
    if operation == "deletenode":
        deleter = MyRemover(node)
        newTree = ast.fix_missing_locations(deleter.visit(astModel))
        print(model.expression)
        models[0] = model.changeModel(ast.unparse(newTree))
        print(model.expression)
        conversation.add_var('models', models, 'model')
    if operation == "modnode":
        nodeType = parse_text[i+2]

    return_string = f"The model is changed"
    return plot_tree_operation(conversation, parse_text, i, model, **kwargs)


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
        node = super().visit(node)
        # If we have a valid node (ie. node not being removed)
        if isinstance(node, ast.AST):
            # update the parent, since this may have been transformed 
            # to a different node by super
            self.parent = node.parent
        return node

    def generic_visit(self, node):
        result = super().generic_visit(node)
        
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