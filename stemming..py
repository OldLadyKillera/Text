import json
import math
import string
import random
from collections import defaultdict
from matplotlib import pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

nltk.download('punkt')
nltk.download('stopwords')
porter_stemmer = PorterStemmer()

# Select Random number i, search ith row in review json to find its business ID
# print(random.randint(0, 200))

# Random Business Id
# id_b = 'TA1KUSCu8GkWP9w0rmElxw'
id_b = '6Hm2FmfLcU_M91TrZI5htA'

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

# Exclude Stopwords
excluded_words_list = set(stopwords.words('english'))

# Exclude Punctuation
for p in string.punctuation:
    excluded_words_list.add(p)

# Exclude Special Cases
excluded_words_list.add('\'s')
excluded_words_list.add('n\'t')
excluded_words_list.add("''")
excluded_words_list.add("``")
excluded_words_list.add(" ")

# Tokenize
for r in reviews:
    tokens = nltk.word_tokenize(r)
    for token in tokens:
        if token.lower() not in excluded_words_list:
            # Add tokens into word frequency dictionary
            word_frequency[token.lower()] += 1
            # Add tokens into stemmed word frequency dictionary
            stemmed_word_frequency[porter_stemmer.stem(token.lower())] += 1
            if porter_stemmer.stem(token.lower()) == 'like':
                print(token.lower())

# Sort word list
word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
stemmed_word_frequency = sorted(stemmed_word_frequency.items(), key=lambda x: x[1], reverse=True)

# Plot Default parameters
words = []
frequency = []
stemmed_words = []
stemmed_frequency = []

# Store non-stemmed word and log-scale frequency
for (k, v) in word_frequency[0:10]:
    words.append(k)
    frequency.append(math.log2(v))

# Store stemmed word and log-scale frequency
for (k, v) in stemmed_word_frequency[0:10]:
    stemmed_words.append(k)
    stemmed_frequency.append(math.log2(v))


def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2. - 0.25, 1.01 * height, '%s' % int(height))


# Plot non-stemmed word frequency
autolabel(plt.bar(range(len(words)), frequency, color='c', align='center', tick_label=words))
plt.title('Word Frequency')
plt.xlabel('Word')
plt.ylabel('Frequency')
plt.show()

# Plot stemmed word frequency
autolabel(plt.bar(range(len(stemmed_words)), stemmed_frequency, color='c', align='center',
                  tick_label=stemmed_words))
plt.title('Stemmed Word Frequency')
plt.xlabel('Word')
plt.ylabel('Frequency')
plt.show()
