
import pandas as pd
import numpy as np
import json
import os

print("ESTATEIQ - INDIAN HOUSE PRICE MODEL")
print("=" * 45)

# 1. Load dataset
data = pd.read_csv("dataset/indian_house_prices.csv")

print("Dataset loaded:", data.shape)

# 2. Select useful features
numerical_features = [
    "BHK",
    "Size_sqft",
    "Property_Age",
    "Parking",
    "Metro_Distance_km",
    "School_Distance_km",
    "Hospital_Distance_km",
    "Location_Rating",
    "Amenities_Score"
]

categorical_features = [
    "City",
    "Locality",
    "Property_Type",
    "Furnishing_Status"
]

X = data[numerical_features + categorical_features].copy()
y = data["Price"].to_numpy(dtype=float)

# 3. Encode categorical variables
X = pd.get_dummies(
    X,
    columns=categorical_features,
    drop_first=True,
    dtype=float
)

feature_names = X.columns.tolist()
X = X.to_numpy(dtype=float)

# 4. Split dataset (80% training, 20% testing)
np.random.seed(42)

indices = np.random.permutation(len(X))
test_size = int(len(X) * 0.20)

test_indices = indices[:test_size]
train_indices = indices[test_size:]

X_train = X[train_indices]
y_train = y[train_indices]

X_test = X[test_indices]
y_test = y[test_indices]

print("Training records:", len(X_train))
print("Testing records:", len(X_test))
print("Encoded features:", len(feature_names))

# 5. Standardize features using training data only
feature_means = X_train.mean(axis=0)
feature_stds = X_train.std(axis=0)

feature_stds[feature_stds == 0] = 1

X_train_scaled = (X_train - feature_means) / feature_stds
X_test_scaled = (X_test - feature_means) / feature_stds

# 6. Train Linear Regression using NumPy
X_train_final = np.column_stack((
    np.ones(len(X_train_scaled)),
    X_train_scaled
))

coefficients, _, _, _ = np.linalg.lstsq(
    X_train_final,
    y_train,
    rcond=None
)

# 7. Evaluate on unseen test data
X_test_final = np.column_stack((
    np.ones(len(X_test_scaled)),
    X_test_scaled
))

predictions = X_test_final @ coefficients

mae = np.mean(np.abs(y_test - predictions))

rmse = np.sqrt(np.mean((y_test - predictions) ** 2))

ss_total = np.sum((y_test - y_test.mean()) ** 2)
ss_residual = np.sum((y_test - predictions) ** 2)

r2 = (
    1 - ss_residual / ss_total
    if ss_total != 0 else None
)

print("\nMODEL EVALUATION")
print("-" * 35)
print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("R2 Score:", round(r2, 4) if r2 is not None else "Undefined")

# 8. Train final model on all available records
all_means = X.mean(axis=0)
all_stds = X.std(axis=0)

all_stds[all_stds == 0] = 1

X_all_scaled = (X - all_means) / all_stds

X_all_final = np.column_stack((
    np.ones(len(X_all_scaled)),
    X_all_scaled
))

final_coefficients, _, _, _ = np.linalg.lstsq(
    X_all_final,
    y,
    rcond=None
)

# 9. Save final model
model = {
    "algorithm": "NumPy Linear Regression",
    "features": feature_names,
    "numerical_features": numerical_features,
    "categorical_features": categorical_features,
    "means": all_means.tolist(),
    "stds": all_stds.tolist(),
    "intercept": float(final_coefficients[0]),
    "coefficients": final_coefficients[1:].tolist(),
    "evaluation": {
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2) if r2 is not None else None,
        "training_records": len(X_train),
        "testing_records": len(X_test),
        "total_records": len(X)
    }
}

os.makedirs("models", exist_ok=True)

with open("models/indian_house_model.json", "w") as file:
    json.dump(model, file, indent=4)

print("\nFinal model trained successfully!")
print("Saved: models/indian_house_model.json")
print("\nESTATEIQ MODEL TRAINING COMPLETED!")
