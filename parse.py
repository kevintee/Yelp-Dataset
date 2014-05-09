#!/usr/bin/env python
"""
    parse.py

    ALL YOUR PARSING NEEDS!
"""
import json

from db import session, User, Business, Tip
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


def import_data_to_sql():
    """
        YOU SHOULD ONLY RUN THIS ONCE
    """
    print "Importing businesses..."
    businesses = load_json('data/yelp_academic_dataset_business.json')
    for b in businesses:
        bid = b['business_id']
        latitude = b['latitude']
        longitude = b['longitude']
        session.add(Business(
            bid=bid,
            latitude=latitude,
            longitude=longitude,
        ))
    session.commit()
    print "Done."

    print "Importing tips..."
    tips = load_json('data/yelp_academic_dataset_tip.json')
    for t in tips:
        bid = t['business_id']
        uid = t['user_id']
        likes = t['likes']
        session.add(Tip(
            bid=bid,
            uid=uid,
            likes=likes
        ))
    session.commit()
    print "Done."

    print "Importing users..."
    users = load_json('data/yelp_academic_dataset_user.json')
    for u in users:
        uid = u['user_id']
        review_count = u['review_count']
        num_fans = u['fans']
        years_elite = len(u['elite'])

        funny = u['votes']['funny']
        useful = u['votes']['useful']
        cool = u['votes']['cool']
        session.add(User(
            uid=uid,
            review_count=review_count,
            num_fans=num_fans,
            years_elite=years_elite,
            funny=funny,
            useful=useful,
            cool=cool
        ))
    session.commit()
    print "Done."


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

        business_id = datum['business_id']

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
        feature_vector.append(fg.generate_average_stars_cluster(idx, business_id))

        feature_vector.append(
            fg.generate_number_of_tips(
                idx, datum['user_id'], business_id)
        )
        feature_vector.append(
            fg.generate_business_latitude(
                idx, business_id)
        )
        feature_vector.append(
            fg.generate_business_longitude(
                idx, business_id)
        )

        X.append(feature_vector)
    return DataSet(X, y)

if __name__ == '__main__':
    #d = create_combined_review_data_set(
    #        'data/yelp_academic_dataset_review_small.json'
    #    )
    pass
