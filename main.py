
import json
import numpy as np

# Load saved model
with open("models/house_price_model.json", "r") as file:
    model = json.load(file)

print("================================")
print("     HOUSE PRICE PREDICTOR")
print("================================")

# Get house details
area = float(input("Enter house area (sq ft): "))
bedrooms = float(input("Enter number of bedrooms: "))
bathrooms = float(input("Enter number of bathrooms: "))
age = float(input("Enter house age (years): "))

# Prepare input
features = np.array([area, bedrooms, bathrooms, age])

# Calculate predicted price
prediction = model["intercept"] + np.dot(
    features, np.array(model["coefficients"])
)

print("\n================================")
print("Predicted House Price: ₹", round(prediction, 2))
print("================================")
