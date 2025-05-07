import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Campaign Analyzer AI", layout="wide")
st.title("📊 AI-Powered Campaign Analyzer")

BACKEND_ANALYZE_URL = "https://campaign-analysis-f8e1.onrender.com/analyze"  # Replace with actual
BACKEND_ASK_URL = "https://campaign-analysis-f8e1.onrender.com/ask"  # Replace with actual

# Session state initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "suggested_paths" not in st.session_state:
    st.session_state.suggested_paths = []
if "file_bytes" not in st.session_state:
    st.session_state.file_bytes = None

uploaded_file = st.file_uploader("Upload your campaign CSV file", type=["csv"])

if uploaded_file and st.button("🔍 Analyze"):
    st.session_state.file_bytes = uploaded_file.getvalue()  # store bytes
    with st.spinner("Analyzing your campaign data..."):
        files = {"file": st.session_state.file_bytes}
        response = requests.post(BACKEND_ANALYZE_URL, files=files)
        if response.status_code == 200:
            data = response.json()
            st.session_state.chat_history = [
                {"role": "system", "content": "Initial analysis complete."},
                {"role": "ai", "content": data['llm_suggestions']}
            ]
            st.session_state.suggested_paths = data['suggested_paths']
            st.subheader("🧠 Insights")
            for insight in data["pro_insights"]:
                st.markdown(f"- {insight}")
        else:
            st.error(f"Error from backend: {response.text}")

# Only show after analysis
if st.session_state.suggested_paths and st.session_state.file_bytes:
    st.subheader("💡 Suggested Follow-up Questions")
    for q in st.session_state.suggested_paths:
        if st.button(q):
            st.session_state.chat_history.append({"role": "user", "content": q})
            with st.spinner("Thinking..."):
                response = requests.post(
                    BACKEND_ASK_URL,
                    files={"file": st.session_state.file_bytes},
                    data={"question": q}
                )
                if response.status_code == 200:
                    answer = response.json()["response"]
                    st.session_state.chat_history.append({"role": "ai", "content": answer})
                    st.markdown(f"**{q}**")
                    st.markdown(answer)
                else:
                    st.error("Failed to get response from backend.")

    st.subheader("💬 Chat with your Data")
    user_input = st.text_input("Ask anything about your campaign data:")
    if st.button("Send") and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            response = requests.post(
                BACKEND_ASK_URL,
                files={"file": st.session_state.file_bytes},
                data={"question": user_input}
            )
            if response.status_code == 200:
                answer = response.json()["response"]
                st.session_state.chat_history.append({"role": "ai", "content": answer})
                st.markdown(f"**You:** {user_input}")
                st.markdown(answer)
            else:
                st.error("Failed to get response from backend.")
