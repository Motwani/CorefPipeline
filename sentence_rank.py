from app.models import cypher
from pagerank import page_rank
from functools import reduce, partial
import json


def get_sentences():
    results = cypher("MATCH (s: Sentence) RETURN \
                             collect(s)")
    sentences = map(lambda x: x['id'], results)
    sentences = sorted(list(sentences))
    return sentences



def get_from_entitites(sentence_id):
    fquery = ('MATCH (e: Entity)-[r:from_entity_of]->(s: Sentence {id: %d})\
              RETURN collect(e)' % sentence_id)
    f_entities = list(map(lambda x: x['name'], cypher(fquery)))

    return(f_entities)

def get_to_entitites(sentence_id):
    tquery = ('MATCH (e: Entity)-[r:to_entity_of]->(s: Sentence {id: %d})\
              RETURN collect(e)' % sentence_id)
    t_entities = list(map(lambda x: x['name'], cypher(tquery)))

    return(t_entities)

def calc_sentence_score(sentence_id, from_weight, to_weight, entity_scores):
    f_entities = get_from_entitites(sentence_id)
    t_entities = get_to_entitites(sentence_id)

    fscore = reduce(lambda x, y: x + from_weight * entity_scores[y], f_entities,
                    0)
    tscore = reduce(lambda x, y: x + from_weight * entity_scores[y], t_entities,
                    0)

    return fscore + tscore

def sentence_rank(sentences, from_weight, to_weight, entity_scores):

    scores = list(map(lambda x: calc_sentence_score(x, from_weight, to_weight,
                                                  entity_scores), sentences))
    sentence_scores = dict(zip(sentences, scores))
    sentence_ranking = sorted(sentence_scores.items(), key=lambda x: x[1],
                              reverse=True)

    return sentence_ranking, sentence_scores

def increase_sentence_score(sentence_id, val, sentence_scores):
    ss = sentence_scores
    ss[sentence_id] += val

    sentence_ranking = sorted(sentence_scores.items(), key=lambda x: x[1],
                              reverse=True)
    return sentence_ranking, ss


def sentence_mapping(sentence_ranking):
    with open('data/sentences_and_numbers.json') as sen_num:
        num_to_sentence_dict = json.load(sen_num)
        
        sentence_score_list = map(lambda x: (num_to_sentence_dict[str(x[0])], x[1]), sentence_ranking)
        '''
        print('Rank   Sentence   Score')
        for i, sen in enumerate(sentence_score_list):
            print('{0}. {1} {2}\n'.format(i + 1, sen[0], sen[1]))
        '''
        return sentence_score_list


def make_rank_html(entity_ranking, sentence_score_list):
    html_string = '''
        <!DOCTYPE html>
    <html lang="en">
    <head>
      <title>Ranker</title>
      <meta charset="utf-8">
      <meta name="viewport"
         content="width=device-width, initial-scale=1, user-scalable=yes">
      <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">
      <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
    </head>
    <body>

    <div class="container-fluid">
      <div class="row">
          <div class="col-md-1"></div>
          <div class="col-md-10"></div>
          <div class="col-md-1"></div>
      </div>

      <div class="row">
          <div class="col-md-2"></div>
          <div class="col-md-7">
            <h1>Detective Novel Analytics System</h1>
          </div>
          <div class="col-md-3"></div>
      </div>
    </div>


    <div class="container">
      <h2>Sentences</h2>
      <table class="table table-hover">
        <thead>
          <tr>
            <th>Sentence Rank</th>
            <th>Sentence</th>
            <th>Sentence Score</th>
          </tr>
        </thead>
        <tbody>

    '''
    for i, sen in enumerate(sentence_score_list):
        html_string += '<tr>'
        html_string += '<td>{0}</td>'.format(i + 1)
        html_string += '<td>{0}</td>'.format(sen[0])
        html_string += '<td>{0}</td>'.format(sen[1])
        html_string += '</tr>'

    html_string += '</tbody></table></div>'

    html_string += '''
         <div class="container">
      <h2>Entities</h2>
      <table class="table table-hover">
        <thead>
          <tr>
            <th>Entity Rank</th>
            <th>Entity</th>
            <th>Entity Score</th>
          </tr>
        </thead>
        <tbody>

    '''

    for i, ent in enumerate(entity_ranking):
        html_string += '<tr>'
        html_string += '<td>{0}</td>'.format(i + 1)
        html_string += '<td>{0}</td>'.format(ent[0])
        html_string += '<td>{0}</td>'.format(ent[1])
        html_string += '</tr>'

    html_string += '</tbody></table></div></body></html>'

    with open('draft_ranking.html', 'w') as html_file:
        html_file.write(html_string)



sentences = get_sentences()
# print(get_from_entitites(1))
entity_ranking, entity_scores = page_rank(1000, 5)
# print(entity_ranking)
# calc_sentence_score(1, 0.8, 0.5, entity_scores)
# print(sentence_rank(sentences, 0.8, 0.5, entity_scores)[0])
sentence_score_list =\
    sentence_mapping(sentence_rank(sentences, 0.8, 0.5, entity_scores)[0])

make_rank_html(entity_ranking, sentence_score_list)