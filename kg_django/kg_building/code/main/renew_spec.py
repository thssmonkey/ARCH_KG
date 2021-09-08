import os
import re
import json
import sys
os.chdir(os.path.dirname(__file__))
sys.path.append("..")
from tool.append_to_json import AppendToJson

def main_run():
	os.chdir(os.path.dirname(__file__))
	kn_path = '../../data/lexicon.json'
	spec_path = '../../data/规范原文.json'
	output_path = "../../data/spec.json"

	if os.path.isfile(output_path):
		os.remove(output_path)
	# os.mkdir(output_path)

	print('Start renew_spec...')

	kn_lines = open(kn_path, 'r', encoding='utf-8').readlines()
	print(len(kn_lines))
	kn_dic = dict()
	for i, line in enumerate(kn_lines):
		line = json.loads(line)
		arrays = line['关系']
		name1 = arrays[0]
		name2 = arrays[2]
		content = line['句子']
		if content not in kn_dic.keys():
			kn_dic[content] = []
		if len(name1) >= 2 and name1 not in kn_dic[content]:
			kn_dic[content].append(name1)
		if len(name2) >= 2 and name2 not in kn_dic[content]:
			kn_dic[content].append(name2)

	spec_lines = open(spec_path, 'r', encoding='utf-8').readlines()
	print(len(spec_lines))
	cnt = 0
	notempty_cnt = 0
	for i, line in enumerate(spec_lines):
		cnt += 1
		line = json.loads(line)
		_id = line["id"]
		_spec = line["spec"]
		_item = line['item']
		_content = line["content"]
		_word_list = []
		if _content in kn_dic.keys():
			_word_list = kn_dic[_content]
		if len(_word_list) == 0:
			notempty_cnt += 1
		AppendToJson().append(output_path, {"id": _id, "spec": _spec, "item": _item, "content": _content, "words": _word_list})
	print(cnt, notempty_cnt)
	print("renew_spec End......")

if __name__ == '__main__':
	main_run()