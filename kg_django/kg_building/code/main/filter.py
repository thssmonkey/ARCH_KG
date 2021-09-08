import os
import re
import json
import sys
os.chdir(os.path.dirname(__file__))
sys.path.append("..")
from tool.append_to_json import AppendToJson

def main_run():
	os.chdir(os.path.dirname(__file__))
	lexicon_name = "lexicon"
	input_path = '../../data/knowledge_triple.json'
	output_path = '../../data/' + lexicon_name + ".json"
	lexicon_path = "../../resource/" + lexicon_name + ".txt"

	if os.path.isfile(output_path):
		os.remove(output_path)
	# os.mkdir(output_path)

	print('Start filtering...')

	lexicon_list = []
	lexicon_lines = open(lexicon_path, 'r', encoding='utf-8').readlines()
	for i, line in enumerate(lexicon_lines):
		line = line.strip()
		lexicon_list.append(line)
	print(len(lexicon_list))

	triple_list = []
	lines = open(input_path, 'r', encoding='utf-8').readlines()
	print(len(lines))
	for i, line in enumerate(lines):
		line = json.loads(line)
		#print(line)
		arrays = line['关系']
		name1 = arrays[0]
		relation = arrays[1].replace('：','').replace(':','').replace('　','').replace(' ','').replace('【','').replace('】','')
		name2 = arrays[2]
		if relation.strip() == "" or name1.strip() == "" or name2.strip() == "":
			continue
		triple = name1 + "->" + relation + "->" + name2
		if triple not in triple_list:
			triple_list.append(triple)
		if name1 in lexicon_list and name2 in lexicon_list:
			AppendToJson().append(output_path, line)
			# print(triple)
		else:
			# print("[不匹配] - " + triple)
			pass
	print("filter Ending...")

if __name__ == '__main__':
	main_run()