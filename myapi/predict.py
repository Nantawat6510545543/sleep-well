import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error


def svm_preprocessing(data):
    flatten_data = []
    for entry in data:
        flat_entry = {}
        flat_entry.update(entry["person"])

        if entry["opinion_analytics"] is not None:
            flat_entry["average_sentiment"] = entry["opinion_analytics"]["average_sentiment"]
        else:
            # Fill missing opinion_analytics data with default values or impute them
            flat_entry.update({
                "average_sentiment": 0
            })

        if entry["environment"] is not None:
            flat_entry.update(entry["environment"])
        else:
            # Fill missing environment data with default values or impute them
            flat_entry.update({
                "avg_temp_c": 0,
                "avg_precip_mm": 0,
                "avg_humidity": 0,
                "avg_noise": 0
            })

        flat_entry["average_score"] = entry["average_score"]
        flatten_data.append(flat_entry)

    # Convert to DataFrame
    df = pd.DataFrame(flatten_data)
    df = df[df['average_score'].notna()]

    df['sex'] = df['sex'].map({'Male': 0, 'Female': 1})

    imputer = SimpleImputer(strategy='mean')
    X_imputed = imputer.fit_transform(df.drop(columns=['average_score']))

    X = pd.DataFrame(X_imputed, columns=df.columns[:-1])
    y = df['average_score']

    return X, y


def svm(data):
    X, y = svm_preprocessing(data)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Initialize and train the SVM regression model
    svm_model = SVR(kernel='rbf')  # Radial Basis Function (RBF) kernel
    svm_model.fit(X_train_scaled, y_train)

    # Make predictions
    y_pred = svm_model.predict(X_test_scaled)
    y_test = np.array(y_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    model_summary = {
        'kernel': svm_model.kernel,
        'C': svm_model.C,
        'epsilon': svm_model.epsilon,
        'gamma': svm_model.gamma,
        'coef0': svm_model.coef0
    }

    return {
        'model': svm_model,
        'Summary': model_summary,
        'MSE': mse,
        'R2': r2,
        'MAE': mae
    }
