# README

This is a end-to-end pipeline from extracting sentences to displaying the sentences and entities in a ranked order.

## Some file descriptions

1. Global_Json_relations_from_sentences.py
    Get a JSON output of ALL the sentences in the text.
    JSON output is structured like [P.Noun,Verb,Noun]

2. Temporal_Json_relations_from_sentences.py
    Get a JSON output of the sentences in the text indicating any time relation.
    JSON output is structured like [P.Noun,Verb,Noun]

3. Final_Coref.py
    Input: Text File with Story
    Output: Text file with resolved coreference relations

4. p1.pkl
    Input: Resolved Story File
    Stores the POS and NER relations of the File

5. Script.py
    Pipeline file for all functions

## Web App

This is a python web application to make a graph out of entity relations in JSON format.  

* Make sure that you have Neo4J installed and running on port 7474.
* Enter `python3 run.py` to start the server.  
* Send a request with the sample data using `curl -H "Content-Type: application/json" -X POST -d @sample.json http://localhost:6565/add_relations`.
* Open `http://localhost:7474/` on a browser.
* Enter `MATCH (n: Entity) RETURN n` in the Cypher query box to get all the entites. Click on the entity nodes to reveal their relations.
