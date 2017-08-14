from flask import Flask, request, flash, g, session, redirect, url_for,\
                  flash, jsonify
from app.models import add_relation
import json

app = Flask(__name__)

@app.route('/')
def index():
    return 'Criminal Finder'

@app.route('/add_relations', methods=['GET', 'POST'])
def add_relations():
    rel_obj = dict(request.get_json(silent=True))
    print(rel_obj['1'][0])

    for sentence_num in rel_obj:
        for from_entity in rel_obj[sentence_num][0]:
            for verb in rel_obj[sentence_num][1]:
                for to_entity in rel_obj[sentence_num][2]:
                    add_relation(from_entity, to_entity, verb,
                                 sentence_num)


    return "Got the JSON object\n"
