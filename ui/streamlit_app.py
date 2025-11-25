import streamlit as st
import os
import sys
import asyncio

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from my_agents.summarizer_agent import summarize_pdf
from my_agents.quiz_agent import generate_quiz

st.title("📚 Study Notes AI Assistant")
st.markdown("Upload a PDF to get a summary or generate a quiz!")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save the uploaded file temporarily
    file_path = os.path.join("./temp_pdfs", uploaded_file.name)
    os.makedirs("./temp_pdfs", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"File '{uploaded_file.name}' uploaded successfully!")

    col1, col2 = st.columns(2)

    # -----------------------------
    # PDF SUMMARIZER COLUMN
    # -----------------------------
    with col1:
        st.header("PDF Summarizer")
        if st.button("Generate Summary"):
            with st.spinner("Generating summary... This may take a moment."):
                try:
                    # Correct async execution for Streamlit
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    summary = loop.run_until_complete(summarize_pdf(file_path))


                    st.subheader("Summary:")
                    st.write(summary)
                except Exception as e:
                    st.error(f"Error generating summary: {e}")

    # -----------------------------
    # QUIZ GENERATOR COLUMN
    # -----------------------------
    with col2:
        st.header("Quiz Generator")
        if st.button("Generate Quiz"):
            with st.spinner("Generating quiz... This may take a moment."):
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    quiz = generate_quiz(file_path)
                    st.subheader("Quiz:")
                    st.write(quiz)
                except Exception as e:
                    st.error(f"Error generating quiz: {e}")

else:
    st.info("Please upload a PDF file to get started.")
