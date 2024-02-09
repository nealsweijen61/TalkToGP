import ast
from explain.actions.utils import plot_tree

def modification_operation(conversation, parse_text, i, **kwargs):
    models = conversation.get_var('models').contents
    model = models[0]
    astModel = model.ast
    print(astModel)
    operation = parse_text[i]
    node = parse_text[i+1]
    print("here", operation, node, model.expression)
    if operation == "nodedelete":
        newTree = ast.fix_missing_locations(MyRemover(int(node)).visit(astModel))
        normal =  ast.unparse(newTree)
        model.changeModel(normal)
        print("output:", model.expression)
        # models[0] = model
        # conversation.add_var('models', models, 'model')
    if operation == "nodemod":
        expression = ""
        for term in parse_text[i+2:]:
            print(term)
            if term == "and" or term == "or" or term == "[e]":
                break
            expression += term
        print(expression)
        astExpression = ast.parse(expression)
        newTree = ast.fix_missing_locations(MyRemover(int(node), astExpression).visit(astModel))
        normal =  ast.unparse(newTree)
        normal = normal.replace('\n', '')
        print("normal:", normal)
        model.changeModel(normal)
        print("output:", model.expression)


    return_string = f"The model is changed"
    return plot_tree(conversation, parse_text, i, model, **kwargs)
    # return return_string, 1


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