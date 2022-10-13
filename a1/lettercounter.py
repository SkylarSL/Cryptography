import re

text = open(r"ctxt0.txt", "r")
text = text.read()
text = re.sub(r"[^a-zA-Z ]", "", text)
map = {}
for word in text:
    if word != " ":
        try:
            map[word] += 1
        except KeyError:
            map[word] = 1
map = sorted(map.items(), key=lambda x:x[1], reverse=True)
map = dict(map)
print(map)

'''
from matplotlib import pyplot as plt
import numpy as np

map = {'N': 5, 'go': 3, 'lx': 3, 'cup': 3, 'ozn': 3, 's': 3, 'nd': 2, 'umwbryy': 2, 'vy': 2, 'ulaz': 2, 'lqne': 2, 'Stgenf': 2, 'jao': 2, 'ercd': 1, 'agagfsvln': 1, 'cser': 1, 'zsz': 1, 'ga': 1, 'ght': 1, 'hscgpwn': 1}
map = sorted(map.items(), key=lambda x:x[1], reverse=True)
map = dict(map)
map = dict(list(map.items())[0:20])
f = plt.figure()
f.set_figwidth(18)
f.set_figheight(10)
plt.bar(list(map.keys()), map.values())
plt.show()
'''