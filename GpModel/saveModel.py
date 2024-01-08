from data.customClassifier import CustomClassifier
import pickle as pkl
import cloudpickle

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    expr = "((((x1+x9)+41.432000)/ ((x10/ (x2+1e-6) )+1e-6) )+(x8+x8))"
    classiefier = CustomClassifier(expr)
    with open("bikes_gp.pkl", "wb") as f:
        # pkl.dump(classiefier, f)
        cloudpickle.dump(classiefier, f)