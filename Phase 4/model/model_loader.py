import pickle

def load_model(model_path = 'model/final_model.pkl'):
    with open (model_path, 'rb') as f:
        model = pickle.load(f)
    return model