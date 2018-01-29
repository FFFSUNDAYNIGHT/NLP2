# Tis file is the setup file
from Keysente import KeysenteEx
from Keyword import KeywordEx

def main_func(filename, funcnum, keynum):
    if funcnum == 1:
        k = KeysenteEx()
        return k.docsummary(filename, Keynum =keynum)
    elif funcnum == 2:
        k = KeywordEx()
        return k.keyword(filename, Keynum = keynum)
    elif funcnum == 3:
        k = KeywordEx()
        return k.keyphrase(filename, Keynum = keynum)

if __name__ == '__main__':
    print('请输入要处理的文件名：',end='')
    s = input()
    print('-------------------------')
    print('功能号1：提取关键句        ')
    print('功能号2：提取关键词        ')
    print('功能号3：提取关键词组      ')
    print('-------------------------')
    funcnum = input()
    print('请输入要提取的关键词/关键句的数量：',end='')
    keynum = input()
    print(main_func(s,int(funcnum), int(keynum)))