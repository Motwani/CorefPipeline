from pycorenlp import StanfordCoreNLP
import json
import pickle
import itertools
import re


Adj_Tags = ['JJ','JJR','JJS']
Adv_Tags = ['RB','RBR','RBS']
Verb_Tags = ['VB','VBD','VBG','VBN','VBP','VBZ']
Noun_Tags = ['NN','NNS','NNP','NNPS']
relations = {}
Block = ['is','are','am','was','were','being','can','could','have','had','having','may','might','must','shall','should','will','would']
js = {}

def final_output(glob_name,glob_verb,glob_noun,line_no):

    # print glob_name,glob_adj,glob_adv,glob_noun
    if len(glob_name) == 0:
        return
    line = []
    line.append(glob_name)
    line.append(glob_verb)
    line.append(glob_noun)
    relations[line_no] = line



def get_sentence_relations(ans):

    for i in range(len(ans['sentences'])):

        glob_name = []
        glob_adj = []
        glob_adv = []
        glob_verb = []
        glob_noun = []
        name = ''
        cont = 0
        for props in ans['sentences'][i]['tokens']:
            if props['ner'] == 'PERSON':
                if cont == 1:
                    name += ' ' + props['word']
                else:
                    cont = 1
                    name = props['word']
            elif cont == 1:
                if name not in glob_name:
                # if len(glob_name) != 0:
                    # for x in glob_name:
                        # print x
                        # raw_input()
                        # if name not in x.split():
                            # glob_name.append(str(name))
                            # print glob_name
                            # raw_input()
                # else:
                    glob_name.append(str(name))
                    # print glob_name
                    # raw_input()
                            # print name
                name = ''
                cont = 0
            if props['pos'] in Adv_Tags:
                if props['word'] not in glob_adv:
                    glob_adv.append(str(props['word']))
            if props['pos'] in Adj_Tags:
                if props['word'] not in glob_adj:
                    glob_adj.append(str(props['word']))
            if props['pos'] in Verb_Tags:
                if props['word'] not in glob_verb and props['word'] not in Block:
                    glob_verb.append(str(props['word']))
            if props['pos'] in Noun_Tags:
                if props['word'] not in glob_noun:
                    glob_noun.append(str(props['word']))

        final_output(glob_name,glob_verb,glob_noun,i+1)
    return relations



if __name__ == "__main__":
    nlp = StanfordCoreNLP('http://localhost:9000')

    with open('data/story_files/Resolved_The_Adv_Blue_Carbuncle.txt','r') as f:
        lines = f.read()
    # print lines
    # raw_input()
    ans = nlp.annotate(lines, properties={'annotators':'pos,ner,lemma,tokenize'})
    # ans = json.loads(ans)

    pickle.dump(ans,open('data/Resolved_The_Adv_Blue_Carbuncle.pkl','w'))
    # ans = pickle.load(open('data/Resolved_The_Adv_Blue_Carbuncle.pkl'))
    ans = json.loads(ans)
    # print ans

    get_sentence_relations(ans)
    # js["1"] = relations
    #for i,line in enumerate(lines):
        #print line,relations[i+1]
        #print "---------------"
        #raw_input()
    relations = json.dumps(relations)
    print relations
    # print "---------------------"
