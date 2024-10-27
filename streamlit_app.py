import streamlit as st
import os
from PIL import Image
import pdfplumber
import requests
import io

# Load API key from secrets
api_key = st.secrets["gemini_api_key"]

# Define the endpoint
api_endpoint = "https://ai.googleapis.com/v1beta1/"

# Function to call Gemini API
def call_gemini_api(file_bytes):
    try:
        files = {'file': file_bytes}
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.post(api_endpoint, files=files, headers=headers)
        response.raise_for_status()  # Ensure we catch HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API call failed: {e}")
        return {"summary": "Error calling API"}

# Function to summarize the document
def summarize_document(file_bytes):
    response = call_gemini_api(file_bytes)
    return response.get('summary', 'No summary provided.')

# Function to analyze the health report
def analyze_health_report(summary):
    # Placeholder function for analyzing the health report
    return "Recommended care strategies, prescriptions, and dietary suggestions."

# Function to handle chat responses
def chat_with_report(question, summary):
    # Simulate a response based on summary and question
    if "prescription" in question.lower():
        return "Based on the report, I would recommend discussing potential prescriptions with your doctor."
    elif "diet" in question.lower():
        return "The report suggests maintaining a balanced diet. Consider foods rich in nutrients as per your doctor's advice."
    elif "exercise" in question.lower():
        return "Regular, moderate exercise is generally beneficial. Please consult a healthcare provider for personalized recommendations."
    else:
        return f"As a healthcare assistant, I suggest consulting the summary: {summary}. For detailed advice, please talk to a professional."

st.title('Medical Report Assistant')
uploaded_file = st.file_uploader("Upload your medical report (X-ray, ECG, Insurance document)", type=['png', 'jpg', 'jpeg', 'pdf'])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()  # Read the file into bytes

    if uploaded_file.type in ['image/png', 'image/jpeg', 'image/jpg']:
        image = Image.open(io.BytesIO(file_bytes))  # Open image from bytes
        st.image(image, caption='Uploaded Image')
    elif uploaded_file.type == 'application/pdf':
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:  # Open PDF from bytes
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            st.text(text)
            file_bytes = io.BytesIO(file_bytes)  # Prepare for API call

    # Summarize document using API
    summary = summarize_document(file_bytes)
    
    # Analyze health report from summary
    feedback = analyze_health_report(summary)
    
    st.subheader('Summary')
    st.write(summary)
    
    st.subheader('Health Recommendations')
    st.write(feedback)
    
    # Chat feature
    st.subheader("Chat with your Health Report")
    question = st.text_input("Ask a question about the report (e.g., 'What are the diet recommendations?')")
    if question:
        response = chat_with_report(question, summary)
        st.write("Assistant's Response:")
        st.write(response)
