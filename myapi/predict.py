import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

from myapi.analytics import get_sentiment


def regression_preprocessing(data):
    flatten_data = []
    for entry in data:
        flat_entry = {}
        flat_entry.update(entry["person"])

        if entry["closest_weather"] is not None:
            flat_entry.update(entry["closest_weather"])
        else:
            flat_entry.update({
                "temp_c": None,
                "precip_mm": None,
                "humidity": None,
            })

        if entry["closest_noise_station"] is not None:
            flat_entry.update(entry["closest_noise_station"])
        else:
            flat_entry.update({
                "noise": None
            })
        flat_entry["sleep_duration"] = entry["sleep_duration"]
        flat_entry["sleep_comment"] = get_sentiment(entry["sleep_comment"])
        flat_entry["sleep_score"] = entry["sleep_score"]

        flatten_data.append(flat_entry)

    df = pd.DataFrame(flatten_data)
    # df.to_json('preprocessed_data.json', orient='records')
    df['sex'] = df['sex'].map({'Male': 0, 'Female': 1})
    df['condition_text'] = LabelEncoder().fit_transform(df['condition_text'])

    categorical_variables = df.select_dtypes(include=['object']).columns
    for col in categorical_variables:
        mode = df[col].mode().iloc[0]
        mode_first = mode.split()[0]
        df.fillna({col: mode_first}, inplace=True)

    numeric_variables = df.select_dtypes(include=['int', 'float']).columns
    for col in numeric_variables:
        mean = df[col].mean()
        df.fillna({col: mean}, inplace=True)

    X = df.drop(columns=['sleep_score', 'person_id'])
    y = df['sleep_score']

    return X, y


def linear(data):
    X, y = regression_preprocessing(data)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LinearRegression()
    model.fit(X_train_scaled, y_train)

    # Make predictions
    y_pred = model.predict(X_test_scaled)
    y_test = np.array(y_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    equation = f"y = {model.intercept_:.2f}"
    for i, coef in enumerate(model.coef_):
        equation += f" + {coef:.2f}·X{i + 1}"

    model_summary = {
        'equation': equation,
        'intercept': model.intercept_,
    }

    return {
        'model': model,
        'Summary': model_summary,
        'MSE': mse,
        'R2': r2,
        'MAE': mae
    }
