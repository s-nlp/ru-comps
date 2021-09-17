import pandas as pd
import numpy as np
import warnings
from argparse import ArgumentParser
from pymystem3 import Mystem
from scipy.stats import spearmanr
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from tqdm import tqdm

morph = Mystem()


def acquiring(wordvecs, compvecs, pos):
    if pos == 'nouns':    
	comp = pd.read_csv('compounds_NN_top10000_annotated.csv')
    else:
	comp = pd.read_csv('compounds_AN_top10000_annotated.csv')

    part1 = list(comp['Часть 1'].values)[250:]
    part2 = list(comp['Часть 2'].values)[250:]
    values = list(comp['Композициональность'].values)[250:]

    compounds = []
    classes = []

    for w1, w2, v in zip(part1, part2, values):
        if v != 2 and v != -1:
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

    for compound, value in zip(compounds, classes):
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

def make_train_data(w1vecs, w2vecs, compvecs):
    train = np.concatenate((np.array(w1vecs), np.array(w2vecs), np.array(compvecs)), axis=1)
    print('Classification data created with shape', train.shape)
    return train


if __name__ == '__main__':
    parser = ArgumentParser(description='Unsupervised metrics experiment')
    parser.add_argument('wordvecs', help='word vectors dump')
    parser.add_argument('compvecs', help='compounds vectors dump')
    args = parser.parse_args()

    w1, w2, c, true = acquiring(args.wordvecs, args.compvecs, 'nouns')
    
    vecs = make_train_data(w1, w2, c)

    accuracies = []
    precision1 = []
    precision0 = []
    recall1 = []
    recall0 = []
    f11 = []
    f10 = []
    spearman = []
    rocaucs = []

    Cs = [1]
    kernels = [1]
    for C in Cs:
        for kernel in kernels:
            print(C, kernel)
            for state in tqdm(range(42, 67)):
                X_train, X_test, y_train, y_test = train_test_split(vecs, true, test_size=.25, random_state=state)

                clf = SVC(C=1, kernel='linear', random_state=42)
                #clf = MLPClassifier(alpha=1, solver='lbfgs', hidden_layer_sizes=(200,20,20, ), random_state=42)
                #clf = DecisionTreeClassifier(max_depth=10, max_features=20, random_state=42)
                #clf = GaussianNB()
                clf.fit(X_train, y_train)
                pred = clf.predict(X_test)
                accuracies.append(accuracy_score(pred, y_test))
                precision1.append(precision_score(pred, y_test))
                precision0.append(precision_score(pred, y_test, pos_label=0))
                recall1.append(recall_score(pred, y_test))
                recall0.append(recall_score(pred, y_test, pos_label=0))
                f11.append(f1_score(pred, y_test))
                f10.append(f1_score(pred, y_test, pos_label=0))
                print(pred, y_test)
                try:
                    rocaucs.append(roc_auc_score(pred, y_test))
                except:
                    pass
                with warnings.catch_warnings():
                    warnings.filterwarnings('error')
                    try:
                        corr = spearmanr(pred, y_test)[0]
                        spearman.append(corr)
                    except Warning:
                        spearman.append(0)
    

            print('accuracy=', '%.4f' % np.mean(accuracies))
            print('precision=', ['%.4f' % np.mean(precision1), '%.4f' % np.mean(precision0)])
            print('recall=', ['%.4f' % np.mean(recall1), '%.4f' % np.mean(recall0)])
            print('f1=',['%.4f' % np.mean(f11), '%.4f' % np.mean(f10)])
            print('spearman=', '%.4f' % np.mean(spearman))
            print('roc_auc=', '%.4f' % np.mean(rocaucs))

            print('.....................................')

    
