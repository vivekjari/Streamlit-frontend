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
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "suggested_paths" not in st.session_state:
    st.session_state.suggested_paths = []
if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False

# File upload
uploaded_file = st.file_uploader("Upload your campaign CSV file", type=["csv"])

# Analyze button
if uploaded_file and st.button("🔍 Analyze"):
    with st.spinner("Analyzing your campaign data..."):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(BACKEND_ANALYZE_URL, files={"file": uploaded_file})

        if response.status_code == 200:
            data = response.json()
            st.session_state.chat_history = [
                {"role": "system", "content": "Initial analysis complete."},
                {"role": "ai", "content": data['llm_suggestions']}
            ]
            st.session_state.suggested_paths = data['suggested_paths']
            st.session_state.file_uploaded = True

            st.subheader("🧠 Insights")
            for insight in data["pro_insights"]:
                st.markdown(f"- {insight}")
        else:
            st.error(f"Error from backend: {response.text}")
            st.session_state.file_uploaded = False

# Only show chat if file was uploaded and analyzed
if st.session_state.file_uploaded:
    # Suggested follow-ups
    if st.session_state.suggested_paths:
        st.subheader("💡 Suggested Follow-up Questions")
        for q in st.session_state.suggested_paths:
            if st.button(q):
                st.session_state.chat_history.append({"role": "user", "content": q})
                with st.spinner("Thinking..."):
                    response = requests.post(BACKEND_ASK_URL, json={"question": q})
                    if response.status_code == 200:
                        answer = response.json()["response"]
                        st.session_state.chat_history.append({"role": "ai", "content": answer})
                        st.markdown(f"**{q}**")
                        st.markdown(answer)
                    else:
                        st.error("Failed to get response from backend.")

    # Freeform chat
    st.subheader("💬 Chat with your Data")
    user_input = st.text_input("Ask anything about your campaign data:")
    if st.button("Send") and user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            response = requests.post(BACKEND_ASK_URL, json={"question": user_input})
            if response.status_code == 200:
                answer = response.json()["response"]
                st.session_state.chat_history.append({"role": "ai", "content": answer})
                st.markdown(f"**You:** {user_input}")
                st.markdown(answer)
            else:
                st.error("Failed to get response from backend.")

# Show chat history
if st.session_state.chat_history:
    st.subheader("📜 Chat History")
    for msg in st.session_state.chat_history:
        role = "🧑‍💼 You" if msg["role"] == "user" else "🤖 AI"
        st.markdown(f"**{role}:** {msg['content']}")
