# -*- coding: utf-8 -*-

# from django.http import HttpResponse
from django.shortcuts import render

from django.http import HttpResponse

from py2neo import Graph, Node, Relationship, database

from django.core import serializers

import os

import json

import numpy as np

import requests

from functools import cmp_to_key

test_graph = Graph(
    "http://127.0.0.1:7474", # 7687
    username="neo4j",
    password="1111"
)
'''
test_graph = Graph(
    "bolt://127.0.0.1:7687",
    username="neo4j",
    password="1111"
)
'''

def f2(a, b):
    return b['val'] - a['val']


def f3(a, b):
    return b['val'] - a['val']


def hello(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'hello.html', context)


def near(request):
    return render(request, 'near.html')


def near_test(request):
    return render(request, 'near0.html')


def find_near_before(request):
    a = request.GET['pname']

    # maxn = request.GET['maxnear']

    data = test_graph.run("Match (n:Entity{name: $str})-[r:REL]-(end:Entity) return r.value, "
                           "n.name,end.name,n.tid order by r.value desc", str=a).data()

    for i in range(0, len(data)):
        for j in range(i + 1, len(data)):
            if (data[i]['n.name'] == data[j]['end.name'] and data[i]['end.name'] == data[j]['n.name']) or \
                    (data[i]['n.name'] == data[j]['n.name'] and data[i]['end.name'] == data[j]['end.name']):
                data[i]['r.value'] += data[j]['r.value']
                data.remove(data[j])
                break

    # mydata = {}
    # for i in range(0,len(data)):
    #    if mydata.has_key(data[i]['n.tid']):
    #       mydata[data[i]['n.tid']]['data'].append({"name":data[i]['end.name'],"val":data[i]['r.value']})
    #   else:
    #      mydata[data[i]['n.tid']] = {}
    #     mydata[data[i]['n.tid']]['data']  = []

    # for item in mydata:
    #    mydata[item]['count'] = len(mydata[item]['data'])
    #    mydata[item]['data'].sort(key=cmp_to_key(f2))
    mydata = []
    help = {}
    cnt = 0
    for i in range(0, len(data)):
        if help.has_key(data[i]['n.tid']):
            mydata[help[data[i]['n.tid']]]['data'].append({'name': data[i]['end.name'], 'val': data[i]['r.value']})
        else:
            mydata.append({'tid': data[i]['n.tid'], 'data': []})
            help[data[i]['n.tid']] = cnt
            cnt += 1
    for i in range(0, len(mydata)):
        mydata[i]['count'] = len(mydata[i]['data'])
    for i in range(0, len(mydata)):
        mydata[i]['data'].sort(key=cmp_to_key(f2))

    mydata.sort(key=cmp_to_key(f3))

    response = HttpResponse(json.dumps(mydata), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def get_node_relation(name):
    data = test_graph.run("Match (n:Entity{name: $str})-[r:REL]->(end:Entity) return r.value, r.rel, r.item, r.spec, r.content, "
                           "n.name,end.name order by r.value desc", str=name).data()
    
    reverse_data = test_graph.run("Match (n:Entity)-[r:REL]->(end:Entity{name: $str}) return r.value, r.rel, r.item, r.spec, r.content, "
                           "n.name,end.name order by r.value desc", str=name).data()
    res_list = {}
    for i in range(0, len(data)):
        data[i]['dir'] = "1"
        if data[i]['end.name'] not in res_list.keys():
            res_list[data[i]['end.name']] = []
        res_list[data[i]['end.name']].append(data[i])

    for i in range(0, len(reverse_data)):
        reverse_data[i]['dir'] = "2"
        reverse_data[i]['end.name'] = reverse_data[i]['n.name']
        reverse_data[i]['n.name'] = name
        if reverse_data[i]['end.name'] not in res_list.keys():
            res_list[reverse_data[i]['end.name']] = []
        res_list[reverse_data[i]['end.name']].append(reverse_data[i])

    res = []
    index = 0
    for key in res_list.keys():
        ls = res_list[key]
        res.append(ls[0])
        res[index]["all"] = 1
        if len(ls) > 1:
            res[index]['all'] = res[index]['all'] + 1
            res[index]['r.value'] = str(res[index]['r.value']) + "@@@" + str(ls[1]['r.value'])
            res[index]['r.rel'] += "###" + ls[1]['r.rel']
            res[index]['r.item'] += "###" + ls[1]['r.item']
            res[index]['r.spec'] += "###" + ls[1]['r.spec']
            res[index]['r.content'] += "###" + ls[1]['r.content']
            res[index]['dir'] += "@@@" + ls[1]['dir']
        index += 1
    return res

def find_near(request):
    request_name = request.GET['pname']
    maxn = request.GET['maxnear']
    print(request_name, maxn)

    data = get_node_relation(request_name)

    '''
    have_list = []
    for i in range(0, len(data)):
        if i in have_list:
            continue
        for j in range(i + 1, len(data)):
            if j in have_list:
                continue
            if (data[i]['n.name'] == data[j]['end.name'] and data[i]['end.name'] == data[j]['n.name']) or \
                    (data[i]['n.name'] == data[j]['n.name'] and data[i]['end.name'] == data[j]['end.name']):
                have_list.append(j)

    data = [data[i] for i in range(0, len(data)) if i not in have_list]
    '''

    node_list = [request_name]
    node_cnt = 0
    for i in range(0, len(data)):
        if data[i]['end.name'] not in node_list:
            node_list.append(data[i]['end.name'])
            node_cnt += 1
            if node_cnt >= int(maxn):
                break

    data_tmp = []
    for i in range(0, len(data)):
        if data[i]['end.name'] in node_list:
            data_tmp.append(data[i])
    data = data_tmp

    last_index = min(int(maxn), len(data))
    data = data[:last_index]

    if (request.GET['mr'] == "1"):
        response = HttpResponse(json.dumps(data), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    # tdata = []
    # for i in range(0,maxn):
    #    tdata[i] = data[i]

    # data = tdata
    '''
    for i in data:
        iname = i['end.name']
        #inode = test_graph.node(i['end.id'])
        for j in data:
            jname = j['end.name']
            if iname==jname:
                continue
            #jnode = test_graph.node(j['end.id'])
            #find_r = test_graph.match_one(start_node=inode,end_node=jnode,bidirectional=True);
            find_r = test_graph.data("Match (n:Entity{name: {i}})-[r:REL]-(end:Entity{name:{j}}) return r.value",i=iname
                                     ,j=jname)
            if find_r:
                data.append({"r.value":find_r[0]['r.value'],"n.name":iname,"end.name":jname})
    '''
    '''
    for i in range(0, len(data)):
        hisdata = test_graph.data(
            "Match (n:Entity{name: {str}})-[r:REL]-(end:Entity) where r.value > 10 return r.value, "
            "n.name,end.name order by r.value desc limit 25", str=data[i]['end.name'])
        for j in range(0, len(hisdata)):
            if hisdata[j]['end.name'] == data[i]['end.name']:
                data.append(hisdata[j])
    '''
    hisdatas = []
    for i in range(0, len(data)):
        hisdata = get_node_relation(data[i]['end.name'])
        hisdatas.append(hisdata)

    have_dic = {}
    for i in range(0, len(data)):
        edgestr1 = data[i]['end.name'] + "&" + data[i]['n.name']
        edgestr2 = data[i]['n.name'] + "&" + data[i]['end.name']
        have_dic[edgestr1] = data[i]['r.value']
        have_dic[edgestr2] = data[i]['r.value']
    
    for i in range(0, len(data)):
        for j in range(0, len(hisdatas)):
            for k in range(0, len(hisdatas[j])):
                if data[i]['end.name'] == hisdatas[j][k]['end.name']:
                    innerval = hisdatas[j][k]['r.value']
                    edgestr1 = hisdatas[j][k]['end.name'] + "&" + hisdatas[j][k]['n.name']
                    edgestr2 = hisdatas[j][k]['n.name'] + "&" + hisdatas[j][k]['end.name']
                    if (edgestr1 not in have_dic.keys()) and (edgestr2 not in have_dic.keys()):
                        have_dic[edgestr1] = innerval
                        have_dic[edgestr2] = innerval
                    else:
                        continue
                    if hisdatas[j][k] in data:
                        continue
                    else:
                        data.append({'r.value': innerval, 'r.rel': hisdatas[j][k]['r.rel'], 'r.content': hisdatas[j][k]['r.content'], 'r.item':hisdatas[j][k]["r.item"], 'r.spec':hisdatas[j][k]["r.spec"], 'n.name': hisdatas[j][k]['end.name'], 'end.name': hisdatas[j][k]['n.name'], 'dir': hisdatas[j][k]['dir'], 'all': hisdatas[j][k]['all']})

    for i in range(0, len(data)):
        if data[i]['end.name'] == "入级":
            print(data[i])

    response = HttpResponse(json.dumps(data), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def path(request):
    return render(request, 'path.html')


def find_path(request):
    # return render(request,'path.html')
    fperson = request.GET['fname']
    tperson = request.GET['tname']
    data = test_graph.run("Match(p1:Entity{name:$fp}),(p2:Entity{name:$tp}),p=allshortestpaths((p1)-[*..20]->(p2)) "
                          "return p", fp=fperson, tp=tperson).data()

    print(data)

    if not data:
        response = HttpResponse(json.dumps([]), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    nodes_total = []
    rels_total = []
    # all_nodes_total = []
    paths = []
    cnt = 0
    for datai in data:
        nodes = datai['p'].nodes
        rels = datai['p'].relationships
        this_path = []
        this_path_val = 0
        this_path_values = []
        for i in range(0, len(nodes)):
            # all_nodes_total.append(nodes[i]['name'])
            if nodes[i]['name'] not in nodes_total:
                nodes_total.append(nodes[i]['name'])
            if i < len(nodes) - 1:
                values = test_graph.run("Match (n:Entity{name: $fp})-[r:REL]->(end:Entity{name: $tp}) return r.value",
                                        fp=nodes[i]['name'], tp=nodes[i + 1]['name']).data()
                rel_val = values[0]['r.value']
                rels_total.append(
                    {"start_node": nodes[i]['name'], "end_node": nodes[i + 1]['name'], "val": rel_val})
                this_path.append(
                    {"start_node": nodes[i]['name'], "end_node": nodes[i + 1]['name'], "val": rel_val})
                this_path_val += rel_val
                this_path_values.append(rel_val)
        paths.append({'path': this_path, 'val': int(np.sum(this_path_values))})
    paths.sort(key=cmp_to_key(f2))

    print(nodes_total)
    print(rels_total)
    print(paths)
    # 双保险
    total_rep = [nodes_total, rels_total, paths]
    response = HttpResponse(json.dumps(total_rep), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def is_friends(request):
    fperson = request.GET['fname']
    tperson = request.GET['tname']
    data = test_graph.run("Match (n:Entity{name: $str1})-[r:REL]-(end:Entity{name:$str2}) return r.value ",
                           str1=fperson, str2=tperson).data()
    rdata = {}
    if (len(data) > 0):
        rdata['status'] = 1
    else:
        rdata['status'] = 0
    response = HttpResponse(json.dumps(rdata), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def getEdgeinfo(request):
    name1 = request.GET['sname']
    name2 = request.GET['tname']

    url = "http://websensor.playbigdata.com/fss3/service.svc/GetSearchResults"

    querystring = {"query": name1 + " " + name2, "num": "5", "start": "1"}

    headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        'upgrade-insecure-requests': "1",
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.8",
        'cache-control': "no-cache",
        'postman-token': "5549dc28-2253-f247-d5f9-1f8e87bd830f"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    res = json.loads(response.text)
    response = HttpResponse(json.dumps(res), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def is_entity(request):
    fperson = request.GET['name']
    data = test_graph.run("Match (n:Entity{name: $str1}) return n.name ", str1=fperson).data()
    rdata = {}
    if (len(data) > 0):
        rdata['status'] = 1
    else:
        rdata['status'] = 0
    response = HttpResponse(json.dumps(rdata), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def graph(request):
    return render(request, 'graph.html')

def get_graph(request):
    data = test_graph.run("Match (n:Entity)-[r:REL]->(end:Entity) return r.value, r.rel, r.item, r.spec, r.content, n.name, end.name").data()
    if not data:
        response = HttpResponse(json.dumps([]), content_type="application/json")
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "*"
        return response

    print(len(data))
    '''
    have_list = []
    for i in range(0, len(data)):
        if i in have_list:
            continue
        for j in range(i + 1, len(data)):
            if j in have_list:
                continue
            if (data[i]['n.name'] == data[j]['end.name'] and data[i]['end.name'] == data[j]['n.name']) or \
                    (data[i]['n.name'] == data[j]['n.name'] and data[i]['end.name'] == data[j]['end.name']):
                have_list.append(j)
    data = [data[i] for i in range(0, len(data)) if i not in have_list]

    print(len(data))
    '''

    response = HttpResponse(json.dumps(data), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def get_spec(request):
    path = "data/spec.json"
    lines = open(path, 'r', encoding='utf-8').readlines()
    print(len(lines))
    data = []
    for i, line in enumerate(lines):
        line = json.loads(line)
        data.append(line)

    response = HttpResponse(json.dumps(data), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def search_spec(request):
    return render(request, 'search_spec.html')

def search_from_spec(request):
    word_name = request.GET['pname']
    print(word_name)

    path = "data/spec.json"
    lines = open(path, 'r', encoding='utf-8').readlines()
    data = []
    for i, line in enumerate(lines):
        line = json.loads(line)
        content = line['content']
        if word_name == "" or content.find(word_name) != -1:
            data.append(line)

    response = HttpResponse(json.dumps(data), content_type="application/json")
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

