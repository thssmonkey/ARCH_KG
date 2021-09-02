from py2neo import Graph,Node,Relationship
# create an unique index

test_graph = Graph(
    "http://127.0.0.1:7474",
    username="neo4j",
    password="1111"
)
test_graph.delete_all()
test_graph.run("CREATE CONSTRAINT ON (cc:Entity) ASSERT cc.name IS UNIQUE")



