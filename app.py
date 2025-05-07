import streamlit as st
import pandas as pd
import requests

# Page settings
st.set_page_config(page_title="Campaign Analyzer AI", layout="wide")
st.title("📊 AI-Powered Campaign Analyzer")

# Backend URLs
BACKEND_ANALYZE_URL = "https://campaign-analysis-f8e1.onrender.com/analyze"
BACKEND_ASK_URL = "https://campaign-analysis-f8e1.onrender.com/ask"

# Session state setup
if "suggested_paths" not in st.session_state:
    st.session_state.suggested_paths = []
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False
if "latest_result" not in st.session_state:
    st.session_state.latest_result = ""

# File upload
uploaded_file = st.file_uploader("Upload your campaign CSV file", type=["csv"])

# Analyze button
if uploaded_file and st.button("🔍 Analyze"):
    with st.spinner("Analyzing your campaign data..."):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(BACKEND_ANALYZE_URL, files={"file": uploaded_file})

        if response.status_code == 200:
            data = response.json()
            st.session_state.file_uploaded = True
            st.session_state.suggested_paths = data['suggested_paths']

            # Prepare insights and suggestions
            insights = "\n".join(f"- {insight}" for insight in data["pro_insights"])
            full_message = f"### 🧠 Insights\n\n{insights}\n\n### 🤖 AI Suggestions\n\n{data['llm_suggestions']}"
            st.session_state.latest_result = full_message

        else:
            st.error(f"Error from backend: {response.text}")
            st.session_state.file_uploaded = False

# Only show results after file is uploaded and analyzed
if st.session_state.file_uploaded:
    # Results section
    st.subheader("📥 Results")
    st.markdown(st.session_state.latest_result, unsafe_allow_html=True)

    # Suggested follow-ups
    if st.session_state.suggested_paths:
        st.subheader("💡 Suggested Follow-up Questions")
        for q in st.session_state.suggested_paths:
            if st.button(q):
                with st.spinner("Thinking..."):
                    response = requests.post(BACKEND_ASK_URL, json={"question": q})
                    if response.status_code == 200:
                        answer = response.json()["response"]
                        st.session_state.latest_result = f"**{q}**\n\n{answer}"
                    else:
                        st.error("Failed to get response from backend.")

    # Freeform chat
    st.subheader("💬 Ask anything about your campaign data")
    user_input = st.text_input("Your question:")
    if st.button("Send") and user_input.strip():
        with st.spinner("Thinking..."):
            response = requests.post(BACKEND_ASK_URL, json={"question": user_input})
            if response.status_code == 200:
                answer = response.json()["response"]
                st.session_state.latest_result = f"**You asked:** {user_input}\n\n{answer}"
            else:
                st.error("Failed to get response from backend.")
