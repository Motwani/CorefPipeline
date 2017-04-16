import json
from pycorenlp import StanfordCoreNLP
import pickle
import codecs

# nlp = StanfordCoreNLP('http://localhost:9000')

# with open('The_Adv_Blue_Carbuncle.txt') as f:
    # lines = f.read()

# ans = nlp.annotate(lines, properties={'annotators':'tokenize,ssplit,pos,lemma,ner,parse,mention,coref','coref.algorithm':'neural'})
# ans = nlp.annotate(lines, properties={'annotators':'tokenize,ssplit,pos,lemma,ner,parse,mention,coref'})

# ans = json.loads(ans)
with open('The_Adv_Blue_Carbuncle.txt.json') as json_data:
    ans = json.load(json_data)

# print ans
# pickle.dump(ans, open('The_Adv_Blue_Carbuncle.pkl','w'))
# ans = pickle.load(open('The_Adv_Blue_Carbuncle.pkl'))
# ans = json.loads(ans)

tokens = []
final = []
ftokens = []


def resolve_corefs(ans):
    #Map all mentions with their referents
    mdict = {}  #Mention dict
    mlist = []
    for i in ans['corefs']:
        entity =  ans['corefs'][i]
        for j in entity:
            if j['isRepresentativeMention']:
                key = str(j['sentNum']-1)+','+str(j['startIndex']-1)+','+str(j['endIndex']-1)
                for k in entity:
                    if (k['type']=='NOMINAL' or k['type']=='PRONOMINAL') and not k['isRepresentativeMention']:
                        snum = k['sentNum']-1
                        start = k['startIndex']-1
                        end = k['endIndex']-1
                        mdict[str(snum)+','+str(start)+','+str(end)]=key
                        mlist+=[[snum, start, end]]



    #print corefs
    #print mdict.keys()
    #print mlist
    mlist.sort()


    nmlist = []
    for i in range(len(ans['sentences'])):
        nmlist.append([])

    for i in mlist:
        snum = i[0]
        nmlist[snum].append([i[1], i[2]])

    #Get original sentences in a list
    tokens = []
    for i in range(len(ans['sentences'])):
        sent = []
        for j in ans['sentences'][i]['tokens']:
            sent+=[j['word']]
        sent = '~'.join(sent)
        tokens+=[str(sent)]
    # print tokens
    # raw_input()

    #Resolve the coreferences, new sentences in ntokens
    ntokens=""
    realtions = {}
    for i, j in enumerate(nmlist):
        sent = tokens[i].split('~')
        for x in j[::-1]:
            refind = mdict[str(i)+','+str(x[0])+','+str(x[1])]
            rsent = int(refind.split(',')[0])
            refind = [int(refind.split(',')[1]), int(refind.split(',')[2])]
            refstring = tokens[rsent].split('~')[refind[0]:refind[1]]
            if x != j[0]:
                sent = sent[:x[0]]+refstring+sent[x[1]:]
            else:
                sent = ' '.join(t for t in sent[:x[0]])+' '+' '.join(t for t in refstring)+' '+' '.join(t for t in sent[x[1]:])
                # print sent
                # raw_input()
            #print '->',refstring
        # print sent
        # raw_input()
        ntokens += str(sent)


    return ntokens

ntokens = resolve_corefs(ans)
print ntokens
