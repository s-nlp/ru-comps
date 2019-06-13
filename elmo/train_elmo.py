import pandas as pd
import numpy as np
from argparse import ArgumentParser
from elmoformanylangs import Embedder
from pymystem3 import Mystem
from scipy import stats
from tqdm import tqdm

morph = Mystem()


def take_a_mean(emb):
    return np.mean(emb, axis=0)

def take_g_mean(emb):
    #print(emb)
    return stats.gmean(np.fabs(emb), axis=0)

def take_h_mean(emb):
    #print(emb)
    return stats.hmean(np.fabs(emb), axis=0)

def take_g_mean(emb):
    #print(emb)
    return stats.gmean(np.fabs(emb), axis=0)

def train_embeds(wordlist, option):
    embs = elmo_embedder.sents2elmo(wordlist)
    
    if option == 'arithmetic':
        return [take_a_mean(emb) for emb in embs]
    if option == 'geometric':
        return [take_g_mean(emb) for emb in embs]
    if option == 'harmonic':
        return [take_h_mean(emb) for emb in embs]
    if option == 'generalized':
        return [take_g_mean(emb) for emb in embs]

if __name__ == '__main__':
    parser = ArgumentParser(description='Enrich model with UD contexts')
    parser.add_argument('option', help='Batch mean option')
    args = parser.parse_args()

    comp = pd.read_csv('embeddings/ref.csv')

    part1 = list(comp['Часть 1'].values)[249:]
    part2 = list(comp['Часть 2'].values)[249:]
    values = list(comp['Класс композициональности'].values)[249:]

    lem_part1 = []
    lem_part2 = []
    compounds = []

    for w1, w2, v in zip(part1, part2, values):
        if v != 2 and v != -1:
            lem_w1 = morph.lemmatize(w1)[0]
            lem_w2 = morph.lemmatize(w2)[0]
            lem_part1.append(lem_w1)
            lem_part2.append(lem_w2)
            compounds.append(' '.join([lem_w1, lem_w2]))

    elmo_embedder = Embedder(model_dir = 'elmo_170')

    with open('elmo_word_embeds.txt', 'w') as embeds_dump:
        embs_part1 = train_embeds(lem_part1, args.option)
        for w, emb in zip(lem_part1, embs_part1):
            embeds_dump.write(w +  ' ' + ' '.join(emb.astype(str)) + '\r\n')

        embs_part2 = train_embeds(lem_part2, args.option)
        for w, emb in zip(lem_part2, embs_part2):
            embeds_dump.write(w +  ' ' + ' '.join(emb.astype(str)) + '\r\n')

    with open('elmo_comp_embeds.txt', 'w') as embeds_dump:
        embs_comps = train_embeds(compounds, args.option)
        for c, emb in zip(compounds, embs_comps):
            embeds_dump.write('_'.join(c.split()) +  ' ' + ' '.join(emb.astype(str)) + '\r\n')
    