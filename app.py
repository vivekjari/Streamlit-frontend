import streamlit as st
import pandas as pd
from chat_engine import get_chat_response
from followups import generate_followups
from utils import normalize_columns

st.set_page_config(page_title="Campaign Trend Chat Analyzer", layout="wide")

st.title("🧠 Campaign Trend Chat Analyzer")

uploaded_file = st.file_uploader("Upload your campaign dataset (CSV)", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        df = normalize_columns(df)

        st.success("✅ File uploaded and processed successfully!")
        st.write("Preview of your data:", df.head())

        # Chat Interface
        user_input = st.text_input("Ask a question about your campaign data:")

        if user_input:
            with st.spinner("Generating insights..."):
                response = get_chat_response(user_input, df)
                followups = generate_followups(user_input, df)

            st.markdown(f"**💬 Response:**\n{response}")
            st.markdown("**💡 Follow-up Suggestions:**")
            for f in followups:
                st.button(f)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
