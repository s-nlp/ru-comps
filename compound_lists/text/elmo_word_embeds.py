import re
import pymorphy2
import numpy as np
from elmoformanylangs import Embedder
from tqdm import tqdm

part1 = []
part2 = []
compounds = []

with open('compounds_top10000_AN.txt') as comp_list:
    for compound in tqdm(comp_list):
        words = compound.split()
        part1.append(words[0])
        part2.append(words[1])
        compounds.append([words[0], words[1]])
            
'''
punct = r'[^w ]+'

sents = [re.sub(punct, '', word).split() for sent in sents]

for sent in tqdm(sents):
	sents = [sent for sent in sents if len(sent) > 0]

print(len(sents))
'''

morph = pymorphy2.MorphAnalyzer()

part1_lemm = []
part2_lemm = []
comps_lemm = []

for w1, w2, c in zip(part1, part2, compounds):
    part1_lemm.append(morph.parse(w1)[0].normal_form)
    part2_lemm.append(morph.parse(w2)[0].normal_form)
    comps_lemm.append([morph.parse(word)[0].normal_form for word in c])
    #sent_lemm = [morph.parse(word)[0].normal_form for word in sent]
    #sents_lemm.append(sent_lemm)

print('Word 1')
elmo_embedder1 = Embedder(model_dir = 'model_rus')
emb1 = elmo_embedder1.sents2elmo(part1_lemm)
print(type(emb1))
print(len(emb1))

emb1 = np.array(emb1)
#print(emb.shape)
np.save('elmo_compounds_w1_embeddings_an.npy', emb1)

print('Word 2')
elmo_embedder2 = Embedder(model_dir = 'model_rus')
emb2 = elmo_embedder2.sents2elmo(part2_lemm)
print(type(emb2))
print(len(emb2))

emb2 = np.array(emb2)
#print(emb.shape)
np.save('elmo_compounds_w2_embeddings_an.npy', emb2)

print('Compound')
elmo_embedder3 = Embedder(model_dir = 'model_rus')
emb3 = elmo_embedder3.sents2elmo(comps_lemm)
print(type(emb3))
print(len(emb3))

emb3 = np.array(emb3)
#print(emb.shape)
np.save('elmo_compounds_comp_embeddings_an.npy', emb3)