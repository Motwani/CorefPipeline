from flask import request, jsonify, flash, g, session, redirect,\
                  url_for
from py2neo import Graph, Node, Relationship

def init_graph(url, username, password):
    return Graph(url + '/db/data/', username=username,
                 password=password)

graph = init_graph('http://localhost:7474', 'neo4j', 'abc123')
cypher = graph.evaluate

def add_relation(name, to_entity_name, relation, sentence_num):
    entity = graph.find_one('Entity', 'name', name)
    to_entity = graph.find_one('Entity', 'name', to_entity_name)
    sentence = graph.find_one('Sentence', 'id', int(sentence_num))

    if not entity:
        entity = Node('Entity', name=name)
        graph.create(entity)

    if not to_entity:
        print(to_entity_name)
        to_entity = Node('Entity', name=to_entity_name)
        graph.create(to_entity)

    if not sentence:
        sentence = Node('Sentence', id=int(sentence_num))
        graph.create(sentence)


    # This shouldn't happen in the first place. Format messed up
    # if isinstance(relation, list):
    #     relation = relation[0]

    rel = Relationship(entity, relation, to_entity)
    graph.create(rel)

    rel_sentence_from = Relationship(entity, 'from_entity_of',
                                     sentence)
    rel_sentence_to = Relationship(to_entity, 'to_entity_of',
                                     sentence)
    graph.create(rel_sentence_from)
    graph.create(rel_sentence_to)
