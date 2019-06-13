import pymorphy2

morph = pymorphy2.MorphAnalyzer()


if __name__ == '__main__':
    data = {'Часть 1': [], 'Часть 2': []}
    with open('compounds_top10000_AN.txt', 'r') as compounds:
        with open('/home/willstudent/russian_compounds/compound_lists/text/compounds_top10000_AN.txt',
                  'w') as infl:
            for line in compounds:
                part1 = line.strip().split()[0]
                part2 = line.strip().split()[1]
                noun_gen = morph.parse(part2)[0].tag.gender
                noun_num = morph.parse(part2)[0].tag.number
                adj = morph.parse(part1)[0]
                try:
                    infl.write(adj.inflect({'nomn', noun_gen, noun_num}).word + ' ' + part2 + '\r\n')
                except:
                    infl.write(part1 + ' ' + part2 + '\r\n')