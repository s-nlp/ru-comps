import json
import numpy as np
import re
from tqdm import tqdm
from nltk.corpus import stopwords


nums = r'[0-9]+'
latins = r'[A-Za-z]+'
stop = set(stopwords.words('russian') + ['года', 'века', 'метров', 'м', 'э', 'лет', 'руб', 'млрд', 'млн', 'км', 'кг',
                                         'мм', 'сек', 'тысячи', 'ночи', 'см', 'км/ч', 'г', 'тыс', 'эры', 'минут'])

with open('noun_compounds_NN', 'r') as compounds_train:
    with open('noun_compounds_NN_context', 'r') as context:
        compounds = []
        contexts = []
        for line1, line2 in zip(compounds_train, context):
            if not re.match(nums, line1) and not re.match(latins, line1) and line1.split()[0] not in stop and \
                    line1.split()[1] not in stop and '-' not in line1 and '2' not in line1 and '.' not in line1:
                compounds.append(line1.strip())
                contexts.append(line2.strip())
        print(len(compounds))
        print(len(np.unique(compounds, return_counts=True)[0]))
        inds = np.unique(compounds, return_counts=True)[1].argsort()
        compounds_sort = np.unique(compounds, return_counts=True)[0][inds[::-1]]
        #print(compounds_sort[:1000])
        with open('compounds_top10000_NN.txt', 'w') as top1000:
            with open('compounds_top10000_NN_context.txt', 'w') as top1000_context:
                for i in tqdm(range(15001)):
                    top1000.write(compounds_sort[i].split()[1] + ' ' + compounds_sort[i].split()[0] + '\r\n')
                    top1000_context.write('|'.join([contexts[num] for num, compound in enumerate(compounds)
                                           if compound == compounds_sort[i]]) + '\r\n')