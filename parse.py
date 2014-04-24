#!/usr/bin/env python
"""
    parse.py

    ALL YOUR PARSING NEEDS!
"""
import json
from textblob import TextBlob


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
    for datum in data:
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
        blob = TextBlob(datum['text'])

        feature_vector.append(len(blob))
        feature_vector.append(blob.sentiment.polarity)
        feature_vector.append(blob.sentiment.subjectivity)

        words = [x.singularize() for x in blob.lower().words]
        # TODO: add features of selected word counts
        #       need to do some processing to figure out which words matter

        # Add feature vector to list of feature vectors
        X.append(feature_vector)
    return DataSet(X, y)

if __name__ == '__main__':
    d = create_combined_review_data_set(
            'data/yelp_academic_dataset_review.json'
        )
