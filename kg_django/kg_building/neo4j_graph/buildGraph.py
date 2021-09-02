from neo4j import GraphDatabase
import os
import json

class neo4jGraph:

    driver = None
    triple_list = []

    def __init__(self, url, user, password):
        self.triple_list = []
        self.driver = GraphDatabase.driver(url, auth=(user, password))

    def close(self):
        self.driver.close()

    def clear_data(self):
        with self.driver.session() as session:
            cmd = ("match (n) detach delete n")
            try:
                session.run(cmd)
                print("清空数据")
            except Exception as e:
                print(str(e))
            
    def _add_node(self, tx, name1, relation, name2):
        cmd = (
            "MERGE (a:Node {name: $name1}) "
            "MERGE (b:Node {name: $name2}) "
            "MERGE (a)-[:"+relation+"]-> (b)"
            )
        tx.run(cmd, name1=name1, name2=name2)

    def add_node(self, session, name1, relation, name2):
        try:
            session.write_transaction(self._add_node, name1, relation, name2)
        except Exception as e:
            print(name1, relation, name2, str(e))

    def summary():
        base_path = "../data/概念关系/"
        summary_file = "../data/概念关系汇总.txt"
        outfile = open(summary_file, "w+")
        filels = os.listdir(base_path)
        for file in filels:
            if file != ".DS_Store":
                print("==== " + file)
                lines = open(base_path + file, 'r', encoding='utf-8').readlines()
                for i, line in enumerate(lines):
                    line = line.strip()
                    outfile.write(line + "\n")
                    print(line)
        outfile.close()
        print("汇总完成")

    def export_txt_2_databse(self, path):
        with self.driver.session() as session:
            lines = open(path, 'r', encoding='utf-8').readlines()
            print(len(lines))
            for i, line in enumerate(lines):
                line = line.strip()
                print(line)
                if line == "":
                    continue
                lists = line.split(" ")
                name1 = lists[0]
                relation = lists[1].replace('：','').replace(':','').replace('　','').replace(' ','').replace('【','').replace('】','')
                name2 = lists[2]
                if name1 == name2:
                    continue
                relation = "子概念"
                triple = name1 + "->" + relation + "->" + name2
                if triple not in self.triple_list:
                    self.triple_list.append(triple)
                    self.add_node(session, name1, relation, name2)
                    print(triple)
                else:
                    print("[重复] - " + triple)

if __name__ == "__main__":
    scheme = "bolt"
    host_name = "localhost"
    port = 7687
    url = "{scheme}://{host_name}:{port}".format(scheme=scheme, host_name=host_name, port=port)
    user = "neo4j"
    password = "1111"
    app = neo4jGraph(url, user, password)
    app.clear_data()
    base_path = "../data/专业分类/" # 概念关系 专业分类 实验
    filels = os.listdir(base_path)
    for file in filels:
        if file != ".DS_Store":
            print("==== " + file)
            app.export_txt_2_databse(base_path + file)
    app.close()
   
