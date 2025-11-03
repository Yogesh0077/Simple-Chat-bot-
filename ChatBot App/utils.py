import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob

# Download only if missing
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

# Load stopwords once
stop_words = set(stopwords.words("english"))

# === Clean Text Function ===
def clean_text(text):
    # Remove special characters except basic punctuation
    text = re.sub(r"[^\w\s]", "", text)

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords and lowercase
    tokens = [word.lower() for word in tokens if word.lower() not in stop_words]

    # Optional: Add lemmatization here using nltk.WordNetLemmatizer()

    return " ".join(tokens)

# === Sentiment Analysis using TextBlob ===
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity      # Range: -1 (neg) to 1 (pos)
    subjectivity = blob.sentiment.subjectivity  # Range: 0 (objective) to 1 (subjective)
    return polarity, subjectivity
