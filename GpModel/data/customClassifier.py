from sklearn.base import BaseEstimator, RegressorMixin
from sympy import symbols, lambdify, parse_expr, count_ops
import numpy as np
import pandas as pd


class CustomClassifier(BaseEstimator, RegressorMixin):

    def __init__(self, expression):
        super().__init__()
        self.expression = expression

        self.symbols = symbols('x0 x1 x2 x3 x4 x5 x6 x7 x8 x9 x10')

        self.expr = parse_expr(expression)

        self.func = lambdify(self.symbols, self.expr, 'numpy')

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

    def operators(self):
        return count_ops(self.expr)

