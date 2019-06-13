from conllu import parse_incr
from conllu import parse

num = 0
with open('UD_Russian-SynTagRus/ru_syntagrus-ud-dev.conllu', 'r') as syntagrus:
    with open('noun_compounds_NN_dev.txt', 'w') as compounds:
        for tokenlist in parse_incr(syntagrus):
            # print(tokenlist)
            for token in tokenlist:
                if token['upostag'] == 'NOUN':
                    if tokenlist[token['head'] - 1]['upostag'] == 'NOUN' and token['feats'] is not None and \
                            'Case' in token['feats'] and token['feats']['Case'] == 'Gen':
                        compounds.write(tokenlist[token['head'] - 1]['lemma'].lower() + ' ' + token['form'].lower() +
                                        '\r\n')
                        num += 1
