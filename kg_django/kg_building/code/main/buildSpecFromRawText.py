import os
import re
import json
import sys
sys.path.append("..")
from tool.append_to_json import AppendToJson

def extract_item(origin_sentence):
	prefixItem = ""
	sub_len = 0
	first_num_cnt = 0
	first_dot_cnt = 0
	for i in range(len(origin_sentence)):
		c = origin_sentence[i]
		if c.isalpha():
			sub_len = i
			break;
		if c.isspace():
			continue
		prefixItem += c
		if c.isdigit():
			first_num_cnt += 1
		elif c == '.':
			first_dot_cnt += 1

	item_level = 4
	if first_dot_cnt > 0 and first_num_cnt + first_dot_cnt == len(prefixItem):
		item_level = 1
	elif "(" in prefixItem or ")" in prefixItem:
		item_level = 2
	elif first_num_cnt + first_dot_cnt > 0:
		item_level = 3
	sentence = origin_sentence[sub_len:]
	return item_level, prefixItem, sentence

def strQ2B(ustring):
	ss = ""
	for s in ustring:
		rstring = ""
		for uchar in s:
			inside_code = ord(uchar)
			if inside_code == 12288:  # 全角空格直接转换
				inside_code = 32
			elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
				inside_code -= 65248
			rstring += chr(inside_code)
		ss += rstring
	return ss

directory_set = {"目录"}

def abnormal_detection(origin_sentence):
	origin_sentence = strQ2B(origin_sentence)
	sentence = origin_sentence.replace(' ', '')
	# 原始句子长度小于2，跳过
	if len(sentence) <= 2:
		return True
	if sentence in directory_set:
		return True
	if re.match(r'^\d+\-\d+$', sentence):
		return True

	matchObj = re.match(r'^第\d+[篇章节]', sentence)
	if matchObj:
		sub_str = sentence[len(matchObj.group(0)):]
		directory_set.add(sub_str)
		return True
	matchObj = re.match(r'^第\d+分册', sentence)
	if matchObj:
		sub_str = sentence[len(matchObj.group(0)):]
		directory_set.add(sub_str)
		return True
	matchObj = re.match(r'^附录[A-Za-z\d]+', sentence)
	if matchObj:
		sub_str = sentence[len(matchObj.group(0)):]
		directory_set.add(sub_str)
		return True
	return False

if __name__ == '__main__':
	input_path = '../../data/final_text.txt'
	output_path = '../../data/规范原文.json'

	if os.path.isfile(output_path):
		os.remove(output_path)
	# os.mkdir(output_path)

	print('Start filtering...')

	recordItem = [] # 前缀条目记录
	prevItem = ""   # 上一条前缀条目记录

	specList = []
	reId = 0
	prevLine = ""

	start = False

	with open(input_path, 'r', encoding='utf-8') as f_in:
		# 预处理
		origin_sentences = f_in.readlines()
		# 分句，获得句子列表
		# origin_sentences = re.split('[。？！；]|\n', sentence_tmp)
		for origin_sentence in origin_sentences:
			sen_list = origin_sentence.split("###")
			sen_spec = sen_list[0]
			sen_item = sen_list[1]
			sen_con = sen_list[2]
			sen_con = sen_con.replace(' ', '').replace('􀆰', '.').replace('ꎻ', '；').replace('ꎬ', '，').replace('ꎮ', '。')
			sen_con = sen_con.replace('\n', '').replace('\t', ' ').strip()
			index = sen_con.find(" ")
			sen_con = sen_item + " " + sen_con[index + 1:]
			specList.append({"id": reId + 1, "spec": sen_spec, "item": sen_item, "content": sen_con})
			reId += 1
			'''
			if abnormal_detection(origin_sentence):
				continue

			print('*****')
			# print(origin_sentence)

			# 提取前缀条目信息
			item_level, prefixItem, processed_sentence = extract_item(origin_sentence)
			while recordItem and recordItem[-1][0] >= item_level:
				recordItem.pop()

			sen_item = ""
			if item_level == 1:
				sen_item = prefixItem
			elif item_level == 2:
				if len(recordItem) >= 1:
					sen_item = recordItem[-1][1] + " " + prefixItem
				else:
					sen_item = prefixItem
			elif item_level == 3:
				if len(recordItem) >= 2:
					sen_item = recordItem[-2][1] + " " + recordItem[-1][1] + " " + prefixItem
				elif len(recordItem) >= 1:
					sen_item = recordItem[-1][1] + " " + prefixItem
				else:
					sen_item = prefixItem
			elif item_level == 4:
				sen_item = prevItem
			else:
				sen_item = prefixItem
			prevItem = sen_item
			if item_level != 4:
				recordItem.append((item_level, prefixItem))

			if sen_item == "１.１.１.１":
				start = True

			if start:
				if prevLine != "" and sen_item == prevLine["item"] and processed_sentence != prevLine["content"]:
					specList[reId - 1]["content"] += processed_sentence
				else:
					specList.append({"id": reId + 1, "item": sen_item, "content": sen_item + " " + processed_sentence})
					reId += 1

				prevLine = {"id": reId + 1, "item": sen_item, "content": processed_sentence}
			'''
	for spec in specList:
		AppendToJson().append(output_path, spec)
