import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import os
import gdown

# 🔽 1. Download model from Google Drive
FILE_ID = "1RU97PU9rvE5dlr0bfU0u-zjuOFvdNth7"
URL = f"https://drive.google.com/uc?id={FILE_ID}"

@st.cache_resource
def load_model():
    if not os.path.exists("rsf_model.pkl"):
        with st.spinner("Downloading model from Google Drive..."):
            gdown.download(URL, "rsf_model.pkl", quiet=False)
    with open("rsf_model.pkl", "rb") as f:
        return pickle.load(f)

rsf = load_model()
time_horizon = 5  # years

st.title("5-Year Cardiovascular Event Risk Prediction in People Living with HIV")
st.write("Please enter the patient's clinical and demographic information:")

sex = st.selectbox("Sex", ["Male", "Female"])
transmission = st.selectbox("Transmission mode", ["Homo/bisexual", "Injecting drug user", "Heterosexual", "Other/Unknown"])
origin = st.selectbox("Country of origin", ["Spain", "Not Spain"])
education = st.selectbox("Education level", ["No education", "Primary", "Secondary", "University", "Other/Unknown"])
aids = st.selectbox("AIDS diagnosis", ["No", "Yes"])
age = st.slider("Age", 18, 90, 45)
viral_load = st.selectbox("Baseline viral load", ["<100,000 copies/mL", "≥100,000 copies/mL"])
art = st.selectbox("ART regimen", ["2NRTI+1NNRTI", "2NRTI+1PI", "2NRTI+1INSTI", "Other"])
hcv = st.selectbox("HCV antibodies", ["Negative", "Positive"])
hbv = st.selectbox("HBV core antibodies", ["Negative", "Positive"])
cd4 = st.number_input("CD4 nadir (cells/μL)", min_value=0, max_value=2000, value=350)
cd8 = st.number_input("CD8 nadir (cells/μL)", min_value=0, max_value=3000, value=800)
ratio = st.number_input("CD4/CD8 ratio", value=0.45)
hypertension = st.selectbox("Hypertension", ["No", "Yes"])
smoking = st.selectbox("Smoking status", ["Never smoker", "Current smoker", "Former smoker"])
chol = st.number_input("Total cholesterol (mg/dL)", value=180.0)
hdl = st.number_input("HDL cholesterol (mg/dL)", value=50.0)
trig = st.number_input("Triglycerides (mg/dL)", value=150.0)
non_hdl = st.number_input("Non-HDL cholesterol (mg/dL)", value=130.0)
trig_hdl_ratio = st.number_input("Triglyceride/HDL ratio", value=3.0)
diabetes = st.selectbox("Diabetes", ["No", "Yes"])

df_input = pd.DataFrame({
    "Sex": [0 if sex == "Male" else 1],
    "Transmission_mode": [0 if transmission == "Homo/bisexual" else 1 if transmission == "Injecting drug user" else 2 if transmission == "Heterosexual" else 3],
    "Origin": [0 if origin == "Spain" else 1],
    "Education_level": [0 if education == "No education" else 1 if education == "Primary" else 2 if education == "Secondary" else 3 if education == "University" else 4],
    "AIDS": [0 if aids == "No" else 1],
    "Age": [age],
    "Viral_load": [1 if viral_load == "≥100,000 copies/mL" else 0],
    "ART": [0 if art == "2NRTI+1NNRTI" else 1 if art == "2NRTI+1PI" else 2 if art == "2NRTI+1INSTI" else 3],
    "HCV_antibodies": [0 if hcv == "Negative" else 1],
    "HBV_anticore": [0 if hbv == "Negative" else 1],
    "CD4_nadir": [cd4],
    "CD8_nadir": [cd8],
    "CD4_CD8_ratio": [ratio],
    "High_BP": [1 if hypertension == "Yes" else 0],
    "Smoking": [0 if smoking == "Never smoker" else 1 if smoking == "Current smoker" else 2],
    "Total_Cholesterol": [chol],
    "HDL": [hdl],
    "Triglycerides": [trig],
    "Non_HDL_chol": [non_hdl],
    "Trig_HDL_ratio": [trig_hdl_ratio],
    "Diabetes": [1 if diabetes == "Yes" else 0]
})

surv_fn = rsf.predict_survival_function(df_input)[0]
times = rsf.event_times_

surv_5y = float(surv_fn(time_horizon))
risk_5y = 1 - surv_5y

st.markdown(f"### Estimated 5-year cardiovascular event risk: **{risk_5y:.1%}**")

fig, ax = plt.subplots()
ax.step(times, surv_fn(times), where="post")
ax.set_title("Predicted survival curve")
ax.set_xlabel("Time (years)")
ax.set_ylabel("Survival probability")
st.pyplot(fig)
