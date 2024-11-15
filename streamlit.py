import streamlit as st
import requests

# Set up the Streamlit app title
st.title("PDF Uploader and Sender")

# Use file_uploader to allow the user to upload a PDF file
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
BASE_URL = "http://localhost:8000/api/v1/pdf-qa"
# The backend API endpoint
UPLOAD_API_URL = f"{BASE_URL}/upload-pdf"  # Replace with your backend endpoint URL

ASK_QUESTION_API_URL = f"{BASE_URL}/ask"  # Replace with your backend endpoint URL

# When a PDF is uploaded, and the "Send to API" button is clicked
if uploaded_file and st.button("Send to API"):
    # Send a POST request with the file to the API
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}

    try:
        response = requests.post(UPLOAD_API_URL, files=files)
        response.raise_for_status()  # Check if the request was successful

        # Display the API response
        st.success("File successfully sent to API!")
        st.write("Response from server:", response.json())

    except requests.exceptions.RequestException as e:
        st.error(f"Error sending file: {e}")


question = st.text_input("Enter your question:")
# Button to submit the data
if st.button("Submit Data"):
    # st.write(question)
    # Prepare data to send in POST request
    payload = {
        "question": question,
    }

    # Make POST request
    try:
        response = requests.post(ASK_QUESTION_API_URL, json=payload)
        response.raise_for_status()  # Check for HTTP errors

        # Parse and display the JSON response
        data = response.json()
        st.write("Response from server:", data)

    except requests.exceptions.RequestException as e:
        st.error(f"Error sending data: {e}")
