import json
import string
from collections import defaultdict
from matplotlib import pyplot as plt
from nltk.stem import PorterStemmer
import spacy
import nltk

nltk.download('punkt')
nltk.download('stopwords')
porter_stemmer = PorterStemmer()

# Default Business Id
id_b = 'XWFjKtRGZ9khRGtGg2ZvaA'
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

# Tokenize
for r in reviews:
    tokens = nltk.word_tokenize(r)
    for token in tokens:
        # Add tokens into word frequency dictionary
        word_frequency[token.lower()] += 1
        # Add tokens into stemmed word frequency dictionary
        stemmed_word_frequency[porter_stemmer.stem(token.lower())] += 1

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
    stemmed_word_frequency.pop(e, None)

# Sort word list
word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
stemmed_word_frequency = sorted(stemmed_word_frequency.items(), key=lambda x: x[1], reverse=True)

# Plot
words = []
frequency = []
stemmed_words = []
stemmed_frequency = []

for (k, v) in word_frequency[0:10]:
    words.append(k)
    frequency.append(v)

for (k, v) in stemmed_word_frequency[0:10]:
    stemmed_words.append(k)
    stemmed_frequency.append(v)


def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2. - 0.25, 1.01 * height, '%s' % int(height))


autolabel(plt.bar(range(len(words)), frequency, color='c', align='center', tick_label=words))
plt.title('Word Frequency')
plt.xlabel('Word')
plt.ylabel('Frequency')
plt.show()

autolabel(plt.bar(range(len(stemmed_words)), stemmed_frequency, color='c', align='center',
                  tick_label=stemmed_words))
plt.title('Stemmed Word Frequency')
plt.xlabel('Word')
plt.ylabel('Frequency')
plt.show()
