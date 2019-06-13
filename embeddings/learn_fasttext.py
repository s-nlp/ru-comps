from gensim.utils import tokenize
from gensim.models import FastText
from tqdm import tqdm
import multiprocessing
import smart_open
import logging

class myIter(object):
	def __iter__(self):
		with smart_open.smart_open('ruwiki_text_lem_comp.txt', 'r', encoding='utf-8') as text:
			for line in text:
				yield list(tokenize(line))
if __name__ == '__main__':
	logger = logging.getLogger('learn_fasttext.py')

	logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
	logging.root.setLevel(level=logging.INFO)
	logger.info("running %s" % 'learn_fasttext.py')

	print('Initializing model')
	model = FastText(size=300, window=5, min_count=2, workers=multiprocessing.cpu_count())
	print('Building vocabulary')
	model.build_vocab(sentences=myIter())
	print('Started training')
	model.train(sentences=myIter(), total_examples=model.corpus_count, epochs=5)
	print('Saving model')
	model.save('ruwiki_300_comp_5.fasttext.model')