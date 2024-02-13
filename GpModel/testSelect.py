import pickle
import os

def load_sklearn_model(filepath):
    """Loads a sklearn model."""
    with open(filepath, 'rb') as file:
        model = pickle.load(file)
    return model


def filter_dataset(dataset, bools):
    """Selects x and y of dataset by booleans."""
    dataset = dataset[bools]
    return dataset

folderpath = "./data/models"
files = os.listdir(folderpath)
models = []

for file in files:
    filepath = os.path.join(folderpath, file)
    if filepath.endswith('.pkl'):
        model = load_sklearn_model(filepath)
        models.append(model)

bool_list = [model.numOperators() > 3 for model in models]
models = [model for model in models if model.numOperators() > 3]
print(models)
# filter_dataset(models, bool_list)



