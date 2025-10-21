import streamlit as st
import requests
from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

st.set_page_config(page_title="MULTI-Agent Chat", layout="centered")
st.title("MULTI-Agent Chat Interface")
system_prompt = st.text_area("Define your AI agnet", height=70)
selected_model = st.selectbox("Select Your AI Model", settings.ALLOWED_MODEL_NAMES)
allow_search = st.checkbox("Allow Web Search", value=False)
user_input = st.text_area("Enter your message here:", height=150)


API_URL = "http://localhost:9999/chat"

if  st.button("Ask Agent") and user_input.strip():
    payload = {
        "model_name": selected_model,
        "system_prompt": system_prompt,
        "messages": [user_input],
        "allow_search": allow_search
    }

    try:
        logger.info(f"Sending request to AI agent with model {selected_model}")
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            agent_response = response.json().get("response", "No response from AI agent.")
            logger.info(f"Received response from AI agent for model {selected_model}")
            st.subheader("AI Agent Response:")
            st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html=True)
        
        else:
            logger.error(f"Error response from AI agent: {response.status_code}, {response.text}")
            st.error("Error from AI agent")

    except Exception as e:
        logger.error(f"Some error occurred during response generation")
        custom_error = CustomException("Failed to get AI response")
        st.error(str(custom_error))
