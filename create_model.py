import pickle
from sklearn.linear_model import LinearRegression
import numpy as np

# Dummy data: years & districts → crime counts
X = np.array([
    [2020, 1],
    [2021, 1],
    [2022, 2],
    [2023, 2],
    [2024, 3],
    [2025, 3],
    [2026, 4],
    [2027, 4]
])
y = np.array([1000, 950, 900, 870, 850, 820, 800, 780])

# Train a simple linear model
model = LinearRegression()
model.fit(X, y)

# Save it as model.pkl
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model saved as model.pkl")
