from py2neo import Graph, Node, Path, Relationship
import numpy as np
test_graph = Graph(
    "http://127.0.0.1:7474",
    username="neo4j",
    password="1111"
)

a = '船舶'
b = '入级'
maxn = '100'
data = test_graph.run("Match (n:Entity{name: $str})-[r:REL]->(end:Entity{name: $str1}) return r.value, r.rel, r.item, r.content, "
                           "n.name,end.name order by r.value desc", str=a,str1=b).data()
print(len(data), data)

data1 = test_graph.run("Match (n:Entity{name: $str})-[r:REL]->(end:Entity{name: $str1}) return r.value, r.rel, r.item, r.content, "
                           "n.name,end.name order by r.value desc", str=b,str1=a).data()
print(len(data1), data1)


'''
data = test_graph.run("Match (n:Entity)-[r:REL]-(end:Entity) return r.value, r.rel, r.content, n.name, end.name").data()
print('0', data)

print(len(data))
have_list = []
for i in range(0, len(data)):
    if i in have_list:
        continue
    for j in range(i + 1, len(data)):

        if data[i]["n.name"] == "a" and data[i]["end.name"] == "b":
            print(data[i])
        if j in have_list:
            continue
        if data[i]['n.name'] == data[j]['end.name'] and data[i]['end.name'] == data[j]['n.name']:
            data[i]['r.value'] += data[j]['r.value']
            have_list.append(j)
        if data[i]['n.name'] == data[j]['n.name'] and data[i]['end.name'] == data[j]['end.name']:
            have_list.append(j)

data = [data[i] for i in range(0, len(data)) if i not in have_list]
print(len(data))
print(data)
cnt = 0

name = "主机"
for i in range(0, len(data)):
    if data[i]["n.name"] == name or data[i]["end.name"] == name:
        print(data[i]["n.name"] + " " + data[i]["end.name"] + "：" + str(data[i]["r.value"]))
        cnt += 1
print(cnt)

for i in range(0, len(data)):
    if data[i]["n.name"] == "主机" and data[i]["end.name"] == "温度":
        print(data[i]["n.name"] + " " + data[i]["end.name"] + "：" + str(data[i]["r.value"]))

    if data[i]["n.name"] == "温度" and data[i]["end.name"] == "主机":
        print(data[i]["n.name"] + " " + data[i]["end.name"] + "：" + str(data[i]["r.value"]))
'''