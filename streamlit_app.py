mport streamlit as st
import os
from PIL import Image
import pdfplumber
import requests

# Load API key from secrets
api_key = st.secrets["gemini_api_key"]

# Define the endpoint
api_endpoint = "https://api.gemini.com/analyze"

# Function to call Gemini API
def call_gemini_api(file_path):
    files = {'file': open(file_path, 'rb')}
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.post(api_endpoint, files=files, headers=headers)
    return response.json()

# Function to summarize the document
def summarize_document(file_path):
    response = call_gemini_api(file_path)
    return response.get('summary', 'No summary provided.')

# Function to analyze the health report
def analyze_health_report(summary):
    # Placeholder function for analyzing the health report
    return "Recommended care strategies, prescriptions, and dietary suggestions."

st.title('Medical Report Assistant')
uploaded_file = st.file_uploader("Upload your medical report (X-ray, ECG, Insurance document)", type=['png', 'jpg', 'jpeg', 'pdf'])
if uploaded_file is not None:
    if uploaded_file.type in ['image/png', 'image/jpeg', 'image/jpg']:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image')
    elif uploaded_file.type == 'application/pdf':
        with pdfplumber.open(uploaded_file) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            st.text(text)
    summary = summarize_document(uploaded_file)
    feedback = analyze_health_report(summary)
    st.subheader('Summary')
    st.write(summary)
    st.subheader('Health Recommendations')
    st.write(feedback)
