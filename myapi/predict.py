import pandas as pd
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix


def svm_preprocessing(data):
    flatten_data = []
    for entry in data:
        flat_entry = {}
        flat_entry.update(entry["person"])
        flat_entry["average_sentiment"] = entry["opinion_analytics"]["average_sentiment"]
        flat_entry.update(entry["environment"])
        flat_entry["average_score"] = entry["average_score"]
        flatten_data.append(flat_entry)

    # Convert to DataFrame
    df = pd.DataFrame(flatten_data)

    df['sex'] = df['sex'].map({'Male': 0, 'Female': 1})

    # Split into features and target variable
    X = df.drop(columns=['person_id', 'average_score'])
    y = df['average_score']

    return X, y


def svm(data):
    X, y = svm_preprocessing(data)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Initialize and train the SVM regression model
    svm_model = SVR(kernel='rbf')  # Radial Basis Function (RBF) kernel
    svm_model.fit(X_train_scaled, y_train)

    # Make predictions
    y_pred = svm_model.predict(X_test_scaled)

    # Calculate accuracy
    acc = accuracy_score(y_test, y_pred)

    # Generate confusion matrix
    matrix = confusion_matrix(y_test, y_pred)

    return svm_model, acc, matrix
