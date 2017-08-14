source setpath.sh

# Export path to the Neo4J bin to N4JPATH
$N4JPATH/neo4j start

sleep 10

# Export path to the Stanford CoreNLP directory
cd $STANNLPPATH
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 1500000 &
cd -

sleep 5

python3.5 text_process.py

python3.5 run.py &

sleep 5

curl -H "Content-Type: application/json" -X POST -d @data/global_relations_from_sentences.json http://localhost:6565/add_relations

python3.5 sentence_rank.py