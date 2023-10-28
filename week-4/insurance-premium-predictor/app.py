import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import pickle

app = Flask(__name__)
rf_model = pickle.load(open("rf_model.pkl", "rb"))
sex_enc = pickle.load(open("sex_enc.pkl", "rb"))
smoke_enc = pickle.load(open("smoke_enc.pkl", "rb"))
reg_enc = pickle.load(open("reg_enc.pkl", "rb"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    """
    For rendering results on HTML GUI
    """
    # Get inputs
    age = int(request.form["age"])
    sex = request.form["sex"]
    bmi = float(request.form["bmi"])
    children = int(request.form["children"])
    smoker = request.form["smoker"]
    region = request.form["region"]

    # Encode categorical variables
    sex = sex_enc.transform([sex])[0]
    smoker = smoke_enc.transform([smoker])[0]
    region = reg_enc.transform([region])[0]

    # Turn inputs into dataframe for prediction
    feature_vector = pd.DataFrame(
        [[age, sex, bmi, children, smoker, region]],
        columns=["age", "sex", "bmi", "children", "smoker", "region"],
    )

    # Make prediction
    prediction = rf_model.predict(feature_vector)[0]
    prediction = round(prediction, 2)

    return render_template(
        "index.html", prediction_text=f"Insurance premium predicted as ${prediction}"
    )


if __name__ == "__main__":
    app.run(debug=True)
