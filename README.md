# Semantic Readability Analyzer

An interactive NLP-powered application that performs sentiment and readability analysis on raw text or article URLs. Built with Python and Streamlit, it allows users to upload datasets, supply custom stopword and dictionary files, and download detailed analysis results in Excel format.

---

## 🔍 What It Does

* Accepts `.csv` or `.xlsx` files with either **text** or **URLs**
* Uses **NLP techniques** to analyze sentiment and structure of the text
* Calculates metrics like **Polarity Score**, **Subjectivity**, **FOG Index**, **Complex Word Count**, etc.
* Allows users to upload multiple stopword files and separate positive/negative dictionaries
* Offers real-time previews and Excel export of results

---

## 📊 Key Metrics Computed

* **Positive Score / Negative Score**
* **Polarity Score**: `(pos - neg) / (pos + neg)`
* **Subjectivity Score**: `(pos + neg) / total_words`
* **Avg Sentence Length**
* **Percentage of Complex Words** (words with > 2 syllables)
* **FOG Index**
* **Syllables Per Word**
* **Personal Pronouns Count**
* **Avg Word Length**

---

## 🧠 How This Project Uses NLP

* **Tokenization** (NLTK) to split text into words and sentences
* **Stopword Removal** using custom files to clean text
* **Lexicon-based Sentiment Analysis** with user-defined dictionaries
* **Regex-based Parsing** for pronouns and syllables
* **Structural Readability Metrics** using psycholinguistic heuristics (e.g., FOG index)

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/semantic-readability-analyzer.git
cd semantic-readability-analyzer
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run streamlit_app.py
```

---

## 📂 Project Structure

```
semantic-readability-analyzer/
├── streamlit_app.py            # Main UI logic
├── analyzer.py                 # All NLP logic and metric computations
├── scraper.py                  # Article extraction from URLs
├── requirements.txt            # Python dependencies
```

---

## 📥 Inputs Expected

* `.csv` or `.xlsx` file with a **text** or **URL** column
* One or more `.txt` stopword files
* One `.txt` positive dictionary file
* One `.txt` negative dictionary file

---

## 📤 Output

* Preview of top 10 analyzed rows
* Downloadable `.xlsx` file with all computed scores

---

## 📦 Tech Stack

* Python 3.10+
* Streamlit
* Pandas
* BeautifulSoup
* NLTK

---

## 🧪 Sample Use Cases

* Financial sentiment analysis on scraped articles
* Readability scoring for educational or legal text
* Preprocessing engine for larger NLP pipelines

---

## 👤 Author

**Chirag Dahiya**

> This project reflects my interest in building practical NLP applications that combine rule-based linguistics with usable, deployable tools.

---

## 📃 License

MIT License. Feel free to use, modify, and build on top of this project.
