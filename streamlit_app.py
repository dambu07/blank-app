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

# Function to customize response based on keywords in the summary
def generate_doctor_advice(summary):
    advice = {
        "prescription": "",
        "diet": "",
        "exercise": "",
        "general": ""
    }
    
    # Prescription advice based on conditions
    if "inflammation" in summary.lower():
        advice["prescription"] += "- **Anti-inflammatory medications**: NSAIDs like ibuprofen may help with inflammation.\n"
    if "high blood pressure" in summary.lower():
        advice["prescription"] += "- **Blood pressure management**: ACE inhibitors or beta-blockers could be beneficial.\n"
    if "chronic pain" in summary.lower():
        advice["prescription"] += "- **Pain management**: Medications like acetaminophen may help manage chronic pain.\n"

    # Dietary advice based on conditions
    if "cholesterol" in summary.lower():
        advice["diet"] += "- **Low-cholesterol foods**: Limit intake of red meat, and consume more vegetables and whole grains.\n"
    if "diabetes" in summary.lower() or "blood sugar" in summary.lower():
        advice["diet"] += "- **Low-sugar diet**: Focus on whole foods, and avoid processed sugars to manage blood sugar levels.\n"
    if "weight" in summary.lower():
        advice["diet"] += "- **Balanced diet**: Consider a nutrient-dense, calorie-controlled diet to manage weight.\n"

    # Exercise recommendations based on conditions
    if "heart" in summary.lower() or "cardio" in summary.lower():
        advice["exercise"] += "- **Aerobic exercises**: Activities like brisk walking and swimming are great for heart health.\n"
    if "arthritis" in summary.lower() or "joint pain" in summary.lower():
        advice["exercise"] += "- **Low-impact exercises**: Gentle activities such as yoga and cycling can ease joint pain.\n"

    # General advice based on conditions
    if "stress" in summary.lower():
        advice["general"] += "- **Stress management**: Techniques like meditation and breathing exercises are beneficial for mental health.\n"
    if "insomnia" in summary.lower() or "sleep" in summary.lower():
        advice["general"] += "- **Improved sleep habits**: Aim for a consistent bedtime routine and reduce screen time before bed.\n"
    
    return advice

# Function for AI-based health chat responses
def chat_with_report(summary):
    # Display the summary overview first
    condition_overview = f"The health report indicates the following summary of your condition:\n\n{summary}\n\n"
    st.write(condition_overview)
    
    # Generate customized advice based on the summary
    advice = generate_doctor_advice(summary)
    
    # Buttons for specific health-related responses with AI-based suggestions
    if st.button("Get Prescription Advice"):
        st.write("As your healthcare assistant, here are possible prescription suggestions:")
        st.write(advice["prescription"] if advice["prescription"] else "No specific prescription advice based on the report.")

    if st.button("Get Dietary Suggestions"):
        st.write("Based on the health report, here are dietary adjustments:")
        st.write(advice["diet"] if advice["diet"] else "No specific dietary suggestions based on the report.")

    if st.button("Get Exercise Recommendations"):
        st.write("Here are exercise recommendations suitable for your condition:")
        st.write(advice["exercise"] if advice["exercise"] else "No specific exercise recommendations based on the report.")

    if st.button("General Advice"):
        st.write("General health advice for ongoing wellness:")
        st.write(advice["general"] if advice["general"] else "No specific general advice based on the report.")

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
    
    # Interactive Chat Feature for Specific Questions
    st.subheader("Chat with your Health Report")
    chat_with_report(summary)
