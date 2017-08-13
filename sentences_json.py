
import json
from pycorenlp import StanfordCoreNLP
import pickle
import codecs

with open('The_Adv_Blue_Carbuncle.txt') as f:
    lines = f.read()

nlp = StanfordCoreNLP('http://localhost:9000')

ans = nlp.annotate(lines, properties={'annotators':'ssplit'})
ans = json.loads(ans)

js = {}

for i in range(len(ans['sentences'])):
    sentence = ''
    for words in ans['sentences'][i]['tokens']:
        sentence += words['word'] + ' '
    js[i+1] = sentence

js = json.dumps(js)
print(js)
