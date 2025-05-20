import os
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

# Download the Punkt tokenizer model (only once per machine)
nltk.download('punkt_tab')

# Load stopwords from a folder containing multiple .txt files
def load_stopwords(folder_path="default_resources/StopWords"):
    stopwords = set()
    for fname in os.listdir(folder_path):
        full_path = os.path.join(folder_path, fname)
        if os.path.isfile(full_path):  # ✅ Skip folders
            with open(full_path, "r", encoding="ISO-8859-1") as f:
                for line in f:
                    word = line.strip().split('|')[0].strip().lower()
                    if word:
                        stopwords.add(word)
    return stopwords


# Load positive and negative word dictionaries
def load_master_dict(path="default_resources/MasterDictionary"):
    pos_words, neg_words = set(), set()

    for fname in os.listdir(path):
        full_path = os.path.join(path, fname)
        if not os.path.isfile(full_path):
            continue  # ✅ Skip folders

        if "positive" in fname.lower():
            with open(full_path, encoding="ISO-8859-1") as f:
                pos_words.update(f.read().split())

        elif "negative" in fname.lower():
            with open(full_path, encoding="ISO-8859-1") as f:
                neg_words.update(f.read().split())

    return pos_words, neg_words


# Clean text, remove punctuation, tokenize, and remove stopwords
def clean_and_tokenize(text, stopwords):
    text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
    tokens = word_tokenize(text)
    return [w.lower() for w in tokens if w.lower() not in stopwords]

# Count syllables per word
def count_syllables(word):
    word = word.lower()
    count = len(re.findall(r'[aeiouy]+', word))
    if word.endswith(("es", "ed")):
        count -= 1
    return max(1, count)

# Count personal pronouns from a text
def count_personal_pronouns(text):
    matches = re.findall(r"\b(I|we|my|ours|us)\b", text, flags=re.IGNORECASE)
    return len([m for m in matches if m.lower() != "us" or not re.search(r'\bUS\b', text)])

# Perform full sentiment + readability analysis
def analyze_text(text, stopwords, pos_words, neg_words):
    tokens = clean_and_tokenize(text, stopwords)
    sentences = sent_tokenize(text)

    pos_score = sum(1 for w in tokens if w in pos_words)
    neg_score = sum(-1 for w in tokens if w in neg_words)
    neg_score *= -1  # to make it positive, per spec

    polarity = (pos_score - neg_score) / ((pos_score + neg_score) + 1e-6)
    subjectivity = (pos_score + neg_score) / (len(tokens) + 1e-6)

    total_words = len(tokens)
    total_sentences = len(sentences)
    avg_sent_len = total_words / total_sentences if total_sentences > 0 else 0

    complex_words = [w for w in tokens if count_syllables(w) > 2]
    complex_count = len(complex_words)
    pct_complex = complex_count / total_words if total_words > 0 else 0
    fog_index = 0.4 * (avg_sent_len + pct_complex)

    syllables_per_word = sum(count_syllables(w) for w in tokens) / total_words if total_words > 0 else 0
    avg_word_len = sum(len(w) for w in tokens) / total_words if total_words > 0 else 0
    personal_pronouns = count_personal_pronouns(text)

    return {
        "POSITIVE SCORE": pos_score,
        "NEGATIVE SCORE": neg_score,
        "POLARITY SCORE": polarity,
        "SUBJECTIVITY SCORE": subjectivity,
        "AVG SENTENCE LENGTH": avg_sent_len,
        "PERCENTAGE OF COMPLEX WORDS": pct_complex,
        "FOG INDEX": fog_index,
        "AVG NUMBER OF WORDS PER SENTENCE": avg_sent_len,
        "COMPLEX WORD COUNT": complex_count,
        "WORD COUNT": total_words,
        "SYLLABLE PER WORD": syllables_per_word,
        "PERSONAL PRONOUNS": personal_pronouns,
        "AVG WORD LENGTH": avg_word_len
    }
