from data.customClassifier import CustomClassifier
from data.gpModel import GpModel
import pickle as pkl
import cloudpickle

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    expr = "(1.000000*x0) "
    expr1 = "(1.000000*(x0/x10))"
    expr2 ="(ln(x0)*(x0+x0))"
    expr3 ="(x0*ln(x0))"
    expr4 ="(((x0+x0)*ln((x9*x0))))"
    expr5 ="(x0*(x1+(ln(x0)+x9)))"
    expr6 ="((x0/x10)/x10)"
    expr7 ="(sqrt(sqrt(x0))*(x0+x0))"
    expr8 ="(((x0+(x8*x0))+x3)*ln(x0))"
    expr9 ="((((x0+x3)*ln(x0))*((x9/x10)+x9))/abs(cos(cos(x2))))"
    expr10 ="((((x0+x3)*ln(x0))*((x8/x10)+x9))/cos(cos(x2)))"
    expr11 ="(((abs((sqrt(sin(x9))+((x5+x6)/sqrt(x0))))+(x9-x10))+((x9+x8)+cos(x2)))*((((x0+x3)+(x0/x10))+((x0+x5)+(x5*x5)))/cos(sin(ln(x0)))))"
    expr12 ="((((x0+x5)*ln(x0))*((x9/x10)+cos(x2)))-((((((x9*x3)+(x1+x7))+((((x3/x9)+(((sqrt(x0)/(x7-x10))/abs(cos(x1)))*(sin(sqrt(x3))/x9)))/ln(sin(x7)))+((ln(x10)*(x5+x0))-((((sqrt(x0)/(x7-x10))/abs(cos(x1)))*(sin(sqrt(x3))/x9))+(((sqrt(x0)/(x7-x10))/abs(cos(x1)))*(sin(sqrt(x3))/x9))))))/abs(((x7/x7)-(x8-x2))))+(x5-x5))+((x3*x3)/(x1/x3))))"
  
    # expr = "((((x1+x9)+41.432000)/ ((x10/ (x2+1e-6) )+1e-6) )+(x8+x8))"
    # expr2 = "(57.700000/ (x10+1e-6))"
    # expr3 = "x0*(x8+x8)"
    # expr4 = "((21.783000*56.278000)*x0)"
    # expr5 = "(((x1+(2.793000*x8))*(57.470000*(32.096000+x2)))+(((36.191000/ (x6+1e-6) )+(x0-19.821000))*((x4+x2)*4.235000)))"
    # expr6 = "(0.000000+(1.000000*((ln((x0+x0+1e-6))*x0)/cos(sin(ln(x3+1e-6)))+1e-6)))"
    # expr = "((((x1+x3)+41.432000)/ ((x5/ (x2+1e-6) )+1e-6) )+(x7+x7))"
    # expr2 = "(57.700000/ (x5+1e-6))"
    # expr3 = "x0*(x7+x7)"
    # expr4 = "((21.783000*56.278000)*x0)"
    # expr5 = "(((x1+(2.793000*x7))*(57.470000*(32.096000+x2)))+(((36.191000/ (x6+1e-6) )+(x0-19.821000))*((x4+x2)*4.235000)))"
    # expr6 = "(0.000000+(1.000000*((ln((x0+x0+1e-6))*x0)/cos(sin(ln(x3+1e-6)))+1e-6)))"
    expressions = []
    # expressions.append([expr, 911789, 15])
    # expressions.append([expr2, 2.06328e+07, 4])
    # expressions.append([expr3, 2.37852e+07, 1])
    # expressions.append([expr4, 5.9193e+06, 5])
    # expressions.append([expr5, 750528, 24])
    # expressions.append([expr6, 3230261, 15])
    expressions.append([expr, 911789, 15])
    expressions.append([expr2, 2.06328e+07, 4])
    expressions.append([expr3, 2.37852e+07, 1])
    expressions.append([expr4, 5.9193e+06, 5])
    expressions.append([expr5, 750528, 24])
    expressions.append([expr6, 3230261, 15])
    expressions.append([expr7, 911789, 15])
    expressions.append([expr8, 2.06328e+07, 4])
    expressions.append([expr9, 2.37852e+07, 1])
    expressions.append([expr10, 5.9193e+06, 5])
    expressions.append([expr11, 750528, 24])
    expressions.append([expr12, 3230261, 15])
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