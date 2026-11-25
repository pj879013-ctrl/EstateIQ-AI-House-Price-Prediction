
import pandas as pd
import numpy as np
import json

# 1. Load dataset
data = pd.read_csv("dataset/house_data.csv")

print("Dataset loaded successfully!")
print("Dataset shape:", data.shape)

# 2. Prepare features and target
X = data[["Area", "Bedrooms", "Bathrooms", "Age"]].to_numpy(dtype=float)
y = data["Price"].to_numpy(dtype=float)

# 3. Split dataset into training and testing sets
np.random.seed(42)

indices = np.random.permutation(len(X))
test_size = max(1, int(len(X) * 0.2))

test_indices = indices[:test_size]
train_indices = indices[test_size:]

X_train = X[train_indices]
y_train = y[train_indices]

X_test = X[test_indices]
y_test = y[test_indices]


# 4. Linear Regression training function
def train_linear_regression(X_data, y_data):

    X_intercept = np.column_stack(
        (np.ones(len(X_data)), X_data)
    )

    coefficients, _, _, _ = np.linalg.lstsq(
        X_intercept, y_data, rcond=None
    )

    return coefficients


# 5. Train using training data
test_coefficients = train_linear_regression(
    X_train, y_train
)

# 6. Evaluate on unseen test data
X_test_intercept = np.column_stack(
    (np.ones(len(X_test)), X_test)
)

test_predictions = X_test_intercept @ test_coefficients

mae = np.mean(np.abs(y_test - test_predictions))

ss_total = np.sum((y_test - np.mean(y_test)) ** 2)
ss_residual = np.sum((y_test - test_predictions) ** 2)

r2 = (
    1 - ss_residual / ss_total
    if ss_total != 0 else None
)

print("\nMODEL EVALUATION")
print("-------------------------")
print("Training records:", len(X_train))
print("Testing records:", len(X_test))
print("Test MAE:", round(mae, 2))
print("Test R2 Score:", round(r2, 4) if r2 is not None else "Undefined")


# 7. Train final model using all available records
final_coefficients = train_linear_regression(X, y)

# 8. Save model and evaluation metrics
model = {
    "algorithm": "Linear Regression",
    "features": ["Area", "Bedrooms", "Bathrooms", "Age"],
    "intercept": float(final_coefficients[0]),
    "coefficients": [
        float(value) for value in final_coefficients[1:]
    ],
    "evaluation": {
        "test_mae": float(mae),
        "test_r2": float(r2) if r2 is not None else None,
        "training_records": int(len(X_train)),
        "testing_records": int(len(X_test)),
        "total_records": int(len(X))
    }
}

with open("models/house_price_model.json", "w") as file:
    json.dump(model, file, indent=4)

print("\nFinal model trained on all records.")
print("Model saved successfully!")
