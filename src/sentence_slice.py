'''
 # @ Author: Liaco
 # @ Create Time: 2023-05-13 23:54:09
 # @ Modified by: Liaco
 # @ Modified time: 2023-09-10 18:13:49
 # @ Description:
 '''

import re

from src.cn2dig import cn2dig


def sentence_slice(sentence_list: list):

    def extract_lines_with_string(text, target_strs):  # 显示删除的文本。
        x = '\n ------------------------以下是未录入文本-------------------------\n\n'
        lines = text.split('\n')
        result = []
        for line in lines:
            for target_str in target_strs:
                if re.search(target_str, line):
                    result.append(line)
                    break
        result_text = '\n'.join(result)
        s = x+result_text
        return s.splitlines()

    target_strs = ['平', '三中三', '二中二', '3中3', '2中2', '复式',
                   '连肖', '三连', '女', '3肖', '三肖', '家', '五肖']  # 删除所含关键字的文本。
    chars_to_find = ["澳门", "门", "奥", "澳", "们",
                     "香港", "港", "香"]              # 需要查找的字符列表

    sentences_list = sentence_list
    try:
        for i in range(len(sentences_list)):
            for char in chars_to_find:
                if char in sentences_list[i]:
                    # 将字符放到该元素的首位
                    sentences_list[i] = char + \
                        sentences_list[i].replace(char, "", 1)
    except:
        pass
    text = "\n".join(sentences_list)
    text = re.sub(r'(\d{3,})', r'\1\n', text)
    text = re.sub(r'赚:', '', text)
    text = re.sub('[Oo]', '0', text)
    text = re.sub(r'(各|一|每|个)肖', '包肖', text)
    text = re.sub(r'包肖(\d+)', r'包肖\1\n', text)
    text = re.sub(r'各(\d+)', r'各\1\n', text)
    text = re.sub(r'(各数|个数)(\d+)', r'\1\2\n', text)
    text = re.sub(r'(\d+)(元|米|斤)', r'\1\2\n', text)
    text = re.sub(r'(共|计|记)(\d+)', '', text)

    try:
        del_text = extract_lines_with_string(
            text=text, target_strs=target_strs)  # 显示删除的文本
    except:
        del_text = '无'
    for s in target_strs:
        text = re.sub(r'[\n\\s]*.*'+s+'.*[\n\\s]*', '\n', text)  # 删除所含关键字的文本。

    text = cn2dig(text)
    text = re.sub(r'十', r'10', text)
    text = re.sub(r'(\d{3,})', r'\1\n', text)
    sentences_list = text.split('\n')
    sentences_list = [s for s in sentences_list if s]
    sentences_list = [item for item in sentences_list if any(
        char.isdigit() for char in item)]
    try:
        with open('../output/已录入数据.txt', 'w', encoding='utf-8') as f:
            for sentence in sentences_list:
                f.write(sentence + '\n')

        with open('../output/未录入数据.txt', 'w', encoding='utf-8') as f:
            f.write(del_text)
    except:
        pass

    return sentences_list, del_text


def input_text(path):
    path = ''
    path = input('输入文本地址，默认地址直接按空格即可')
    if path == '':
        path = '../output/input.txt'
    with open(f'{path}', 'r', encoding='utf-8') as f:
        text = f.read()
        text = re.sub(r'赚:', r'', text)
        sentences_list = text.split('\n')
    return sentences_list


if __name__ == '__main__':
    path = ''
    print(sentence_slice(input_text(path)))
