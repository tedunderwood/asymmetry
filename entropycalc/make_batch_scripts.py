# make_batch_scripts.py

lines = []

with open('batch_template.pbs', encoding = 'utf-8') as f:
    for line in f:
        lines.append(line)

for floor in range(0, 40000, 2000):
    filename = 'kld' + str(floor) + '.pbs'
    with open('pbs/' + filename, mode = 'w', encoding = 'utf-8') as f:
        for l in lines:
            l = l.replace('<insert>', str(floor))
            f.write(l)


