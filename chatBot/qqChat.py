#-*- coding:utf-8 -*-
import re
import os
import collections
import jieba

class Conversation:
    content=""
    userName=""
    wordList=[]

    def __init__(self,content,userName):
        self.content = content
        self.userName = userName

    def cutWord(self):
        segList=jieba.cut(content)
        self.wordList=list(segList)

    def getWordList(self):
        string = ""
        for word in self.wordList:
            string += word+" "
        return string

def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 12288:  # 全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += unichr(inside_code)
    return rstring

def cutArticle(ustr):
    # 全角半角转化
    ustr=strQ2B(ustr)
    #转成str格式方便re处理
    str = ustr.encode("utf-8")
    # 根据符号分句
    punctuation = '\!|\,|\.|\。|\?|\s+'
    sentenceList = re.split(punctuation, str)
    return sentenceList

def analysisSentence(sentenceList):
    for sentence in sentenceList:
        if sentence not in chatMessageDict:
            chatMessageDict[sentence] = 1
        else:
            chatMessageDict[sentence] += 1

def isChinese(uchar):
    #判断一个unicode是否是汉字
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

def sortByCount(dict):
    dict = collections.OrderedDict(sorted(dict.items(), key = lambda t: -t[1]))
    return dict

def countList(list,result):
    for word in range(len(list)+1):
        if word not in result:
            result[word] = 0.0
        result[word] += 1.0
    return result

chatMessageList = []
chatMessageDict = {}
allMessage=""

basicPath = os.getcwd()
filePath = os.path.join(basicPath, 'resource\QMessage.txt')
print filePath

fp = open(filePath,'r')
lines=fp.readlines()

#整理成一个字符串
for line in lines:
    if('花海' in line):
        content = lines[lines.index(line)+1].replace("\n","")
        if content != "":
            allMessage+=content+" "
#分词探究
# wordDict = {}
# seg_list = list(jieba.cut(allMessage))
# for i in seg_list:
#     if isChinese(i) is False:
#         del seg_list[seg_list.index(i)]
# seg_set = set(seg_list)
#
# for item in seg_set:
#     wordDict[item] = seg_list.count(item)
#
# wordDict = sortByCount(wordDict)
# for word,value in wordDict.items():
#     print str(value)+word


#统计个数，可以找到一些常用的口头回答，比如 嗯嗯 好的 好好好 握草 等。。。
# sentenceList = cutArticle(allMessage.decode("utf-8"))
# analysisSentence(sentenceList)
# chatMessageDict=sortByCount(chatMessageDict)
# print len(chatMessageDict)
#
# for sentence,value in chatMessageDict.items():
#     print str(value)+" "+sentence

#用对象去存储
# for line in lines:
#     if('tinue' in line):
#         content = lines[lines.index(line)+1].replace("\n","")
#         if content != "":
#             conversation = Conversation(content=content, userName='花海')
#             conversation.cutWord()
#             chatMessageList.append(conversation)

outPath = os.path.join(basicPath, 'resource\QMessageOut.txt')
output = open(outPath, 'a+')

sentenceList = cutArticle(allMessage.decode("utf-8"))

for i in sentenceList:
    output.write(i+"\n")

