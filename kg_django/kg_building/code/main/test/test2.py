
def add_wordlist_2_lexicon(word_list):
    input_path = "../../../resource/lexicon.txt"
    print('Start add_word...')
    lexicon_list = []
    with open(input_path, 'r', encoding='utf-8') as in_f:
        lexicon_lines = in_f.readlines()
        for i, line in enumerate(lexicon_lines):
            line = line.strip()
            lexicon_list.append(line)
    print(len(lexicon_list))
    with open(input_path, 'a') as out_f:
        for word in word_list:
            word = word.strip()
            if word != "" and word not in lexicon_list:
                out_f.write("\n" + word)
                lexicon_list.append(word)
    print(len(lexicon_list))
    print('add_word Ending...')

add_wordlist_2_lexicon(["嘿嘿", "哈哈"])