from data.customClassifier import CustomClassifier
from data.gpModel import GpModel
import pickle as pkl
import cloudpickle

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    expr = "(1.000000*x3)"
    expr2 = "(1.000000*(x1*x3))"
    expr3 = "(1.000000*((x1*abs(x0))*x1))"
    expr4 = "((x1*x7)/abs(((abs(x5)+(x1+x6))/(abs(x1)*(x6*x0)))))"
    expr5 = "((x1*(x7*x1))*x1)"
    expr6 = "(((x1+(sqrt(x1)/x7))*x7)/abs(((abs(x5)+(x1+x6))/(abs(x1)*(x6*x0)))))"
    # expr = "((((x1+x3)+41.432000)/ ((x5/ (x2+1e-6) )+1e-6) )+(x7+x7))"
    # expr2 = "(57.700000/ (x5+1e-6))"
    # expr3 = "x0*(x7+x7)"
    # expr4 = "((21.783000*56.278000)*x0)"
    # expr5 = "(((x1+(2.793000*x7))*(57.470000*(32.096000+x2)))+(((36.191000/ (x6+1e-6) )+(x0-19.821000))*((x4+x2)*4.235000)))"
    # expr6 = "(0.000000+(1.000000*((ln((x0+x0+1e-6))*x0)/cos(sin(ln(x3+1e-6)))+1e-6)))"
    expressions = []
    expressions.append([expr, 45376929792, 15])
    expressions.append([expr2, 20401788928, 4])
    expressions.append([expr3, 10064391168, 1])
    expressions.append([expr4, 3329543680, 5])
    expressions.append([expr5, 4784167424, 24])
    expressions.append([expr6, 3211574528, 15])
    # expressions.append([expr6, 3211574528, 15])
    # expressions.append([expr, 911789, 15])
    # expressions.append([expr2, 2.06328e+07, 4])
    # expressions.append([expr3, 2.37852e+07, 1])
    # expressions.append([expr4, 5.9193e+06, 5])
    # expressions.append([expr5, 750528, 24])
    # expressions.append([expr6, 3230261, 15])
    # expressions.append([expr7, 911789, 15])
    # expressions.append([expr8, 2.06328e+07, 4])
    # expressions.append([expr9, 2.37852e+07, 1])
    # expressions.append([expr10, 5.9193e+06, 5])
    # expressions.append([expr11, 750528, 24])
    # expressions.append([expr12, 3230261, 15])
    count = 0
    for expression in expressions:
        count += 1
        classifier = GpModel(expression=expression[0], accuracy=expression[1], complexity=expression[2])
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
