from model import predict_crime

# Example prediction for year 2026, district 10
predicted_crimes = predict_crime(2026, 10)
print(f"Predicted crimes for District 10 in 2026: {predicted_crimes:,.0f}")