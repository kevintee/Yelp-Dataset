from nltk.corpus import stopwords
from textblob import TextBlob

class FeatureGenerator(object):

    def __init__(self, data):
        self.blobs = []
        self.stars = []
        for datum in data:
            blob = TextBlob(datum['text'])
            self.blobs.append(blob)
            self.stars.append(int(datum['stars']))
        self.common_words = [self._get_star_words(x) for x in range(1, 6)]

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
        for word in self.blobs[idx].words:
            if word in words:
                score += words[word]
        return score

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
