import re
import random
import pickle
import collections



class Generator:
    def __init__(self, file, n_sens, seed):
        self.file = file
        self.n_sens = n_sens  # number of sentences
        self.seed = seed

    def fit(self):
        text = open(self.file, 'r')
        text = text.read().lower()

        # cleaning text to count sentences
        text = re.sub('[^A-Za-z?!. ]', '', text)

        sentences = re.split('[?!.]', text)

        # making the list of lengths of sentences and list of endings and beginnings
        len_s = []  # Length of sentences
        endings = []
        beginnings = []
        for i in range(len(sentences)):
            sentence = sentences[i].split(' ')
            endings.append(sentence[-1])
            beginnings.append(sentence[0])
            c = 0
            for word in sentence:
                c += 1
            len_s.append(c)
        beginnings = list(filter(None, beginnings))
        endings = list(filter(None, endings))

        mean = sum(len_s) / len(len_s)
        common = dict(collections.Counter(len_s).most_common(15)).keys()  # the most frequent numbers of words
        common = list(common)
        common.append(round(mean))


        # Clearing the text to generate keys
        text = re.sub('[^a-zA-Zа-яА-Я ]+', '', text).split()
        text = list(filter(None, text))

        keys = {}
        for i in range(len(text) - 1):
            if text[i] not in keys:
                keys[text[i]] = []
                keys[text[i]].append(text[i + 1])
            else:
                keys[text[i]].append(text[i + 1])

        with open('keys.pkl', 'wb') as f:
            pickle.dump(keys, f)

        with open('common.pkl', 'wb') as f:
            pickle.dump(common, f)

        with open('endings.pkl', 'wb') as f:
            pickle.dump(endings, f)

        with open('beginnings.pkl', 'wb') as f:
            pickle.dump(beginnings, f)

    def generate(self):

        with open('keys.pkl', 'rb') as f:
            keys = pickle.load(f)

        with open('common.pkl', 'rb') as f:
            common = pickle.load(f)

        with open('endings.pkl', 'rb') as f:
            endings = pickle.load(f)

        with open('beginnings.pkl', 'rb') as f:
            beginnings = pickle.load(f)

        self.seed = self.seed.lower()
        new_text = self.seed.capitalize()
        new_text += ' ' + random.choice(keys[self.seed])

        # generating the new text
        for s in range(self.n_sens - 1):  #
            for i in range(random.choice(common) - 4):
                new_text += ' ' + random.choice(keys[new_text.split()[-1]]) + ' '
            key_of_end = random.choice(keys[new_text.split()[-1]])  # key of the last word in sentence
            new_text += key_of_end + ' '
            true_endings = []  # list with endings that suit values from keys
            for e in endings:
                if e in keys[key_of_end]:
                    true_endings.append(e)
            new_text += random.choice(true_endings) + '. '

            if s != (self.n_sens - 1):  # starting the new sentence
                beginning = random.choice(beginnings)
                new_text += beginning.capitalize() + ' ' + random.choice(keys[beginning])
        new_text += '.'

        print(new_text)


t = Generator('The_Hunger_Games.txt', 3, 'i')
t.fit()
t.generate()
