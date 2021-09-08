import os
import json
import re
import sys
os.chdir(os.path.dirname(__file__))
sys.path.append("..")
from core.nlp import NLP
from core.extractor import Extractor

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

def main_run():
    os.chdir(os.path.dirname(__file__))
    input_path = '../../data/规范原文.json'          # 输入的文本文件
    output_path = '../../data/knowledge_triple.json'  # 输出的处理结果Json文件

    if os.path.isfile(output_path):
        os.remove(output_path)
    # os.mkdir(output_path)

    print('Start extract...')

    # NLP(分词，词性标注，命名实体识别，依存句法分析)
    nlp = NLP()
    num = 1  # 关系知识三元组

    with open(input_path, 'r', encoding='utf-8') as f_in:
        # 预处理
        sentence_lines = f_in.readlines()
        for i, line in enumerate(sentence_lines):
            line = json.loads(line)
            item = line['item']
            spec = line['spec']
            sentence_content = line['content']
            origin_sentence = sentence_content
            sentence_content = sentence_content.split(item + " ")[1]
            # 分句，获得句子列表
            line_sentences = re.split('[。？！；]|\n', sentence_content)

            for line_sentence in line_sentences:
                # 分词处理 jieba分词工具
                lemmas = nlp.segment(line_sentence)
                # 词性标注 ltp
                words_postag = nlp.postag(lemmas)
                # 命名实体识别 ltp
                words_netag = nlp.netag(words_postag)
                #for word in words_netag:
                #    if word.postag not in pos_list:
                #        pos_list.append(word.postag)
                #    print(word.to_string())
                # 依存句法分析 ltp
                dealed_sentence = nlp.parse(words_netag)
                #print(dealed_sentence.to_string())

                extractor = Extractor()
                num = extractor.extract(origin_sentence, dealed_sentence, output_path, num, spec, item)

    print("extract End...")

if __name__ == '__main__':
    main_run()