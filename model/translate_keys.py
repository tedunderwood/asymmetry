import csv

vocab = set()

with open('vocab.tsv', encoding = 'utf-8') as f:
    for line in f:
        row = line.strip().split('\t')
        docfreq = int(row[1])
        if docfreq < 34008 and docfreq > 2400:
            vocab.add(row[0])

lines = []

with open('keys.txt', encoding = 'utf-8') as f:
    for line in f:
        row = line.strip().split()
        topicnum = row[0]
        topicsize = float(row[1])
        filteredline = []
        for i in range(2, 150):
            word = row[i]
            if word in vocab:
                filteredline.append(word)
                if len(filteredline) > 25:
                    break
        if len(filteredline) < 25:
            for word in row[2: 150]:
                if word not in filteredline:
                    filteredline.append(word)
                    if len(filteredline) > 25:
                        break

        lines.append((topicsize, topicnum, filteredline))

lines.sort(reverse = True)

with open('filtered_keys.txt', mode = 'w', encoding = 'utf-8') as f:
    for l in lines:
        size, num, fline = l
        outline = str(size) + '\t' + str(num) + '\t' + ' '.join(fline) + '\n'
        f.write(outline)


