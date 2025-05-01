import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Campaign Trend Analyzer", layout="centered")

st.title("📊 Campaign Trend Analyzer")
st.markdown("Upload your campaign CSV file to generate automated insights.")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    try:
        # Preview uploaded data
        df = pd.read_csv(uploaded_file)
        st.subheader("📄 File Preview")
        st.dataframe(df.head())

        if st.button("Generate Insights"):
            with st.spinner("Analyzing..."):
                # Send file to backend
                files = {"file": (uploaded_file.name, uploaded_file, "text/csv")}
                response = requests.post("https://campaign-insights-backend.onrender.com/upload", files=files)

                if response.status_code == 200:
                    insights = response.json().get("insights", [])
                    st.success("✅ Insights generated successfully!")
                    st.subheader("🧠 AI-Generated Insights")
                    for i, insight in enumerate(insights, 1):
                        st.markdown(f"**{i}.** {insight}")
                else:
                    st.error(f"❌ Error: {response.json().get('error')}")
    except Exception as e:
        st.error(f"Error reading file: {e}")

