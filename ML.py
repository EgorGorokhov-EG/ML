import re
import random
import pickle


class Generator:
    def __init__(self, file, length, seed):
        self.file = file
        self.length = length
        self.seed = seed

    def fit(self):
        text = open(self.file, 'r')
        text = text.read().lower()
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

    def generate(self):
        with open('keys.pkl', 'rb') as f:
            keys = pickle.load(f)
        self.seed = self.seed.lower()
        new_text = self.seed.capitalize()
        new_text += ' ' + random.choice(keys[self.seed])
        for i in range(self.length - 2):
            new_text += ' ' + random.choice(keys[new_text.split()[-1]])
        new_text += '.'

        print(new_text)


t = Generator('Jane_Eyre.txt', 5, 'tHe')
t.generate()