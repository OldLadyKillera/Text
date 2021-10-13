import json
import string
from collections import defaultdict
from nltk.corpus import stopwords
import spacy
import nltk

nltk.download('punkt')
nltk.download('stopwords')

# Default Business Id
id_b = '9Bto7mky640ocgezVKSfVg'
# id_b = '9Bto7mky640ocgezVKSfVg'

# Business Review List
reviews = []

# Open File
file = open('yelp_academic_dataset_review.json', encoding='utf-8')
# For each line, save the text of the review if the business id equals
for line in file:
    line_contents = json.loads(line)
    if line_contents['business_id'] == id_b:
        reviews.append(line_contents['text'])
# Close File
file.close()

# Create word frequency dictionary
word_frequency = defaultdict(int)
stemmed_word_frequency = defaultdict(int)

# Tokenize and add tokens into word frequency dictionary
for r in reviews:
    tokens = nltk.word_tokenize(r)
    for token in tokens:
        word_frequency[token.lower()] += 1

# Get rid of stop words and punctuation
en = spacy.load('en_core_web_sm')
excluded_words_list = en.Defaults.stop_words
for p in string.punctuation:
    excluded_words_list.add(p)
excluded_words_list.add('\'s')
excluded_words_list.add('n\'t')
excluded_words_list.add("''")
excluded_words_list.add("``")
for e in excluded_words_list:
    word_frequency.pop(e, None)

# Sort word list
word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
print(word_frequency)


