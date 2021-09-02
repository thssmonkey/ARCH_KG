import os
import re
import json
import sys
sys.path.append("..")
from tool.append_to_json import AppendToJson

if __name__ == '__main__':
	lexicon_name = "lexicon"
	input_path = '../../data/' + lexicon_name + ".json"
	output_path = '../../data/' + lexicon_name + ".json"

	print('Start filtering repeat...')
	had_dict = {}
	lines = open(input_path, 'r', encoding='utf-8').readlines()

	if os.path.isfile(output_path):
		os.remove(output_path)
	
	for i, line in enumerate(lines):
		line = json.loads(line)
		content = line['句子']
		arrays = line['关系']
		name1 = arrays[0]
		relation = arrays[1].replace('：','').replace(':','').replace('　','').replace(' ','').replace('【','').replace('】','')
		name2 = arrays[2]
		if relation.strip() == "" or name1.strip() == "" or name2.strip() == "":
			continue
		triple = name1 + "->" + relation + "->" + name2
		if content not in had_dict.keys():
			had_dict[content] = []
		if triple not in had_dict[content]:
			had_dict[content].append(triple)
			AppendToJson().append(output_path, line)
			print(triple)
		else:
			print("[重复] - " + triple)
	print("Ending...")