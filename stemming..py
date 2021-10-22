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

# Random Selection


# Select Random number i, search ith row in review json to find its business ID
# print(random.randint(0, 200))

# Random Business Id
def random_select_business():
    business_id_list = []
    file = open('yelp_academic_dataset_review.json', encoding='utf-8')
    for line in file:
        line_contents = json.loads(line)
        business_id_list.append(line_contents['business_id'])
    file.close()
    random_ids = random.sample(range(0, len(business_id_list) - 1), 2)

    # Close file
    file.close()
    return [business_id_list[random_ids[0]], business_id_list[random_ids[1]]]


def get_business_review(business_id):
    review = []
    # Open File
    file = open('yelp_academic_dataset_review.json', encoding='utf-8')
    # For each line, save the text of the review if the business id equals
    for line in file:
        line_contents = json.loads(line)
        if line_contents['business_id'] == business_id:
            review.append(line_contents['text'])
    # Close file
    file.close()
    return review


def plot_fre_distribution(ranks, fre, stemmed_ranks, stemmed_fre, color, stemmed_color):
    plt.figure(figsize=(8, 6), dpi=80)
    plt.loglog(ranks, fre, color)
    plt.loglog(stemmed_ranks, stemmed_fre, stemmed_color)

    plt.xlabel('rank', fontsize=20, fontweight='bold')
    plt.ylabel('frequency', fontsize=20, fontweight='bold')
    plt.legend(['Not Stemming', 'Stemming'], prop={'size': 20})
    plt.title('Word frequency distribution', fontsize=20, fontweight='bold')
    plt.tight_layout()
    plt.show()


# Create word frequency dictionary
b1_word_frequency = defaultdict(int)
b1_stemmed_word_frequency = defaultdict(int)
b2_word_frequency = defaultdict(int)
b2_stemmed_word_frequency = defaultdict(int)

# Excluded words list
excluded_words_list = set(stopwords.words('english'))
excluded_words_list.add('\'s')
excluded_words_list.add('n\'t')
excluded_words_list.add("''")
excluded_words_list.add("``")

# Generate 2 Random business id
business_ids = random_select_business()
b1_id = business_ids[0]
b2_id = business_ids[1]

# Business Review List
b1_reviews = get_business_review(b1_id)
b2_reviews = get_business_review(b2_id)

# Lower case, get rid of the effects of different cases
b1_reviews = [i.lower() for i in b1_reviews]
b2_reviews = [i.lower() for i in b2_reviews]

# Put all reviews of the business together
b1_reviews = ' '.join(b1_reviews)
b2_reviews = ' '.join(b2_reviews)

# Tokenization
b1_tokens = nltk.word_tokenize(b1_reviews)
b2_tokens = nltk.word_tokenize(b2_reviews)

# Remove stopwords and punctuation
b1_tokens = [i for i in b1_tokens if i not in string.punctuation]
b1_tokens = [i for i in b1_tokens if i not in excluded_words_list]
b2_tokens = [i for i in b2_tokens if i not in string.punctuation]
b2_tokens = [i for i in b2_tokens if i not in excluded_words_list]

# Add to the normal and stemming dictionary
for token in b1_tokens:
    b1_word_frequency[token] += 1
    b1_stemmed_word_frequency[porter_stemmer.stem(token)] += 1

for token in b2_tokens:
    b2_word_frequency[token] += 1
    b2_stemmed_word_frequency[porter_stemmer.stem(token)] += 1

# Sort
b1_word_frequency = sorted(b1_word_frequency.items(), key=lambda x: x[1], reverse=True)
b2_word_frequency = sorted(b2_word_frequency.items(), key=lambda x: x[1], reverse=True)
b1_stemmed_word_frequency = sorted(b1_stemmed_word_frequency.items(), key=lambda x: x[1], reverse=True)
b2_stemmed_word_frequency = sorted(b2_stemmed_word_frequency.items(), key=lambda x: x[1], reverse=True)

# Plot inputs
b1_words_list = [i[0] for i in b1_word_frequency]
b1_word_frequency_list = [i[1] for i in b1_word_frequency]
b1_ranks = [i+1 for i in range(len(b1_word_frequency))]
b1_stemmed_words_list = [i[0] for i in b1_stemmed_word_frequency]
b1_stemmed_word_frequency_list = [i[1] for i in b1_stemmed_word_frequency]
b1_stemmed_ranks = [i+1 for i in range(len(b1_stemmed_word_frequency))]

b2_words_list = [i[0] for i in b2_word_frequency]
b2_word_frequency_list = [i[1] for i in b2_word_frequency]
b2_ranks = [i+1 for i in range(len(b2_word_frequency))]
b2_stemmed_words_list = [i[0] for i in b2_stemmed_word_frequency]
b2_stemmed_word_frequency_list = [i[1] for i in b2_stemmed_word_frequency]
b2_stemmed_ranks = [i+1 for i in range(len(b2_stemmed_word_frequency))]

# Plot b1
plot_fre_distribution(b1_ranks, b1_word_frequency_list, b1_stemmed_ranks, b1_stemmed_word_frequency_list, 'b-', 'r-')

# Plot b2
plot_fre_distribution(b2_ranks, b2_word_frequency_list, b2_stemmed_ranks, b2_stemmed_word_frequency_list, 'b-', 'r-')

print(b1_word_frequency)
print(b1_stemmed_word_frequency)
print(b2_word_frequency)
print(b2_stemmed_word_frequency)


def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.03*height, "%i" % int(height), fontsize=15, fontweight='bold')


def plot_word_frequency(words, fre, stem):
    plt.figure(figsize=(8, 6), dpi=80)
    autolabel(plt.bar(range(len(words)), fre, color=['orange'], align='center', tick_label=words))
    plt.xticks(fontsize=15, fontweight='bold')
    plt.title(stem + 'Word Frequency', fontsize=20, fontweight='bold')
    plt.xlabel('Word', fontsize=20, fontweight='bold')
    plt.ylabel('Frequency', fontsize=20, fontweight='bold')
    plt.tight_layout()
    plt.show()


plot_word_frequency(b1_words_list[0:10], b1_word_frequency_list[0:10], '')
plot_word_frequency(b1_stemmed_words_list[0:10], b1_stemmed_word_frequency_list[0:10], 'Stemmed ')
plot_word_frequency(b2_words_list[0:10], b2_word_frequency_list[0:10], '')
plot_word_frequency(b2_stemmed_words_list[0:10], b2_stemmed_word_frequency_list[0:10], 'Stemmed ')

