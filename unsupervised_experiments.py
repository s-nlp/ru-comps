import pandas as pd
import numpy as np
from scipy.stats import spearmanr
from scipy.spatial import distance
from pymystem3 import Mystem
from argparse import ArgumentParser


morph = Mystem()

def acquiring(wordvecs, compvecs, pos):
    if pos == 'nouns':    
	comp = pd.read_csv('compounds_NN_top10000_annotated.csv')
    else:
	comp = pd.read_csv('compounds_AN_top10000_annotated.csv')

    part1 = list(comp['Часть 1'].values)
    part2 = list(comp['Часть 2'].values)
    values = list(comp['Класс композициональности'].values)

    compounds = []
    classes = []

    for w1, w2, v in zip(part1, part2, values):
        if v != 2:
            lem_w1 = morph.lemmatize(w1)[0]
            lem_w2 = morph.lemmatize(w2)[0]
            compounds.append('_'.join([lem_w1, lem_w2]))
            classes.append(v)

    vecs1 = []
    vecs2 = []
    vecsc = []
    true_comp_class = []

    words = []
    comps = []
    
    with open(wordvecs) as w:
        for line in w:
            words.append(line.split())

    with open(compvecs) as c:
        for line in c:
            comps.append(line.split())

    for compound, value in zip(compounds, values):
        comp_flag = 0
        w1_flag = 0
        w2_flag = 0
        for line in comps:
            if compound == line[0]:
                vecc = np.array(line[1:]).astype(np.float32)
                comp_flag = 1
        w1 = compound.split('_')[0]
        w2 = compound.split('_')[1]
        if comp_flag:
            for line in words:
                if w1 == line[0]:
                    vec1 = np.array(line[1:]).astype(np.float32)
                    w1_flag = 1
                    break
            for line in words:
                if w2 == line[0]:
                    w2_flag = 1
                    vec2 = np.array(line[1:]).astype(np.float32)
                    break
        if comp_flag and w1_flag and w2_flag:
            vecs1.append(vec1)
            vecs2.append(vec2)
            vecsc.append(vecc)
            true_comp_class.append(value)

    print(len(vecsc), 'examples retrieved for experiment')
    return vecs1, vecs2, vecsc, true_comp_class


def get_mean(part1_vecs, part2_vecs):
    parts_mean = []
    for vec1, vec2 in zip(part1_vecs, part2_vecs):
        parts_mean.append((vec1 + vec2) / 2)

    return parts_mean


def cosine_between_parts_and_compound(part1_vecs, part2_vecs, comp_vecs, true_class):
    parts_mean = get_mean(part1_vecs, part2_vecs)

    cosines = []
    for w, c in zip(parts_mean, comp_vecs):
        cosines.append(abs(1 - distance.cosine(w, c)))
    print(spearmanr(cosines, true_class)[0])


def chebyshev_between_parts_and_compound(part1_vecs, part2_vecs, comp_vecs, true_class):
    parts_mean = get_mean(part1_vecs, part2_vecs)

    chebyshevs = []
    for w, c in zip(parts_mean, comp_vecs):
        chebyshevs.append(abs(distance.chebyshev(w, c)))
    print(spearmanr(chebyshevs, true_class)[0])


def manhattan_between_parts_and_compound(part1_vecs, part2_vecs, comp_vecs, true_class):
    parts_mean= get_mean(part1_vecs, part2_vecs)

    manhattans = []
    for w, c in zip(parts_mean, comp_vecs):
        manhattans.append(abs(distance.cityblock(w, c)))
    print(spearmanr(manhattans, true_class)[0])


def euclidean_between_parts_and_compound(part1_vecs, part2_vecs, comp_vecs, true_class):
    parts_mean= get_mean(part1_vecs, part2_vecs)

    euclideans = []
    for w, c in zip(parts_mean, comp_vecs):
        euclideans.append(abs(distance.euclidean(w, c)))
    print(spearmanr(euclideans, true_class)[0])


if __name__ == '__main__':
    parser = ArgumentParser(description='Unsupervised metrics experiment')
    parser.add_argument('wordvecs', help='word vectors dump')
    parser.add_argument('compvecs', help='compounds vectors dump')
    args = parser.parse_args()

    w1, w2, c, true = acquiring(args.wordvecs, args.compvecs, 'nouns')

    cosine_between_parts_and_compound(w1, w2, c, true)
    chebyshev_between_parts_and_compound(w1, w2, c, true)
    manhattan_between_parts_and_compound(w1, w2, c, true)
    euclidean_between_parts_and_compound(w1, w2, c, true)
