import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import nltk

nltk.download('stopwords')
nltk.download('punkt')

def clean_text(text):
    """
    Cleans the text by removing HTML tags, special characters, and stop words.
    """
    # Remove HTML tags
    text = BeautifulSoup(text, "html.parser").get_text()

    # Remove special characters and punctuation
    text = re.sub(r'[^a-zA-Z\s]', '', text, re.I|re.A)

    # Tokenize the text
    tokens = word_tokenize(text.lower())

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]

    # Stemming (optional)
    stemmer = PorterStemmer()
    stemmed_tokens = [stemmer.stem(w) for w in tokens]

    return " ".join(stemmed_tokens)
