import pandas as pd
import os
from django.conf import settings

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor

from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


def train_models(selected_model=None):
    file_path = os.path.join(settings.BASE_DIR, "admission_app", "data", "admission_data.csv")
    data = pd.read_csv(file_path)

    data.columns = data.columns.str.strip()
    data.columns = data.columns.str.replace(" ", "_")

    X = data[[
        "GRE_Score",
        "TOEFL_Score",
        "CGPA",
        "SOP",
        "LOR",
        "Research"
    ]]

    y = data["Chance_of_Admit"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    all_models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(),
        "Random Forest": RandomForestRegressor(),
        "SVR": SVR(),
        "KNN": KNeighborsRegressor()
    }

    results = {}

    for name, model in all_models.items():
        if selected_model and name != selected_model:
            continue

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        results[name] = {
            "model": model,
            "r2": r2_score(y_test, y_pred),
            "mse": mean_squared_error(y_test, y_pred),
            "mae": mean_absolute_error(y_test, y_pred)
        }

    return results