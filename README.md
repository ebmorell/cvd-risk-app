# Cardiovascular Risk Prediction App for People Living with HIV

This Streamlit web application estimates the 5-year risk of cardiovascular events in people living with HIV using a machine learning model based on Random Survival Forests.

## 🚀 Features
- Predicts 5-year cardiovascular risk from clinical and demographic data
- Based on a trained Random Survival Forest model
- Uses a large clinical cohort (CoRIS)
- Visualizes predicted survival curve

## 📦 Model Info
- Trained with over 20 variables
- Hosted on [Hugging Face Hub](https://huggingface.co/ebmorell/cvd-risk-model)
- Automatically downloaded when the app starts (no manual download needed)

## 🧪 Input Variables
- Sex
- Mode of transmission
- Country of origin
- Education level
- AIDS diagnosis
- Age
- Baseline viral load
- ART regimen
- HCV / HBV serologies
- CD4 / CD8 counts and ratio
- Blood pressure
- Smoking
- Cholesterol, HDL, triglycerides, etc.
- Diabetes

## 🖥️ How to Run

### Option 1: Streamlit Cloud
1. Fork this repository
2. Deploy via [Streamlit Cloud](https://streamlit.io/cloud)

### Option 2: Local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 📁 Files
- `app.py` → Main Streamlit application
- `requirements.txt` → Dependencies

## 🤝 Author
**Enrique Bernal Morell**  
Internal Medicine & Infectious Diseases  
Project hosted on [Hugging Face](https://huggingface.co/ebmorell/cvd-risk-model)
