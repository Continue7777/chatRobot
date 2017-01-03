# -*- coding: utf-8 -*-
import os
import jieba.analyse
import jieba.posseg as pseg

#writePattertnXml：单个pattern输入，得到aiml结构的一个完整<category>字符串
def writePattertnXml(pattern):
    #查找关键词的句子集合
    sentenceList=[]
    for line in lines:
        if pattern in line:
            sentenceList.append(line)

    sentenceSet=set(sentenceList)

    #建立句子集合的XML格式<li></li>
    randomAnswer=""
    for sentence in sentenceSet:
        randomAnswer += "\n<li>"+sentence+"</li>"

    #建立各个内容，非<aiml标签>,放入问题和答案
    xmlContent='''<category>
            <pattern>'''+"*"+pattern+"*"+'''</pattern>
            <template>
                <random>'''\
               +randomAnswer+'''
                </random>
            </template>
        </category>'''
    return xmlContent

#writePatterListnXml：传入想要得到任意回复的列表，返回一个aiml的完整文档
def writePatterListnXml(patternList):
    xmlContent = ""
    for pattern in patternList:
        xmlContent += writePattertnXml(pattern.encode("utf-8"))+"\n\n"

    xmlStr = '''<aiml version="1.0.1" encoding="UTF-8">'''+xmlContent+'''</aiml>'''
    return xmlStr


def getPatternList(message, topN):
    # 获取文章的前N个关键词
    tags = jieba.analyse.extract_tags(message, topN)
    # 输出名词或者动词
    patternList = []
    for tag in tags:
        for word in pseg.cut(tag):
            if 'v' in word.flag or 'n' in word.flag:
                patternList.append(word.word)

    return patternList

###########################start##########################################
basicPath = os.getcwd()
filePath = os.path.join(basicPath, 'resource\QMessageOut.txt')

fp = open(filePath,'r')
lines=fp.readlines()

fp1 = open(filePath,'r')
allMessage=fp1.read()

patternList = getPatternList(allMessage,20)

xmlStr  = writePatterListnXml(patternList)

outPath = os.path.join(basicPath, 'aiml\qqOut_chat.aiml')
output = open(outPath, 'a+')
output.write(xmlStr)

