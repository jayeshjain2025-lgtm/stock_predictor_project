from flask import Flask, request, jsonify
import pickle
import os
import pandas as pd

# ------------------------
# Paths & Load Model
# ------------------------
project_root = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(project_root, "model", "final_model.pkl")

# Load model + feature order
with open(model_path, "rb") as f:
    data = pickle.load(f)
model = data["model"]
feature_order = data["features"]

# ------------------------
# Flask setup
# ------------------------
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Stock Prediction API is running. Use POST /predict with JSON."

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or "features" not in data:
        return jsonify({"error": "Missing 'features' in JSON request."}), 400

    input_dict = data["features"]

    # Convert input to DataFrame in correct feature order
    try:
        # if input is a dict with feature names, align automatically
        if isinstance(input_dict, dict):
            df = pd.DataFrame([input_dict], columns=feature_order)
        else:  # if input is a list, assume correct order
            if len(input_dict) != len(feature_order):
                return jsonify({"error": f"Expected {len(feature_order)} features, got {len(input_dict)}."}), 400
            df = pd.DataFrame([input_dict], columns=feature_order)

        prediction = model.predict(df)[0]

    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

    return jsonify({
        "input": input_dict,
        "prediction": float(prediction)
    })

# ------------------------
# Run server
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)
