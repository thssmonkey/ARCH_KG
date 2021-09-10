import os
import json
from py2neo import Graph, Node, Relationship
os.chdir(os.path.dirname(__file__))

def build_neo4j_graph():
    # create an unique index
    neo4j_graph = Graph(
        # "http://166.111.80.235:7475/"
        "http://127.0.0.1:7475",
        username="neo4j",
        password="1111"
    )
    neo4j_graph.delete_all()
    # neo4j_graph.run("CREATE CONSTRAINT ON (cc:Entity) ASSERT cc.name IS UNIQUE")

    return neo4j_graph

def export_json_2_neo4j(path, neo4j_graph):
    triple_dic = {}
    node_dic = {}

    print("Start export...")

    lines = open(path, 'r', encoding='utf-8').readlines()
    print(len(lines))
    for i, line in enumerate(lines):
        line = json.loads(line)
        arrays = line['关系']
        content = line['句子']
        item = line['条目']
        spec = line["规范"]
        name1 = arrays[0]
        relation = arrays[1].replace('：', '').replace(':', '').replace('　', '').replace(' ', '').replace('【','').replace('】', '')
        name2 = arrays[2]
        triple = name1 + "&" + name2
        if name1 == "" or name2 == "" or relation == "":
            continue
        
        if triple not in triple_dic.keys():
            if name1 not in node_dic.keys():
                test_node_1 = Node("Entity", name=name1)
                neo4j_graph.create(test_node_1)
                node_dic[name1] = test_node_1
            else:
                test_node_1 = node_dic[name1]
            if name2 not in node_dic.keys():
                test_node_2 = Node("Entity", name=name2)
                neo4j_graph.create(test_node_2)
                node_dic[name2] = test_node_2
            else:
                test_node_2 = node_dic[name2]
            node_1_call_node_2 = Relationship(test_node_1, "REL", test_node_2)
            node_1_call_node_2['value'] = 1
            node_1_call_node_2['rel'] = relation
            node_1_call_node_2['content'] = content
            node_1_call_node_2['item'] = item
            node_1_call_node_2['spec'] = spec
            neo4j_graph.create(node_1_call_node_2)

            triple_dic[triple] = []
            triple_dic[triple].append(node_1_call_node_2)

            # print(triple)
        else:
            node_1_call_node_2 = triple_dic[triple][0]
            node_1_call_node_2['value'] += 1
            node_1_call_node_2['rel'] += "###" + relation     # 两个句子中间用"###"分割
            node_1_call_node_2['content'] += "###" + content
            node_1_call_node_2['item'] += "###" + item
            node_1_call_node_2['spec'] += "###" + spec
            neo4j_graph.push(node_1_call_node_2)
            # print("[重复] - " + triple)
    print("export Ending...")

def main_run():
    os.chdir(os.path.dirname(__file__))
    json_path = '../kg_building/data/lexicon.json'
    neo4j_graph = build_neo4j_graph()
    export_json_2_neo4j(json_path, neo4j_graph)

if __name__ == "__main__":
    main_run()
