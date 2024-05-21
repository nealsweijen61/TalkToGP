from data.customClassifier import CustomClassifier
from data.gpModel import GpModel
import pickle as pkl
import cloudpickle

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    expr = "(128038.565000--65500.791000)"
    expr2 = "(90747.418000*sqrt(x7))"
    expr3 = "(87694.852000-(x7*-33431.155000))"
    expr4 = "((((x4*x2)+(x7*55966.764000))+16510.250000)*sin(cos(sin(x0))))"
    expr5 = "(((x3+(x7*55966.764000))+((88382.076000/ (x7+1e-6) )+x4))*sin(cos(sin(x0))))"
    expr6 = "((((x4*x2)+(x7*55966.764000))+((60840.333000/ (x7+1e-6) )+x4))*sin(cos(sin(x0))))"
    expr7 = "((38714.865000-6404.511000)+(x7*41230.930000))"
    expr8 = "((((x4*x2)+(x7*55966.764000))+((59111.773000/ (x7+1e-6) )+(x2*x2)))*sin(cos(sin(x0))))"
    expr9 = "((x0--62467.385000)-(x7*-33431.155000))"
    expr10 = "((((x6/ (x5+1e-6) )*139366.254000)-56759.704000)+(((42076.555000*x7)+x5)-(x2*(119829.645000/ (x0+1e-6) ))))"
    expr11 = "((((x6/ (x5+1e-6) )*139366.254000)-60222.572000)+(((42076.555000*x7)+(x6*x2))-(x2*(88422.150000/ (x0+1e-6) ))))"
    expr12 = "(((x3+(x7*55966.764000))+24423.635000)*sin(cos(sin(x0))))"
    expressions = []
    expressions.append([expr, 9.57798e+9, 15])
    expressions.append([expr2, 5.19642e+9, 4])
    expressions.append([expr3, 4.1584e+9, 1])
    expressions.append([expr4, 2.98372e+9, 5])
    expressions.append([expr5, 2.97052e+9, 24])
    expressions.append([expr6, 2.87533e+9, 15])
    expressions.append([expr7, 3.36917e+9, 15])
    expressions.append([expr8, 2.87311e+9, 4])
    expressions.append([expr9, 3.54174e+9, 1])
    expressions.append([expr10, 2.871e+9, 5])
    expressions.append([expr11, 2.80815e+9, 24])
    expressions.append([expr12, 3.11271e+9, 15])
    count = 0
    for expression in expressions:
        count += 1
        classifier = GpModel(expression=expression[0], accuracy=expression[1], complexity=expression[2], explain=False)
        print(classifier.expr)
        with open(f"bikes_gp_{count}.pkl", "wb") as f:
            # pkl.dump(classiefier, f)
            cloudpickle.dump(classifier, f)


    def load_sklearn_model(filepath):
        """Loads a sklearn model."""
        with open(filepath, 'rb') as file:
            model = pkl.load(file)
        return model


    model = load_sklearn_model("bikes_gp_6.pkl")
    model.reInit()


    print("expr", model.expr)
