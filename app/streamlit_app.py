import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import streamlit as st
from src.extract import extract_text_from_pdf
from src.ai_processor import extract_kv_pairs_from_text
from src.excel_writer import write_to_excel
from src.utils import save_json
import tempfile, os


st.title("AI Document → Structured Excel")
st.write("Upload a PDF or click 'Use sample'")

uploaded = st.file_uploader("Upload PDF", type=["pdf"])
use_sample = st.button("Use sample /mnt/data/Data Input.pdf")

if uploaded or use_sample:
    if uploaded:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tf:
            tf.write(uploaded.read())
            pdf_path = tf.name
    else:
        pdf_path = "/mnt/data/Data Input.pdf"

    st.info(f"Processing {pdf_path}...")
    text = extract_text_from_pdf(pdf_path)

    st.text_area("Extracted text preview", text[:2000], height=200)

    if st.button("Run AI Extraction"):
        with st.spinner("Extracting key:value pairs using Gemini..."):
            items = extract_kv_pairs_from_text(text)

            os.makedirs("sample_runs", exist_ok=True)

            save_json(items, "sample_runs/extracted.json")
            write_to_excel(items, "sample_runs/Output.xlsx")

            st.success("Output.xlsx generated!")

            with open("sample_runs/Output.xlsx", "rb") as f:
                st.download_button("Download Output.xlsx", f, "Output.xlsx")
