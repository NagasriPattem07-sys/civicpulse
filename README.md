# CivicPulse: Public Grievance Intelligence

CivicPulse is an ML-powered decision-support prototype for public grievance
management. A citizen describes a public issue in plain language, and the
system classifies it, recommends the responsible department, estimates
confidence and flags urgency, so officials receive organised complaints
instead of raw text. Every result is recommended for human review.

**Live demo:** https://civicpulse-grievance.streamlit.app/


## Features

- Complaint classification with a TF-IDF + Linear SVM pipeline
- Automatic department recommendation
- Model confidence score (relative score from the classifier's decision values)
- Rule-based priority detection (High / Medium / Low) with the triggering keyword
- Ticket ID and timestamp for every analysed complaint
- Custom-branded Streamlit interface

## How it works

1. **Report:** the citizen describes the issue in plain words
2. **Classify:** the ML model identifies the problem category
3. **Route:** the responsible department is recommended for human review

## Project structure

```
app.py                      Streamlit interface
agent/
  classifier.py             loads the model, predicts category + confidence
  department_router.py      maps category to department
  civicpulse_agent.py       orchestrates classification, routing, priority, ticket ID
  test_model.py             quick model test script
notebooks/
  CivicPulse_ML_Development.ipynb   data preparation, training and evaluation
models/
  citizen_complaint_model.pkl       trained scikit-learn pipeline
requirements.txt
```

## Data

The model is trained on a sample of NYC 311 service requests from
[NYC Open Data](https://data.cityofnewyork.us/). The notebook downloads the
data directly, so the CSV is not stored in this repository.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Notes

- This is a prototype (v1.0) intended for decision support, not automated action.
- Priority detection is keyword-based and can be edited in `agent/civicpulse_agent.py`.
- Complaints are not stored yet; a dashboard for officials is planned.
- Because the training data comes from NYC 311, the categories and phrasing reflect US municipal complaints; other regions would need local data.

## Tech stack

Python, scikit-learn, Streamlit, Plotly
