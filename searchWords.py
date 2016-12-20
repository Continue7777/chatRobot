#-*- coding:utf-8 -*-s
from urllib import quote
import collections
import re
import locale
import time
#定义常量
countValue=2#显示阈值
relateValue=0.05#显示阈值
squareValue=0.05 #三次方的阈值设定
subValue=5#子串独立性

countIndex=0#list索引
relateIndex=1#list索引
squareIndex=2#list索引

wordLen=5#词语最大长度
typeRelate=1#计算type
typeSquare=2#计算type


#功能 ：分解出一个句子中可能的词语和个数
#参数 ：句子str 读取句子的字数number
def analysisSentence(sentence,number,result):
    for wordIndex in range(len(sentence)-number+1):
        word=""
        for i in range(number):
            word+=sentence[wordIndex+i]
        if word not in result:
            result[word] = [0.0]
        result[word][0] += 1.0
    return result

# 字典排序
def sortByCount(dict):
    dict = collections.OrderedDict(sorted(dict.items(), key = lambda t: -t[1][0]))
    return dict

#查询多字词组需要去重复的内容
def findCheckList(str):
    checkList=[]
    for i in range(2, len(str)):
        checkList.append(str[:i])
        checkList.append(str[-i:])
    return checkList

# 查找重复包含的内容，相等则一定是包含用法
def delSameKey(result):
    delList = []
    for word in result:
        #这里需要检查的词需要一定的词频，不然意义不大，也算是个计算优化。
        if len(word) > 2 and result[word][countIndex] > countValue :
            checkList=findCheckList(word)
            #内部查询去重复
            for subWord in checkList:
                #如果有这个子串，并且子串使用频率在一个范围之内
                if result.has_key(subWord):
                    #这里用词频比用比例更好，一定的词频就一定能说明成词规律
                    if result[subWord][countIndex] - result[word][countIndex] <= subValue:
                        delList.append(subWord)
    # 删除多余
    delList = list(set(delList))
    #查看删除了哪些重复的东西
    # for i in delList:
    #     print i

    for name in delList:
        del result[name]
    return result


# 显示
def show():
    for key, value in result.items():
        if len(key) >1 and value[countIndex] > countValue  and value[relateIndex] > relateValue :
            print key + ":%f" % value[countIndex] + " :%f" % value[relateIndex] +" :%f" % value[squareIndex]

    # unicode方式的中文句子拆分，返回句子LIST
def cutArticle(txt):
    # txt格式去空格、制表等符号//这里不用去，只需要做全角半角转化就可以了
    txt.replace(u'\u3000',' ')
    str = txt.encode("utf-8")

    # 根据符号分句
    sentenceList = re.split('\-|\%|\~|\ |\＋|\?|\　|\【|\’|\•|\‘|\！|\!|\+|\…|\·|\—|\〈|\〉|\；|\}|\{|\[|\]|\>|\<|\》|\《|\\\\|\||\=|\'|\"|\”|\“|\/|\：|:|\（|\）|\)|\(|\.|,|; |\，|\。|\、|\？|\*|\s+|\w+|\n', str)
    return sentenceList

def analysisEngAndInt(txt,result):
    p = re.compile(r'\w+')
    list=p.findall(txt)
    for word in list:
        if word not in result:
            result[word] = 0.0
        result[word] += 1.0
    return result

#判断是否还有英文字母
def containEnglish(string):
    for c in string:
        if c.isalpha():
            return True
    return False

#判断是否是中文
def isChinese(uchar):
    #判断一个unicode是否是汉字
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

#计算相对词语紧密度
def countScore(result,type):
    if type == typeRelate:
        #遍历每一个词语，长度不为1
        for word in result:
            if (len(word) > 1) and isChinese(word[0]):
                #得到的value为词语个数除以字的个数
                result[word].append( pow(result[word][countIndex], len(word)) )
                for character in word:
                    result[word][relateIndex] = result[word][relateIndex] / result[character][countIndex]
        return result
    #选取一个大于阈值加分，小与阈值减分的措施。
    if type == typeSquare:
        for word in result:
            if (len(word) > 1) and isChinese(word[0]):
                #得到的value为词语个数除以字的个数
                result[word].append(0.0)
                for character in word:
                    if result[word][countIndex]/result[character][countIndex]-squareValue > 0: #x表示隔阈值的远近
                        x=1
                    else:
                        x=-1
                    result[word][squareIndex] = result[word][squareIndex] + x
        return result
start=time.clock()
#定义全局结果集
result={}

#打开文件
fp = open("e:\content.txt",'r')
txt=fp.read().decode("utf-8")

#解析英文
#result=analysisEngAndInt(txt,result)
#拆分句子
sentenceList=cutArticle(txt)
#解析句子
for sentence in sentenceList:
    sentence=sentence.decode("utf-8")
    #句子预处理，抽出其中的数字和英文
    for wordNumber in range(1,wordLen+1):
        result=analysisSentence(sentence,wordNumber,result)


result = countScore(result,typeRelate)
result = countScore(result,typeSquare)
delSameKey(result)
result = sortByCount(result)
show()
