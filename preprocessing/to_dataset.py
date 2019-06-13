import pandas as pd


if __name__ == '__main__':
    data = {'Часть 1': [], 'Часть 2': []}
    for num in range(250):
        data['Контекст' + ' ' + str(num + 1)] = []
    with open('compounds_top10000_NN.txt', 'r') as compounds, \
        open('compounds_top10000_NN_context.txt', 'r') \
                as context:
        for line1, line2 in zip(compounds, context):
            part1 = line1.strip().split()[0]
            part2 = line1.strip().split()[1]
            data['Часть 1'].append(part2)
            data['Часть 2'].append(part1)
            contexts = line2.split('|')
            for i in range(250):
                if i < len(contexts):
                    data['Контекст' + ' ' + str(i + 1)].append(contexts[i])
                else:
                    data['Контекст' + ' ' + str(i + 1)].append('')
    df = pd.DataFrame(data=data)
    df.to_csv('/home/willstudent/russian_compounds/compound_lists/table/compounds_NN_top10000.csv')