'''
 # @ Author: Liaco
 # @ Create Time: 2023-05-13 23:54:09
 # @ Modified by: Liaco
 # @ Modified time: 2023-09-10 18:12:15
 # @ Description:
    将中文数字转换为阿拉伯数字
 '''

import cn2an

def cn2dig(text):
    arabic_text = ""
    idx = 0
    while idx < len(text):
        if text[idx] in {'一', '二', '三', '四', '五', '六', '七', '八', '九'}:
            # 如果当前字符是中文数字，就进行转换
            end_idx = idx + 1
            while end_idx < len(text) and text[end_idx] in {'一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万', '亿'}:
                end_idx += 1
            cn_num = text[idx:end_idx]
            arabic_num = str(cn2an.cn2an(cn_num,mode='normal'))
            arabic_text += arabic_num
            idx = end_idx
        else:
            # 如果当前字符不是中文数字，直接复制到结果中
            arabic_text += text[idx]
            idx += 1
    return arabic_text
    
if __name__ == '__main__':
    text = input('输入中文')
    cn2dig(text)