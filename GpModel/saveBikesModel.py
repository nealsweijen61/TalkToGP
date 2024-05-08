from data.customClassifier import CustomClassifier
from data.gpModel import GpModel
import pickle as pkl
import cloudpickle

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    expr = "(0.000000+(1.000000*x4))"
    expr2 = "(1.000000*abs(x2))"
    expr3 = "(1.000000*(x2*x2))"
    expr4 = "(x2/(1e-6+cos(x2)))"
    expr5 = "((x2*x2)*x2)"
    expr6 = "abs(((x2*x2)/(1e-6+ln(1e-6+sin(sqrt(x0))))))"
    expr7 = "(((x1+(2.793000*x8))*(57.470000*(32.096000+x2)))+(((36.191000/ (x6+1e-6) )+(x0-19.821000))*((x4+x2)*4.235000)))"
    expr8 = "((((54.204000*x8)+(x0*10.456000))-(-41.819000*(x1+x7)))*(((x1-x6)*(x6*x6))--51.873000))"
    expr9 = "(((sqrt(x1)/ ((x6+0.185000)+1e-6) )+sqrt((x8*x0)))*((56.932000)**2))"
    expr10 = "(((ln(abs(x2))+(x1+x7))*(39.322000-(31.804000*-58.164000)))-((x6-(4.079000-x2))*((x6*10.594000)*(4.572000/ (x7+1e-6)))))"
    # expr = "((((x1+x3)+41.432000)/ ((x5/ (x2+1e-6) )+1e-6) )+(x7+x7))"
    # expr2 = "(57.700000/ (x5+1e-6))"
    # expr3 = "x0*(x7+x7)"
    # expr4 = "((21.783000*56.278000)*x0)"
    # expr5 = "(((x1+(2.793000*x7))*(57.470000*(32.096000+x2)))+(((36.191000/ (x6+1e-6) )+(x0-19.821000))*((x4+x2)*4.235000)))"
    # expr6 = "(0.000000+(1.000000*((ln((x0+x0+1e-6))*x0)/cos(sin(ln(x3+1e-6)))+1e-6)))"
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
