import pickle
import array as arr

def load_sklearn_model(filepath):
    """Loads a sklearn model."""
    with open(filepath, 'rb') as file:
        model = pickle.load(file)
    return model


model = load_sklearn_model("bikes_gp_5.pkl")
print("COmplex", model.getComplexity())
print(model)
# X = [[1,0,1,0,6,0,2,0.344167,0.363625,0.805833,0.160446]]
# print(X[0][0])
X = [[3,0,7,0,6,0,1,0.686667,0.638263,0.585,0.208342]]
# X = [[3,0,7,0,6,0,1,0.686667,0.638263,0.585,0.208342]]
# X = X.reshape(-1, 1)
pred = model.predict(X)
print(pred)
# predProb = model.predict_proba(X)
# print(pred, predProb)
