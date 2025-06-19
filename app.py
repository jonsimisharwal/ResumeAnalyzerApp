import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import joblib
import resume_parser
from model.train_model import predict_job_role

st.set_page_config(page_title="Smart Resume Analyzer", layout="centered")
st.title("📄 Smart Resume Analyzer")

uploaded_file = st.file_uploader("Upload your Resume (PDF only)", type=["pdf"])

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    st.success("Uploaded Successfully!")

    text = resume_parser.extract_text_from_pdf("temp.pdf")
    parsed_data = resume_parser.extract_info(text)

    st.subheader("📋 Extracted Information:")
    st.json(parsed_data)

    role = predict_job_role(parsed_data["skills"])
    st.subheader("🔍 Predicted Role: ")
    st.write(role)