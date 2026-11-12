
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the real dataset
data = pd.read_csv("New folder/Chennai_AQI_Dataset.txt")

# Select input features
features = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]

# Convert AQI into numeric values
data["AQI"] = pd.to_numeric(data["AQI"], errors="coerce")

# Remove rows with missing values
data = data.dropna(subset=features + ["AQI"])

# Classify air quality using AQI ranges
def classify_aqi(aqi):
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Satisfactory"
    elif aqi <= 200:
        return "Moderate"
    elif aqi <= 300:
        return "Poor"
    elif aqi <= 400:
        return "Very Poor"
    else:
        return "Severe"

data["Air_Quality"] = data["AQI"].apply(classify_aqi)

X = data[features]
y = data["Air_Quality"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train Random Forest model
model = RandomForestClassifier(
    n_estimators=100, random_state=42
)

model.fit(X_train, y_train)

# Check accuracy
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions) * 100

# Save model
with open("air_quality_model.pkl", "wb") as file:
    pickle.dump(model, file)

# Save accuracy
with open("air_quality_accuracy.txt", "w") as file:
    file.write(str(accuracy))
print("Model Training Completed!")
print("Test Accuracy:", round(accuracy, 2), "%")
print("Total Records:", len(data))
