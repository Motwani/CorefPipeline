from app.models import cypher

def get_entities():
    results = cypher("MATCH (e: Entity) RETURN \
                             collect(distinct e)")
    entities = map(lambda x: x['name'], results)
    entities = sorted(list(set(entities)))
    return entities

def get_init_page_ranks(total, entities):
    base_score = total / len(entities)
    init_pr = {}

    for entity in entities:
        init_pr[entity] = base_score

    return init_pr

def get_in_degree(entity_name):
    in_query = ('MATCH (e: Entity)-[r]->(f:Entity {name: "%s"}) RETURN count(r)'
                % entity_name)
    in_degree = cypher(in_query)
    return int(in_degree)

def get_out_degree(entity_name):
    out_query = ('MATCH (e: Entity {name: "%s"})-[r]->(f:Entity) RETURN count(r)'
                % entity_name)
    out_degree = cypher(out_query)
    return int(out_degree)

def get_degree_info(entities):
    degree_info = {}

    for entity in entities:
        degree_info[entity] = {'in': get_in_degree(entity),
                               'out': get_out_degree(entity)}
    return degree_info

def get_in_neighbours(entity_name, entities):
    query = ('MATCH (e: Entity)-[r]->(f: Entity {name: "%s"}) RETURN collect(e)'
             % entity_name)
    in_neighbours = list(map(lambda x: x['name'], cypher(query)))

    return in_neighbours

def updated_page_ranks(old_pr, degree_info, alpha, entities):
    n = len(old_pr)
    new_pr = {}

    for entity in entities:
        in_neighbour_contrib = list(map(lambda x: (old_pr[x] /
                                                   degree_info[x]['out']),
                                        get_in_neighbours(entity, entities)))
        new_pr[entity] = (1 - alpha) / n + alpha * sum(in_neighbour_contrib)
    return new_pr

# print(get_entities())
# print(get_indegree('Watson'))
# print(get_in_neighbours('Watson', get_entities()))

def page_rank(total, iterations):

    entities = get_entities()
    old_pr = get_init_page_ranks(10000, entities)
    degree_info = get_degree_info(entities)
    for i in range(iterations):
        print("Iteration {}".format(i + 1))
        new_pr = updated_page_ranks(old_pr, degree_info, 0.2, entities)
        old_pr = new_pr

    ranking = sorted(new_pr.items(), key=lambda x: x[1], reverse=True)
    '''
    print("Top 10 most important entities:")
    for i, e in enumerate(ranking[:10]):
        print(i, e)

    print("Top 10 least important entities:")
    for i, e in enumerate(ranking[-1:-10:-1]):
        print(i, e)
    '''
    return ranking, new_pr
