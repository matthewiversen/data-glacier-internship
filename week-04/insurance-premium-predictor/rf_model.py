# Importing the libraries
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import pickle

# read data
data = pd.read_csv("insurance.csv")

# encode
sex_enc = LabelEncoder()
smoke_enc = LabelEncoder()
reg_enc = LabelEncoder()
data["sex"] = sex_enc.fit_transform(data["sex"])
data["smoker"] = smoke_enc.fit_transform(data["smoker"])
data["region"] = reg_enc.fit_transform(data["region"])

# splitting columns
X, y = data[data.columns[:-1]], data[data.columns[-1]]

# fit the model
rf_model = RandomForestRegressor()
rf_model.fit(X, y)

# saving model and encoders
pickle.dump(rf_model, open("rf_model.pkl", "wb"))
pickle.dump(sex_enc, open("sex_enc.pkl", "wb"))
pickle.dump(smoke_enc, open("smoke_enc.pkl", "wb"))
pickle.dump(reg_enc, open("reg_enc.pkl", "wb"))
