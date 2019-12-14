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
        print(sentences)
        for i in range(len(sentences)):
            sentence = sentences[i].split(' ')
            sentence = list(filter(None, sentence))
            if sentence:
                endings.append(sentence[-1])
                beginnings.append(sentence[0])
            print(sentence)
            c = 0
            for word in sentence:
                c += 1
            len_s.append(c)
        beginnings = list(filter(None, beginnings))
        endings = list(filter(None, endings))

        end_beg = {}  # dict of ends and beginnings of sentences
        for i in range(len(endings) - 2):
            if endings[i] not in end_beg:
                end_beg[endings[i]] = []
                end_beg[endings[i]].append(beginnings[i + 1])
            else:
                end_beg[endings[i]].append(beginnings[i + 1])

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

        with open('end_beg.pkl', 'wb') as f:
            pickle.dump(end_beg, f)

    def generate(self):

        with open('keys.pkl', 'rb') as f:
            keys = pickle.load(f)

        with open('common.pkl', 'rb') as f:
            common = pickle.load(f)

        with open('endings.pkl', 'rb') as f:
            endings = pickle.load(f)

        with open('end_beg.pkl', 'rb') as f:
            end_beg = pickle.load(f)

        self.seed = self.seed.lower()
        new_text = self.seed.capitalize()
        new_text += ' ' + random.choice(keys[self.seed]) + ' '

        # generating the new text
        for s in range(self.n_sens - 1):  #
            for i in range(random.choice(common) - 4):
                new_text += random.choice(keys[new_text.split()[-1]]) + ' '
            key_of_end = random.choice(keys[new_text.split()[-1]])  # key of the last word in sentence
            new_text += key_of_end + ' '
            true_endings = []  # list with endings that suit values from keys
            for e in endings:
                if e in keys[key_of_end]:
                    true_endings.append(e)
            end = random.choice(true_endings)
            new_text += end + '. '

            if s != (self.n_sens - 1):  # starting the new sentence
                beginning = random.choice(end_beg[end])
                new_text += beginning.capitalize() + ' ' + random.choice(keys[beginning]) + ' '
        new_text += '.'

        print(new_text)


file_name = input('Please choose the text to train the generator: ')
sentences = int(input('Now input a number of sentences to generate: '))
seed = input('The first word of the generated text: ')


generator = Generator(file_name, sentences, seed)
generator.fit()
generator.generate()
