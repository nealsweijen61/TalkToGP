import pickle
import array as arr

def load_sklearn_model(filepath):
    """Loads a sklearn model."""
    with open(filepath, 'rb') as file:
        model = pickle.load(file)
    return model

if __name__ == '__main__':
    model = load_sklearn_model("diabetes_model_grad_boosted_tree.pkl")
    print(model)
    X = [[51,1,101,50,15,36,24.2,26], [27,0,85,66,5,140,19.2,21]]
    # X = X.reshape(-1, 1)
    pred = model.predict(X)
    predProb = model.predict_proba(X)
    print(pred, predProb)
