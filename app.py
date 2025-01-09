import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
# Constants
BASE_API_URL = os.getenv("BASE_API_URL")
LANGFLOW_ID = os.getenv("LANGFLOW_ID")
FLOW_ID = os.getenv("FLOW_ID")
APPLICATION_TOKEN = os.getenv("APPLICATION_TOKEN")
ENDPOINT = ""  # Endpoint name in LangFlow settings, optional.

# Function to call LangFlow API
def call_langflow_api(message, endpoint, tweaks=None):
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{endpoint}"
    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    if tweaks:
        payload["tweaks"] = tweaks

    response = requests.post(api_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": f"Error: {response.status_code}",
            "details": response.text,
        }

# Streamlit Application
def main():
    st.title("Social Media Analytics Chatbot")


    # User input
    question = st.text_area("Enter your question:", placeholder="e.g., What is the engagement rate for reels?")


    if st.button("Analyze"):
        if not question.strip():
            st.warning("Please enter a question to proceed.")
        else:
            try:
                result = call_langflow_api(
                    message=question, endpoint=ENDPOINT or FLOW_ID, tweaks={}
                )
                if "error" in result:
                    st.error(result["error"])
                    st.write(result.get("details", ""))
                else:
                    text = result["outputs"][-1]["outputs"][-1]["results"]["message"]["data"]["text"]
                    st.success("Analysis Completed!")
                    st.write(text)
            except json.JSONDecodeError:
                st.error("Invalid tweaks JSON. Please correct and try again.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
