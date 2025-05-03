import streamlit as st
import pandas as pd
from chat_engine import get_chat_response
from insights import generate_insights
import os
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="Campaign Trend Analyzer", layout="wide")

st.title("📊 Campaign Trend Analyzer")
st.markdown("Upload a dataset to get smart, AI-generated insights and ask questions like a superhuman.")

uploaded_file = st.file_uploader("Upload your campaign dataset (CSV)", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")
        st.dataframe(df.head())

        if st.button("Generate Insights"):
            try:
                insights = generate_insights(df)
                st.subheader("📌 Key Insights")
                for ins in insights:
                    st.markdown(f"- {ins}")
            except Exception as e:
                st.error(f"Error generating insights: {str(e)}")

        st.subheader("💬 Ask a question about your data")
        user_query = st.text_input("What would you like to know?")
        if user_query:
            try:
                response = get_chat_response(df, user_query)
                st.markdown(f"**🧠 AI says:** {response}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    except Exception as e:
        st.error(f"Internal server error: {str(e)}")