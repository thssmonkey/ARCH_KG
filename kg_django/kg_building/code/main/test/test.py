import os
import re

import sys
sys.path.append("..")

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

    '''
    space_index = -1
    for i in range(sen_len):
        if i + 1 < sen_len and origin_sentence[i].isspace() and origin_sentence[i + 1].isalpha():
            space_index = i
            break;

    if space_index != -1:
        for i in range(space_index):
            c = origin_sentence[i]
            if c.isspace():
                continue
            if c.isnumeric() or c == '.':
                haveItem = True
                prefixItem += c
            else:
                haveItem = False
                break

    sentence = origin_sentence
    if space_index != -1:
        sentence = origin_sentence[space_index + 1:]
    return haveItem, prefixItem, sentence
    '''


if __name__ == '__main__':
    input_path = '../../data/test_input.txt'          # 输入的文本文件
    print('Start extracting...')
    cnt = 0
    recordItem = []
    prevItem = ""
    with open(input_path, 'r', encoding='utf-8') as f_in:
        # 预处理
        sentence_tmp = f_in.read().replace(' ', '').replace('􀆰', '.').replace('ꎻ', '；').replace('ꎬ', '，').replace('ꎮ', '。')
        # 分句，获得句子列表
        origin_sentences = re.split('[。？！；]|\n', sentence_tmp)
        for origin_sentence in origin_sentences:
            # 原始句子长度小于2，跳过
            if (len(origin_sentence) <= 2):
                continue
            cnt += 1
            print(origin_sentence)
            # １.１.１.１
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
            print("===== 【" + str(item_level) + "】 【" + sen_item + "】 【" + processed_sentence + "】 ")












