import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Campaign Analyzer AI", layout="wide")
st.title("📊 AI-Powered Campaign Analyzer")

backend_url = "https://your-backend-url.onrender.com/analyze"  # Replace with your actual backend URL

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "suggested_paths" not in st.session_state:
    st.session_state.suggested_paths = []

uploaded_file = st.file_uploader("Upload your campaign CSV file", type=["csv"])

if uploaded_file and st.button("🔍 Analyze"):
    with st.spinner("Analyzing your campaign data..."):
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(backend_url, files={"file": uploaded_file})
        if response.status_code == 200:
            data = response.json()
            st.session_state.chat_history.append({"role": "system", "content": "Initial analysis complete."})
            st.session_state.chat_history.append({"role": "ai", "content": data['llm_suggestions']})
            st.session_state.suggested_paths = data['suggested_paths']
            st.subheader("🧠 Insights")
            for insight in data["pro_insights"]:
                st.markdown(f"- {insight}")
        else:
            st.error(f"Error from backend: {response.text}")

if st.session_state.suggested_paths:
    st.subheader("💡 Suggested Follow-up Questions")
    for q in st.session_state.suggested_paths:
        if st.button(q):
            st.session_state.chat_history.append({"role": "user", "content": q})
            with st.spinner("Thinking..."):
                chat_input = {"question": q}
                followup = requests.post("https://your-backend-url.onrender.com/ask", json=chat_input)
                if followup.status_code == 200:
                    answer = followup.json()["response"]
                    st.session_state.chat_history.append({"role": "ai", "content": answer})
                    st.markdown(f"**{q}**")
                    st.markdown(answer)
                else:
                    st.error("Failed to get response from backend.")

st.subheader("💬 Chat with your Data")
user_input = st.text_input("Ask anything about your campaign data:")
if st.button("Send") and user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.spinner("Thinking..."):
        chat_input = {"question": user_input}
        followup = requests.post("https://your-backend-url.onrender.com/ask", json=chat_input)
        if followup.status_code == 200:
            answer = followup.json()["response"]
            st.session_state.chat_history.append({"role": "ai", "content": answer})
            st.markdown(answer)
        else:
            st.error("Failed to get response from backend.")
