from data.customClassifier import CustomClassifier
from data.gpModel import GpModel
import pickle as pkl
import cloudpickle

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    expr = "(58.520000*59.715000)"
    expr2 = "((57.795000+((x1+x7)*58.646000))*40.257000)"
    expr3 = "((((38.145000*26.640000)-(x2*-56.715000))*((x1+x7)+sin(x6)))/ (sin(cos(cos(x10)))+1e-6) )"
    expr4 = "((50.720000*57.785000)/ (sin(cos(x1))+1e-6) )"
    expr5 = "((57.795000*(x0+53.218000))/ (cos(x1)+1e-6) )"
    expr6 = "((57.795000*((x1+x7)*58.462000))/ (cos(cos(x1))+1e-6) )"
    expr7 = "((((-48.589000*27.965000)/ (sin(-53.204000)+1e-6) )*sin((x1+x7)))*cos((x1/ (x0+1e-6) )))"
    expr8 = "((((-48.589000*27.965000)/ (sin(-53.204000)+1e-6) )*sin((x1+x7)))*cos((x1/ ((x0*x0)+1e-6) )))"
    expr9 = "((((-48.589000*27.965000)/ (sin(-53.204000)+1e-6) )*sin(x8))/ (cos(x1)+1e-6) )"
    expr10 = "((((-48.589000*26.640000)/ (sin(-53.204000)+1e-6) )*sin(x8))/ (sin(cos(x1))+1e-6) )"
    expr11 = "((((-48.589000*27.965000)/ (sin(-53.204000)+1e-6) )*sin((x1+x7)))*cos(((x1-x8)/ ((0.306000-x0)+1e-6) )))"
    expr12 = "((57.795000*56.798000)/ (cos(x1)+1e-6) )"
    expressions = []
    expressions.append([expr, 23706536, 15])
    expressions.append([expr2, 23670866, 4])
    expressions.append([expr3, 23210604, 1])
    expressions.append([expr4, 22548588, 5])
    expressions.append([expr5, 19459396, 24])
    expressions.append([expr6, 9721504, 15])
    expressions.append([expr7, 750528, 15])
    expressions.append([expr8, 699734, 15])
    expressions.append([expr9, 879670, 15])
    expressions.append([expr10, 774076, 15])
    expressions.append([expr11, 774076, 15])
    expressions.append([expr12, 774076, 15])
    

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
