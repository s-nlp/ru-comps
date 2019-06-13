import pandas as pd
from argparse import ArgumentParser
from pymystem3 import Mystem
from tqdm import tqdm

morph = Mystem()

if __name__ == '__main__':
    parser = ArgumentParser(description='Enrich model with UD contexts')
    parser.add_argument('text', help='start text')
    parser.add_argument('compounds_text', help='text with marked compounds')
    args = parser.parse_args()

    comp = pd.read_csv('compounds_select_1000.csv')

    chast1 = list(comp['Часть 1'].values)
    chast2 = list(comp['Часть 2'].values)

    compounds = []
    compounds_reverse = []

    for w1, w2 in zip(chast1, chast2):
        lem_w1 = morph.lemmatize(w1)[0]
        lem_w2 = morph.lemmatize(w2)[0]
        compounds.append(' '.join([lem_w1, lem_w2]))
        compounds_reverse.append(' '.join([lem_w2, lem_w1]))
   
    with open(args.text) as text:
        with open(args.compounds_text, 'w') as text_comp:
            for line in tqdm(text):
                for compound in compounds:
                    if compound in line:
                        line=line.replace(compound, '_'.join(compound.split()))
                for compound in compounds_reverse:
                    if compound in line:
                        line=line.replace(compound, '_'.join(compound.split()[::-1]))
                text_comp.write(line)
