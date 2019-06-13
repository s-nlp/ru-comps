from pymystem3 import Mystem
from tqdm import tqdm


if __name__ == '__main__':
    m = Mystem()

    with open('wiki_ru_20190120.txt', 'r') as wiki:
        with open('wiki_ru_lem_20190120.txt', 'w') as wiki_lem:
            for line in tqdm(wiki):
                lemmas = m.lemmatize(line)
                wiki_lem.write(''.join(lemmas) + '\r\n')
