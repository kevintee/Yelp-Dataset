#!/usr/bin/env python
"""
    parse.py

    ALL YOUR PARSING NEEDS!
"""
import json
from features import FeatureGenerator


class DataSet(object):
    def __init__(self, X, y):
        self.x = X
        self.y = y


def load_json(file_name):
    """
        Returns a list containing dictionaries of the parsed JSON.
    """
    with open(file_name, 'r') as f:
        return [json.loads(line) for line in f.readlines()]


def create_combined_review_data_set(review_file_name):
    """
        Derp
    """
    data = load_json(review_file_name)
    X = []
    y = []

    # Pre-process all features
    fg = FeatureGenerator(data)

    for idx, datum in enumerate(data):
        # Our labels are the star counts
        y.append(int(datum['stars']))

        # Our features are everything else we can get our hands on
        feature_vector = []
        # Add as many features as we can think of
        # Features must be NUMERIC -- ints or floats!
        # DO NOT INCLUDE THE 'STARS' CATEGORY
        feature_vector.append(int(datum['votes']['cool']))
        feature_vector.append(int(datum['votes']['funny']))
        feature_vector.append(int(datum['votes']['useful']))

        # TextBlob processing
        blob = fg.get_blob(idx)


        words = blob.words.lower().singularize()

        # TODO: add features of selected word counts
        #       need to do some processing to figure out which words matter
        #
        #       the feature generation is separated into a separate class
        #       because some features may need to reference the context of
        #       the entire dataset before determining it's features
        #       (e.g. counts of words that are most widespread across all data)
        #
        #       feature generation can potentially look up yelp user accounts
        #       which should be done through the FeatureGenerator class

        # Add feature vector to list of feature vectors
        feature_vector.append(fg.generate_subjectivity(idx))
        feature_vector.append(fg.generate_polarity(idx))
        feature_vector.append(fg.generate_length(idx))
        feature_vector.append(fg.generate_num_sentences(idx))
        feature_vector.append(fg.generate_avg_sentence_len(idx))
        feature_vector.append(fg.generate_count_exclamation(idx))
        feature_vector.append(fg.generate_punctuation_to_sentence_ratio(idx))
        feature_vector.append(fg.generate_number_of_all_cap_words(idx))
        feature_vector.append(fg.generate_similarity_between_words(idx, 1))
        feature_vector.append(fg.generate_similarity_between_words(idx, 2))
        feature_vector.append(fg.generate_similarity_between_words(idx, 3))
        feature_vector.append(fg.generate_similarity_between_words(idx, 4))
        feature_vector.append(fg.generate_similarity_between_words(idx, 5))

        X.append(feature_vector)
    return DataSet(X, y)

if __name__ == '__main__':
    d = create_combined_review_data_set(
            'data/yelp_academic_dataset_review_small.json'
        )
