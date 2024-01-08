import pickle
import array as arr

def load_sklearn_model(filepath):
    """Loads a sklearn model."""
    with open(filepath, 'rb') as file:
        model = pickle.load(file)
    return model

if __name__ == '__main__':
    model = load_sklearn_model("bikes_model_linear_regression.pkl")
    print(model)
    X = [[1,0,1,0,6,0,2,0.344167,0.363625,0.805833,0.160446]]
    # X = X.reshape(-1, 1)
    pred = model.predict(X)
    predProb = model.predict_proba(X)
    # print(pred, predProb)
