import streamlit as st
import os
from PIL import Image
import pdfplumber
import requests
import io

# Load API key from secrets
api_key = st.secrets["gemini_api_key"]

# Define the API endpoint
api_endpoint = "https://ai.googleapis.com/v1beta1/"

# Function to call Gemini API
def call_gemini_api(file_bytes):
    try:
        files = {'file': file_bytes}
        headers = {'Authorization': f'Bearer {api_key}'}
        response = requests.post(api_endpoint, files=files, headers=headers)
        response.raise_for_status()  # Ensure HTTP errors are caught
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API call failed: {e}")
        return {"summary": "Error calling API"}

# Function to summarize the document
def summarize_document(file_bytes):
    response = call_gemini_api(file_bytes)
    return response.get('summary', 'No summary provided.')

# Function to analyze health report
def analyze_health_report(summary):
    return "Recommended care strategies, prescriptions, and dietary suggestions."

# Function for AI-based health chat responses
def chat_with_report(summary):
    # Display the summary overview first
    condition_overview = f"The health report indicates the following summary of your condition:\n\n{summary}\n\n"
    st.write(condition_overview)
    
    # Buttons for specific health-related responses with AI-based suggestions
    if st.button("Get Prescription Advice"):
        st.write("As your healthcare assistant, here are possible prescription suggestions:")
        st.write("- **Anti-inflammatory medications**: NSAIDs like ibuprofen may help if inflammation is present.")
        st.write("- **Blood pressure management**: ACE inhibitors, beta-blockers, or diuretics may be options if needed.")
        st.write("- **Pain management**: Acetaminophen or specific pain relievers tailored to chronic pain.")
    
    if st.button("Get Dietary Suggestions"):
        st.write("Based on the health report, here are dietary adjustments:")
        st.write("- **High-fiber foods**: More vegetables, fruits, and whole grains can aid digestion and blood sugar.")
        st.write("- **Low-sodium diet**: Reducing salt intake can help manage blood pressure.")
        st.write("- **Healthy fats**: Foods like avocados, nuts, and olive oil support heart health.")
        st.write("- **Hydration**: Aim for adequate water intake daily for overall health.")

    if st.button("Get Exercise Recommendations"):
        st.write("Here are exercise recommendations suitable for your condition:")
        st.write("- **Aerobic exercises**: Brisk walking, cycling, or swimming for cardiovascular health.")
        st.write("- **Strength training**: Light resistance exercises for muscle and joint support.")
        st.write("- **Flexibility and balance**: Yoga or stretching exercises for flexibility and mental wellness.")
        st.write("- **Customized plan**: A fitness professional can provide a personalized program if needed.")

    if st.button("General Advice"):
        st.write("General health advice for ongoing wellness:")
        st.write("- **Routine check-ups**: Regular check-ups help monitor health changes and address concerns early.")
        st.write("- **Stress management**: Techniques like meditation and deep breathing reduce stress.")
        st.write("- **Adequate sleep**: Aim for 7-8 hours of restful sleep each night.")
        st.write("- **Limit alcohol and avoid smoking**: Reducing alcohol and avoiding tobacco can greatly reduce risks.")

# App layout and main execution flow
st.title('Medical Report Assistant')
uploaded_file = st.file_uploader("Upload your medical report (X-ray, ECG, Insurance document)", type=['png', 'jpg', 'jpeg', 'pdf'])

if uploaded_file is not None:
    file_bytes = uploaded_file.read()  # Read the file into bytes

    # Display uploaded image or first page of PDF
    if uploaded_file.type in ['image/png', 'image/jpeg', 'image/jpg']:
        image = Image.open(io.BytesIO(file_bytes))
        st.image(image, caption='Uploaded Image')
    elif uploaded_file.type == 'application/pdf':
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            st.text(text)
            file_bytes = io.BytesIO(file_bytes)

    # Generate and display summary of the document
    summary = summarize_document(file_bytes)
    st.subheader('Summary')
    st.write(summary)
    
    # Display general health recommendations based on the summary
    feedback = analyze_health_report(summary)
    st.subheader('Health Recommendations')
    st.write(feedback)
    
    # Interactive Chat Feature for Specific Questions
    st.subheader("Chat with your Health Report")
    chat_with_report(summary)
