from data.customClassifier import CustomClassifier
from data.gpModel import GpModel
import ast

# expr = "((((x1+x9)+41.432000)/ ((x10/ (x2+1e-6) )+1e-6) )+(x8+x8))"
expr = "(57.700000/ (x10+1e-6))"
expr = "(57.700000/ (log(3)))"
expr3 = "x0*(x8+x8)"
classifier = GpModel(expr3, 5, 6)

print("class", classifier.expr)
classifier.getSimplify()
print("class", classifier.expr)
# X = [[3,0,7,0,6,0,1,0.686667,0.638263,0.585,0.208342]]
# res = classifier.predict(X)
res = classifier.ast
class MyVisitor(ast.NodeTransformer):
    def __init__(self, node_number):
        self.node_number = node_number
        self.index = 0

    def generic_visit(self, node):
        result = super().generic_visit(node)
        print(node.__class__.__name__, self.index)
        if not (isinstance(node, ast.Module) or isinstance(node, ast.Expr)):
            self.index += 1
        
        if self.node_number == self.index:
            return None
        return result


visitor = MyVisitor(2)
new = visitor.visit(res)
# print(res)