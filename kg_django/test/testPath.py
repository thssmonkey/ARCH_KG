from py2neo import Graph, Node, Path, Relationship
import numpy as np
test_graph = Graph(
    "http://127.0.0.1:7474",
    username="neo4j",
    password="1111"
)

fperson = "主机"
tperson = "温度"

data0 = test_graph.run("MATCH (n) RETURN n").data()
print('0', data0)

print(len(data0))

data = test_graph.run("Match(p1:Entity{name:$fp}),(p2:Entity{name:$tp}),p=allshortestpaths((p1)-[*..10]->(p2)) "
                       "return p limit 30", fp=fperson, tp=tperson).data()

print('1', data)

nodes_total = []
rels_total = []
paths = []
this_path = []
this_path_val = 0
this_path_values = []
cnt = 0
for datai in data:
        nodes = datai['p'].nodes
        rels = datai['p'].relationships
        print(nodes)
        print(rels)
        # print rel
        # print nodes
        # print rels
        this_path = []
        this_path_val = 0
        this_path_values = []
        for i in range(0, len(nodes)):
            #all_nodes_total.append(nodes[i]['name'])
            if nodes[i]['name'] not in nodes_total:
                nodes_total.append(nodes[i]['name'])
            if i < len(nodes) - 1:
                values = test_graph.run("Match (n:Entity{name: $fp})-[r:REL]-(end:Entity{name: $tp}) return r.value",
                                        fp=nodes[i]['name'], tp=nodes[i + 1]['name']).data()
                rel_val = values[0]['r.value']
                rels_total.append(
                    {"start_node": nodes[i]['name'], "end_node": nodes[i + 1]['name'], "val": rel_val})
                this_path.append(
                    {"start_node": nodes[i]['name'], "end_node": nodes[i + 1]['name'], "val": rel_val})
                this_path_val += rel_val
                this_path_values.append(rel_val)
            paths.append({'path': this_path, 'val': int(np.sum(this_path_values))})
            print(paths)