from sklearn.base import BaseEstimator, RegressorMixin
from sympy import symbols, lambdify, parse_expr, count_ops, preorder_traversal, Function, Pow, Mod, Number
import numpy as np
import pandas as pd


class CustomClassifier(BaseEstimator, RegressorMixin):

    def __init__(self, accuracy, expression, complexity, ben=0):
        super().__init__()
        self.expression = expression
        self.accuracy = accuracy
        self.ben = ben
        self.symbols = symbols('x0 x1 x2 x3 x4 x5 x6 x7 x8 x9 x10')

        self.expr = parse_expr(accuracy, evaluate=False)

        self.func = lambdify(self.symbols, self.expr, 'numpy')

        self.complexity = complexity

    def fit(self, X, y=None):
        pass

    def predict(self, X, y=None):
        if isinstance(X, pd.DataFrame):
            X = X.values  # Convert DataFrame to NumPy array

        preds = np.empty(len(X), dtype=float)
        for i, x in enumerate(X):
            pred = self.func(*x)
            print("pred", pred)
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
        return self.expression

    def getComplexity(self):
        return self.complexity
    
    def kloenker(self):
        return "klooooenmk"
    