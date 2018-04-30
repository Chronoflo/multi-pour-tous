from modules.handyfunctions import take_part, BEFORE, AFTER, LEFT, RIGHT

with open('dkey', 'r') as f:
    data = f.read()

liste = data.split('#')
keys = []
codes = []
for i, v in enumerate(liste):
    keys.append(take_part(take_part(v, AFTER, ' ', start_from=LEFT), BEFORE, ' ', start_from=LEFT))
    codes.append(take_part(take_part(take_part(v, AFTER, '0', start_from=LEFT, keep_sep=True), AFTER, ' ', start_from=RIGHT), BEFORE, '\n', start_from=RIGHT))

keys = [i for i in keys if i != '']
codes = [i for i in codes if i != '']
print(keys)
print(codes)
print(len(keys) == len(codes))


# Attention, voici le code qui écrit dans le fichier une fois les modifs effectuées
# with open('../modules/const.py', 'a') as f:
#     for key, code in zip(keys, codes):
#         f.write(key + ' = ' + code + '\n')
