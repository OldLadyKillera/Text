import json
import random
import string
from collections import defaultdict
from matplotlib import pyplot as plt
import nltk
from nltk.corpus import stopwords

nltk.download('averaged_perceptron_tagger')


# Return num_reviews of reviews of unique business with stars = input stars
def random_select(stars, num_reviews):
    # Default List
    review_list = []
    business_list = []
    lines_contents_list = []
    content_list = []

    # Open File
    file = open('yelp_academic_dataset_review.json', encoding='utf-8')
    # Generate 1-star review-id list
    for line in file:
        line_contents = json.loads(line)
        if line_contents['stars'] == stars:
            lines_contents_list.append(line_contents)
    # Shuffle review_id list
    random_numbers = random.sample(range(0, len(lines_contents_list)), 2000)
    for i in random_numbers:
        # Get random business
        business_id = lines_contents_list[i]['business_id']
        # Make sure unique business
        if (business_id not in business_list) & (len(review_list) < num_reviews):
            business_list.append(business_id)
            review_list.append(lines_contents_list[i]['review_id'])
            content_list.append(lines_contents_list[i]['text'])
    print(business_list)
    print(review_list)
    print(content_list)
    return review_list


# Find the closest noun of a given tag_tokens and the location of the input adjective
def find_closest_noun(tag_tokens, index):
    # The largest distance of searching  the target noun
    count = 20
    # List of nouns by searching forward
    forward_noun = []
    # List of nouns by searching backward
    backward_noun = []
    # The distance of the closest noun by searching forward
    forward_distance = 1
    # The distance of the closest noun by searching backward
    backward_distance = 1

    # Searching forward (Back to front)
    if index > 0:
        for j in range(index - 1, -1, -1):
            # If searching meets a punctuation, searching stops
            if tag_tokens[j][0] in string.punctuation:
                break
            # Find the first noun of the searching
            if ('NN' in tag_tokens[j][1]) & (forward_distance <= count):
                forward_noun.append(tag_tokens[j][0])
                # Solving an adjective modifies multiple nouns
                if j > 0:
                    for k in range(j - 1, -1, -1):
                        if 'NN' in tag_tokens[k][1]:
                            forward_noun.append(tag_tokens[k][0])
                        else:
                            break
                break
            forward_distance += 1

    # Searching backward (Front to back)
    if index < len(tag_tokens) - 1:
        for j in range(index + 1, len(tag_tokens)):
            # If searching meets a punctuation, searching stops
            if tag_tokens[j][0] in string.punctuation:
                break
            # Find the first noun of the searching
            if ('NN' in tag_tokens[j][1]) & (backward_distance <= count):
                backward_noun.append(tag_tokens[j][0])
                # Solving an adjective modifies multiple nouns
                if j < len(tag_tokens) - 1:
                    for k in range(j + 1, len(tag_tokens) - 1):
                        if 'NN' in tag_tokens[k][1]:
                            backward_noun.append(tag_tokens[k][0])
                        else:
                            break
                break
            backward_distance += 1

    # Decide to use forward or backward searching results
    if len(backward_noun) != 0:
        if backward_distance < forward_distance:
            forward_noun = backward_noun
    return forward_noun


def find_pair(review_id, word_frequency):
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

    stopwords_list = set(stopwords.words('english'))
    sentence_list = nltk.sent_tokenize(review)
    # Search by each sentence
    for sentence in sentence_list:
        tokens = nltk.word_tokenize(sentence)
        # Get the POS TAG of the sentence tokens
        tag_tokens = nltk.pos_tag(tokens)
        # Get rid of stopwords
        for tag_token in tag_tokens:
            if tag_token[0] in stopwords_list:
                tag_tokens.remove(tag_token)
        # Locate all adjectives
        for i in range(0, (len(tag_tokens) - 1)):
            if 'JJ' in tag_tokens[i][1]:
                # Each adjective pairs up with its closest noun
                nouns = find_closest_noun(tag_tokens, i)
                # There is a noun in the sentence
                if len(nouns) != 0:
                    for noun in nouns:
                        if i > 0:
                            # Solve 'not adjective + noun' problem
                            if tag_tokens[i - 1][0].lower() == 'not':
                                word_frequency[('not ' + tag_tokens[i][0], noun)] += 1
                            # Solve 'not verb adjective + noun' problem
                            elif (i > 1) & (tag_tokens[i - 2][0].lower() == 'not'):
                                word_frequency[('not ' + tag_tokens[i][0], noun)] += 1
                            else:
                                word_frequency[(tag_tokens[i][0], noun)] += 1


# Create word frequency dictionary
word_frequency = defaultdict(int)

# 1 star review Id
review_id_list = random_select(1, 50)
if len(review_id_list) != 50:
    print("OMG, 2000 is not enough")

# 2 star review Id
# review_id_list = random_select(2, 20)
# if len(review_id_list) != 20:
#    print("OMG, 2000 is not enough")

# 3 star review Id
# review_id_list = random_select(3, 20)
# if len(review_id_list) != 20:
#     print("OMG, 2000 is not enough")

# 4 star review Id
# review_id_list = random_select(4, 20)
# if len(review_id_list) != 20:
#    print("OMG, 2000 is not enough")

# 5 star review Id
# review_id_list = random_select(5, 20)
# if len(review_id_list) != 20:
#    print("OMG, 2000 is not enough")

for review in review_id_list:
    find_pair(review, word_frequency)

# Sort word frequency dictionary
word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
print(word_frequency)


# Simplest way to locate adverb-noun pair and noun-adverb pairs
# for i in range(0, len(tokens)-1):
#   if ('JJ' in tag_tokens[i][1]) & ('NN' in tag_tokens[i+1][1]):
#      if (i > 0) & (tag_tokens[i - 1][0].lower() == 'not'):
#         word_frequency[('not ' + tag_tokens[i][0], tag_tokens[i + 1][0])] += 1
#    else:
#       word_frequency[(tag_tokens[i][0], tag_tokens[i+1][0])] += 1
# if ('NN' in tag_tokens[i][1]) & ('JJ' in tag_tokens[i+1][1]):
#    word_frequency[(tag_tokens[i+1][0], tag_tokens[i][0])] += 1
# print(word_frequency)
