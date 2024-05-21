from sklearn.base import BaseEstimator, RegressorMixin
from sympy import symbols, lambdify, parse_expr, count_ops, simplify, preorder_traversal, Function, Pow, Mod, Number
import numpy as np
import pandas as pd
import ast


class GpModel(BaseEstimator, RegressorMixin):

    def __init__(self, expression, accuracy, complexity, id=0, explain=False):
        super().__init__()
        self.id = id

        self.expression = expression

        self.oldExpression = expression

        self.accuracy = accuracy

        self.explain = explain

        self.symbols = symbols('x0 x1 x2 x3 x4 x5 x6 x7')
        if explain:
            self.symbols = symbols('x0 x1 x2 x3 x4 x5 x6 x7 x8')

        self.expr = parse_expr(expression, evaluate=False)

        self.func = lambdify(self.symbols, self.expr, 'numpy')

        self.complexity = complexity
        self.complexity = self.numNodes()

        self.ast = ast.parse(str(self.expr))
        self.subtrees = []
        self.getSubTrees(self.ast)

    def reInit(self):
        print("reinit", self.expression)
        self.expr = parse_expr(self.expression, evaluate=False)
        self.ast = ast.parse(str(self.expr))
    
    def count_nodes(self, node):
        return sum(1 for _ in ast.walk(node))
    
    def getSubTrees(self, node):
        if isinstance(node, ast.Module) or isinstance(node, ast.Expr) or self.count_nodes(node) < 3:
            for child_node in ast.iter_child_nodes(node):
                self.getSubTrees(child_node)
        else:
            self.subtrees.append(ast.unparse(node))
            for child_node in ast.iter_child_nodes(node):
                self.getSubTrees(child_node)

    def fit(self, X, y=None):
        pass

    def predict(self, X, y=None):
        if isinstance(X, pd.DataFrame):
            X = X.values  # Convert DataFrame to NumPy array

        preds = np.empty(len(X), dtype=float)
        for i, x in enumerate(X):
            pred = self.func(*x)
            preds[i] = pred
        return preds

    def numOperators(self):
        return count_ops(self.expr)
    
    def getOperators(self):
        return count_ops(self.expr,visual=True).free_symbols 
    
    def numNodes(self):
        exlcude_values = [1e-6]
        print((1 for node in preorder_traversal(self.expr) if node not in exlcude_values))
        return sum(1 for node in preorder_traversal(self.expr) if node not in exlcude_values)

    def getFeatures(self):
        return self.expr.free_symbols

    def numFeatures(self):
        return len(self.expr.free_symbols)
    
    def getExpr(self):
        return self.expr
    
    def numConstants(self):
        return sum(1 for node in preorder_traversal(self.expr) if isinstance(node, Number))

    def getAccuracy(self):
        return self.accuracy

    def getComplexity(self):
        return self.complexity
    
    def changeModel(self, expression):
        self.expression = expression

        print("GP model expression:", self.expression)
        self.expr = parse_expr(expression, evaluate=False)

        self.func = lambdify(self.symbols, self.expr, 'numpy')

        self.complexity = self.numNodes()
        self.ast = ast.parse(str(self.expr))
        self.subtrees = []
        self.getSubTrees(self.ast)
        print("changing")
        return self
    
    def getSimplify(self):
        # self.expression = simplify(self.expression)
        self.expr = simplify(self.expr)
    
        self.func = lambdify(self.symbols, self.expr, 'numpy')
        self.complexity = self.numNodes()
        self.ast = ast.parse(str(self.expr))
        self.subtrees = []
        self.getSubTrees(self.ast)