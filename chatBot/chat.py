# -*- coding: utf-8 -*-
from Tkinter import *
from random import choice
import tkMessageBox
import jieba
import time

#定义变量
botName="bot"
userName="continue"
answer=["你好","我听不懂你在说什么","你真棒","真的么","我还太小了","你说的好多我都听不懂","我叫"+botName]

app = Tk()
app.title('与'+botName+'聊天中')

def sendMessage(event):
	#获得事件 人物 对话内容
	nowtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	botTalk=choice(answer)
	userTalk=E1.get()
	#显示数据
	textMessage.insert(END,userName +"  "+ nowtime + "\n", 'green')
	textMessage.insert(END,userTalk + "\n")
	textMessage.insert(END,botName +"  "+ nowtime + "\n", 'green')
	textMessage.insert(END,botTalk + "\n")
	#分词
	seg_list = jieba.cut(userTalk)
	str=""
	for i in seg_list:
		str+=i.encode("utf-8")+" "
	print str
	textCutJieba.insert(END,"jieba: "+str+"\n")
	#清空输入框
	E1.delete(0, END)
	textMessage.see(END)
	textCutJieba.see(END)

#创建容器1
f1 = Frame(app,height = 100)
f1.pack()
#创建滑轮
scrollbar = Scrollbar(f1)
scrollbar.pack( side = RIGHT, fill=Y )
#添加容器2
f2 = Frame(app,height = "30px")
f2.pack()
#添加容器3
f3 = Frame(app,height=300)
f3.pack()
#添加分词结果窗口
textCutJieba = Text(f3,height = "30px")
textCutJieba.pack()
LabelJieba = Label(f3,text="jieba")
LabelJieba.pack()
#添加聊天窗口
textMessage = Text(f1, yscrollcommand = scrollbar.set)
textMessage.tag_config('green', foreground='#008B00')
textMessage.pack()
scrollbar.config(command=textMessage.yview)
#添加输入框
E1 = Entry(f2, bd = 2, width = 40)
E1.bind('<Return>', sendMessage)
E1.pack(side = LEFT)
#添加按钮
Btn = Button(f2, text = "发送", command = sendMessage)
Btn.pack(side = LEFT)

#主事件循环
app.mainloop()