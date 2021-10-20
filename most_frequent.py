import json
import random
import string
from collections import defaultdict
from matplotlib import pyplot as plt
import nltk
from nltk.corpus import stopwords

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


def find_closest_noun(tag_tokens, index):
    count = 50
    forward_noun = []
    backward_noun = []
    forward_distance = 1
    backward_distance = 1

    if index > 0:
        for j in range(index - 1, -1, -1):
            if tag_tokens[j][0] in string.punctuation:
                break
            if ('NN' in tag_tokens[j][1]) & (forward_distance <= count):
                forward_noun.append(tag_tokens[j][0])
                if j > 0:
                    for k in range(j - 1, -1, -1):
                        if 'NN' in tag_tokens[k][1]:
                            forward_noun.append(tag_tokens[k][0])
                        else:
                            break
                break
            forward_distance += 1

    if index < len(tag_tokens) - 1:
        for j in range(index + 1, len(tag_tokens)):
            if tag_tokens[j][0] in string.punctuation:
                break
            if ('NN' in tag_tokens[j][1]) & (backward_distance <= count):
                backward_noun.append(tag_tokens[j][0])
                if j < len(tag_tokens) - 1:
                    for k in range(j + 1, len(tag_tokens) - 1):
                        if 'NN' in tag_tokens[k][1]:
                            backward_noun.append(tag_tokens[k][0])
                        else:
                            break
                break
            backward_distance += 1

    if len(backward_noun) != 0:
        if backward_distance < forward_distance:
            forward_noun = backward_noun
    return forward_noun

# Default Business Id
review_id = '8bFej1QE5LXp4O05qjGqXA'

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
stopwords_list = set(stopwords.words('english'))

sentence_list = nltk.sent_tokenize(review)
for sentence in sentence_list:
    tokens = nltk.word_tokenize(sentence)
    tag_tokens = nltk.pos_tag(tokens)
    counter = len(tag_tokens)
    for tag_token in tag_tokens:
        if tag_token[0] in stopwords_list:
            tag_tokens.remove(tag_token)
    for i in range(0, (len(tag_tokens) - 1)):
        if 'JJ' in tag_tokens[i][1]:
            nouns = find_closest_noun(tag_tokens, i)
            if len(nouns) != 0:
                for noun in nouns:
                    if i > 0:
                        if tag_tokens[i - 1][0].lower() == 'not':
                            word_frequency[('not ' + tag_tokens[i][0], noun)] += 1
                        else:
                            word_frequency[(tag_tokens[i][0], noun)] += 1
print(word_frequency)


# Simplest way to locate adverb-noun pair and noun-adverb pairs
#for i in range(0, len(tokens)-1):
 #   if ('JJ' in tag_tokens[i][1]) & ('NN' in tag_tokens[i+1][1]):
  #      if (i > 0) & (tag_tokens[i - 1][0].lower() == 'not'):
   #         word_frequency[('not ' + tag_tokens[i][0], tag_tokens[i + 1][0])] += 1
    #    else:
     #       word_frequency[(tag_tokens[i][0], tag_tokens[i+1][0])] += 1
    #if ('NN' in tag_tokens[i][1]) & ('JJ' in tag_tokens[i+1][1]):
    #    word_frequency[(tag_tokens[i+1][0], tag_tokens[i][0])] += 1
#print(word_frequency)
