import json
from pycorenlp import StanfordCoreNLP
import pickle
import codecs
import os
from final_coref import resolve_corefs
from global_json_relations_from_sentenes import get_sentence_relations
from temporal_json_relations_from_sentences import get_temporal_sentence_relations

def get_file():

    if os.path.exists('The_Adv_Blue_Carbuncle.pkl'):
        ans = pickle.load(open('The_Adv_Blue_Carbuncle.pkl'))
        ans = json.loads(ans)
    return ans

def coref_resolver():
    ans = get_file()
    resolved_story = resolve_corefs(ans)
    with open('data/story_files/Resolved_The_Adv_Blue_Carbuncle.txt','w') as f:
        f.write(resolved_story)
    return resolved_story

def global_relation_builder(var):

    sentence_relations = get_sentence_relations(var)
    with open('data/global_relations_from_sentences.json','w') as f:
         json.dump(sentence_relations, f)
    return sentence_relations

def temporal_relation_builder(var):

    sentence_relations = get_temporal_sentence_relations(var)

    with open('data/temporal_relations_from_sentences.json','w') as f:
         json.dump(sentence_relations, f)
    return sentence_relations

def sentence_json():

    with open('data/story_files/The_Adv_Blue_Carbuncle.txt') as f:
        lines = f.read()

    ans = nlp.annotate(lines, properties={'annotators':'ssplit'})
    ans = json.loads(ans)
    js = {}
    for i in range(len(ans['sentences'])):
        sentence = ''
        for words in ans['sentences'][i]['tokens']:
            sentence += words['word'] + ' '
        js[i+1] = sentence
    with open('sentences_and_numbers.json','w') as nf:
        json.dump(js, nf)

if __name__ == "__main__":

    nlp = StanfordCoreNLP('http://localhost:9000')

    resolved_story = coref_resolver()
    var = nlp.annotate(resolved_story, properties={'annotators':'pos,ner,lemma,tokenize'})
    var = json.loads(var)

    all_relations = global_relation_builder(var)
    print all_relations
    temporal_relations = temporal_relation_builder(var)
    sentence_json()
    # print temporal_relations
