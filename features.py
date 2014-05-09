from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from textblob import TextBlob

from db import session, Tip, Business, User

NUM_CLUSTERS = 10

class FeatureGenerator(object):

    def __init__(self, data):
        # Generate text and stars
        self.blobs = []
        self.stars = []
        self.business_stars = {}
        for datum in data:
            blob = TextBlob(datum['text'])
            self.blobs.append(blob)
            self.stars.append(int(datum['stars']))
            self.business_stars[datum['business_id']] = int(datum['stars'])

        # Generate common words
        self.common_words = [self._get_star_words(x) for x in range(1, 6)]

        # Generate business coordinates
        self.business_coordinates = {}
        businesses = session.query(Business).all()
        for business in businesses:
            if business.bid in self.business_stars:
                latitude = float(business.latitude)
                longitude = float(business.longitude)
                self.business_coordinates[business.bid] = (latitude, longitude)
        self.clustering = KMeans(n_clusters=NUM_CLUSTERS)
        self.average_value = [0]*NUM_CLUSTERS
        self.num_businesses = [0]*NUM_CLUSTERS
        self._clustering_businesses()

    def get_blob(self, idx):
        return self.blobs[idx]

    def generate_length(self, idx):
        return len(self.blobs[idx])

    def generate_num_sentences(self, idx):
        return len(self.blobs[idx].sentences)

    def generate_avg_sentence_len(self, idx):
        total_len =  sum([len(s) for s in self.blobs[idx].sentences])
        return float(total_len) / float(len(self.blobs[idx].sentences))

    def generate_polarity(self, idx):
        return self.blobs[idx].polarity

    def generate_subjectivity(self, idx):
        return self.blobs[idx].subjectivity

    def generate_count_exclamation(self, idx):
        return sum([1 for ch in self.blobs[idx].raw if ch == '!'])

    def generate_punctuation_to_sentence_ratio(self, idx):
        count = sum([1 for ch in self.blobs[idx].raw if ch in ['!', '.', '?']])
        return float(count) / float(len(self.blobs[idx].sentences))

    def generate_number_of_all_cap_words(self, idx):
        all_caps_count = 0
        for word in self.blobs[idx].words:
            if word.upper() == word and len(word) > 1:
                all_caps_count += 1
        return all_caps_count

    def generate_similarity_between_words(self, idx, num_stars):
        words = self.common_words[num_stars-1]
        score = 0
        length = len(self.blobs[idx].words)
        for word in self.blobs[idx].words:
            if word in words:
                score += words[word]
        return float(score) / (length * words.values()[0])

    def _get_star_words(self, num_stars):
        words = {}
        stop = stopwords.words('english')
        for star, blob in zip(self.stars, self.blobs):
            if star == num_stars:
                for word in blob.words:
                    word = word.lower()
                    if word in words:
                        words[word] += 1
                    else:
                        words[word] = 1
        words = sorted(words.items(), key=lambda x: x[1])
        words.reverse()
        words = [x for x in words if x[0] not in stop]
        words = [x for x in words if "'" not in x[0]]
        words = words[:50]
        return dict(words)

    def generate_number_of_tips(self, idx, uid, bid):
        return len(
            session.query(Tip).filter(
                Tip.bid == bid
            ).filter(
                Tip.uid == uid
            ).all()
        )

    def generate_business_latitude(self, idx, bid):
        return self.business_coordinates[bid][0]

    def generate_business_longitude(self, idx, bid):
        return self.business_coordinates[bid][1]

    def _clustering_businesses(self):
        total_stars = [0]*NUM_CLUSTERS
        predict = self.clustering.fit_predict(self.business_coordinates.values())
        business_ids = self.business_coordinates.keys()
        for i,p in enumerate(predict):
            if business_ids[i] in self.business_stars:
                total_stars[p] += self.business_stars[business_ids[i]]
                self.num_businesses[p] += 1
        self.average_value = [float(x) / y if y > 0 else 0 for x,y in
                zip(total_stars, self.num_businesses)]

    def generate_average_stars_cluster(self, idx, bid):
        prediction = self.clustering.predict(self.business_coordinates[bid])[0]
        return self.average_value[prediction]

    def generate_num_businesses_in_area(self, idx, bid):
        prediction = self.clustering.predict(self.business_coordinates[bid])[0]
        return self.num_businesses[prediction]

