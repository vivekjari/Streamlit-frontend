import streamlit as st
import requests
import pandas as pd
import io

st.set_page_config(page_title="Campaign AI Assistant", layout="wide")

st.title("📊 Campaign Insight AI")
st.markdown("Upload your campaign CSV file and get expert-level insights instantly.")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    with st.spinner("Analyzing your campaign data..."):
        files = {'file': (uploaded_file.name, uploaded_file, 'text/csv')}
        try:
            response = requests.post("https://campaign-analysis-f8e1.onrender.com/analyze", files=files)
            if response.status_code == 200:
                result = response.json()
                st.subheader("📌 Key Insights")
                for insight in result["pro_insights"]:
                    st.markdown(f"- {insight}")

                st.subheader("🤖 AI Suggestions")
                st.markdown(result["llm_suggestions"])

                st.subheader("💡 Further Questions to Explore")
                for q in result["suggested_paths"]:
                    st.markdown(f"- {q}")
            else:
                st.error("Something went wrong. Please check your backend URL and try again.")
        except Exception as e:
            st.error(f"Error: {e}")