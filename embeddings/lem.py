from pymystem3 import Mystem
from tqdm import tqdm
from argparse import ArgumentParser

if __name__ == '__main__':
	parser = ArgumentParser(description='Lemmatize text')
	parser.add_argument('text', help='text to lemmatize')
	parser.add_argument('lem_text', help='lemmatized text directory')
	args = parser.parse_args()

	morph = Mystem()

	with open(args.text, 'r') as text:
		with open(args.lem_text, 'w') as lem_text:
			for line in tqdm(text):		
				lem_text.write(''.join(morph.lemmatize(line)))
				lem_text.write(u'\r\n')