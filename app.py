# app.py (Streamlit frontend)

import streamlit as st
import requests
import pandas as pd
import io

st.set_page_config(page_title="Campaign Trend Analyzer", layout="centered")

st.title("📊 Campaign Trend Analyzer")
st.write("Upload your campaign CSV file to generate insights using AI.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    try:
        # Read the file to show a preview
        df_preview = pd.read_csv(uploaded_file)
        st.subheader("📄 File Preview")
        st.dataframe(df_preview.head())

        # Reset the file pointer before sending to backend
        uploaded_file.seek(0)

        with st.spinner("🔍 Generating insights..."):
            files = {'file': uploaded_file.getvalue()}
            response = requests.post(
                "https://campaign-insights-backend.onrender.com/upload",
                files={'file': uploaded_file}
            )

        if response.status_code == 200:
            insights = response.json().get("insights", [])
            if insights:
                st.subheader("✅ AI-Generated Insights")
                for i, insight in enumerate(insights, 1):
                    st.markdown(f"- **Insight {i}:** {insight}")
            else:
                st.warning("No insights generated. Please check your data.")
        else:
            error = response.json().get("error", "Unknown error")
            st.error(f"❌ Error: {error}")

    except pd.errors.EmptyDataError:
        st.error("❌ The uploaded file is empty or unreadable.")
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
else:
    st.info("Please upload a CSV file to begin.")
