import os
import tempfile
import streamlit as st
import pandas as pd

from analyzer import analyze_text
from scraper import extract_article

if "dis" not in st.session_state:
    st.session_state.dis = True
st.set_page_config(page_title="Text | URL Analyzer", layout="wide")
st.title("🧠 Universal Text & URL Analyzer (Sentiment + Readability)")

col1,col2,col3,col4 = st.columns(4)
# Upload input dataset
uploaded_file = col1.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    dis = False
# Upload multiple stopword files
stopword_files = col2.file_uploader("Upload StopWords files (.txt)", type="txt", accept_multiple_files=True,disabled=dis)

# Upload dictionary files
positive_dict = col3.file_uploader("Upload Positive Words Dictionary (.txt)", type="txt",disabled=dis,accept_multiple_files=True)
negative_dict = col4.file_uploader("Upload Negative Words Dictionary (.txt)", type="txt",disabled=dis,accept_multiple_files=True)

# Load stopwords from uploaded files
def load_uploaded_stopwords(files):
    stopwords = set()
    for file in files:
        lines = file.read().decode("utf-8", errors="ignore").splitlines()
        for line in lines:
            word = line.strip().split("|")[0].lower()
            if word:
                stopwords.add(word)
    return stopwords

# Load dictionary words
def load_dict(file):
    if file is None:
        return set()
    return set(file.read().decode("utf-8", errors="ignore").split())

if uploaded_file:
    ext = uploaded_file.name.split('.')[-1]
    df = pd.read_csv(uploaded_file) if ext == "csv" else pd.read_excel(uploaded_file)
    st.success("✅ File uploaded successfully!")
    st.dataframe(df.head())

    column_name = st.selectbox("Select the column to analyze (text or URL):", df.columns)

    if st.button("Run Analysis"):
        st.info("⏳ Running analysis...")

        stopwords = load_uploaded_stopwords(stopword_files) if stopword_files else set()
        pos_words = load_dict(positive_dict)
        neg_words = load_dict(negative_dict)

        results = []
        for idx, row in df.iterrows():
            raw = row[column_name]
            is_url = isinstance(raw, str) and raw.startswith(("http://", "https://"))
            text = extract_article(raw) if is_url else str(raw)
            scores = analyze_text(text, stopwords, pos_words, neg_words)
            for col in ["URL_ID", "URL"]:
                if col in df.columns:
                    scores[col] = row[col]

            results.append(scores)

        result_df = df.copy()
        result_df = result_df.assign(**pd.DataFrame(results))

        ordered_cols = [
            "URL_ID", "URL", "POSITIVE SCORE", "NEGATIVE SCORE", "POLARITY SCORE", "SUBJECTIVITY SCORE",
            "AVG SENTENCE LENGTH", "PERCENTAGE OF COMPLEX WORDS", "FOG INDEX",
            "AVG NUMBER OF WORDS PER SENTENCE", "COMPLEX WORD COUNT", "WORD COUNT",
            "SYLLABLE PER WORD", "PERSONAL PRONOUNS", "AVG WORD LENGTH"
        ]
        result_df = result_df[[col for col in ordered_cols if col in result_df.columns]]

        st.success("✅ Analysis complete!")
        st.dataframe(result_df.head(10))

        output_path = os.path.join(tempfile.gettempdir(), "output_results.xlsx")
        result_df.to_excel(output_path, index=False)

        with open(output_path, "rb") as f:
            st.download_button(
                label="📥 Download Full Results as Excel",
                data=f,
                file_name="output_results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
