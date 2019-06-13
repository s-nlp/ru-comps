from argparse import ArgumentParser
from gensim.corpora import WikiCorpus
from tqdm import tqdm


def make_corpus(dump, outp):
    with open(outp, 'w') as output:
        print('Started corpus initializing')
        wiki = WikiCorpus(dump)
        print('Corpus initialized from dump')

        for text in tqdm(wiki.get_texts()):
            output.write(bytes(' '.join(text), 'utf-8').decode('utf-8') + '\n')
        print('Processing complete!')


if __name__ == '__main__':
    parser = ArgumentParser(description='Training nominal compound detection models using word vectors and human '
                                        'validations')
    parser.add_argument('dump', help='Wikipedia dump')
    parser.add_argument('outp', help='Wikipeida corpus text output file')

    args = parser.parse_args()
    make_corpus(args.dump, args.outp)
