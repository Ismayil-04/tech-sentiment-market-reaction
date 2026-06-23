import os
import pandas as pd
import statsmodels.api as sm

data_path = "data/processed/master_regression_data.csv"
if not os.path.exists(data_path):
    raise FileNotFoundError()

df = pd.read_csv(data_path)

df["Abnormal_Return"] = df["Stock_Return"] - df["Market_Return"]
df = df.dropna(subset=["Abnormal_Return"])

df["Is_Negative"] = df["Is_Negative"].fillna(0)
df["Is_Positive"] = df["Is_Positive"].fillna(0)

X = df[["Is_Negative", "Is_Positive"]]
X = sm.add_constant(X)
Y = df["Abnormal_Return"]

model = sm.OLS(Y, X).fit()

print(model.summary())

if not os.path.exists("results"):
    os.makedirs("results")
    
with open("results/regression_report.txt", "w") as f:
    f.write(model.summary().as_text())