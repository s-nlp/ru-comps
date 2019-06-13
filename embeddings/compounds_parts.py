import pandas as pd
from argparse import ArgumentParser
from pymystem3 import Mystem
from tqdm import tqdm
from gensim.models import FastText

morph = Mystem()

if __name__ == '__main__':
    parser = ArgumentParser(description='Enrich model with UD contexts')
    parser.add_argument('model', help='FastText model directory')
    parser.add_argument('vectors', help='where to save vectors')
    args = parser.parse_args()

    comp = pd.read_csv('compounds_select_1000.csv')

    chast1 = list(comp['Часть 1'].values)
    chast2 = list(comp['Часть 2'].values)

    print('loading model')
    model = FastText.load(args.model)
    print('loaded')
    print(len(model.wv.vocab))

    comp_lem = []

    print('Starting lemmatize')

    for w1, w2 in zip(chast1, chast2):
        lem_w1 = morph.lemmatize(w1)[0]
        lem_w2 = morph.lemmatize(w2)[0]
        comp_lem.append(lem_w1 + '_' + lem_w2)

    with open(args.vectors, 'w') as vectors:
        for w1 in comp_lem:
            if w1 in model.wv.vocab:
                vectors.write(w1 + ' ' + ' '.join(model.wv[w1].astype('str')) + '\r\n')
            else:
                print(w1)
