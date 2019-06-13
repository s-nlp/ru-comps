import logging
import re
from argparse import ArgumentParser
from pymystem3 import Mystem
from tqdm import tqdm
from gensim.models import FastText

w = r'[A-ZА-Яa-zа-я]+'

if __name__ == '__main__':
    logger = logging.getLogger('learn_fasttext.py')
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % 'learn_fasttext')
    
    parser = ArgumentParser(description='Enrich model with UD contexts')
    parser.add_argument('AN_context', help='AN compound context')
    parser.add_argument('NN_context', help='NN compound context')
    parser.add_argument('model', help='FastText model directory')
    parser.add_argument('new_model', help='where to save updated model')
    args = parser.parse_args()
    
    sentences = []
    with open(args.AN_context) as context:
    	for line in context:
    	    for sent in line.split('|'):
            	sentences.append(re.findall(w, sent))

    with open(args.NN_context) as context:
    	for line in context:
    	    for sent in line.split('|'):
            	sentences.append(re.findall(w, sent))
    
    model = FastText.load(args.model)
    model.build_vocab(sentences, update=True)
    model.train(sentences, total_examples=len(sentences), epochs=model.epochs)

    model.save(args.new_model)

