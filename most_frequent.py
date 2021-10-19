import json
import random
import string
from collections import defaultdict
from matplotlib import pyplot as plt
import nltk

nltk.download('averaged_perceptron_tagger')


def random_select():
    # Default List
    review_list = []
    stars = 1
    business_list = []
    lines_contents_list = []
    shuffled_lines_contents_list = []

    # Open File
    file = open('yelp_academic_dataset_review.json', encoding='utf-8')
    # Generate 1-star review-id list
    review_id_list = []
    for line in file:
        line_contents = json.loads(line)
        if line_contents['stars'] == stars:
            lines_contents_list.append(line_contents)
    # Shuffle review_id list
    random_numbers = random.sample(range(0, len(lines_contents_list)), len(lines_contents_list))
    for i in random_numbers:
        business_id = lines_contents_list[i]['business_id']
        if (business_id not in business_list) & (len(review_list) <= 50):
            business_list.append(business_id)
            review_list.append(lines_contents_list[i]['text'])
    return review_list


# Default Business Id
review_id = 'J4a2TuhDasjn2k3wWtHZnQ'

# Business Review List
review = ''

# Open File
file = open('yelp_academic_dataset_review.json', encoding='utf-8')
# For each line, save the text of the review if the business id equals
for line in file:
    line_contents = json.loads(line)
    if line_contents['review_id'] == review_id:
        review = (line_contents['text'])
        break
# Close File
file.close()

word_frequency = defaultdict(int)
tokens = nltk.word_tokenize(review)
tag_tokens = nltk.pos_tag(tokens)
print(tag_tokens)
for i in range(0, len(tokens)-1):
    if (tag_tokens[i][1] == 'JJ') & (tag_tokens[i+1][1] == 'NN'):
        word_frequency[(tag_tokens[i][0], tag_tokens[i+1][0])] += 1
    if (tag_tokens[i][1] == 'NN') & (tag_tokens[i+1][1] == 'JJ'):
        word_frequency[(tag_tokens[i][0], tag_tokens[i+1][0])] += 1
print(word_frequency)
