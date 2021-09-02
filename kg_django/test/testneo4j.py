from py2neo import Graph,Node,Relationship
test_graph = Graph(
    "http://127.0.0.1:7474",
    username="neo4j",
    password="1111"
)
test_graph.delete_all()
test_node_1 = Node("Entity",name = "a")
test_node_2 = Node("Entity",name = "b")
test_node_3 = Node("Entity",name = "c")
test_node_4 = Node("Entity",name = "d")
test_graph.create(test_node_1)
test_graph.create(test_node_2)
test_graph.create(test_node_3)
test_graph.create(test_node_4)

node_1_call_node_2 = Relationship(test_node_1,'REL',test_node_2)
node_1_call_node_2['value'] = 1
node_2_call_node_1 = Relationship(test_node_2,'REL',test_node_1)
node_2_call_node_1['value'] = 1
test_graph.create(node_1_call_node_2)
test_graph.create(node_2_call_node_1)



'''
hh1 = Relationship(test_node_2,'REL',test_node_1)
hh1['value'] = 1
hh2 = Relationship(test_node_1,'REL',test_node_2)
hh2['value'] = 1
test_graph.create(hh1)
test_graph.create(hh2)

node_2_call_node_3 = Relationship(test_node_2,'REL',test_node_3)
node_2_call_node_3['value'] = 1
node_3_call_node_2 = Relationship(test_node_3,'REL',test_node_2)
node_3_call_node_2['value'] = 1
test_graph.create(node_1_call_node_2)
#test_graph.create(node_2_call_node_1)
test_graph.create(node_2_call_node_3)
#test_graph.create(node_3_call_node_2)

node_1_call_node_4 = Relationship(test_node_1,'CALL',test_node_4)
node_1_call_node_4['value'] = 1
node_4_call_node_1 = Relationship(test_node_4,'CALL',test_node_1)
node_4_call_node_1['value'] = 1
node_4_call_node_3 = Relationship(test_node_4,'CALL',test_node_3)
node_4_call_node_3['value'] = 1
node_3_call_node_4 = Relationship(test_node_3,'CALL',test_node_4)
node_3_call_node_4['value'] = 1
test_graph.create(node_1_call_node_4)
#test_graph.create(node_4_call_node_1)
test_graph.create(node_4_call_node_3)
#test_graph.create(node_3_call_node_4)

node_2_call_node_4 = Relationship(test_node_2,'CALL',test_node_4)
node_2_call_node_4['value'] = 1
node_4_call_node_2 = Relationship(test_node_4,'CALL',test_node_2)
node_4_call_node_2['value'] = 1
test_graph.create(node_2_call_node_4)
#test_graph.create(node_4_call_node_2)

#node_1_call_node_2['value']+=3
#test_graph.push(node_1_call_node_2)

#find_code_1 = test_graph.find_one(
#  label="Person",
#  property_key="name",
#  property_value="test_node_1"
#)
#find_code_1 = test_graph.find_one('Person', 'name', 'test_node_1')
find_code_1 = test_graph.nodes.match('Person', name='a').first()
print(find_code_1)
print(test_node_1)
if find_code_1 == test_node_1:
    print("right")
else:
    print("not right")
'''