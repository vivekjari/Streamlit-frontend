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

            # Format results
            insights = "\n".join(f"- {insight}" for insight in data["pro_insights"])
            full_message = f"### 🧠 Insights\n\n{insights}\n\n### 🤖 AI Suggestions\n\n{data['llm_suggestions']}"
            st.session_state.latest_result = full_message
        else:
            st.error(f"Error from backend: {response.text}")
            st.session_state.file_uploaded = False

# Only show interaction options if analyzed
if st.session_state.file_uploaded:
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

# Spacer to push result box to bottom
st.markdown("<br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)

# Result section styled as a box
if st.session_state.latest_result:
    st.markdown("""
        <div style="position: fixed; bottom: 0; left: 0; right: 0; background-color: #f9f9f9;
                    border-top: 2px solid #ccc; padding: 20px; max-height: 300px; overflow-y: auto;
                    box-shadow: 0 -2px 10px rgba(0,0,0,0.1); z-index: 1000;">
            <h4 style="margin-top: 0;">📥 Result</h4>
            <div style="white-space: pre-wrap;">{}</div>
        </div>
    """.format(st.session_state.latest_result.replace("\n", "<br>")), unsafe_allow_html=True)
