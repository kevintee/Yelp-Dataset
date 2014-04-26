from textblob import TextBlob

class FeatureGenerator(object):

    def __init__(self, data):
        self.blobs = []
        self.stars = []
        for datum in data:
            blob = TextBlob(datum['text'])
            self.blobs.append(blob)
            self.stars.append(int(datum['stars']))

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

    def _get_star_words(self, num_stars):
        words = {}
        for star, blob in enumerate(stars, blobs):
            if star == num_stars:
                for word in blob.words:
                    if word in words:
                        words[word] += 1
                    else:
                        words[word] = 1
        words = sorted(words.items(), key=lambda x: x[1])
        words.reverse()
        return words
