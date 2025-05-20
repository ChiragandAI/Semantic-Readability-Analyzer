import os
import tempfile
import streamlit as st
import pandas as pd

from analyzer import analyze_text
from scraper import extract_article

# Initialize session state variables
if "dis" not in st.session_state:
    st.session_state.dis = True
if "df" not in st.session_state:
    st.session_state.df = None 
if "progress" not in st.session_state:
    st.session_state.progress = 0 
if "status" not in st.session_state:
    st.session_state.status = 'running'
if "label_status" not in st.session_state:
    st.session_state.label_status = 'Runnin analysis...'
if "analysis" not in st.session_state:
    st.session_state.analysis = False

# UI Setup
st.set_page_config(page_title="Text | URL Analyzer", layout="wide")
st.title("🧠 Universal Text & URL Analyzer (Sentiment + Readability)")

col1, col2, col3, col4 = st.columns(4)

uploaded_file = col1.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])
if uploaded_file:
    st.session_state.dis = False
else:
    st.session_state.dis = True

stopword_files = col2.file_uploader("Upload StopWords files (.txt)", type="txt", accept_multiple_files=True, disabled=st.session_state.dis)
positive_dict = col3.file_uploader("Upload Positive Words Dictionary (.txt)", type="txt", accept_multiple_files=True, disabled=st.session_state.dis)
negative_dict = col4.file_uploader("Upload Negative Words Dictionary (.txt)", type="txt", accept_multiple_files=True, disabled=st.session_state.dis)

# Helper Functions
def load_uploaded_stopwords(files):
    stopwords = set()
    for file in files:
        lines = file.read().decode("utf-8", errors="ignore").splitlines()
        for line in lines:
            word = line.strip().split("|")[0].lower()
            if word:
                stopwords.add(word)
    return stopwords

def load_dict(files):
    if files is None:
        return set()
    ls = set()
    for file in files:
        lines = file.read().decode("utf-8", errors="ignore").splitlines()
        for line in lines:
            word = line.strip().split("|")[0].lower()
            if word:
                ls.add(word)
    return ls

# File Handling
if uploaded_file:
    ext = uploaded_file.name.split('.')[-1]
    st.session_state.df = pd.read_csv(uploaded_file) if ext == "csv" else pd.read_excel(uploaded_file)
    df = st.session_state.df
    st.success("✅ File uploaded successfully!")
    st.dataframe(df.head())

    column_name = st.selectbox("Select the column to analyze (text or URL):", df.columns)

    if st.button("Run Analysis"):
        st.session_state.analysis = True
        st.status(f"{st.session_state.label_status}", state=st.session_state.status)

        stopwords = load_uploaded_stopwords(stopword_files) if stopword_files else set()
        pos_words = load_dict(positive_dict)
        neg_words = load_dict(negative_dict)

        results = []
        progress_bar = st.empty()
        progress_bar = progress_bar.progress(0.0)

        for idx, row in df.iterrows():
            raw = row[column_name]
            is_url = isinstance(raw, str) and raw.startswith(("http://", "https://"))
            text = extract_article(raw) if is_url else str(raw)

            scores = analyze_text(text, stopwords, pos_words, neg_words)
            for col in ["URL_ID", "URL"]:
                if col in df.columns:
                    scores[col] = row[col]

            results.append(scores)
            if text != '':
                st.session_state.progress = len(results) / df.shape[0]
            progress_bar.progress(st.session_state.progress)

        result_df = df.copy()
        st.session_state.result_df = result_df.assign(**pd.DataFrame(results))

        ordered_cols = list(df.columns) + [
            "POSITIVE SCORE", "NEGATIVE SCORE", "POLARITY SCORE", "SUBJECTIVITY SCORE",
            "AVG SENTENCE LENGTH", "PERCENTAGE OF COMPLEX WORDS", "FOG INDEX",
            "AVG NUMBER OF WORDS PER SENTENCE", "COMPLEX WORD COUNT", "WORD COUNT",
            "SYLLABLE PER WORD", "PERSONAL PRONOUNS", "AVG WORD LENGTH"
        ]
        result_df = result_df[[col for col in ordered_cols if col in result_df.columns]]
        
        st.session_state.output_path = os.path.join(tempfile.gettempdir(), "output_results.xlsx")
        st.session_state.result_df.to_excel(st.session_state.output_path, index=False)
        
        if st.session_state.progress == 1.0:
            st.session_state.status = "complete"
            st.session_state.label_status = "Analysis Complete"
            st.rerun()

        

if st.session_state.analysis:
        st.dataframe(st.session_state.get("result_df",pd.DataFrame()))
        with open(st.session_state.get("output_path"), "rb") as f:
            st.download_button(
                label="📥 Download Full Results as Excel",
                data=f,
                file_name="output_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# Static progress fallback
if not st.session_state.dis:
    st.progress(st.session_state.progress)

# Reset button
if st.button("🔄 Restart App"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
