import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import accuracy_score
import joblib

# Load the data
ponzi_data = pd.read_csv("fyp_ponzi_detection-main\Ponzi_label.csv")
transactions_data = pd.read_csv("fyp_ponzi_detection-main\cleaned_external_transactions.csv")

# Check unique values in the "Ponzi" column before merging
print("Unique values in 'Ponzi' column before merging:", ponzi_data["Ponzi"].unique())

# Ensure that both classes are present in the Ponzi data
if len(ponzi_data["Ponzi"].unique()) != 2:
    raise ValueError(f'Expected 2 classes in the Ponzi data, but got {len(ponzi_data["Ponzi"].unique())} classes: {ponzi_data["Ponzi"].unique()}')

# Merge the data
merged_data = pd.merge(transactions_data, ponzi_data, on="contractAddress", how="right")

# Check unique values in the "Ponzi" column after merging
print("Unique values in 'Ponzi' column after merging:", merged_data["Ponzi"].unique())

# Drop columns that are not needed for the model
columns_to_drop = ["blockHash", "hash", "from", "to", "input", "methodId", "functionName", "contractAddress", "ponzi_name", "Date"]
merged_data = merged_data.drop(columns=columns_to_drop)

# Convert categorical columns to numerical values using encoding
merged_data = pd.get_dummies(merged_data)

# Define features and target variable
x = merged_data.drop(["Ponzi"], axis=1)  # Features
y = merged_data["Ponzi"]  # Target variable

# Ensure that both classes are present in the Ponzi data
if len(y.unique()) != 2:
    raise ValueError(f"Expected 2 classes in the target variable, but got {len(y.unique())} classes: {y.unique()}")

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=42)

# Train the model
model = xgb.XGBClassifier()
model.fit(x_train, y_train)

# Make predictions
y_pred = model.predict(x_test)

# Calculate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")