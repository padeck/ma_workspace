
from collections import Counter
import re
import nltk
from nltk.corpus import stopwords



# Step 2: Get the list of English stop words
stop_words = set(stopwords.words('english'))

# Step 3: Preprocess text (lowercasing, removing punctuation, stop words, and tokenizing)
def preprocess_text(text):
    # Convert to lowercase
    text = text.lower()
    # Remove punctuation and non-alphabetic characters using regex
    text = re.sub(r'[^\w\s]', '', text)
    # Split text into individual words (tokenize)
    words = text.split()
    # Remove stop words
    words = [word for word in words if word not in stop_words]
    return words

def get_most_common_words(text_column, n_words=5, preprocessing=True):
    all_words = []
    for text in text_column:
        if preprocessing:
            all_words.extend(preprocess_text(text))
        else:
            all_words.extend(text)
    word_counts = Counter(all_words)
    most_common_words = word_counts.most_common(n_words)
    return most_common_words