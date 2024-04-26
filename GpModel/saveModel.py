from data.customClassifier import CustomClassifier
from data.gpModel import GpModel
import pickle as pkl
import cloudpickle

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    expr = "((((x1+x9)+41.432000)/ ((x10/ (x2+1e-6) )+1e-6) )+(x8+x8))"
    expr2 = "(57.700000/ (x10+1e-6))"
    expr3 = "x0*(x8+x8)"
    expr4 = "((21.783000*56.278000)*x0)"
    expr5 = "(((x1+(2.793000*x8))*(57.470000*(32.096000+x2)))+(((36.191000/ (x6+1e-6) )+(x0-19.821000))*((x4+x2)*4.235000)))"
    expressions = []
    expressions.append([expr, 911789, 15])
    expressions.append([expr2, 2.06328e+07, 4])
    expressions.append([expr3, 2.37852e+07, 1])
    expressions.append([expr4, 5.9193e+06, 5])
    expressions.append([expr5, 750528, 24])
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


    model = load_sklearn_model("bikes_gp_3.pkl")
    model.reInit()

    print("expr", model.expr)

# 1| 2.06328e+07| 1.0875| 2.22577e+07| 1.0875(57.700000/ (x10+1e-6) )
# 2| 5.9193e+06| 1.97995| 2.16444e+06| 1.97995((21.783000*56.278000)*x0)
# 3| 1.41845e+06| 4.65733| 2.93308e+06| 4.65733(((x1+(2.793000*x7))*(57.470000*35.962000))+x0)
# 4| 1.04341e+06| 5.54978| 2.32299e+06| 5.54978(((x1+(2.793000*x8))*((x0+47.293000)*50.734000))+x0)
# 5| 3.77043e+06| 2.87241| 3.52486e+06| 2.87241(((38.549000+41.432000)*56.278000)+x0)
# 6| 2.11493e+06| 3.76487| 4.81936e+06| 3.76487((x8*((15.112000*16.375000)*35.962000))+x0)
# 7| 750528| 10.9045| 2.77997e+06| 10.9045(((x1+(2.793000*x8))*(57.470000*(32.096000+x2)))+(((36.191000/ (x6+1e-6) )+(x0-19.821000))*((x4+x2)*4.235000)))
# 8| 760526| 8.22715| 1.89853e+06| 8.22715(((x1+(2.793000*x8))*(57.470000*(32.096000+x4)))+(x0*((9.367000/ (x6+1e-6) )*48.456000)))
# 9| 777521| 7.3347| 2.03003e+06| 7.3347(((x1+(2.793000*x8))*(57.470000*35.962000))+(x0*((9.367000/ (x6+1e-6) )*44.424000)))
# 10| 911789| 6.44224| 2.33072e+06| 6.44224(((x1+(2.793000*x7))*(57.470000*35.962000))+(x0*(x2*31.978000)))