import re

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

def abnormal_detection(origin_sentence):
    origin_sentence = strQ2B(origin_sentence)
    sentence = origin_sentence.replace(' ', '')
    # 原始句子长度小于2，跳过
    if len(sentence) <= 2:
        return True, ""
    matchObj = re.match(r'^\d+\-\d+$', sentence)
    if matchObj:
        return True, sentence[len(matchObj.group(0)):]
    matchObj = re.match(r'^第\d+[篇章节]', sentence)
    if matchObj:
        return True, sentence[len(matchObj.group(0)):]
    matchObj = re.match(r'^第\d+分册', sentence)
    if matchObj:
        return True, sentence[len(matchObj.group(0)):]
    matchObj = re.match(r'^附录[A-Za-z\d]+', sentence)
    if matchObj:
        return True, sentence[len(matchObj.group(0)):]
    return False, ""

str = "第１０ 篇　 第2章"
flag, dir = abnormal_detection(str)
print(flag, dir)
