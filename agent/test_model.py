import joblib

model = joblib.load("models/citizen_complaint_model.pkl")

complaint = "A huge pothole has formed on our road."

prediction = model.predict([complaint])[0]

print("Complaint:", complaint)
print("Predicted Category:", prediction)