import streamlit as st
import pandas as pd
import requests

# Page setup
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
        response = requests.post(BACKEND_ANALYZE_URL, files={"file": uploaded_file})

        if response.status_code == 200:
            data = response.json()
            st.session_state.file_uploaded = True
            st.session_state.suggested_paths = data['suggested_paths']

            insights = "\n".join(f"- {insight}" for insight in data["pro_insights"])
            full_message = f"### 🧠 Insights\n\n{insights}\n\n### 🤖 AI Suggestions\n\n{data['llm_suggestions']}"
            st.session_state.latest_result = full_message
        else:
            st.error(f"Error from backend: {response.text}")
            st.session_state.file_uploaded = False

# Show follow-up options
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

# Result section at the bottom of the page
st.markdown("---")
st.subheader("📥 Result")
if st.session_state.latest_result:
    st.markdown(
        f"""
        <div style="
            background-color: #f0f2f6;
            border: 1px solid #d0d0d0;
            padding: 20px;
            border-radius: 8px;
            color: black;
            font-size: 16px;
            white-space: pre-wrap;
            ">
            {st.session_state.latest_result.replace('\n', '<br>')}
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.info("Results will appear here after analysis or asking a question.")
