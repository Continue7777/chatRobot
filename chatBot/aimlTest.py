# -*- coding: utf-8 -*-
import aiml
import os
import re

def fitChinese(strOriChinese):
    punctuation = '\…|\•|\、|\……|\“|\”|\—|\，|\》|\《|\·|\。|\!|\"|\#' \
                  '|\$|\%|\&|\‘|\’|\'|\(|\)|\+|\,|\-|\.' \
                  '|\/|\:|\;|\<|\=|\>|\?|\@|\[|\\\\|\]|\^|\_|\`|\{|\||\}|\~|\s+'
    p1 = re.compile(punctuation)
    strChinese = p1.sub(' ',strOriChinese)

    ustring = strChinese.decode("utf-8")
    ustringAddSpace=""
    for i in ustring:
        ustringAddSpace+= i + " "
    strChinese=ustringAddSpace.encode("utf-8")
    return strChinese

path = os.getcwd()
mybot_path = path+'/aiml'
# 切换到语料库所在工作目录
os.chdir(mybot_path)
mybot = aiml.Kernel()
mybot.learn("std-startup.xml")
mybot.respond('load aiml b')

while True:
    print mybot.respond(raw_input("Enter your message >> "))