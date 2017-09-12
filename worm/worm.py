#!/usr/bin/env python


import re
from urllib import request
from bs4 import BeautifulSoup as bs

import jieba
import jieba.analyse

#import matplotlib.pyplot as plt
#一，载入网页
#设置网址
resp = request.urlopen('http://k.autohome.com.cn/spec/23721/index_2.html#dataList')
#使用GBK读取网页
html_data = resp.read().decode('gbk')

#使用BeautifulSoup的html.parser解释网页
soup = bs(html_data, 'html.parser')

#二、数据抓取
#在汽车之家口碑频道里，所有评价都包含在
#属性【id】中含有【divfeeling】的【div】标签中

#查找属性【id】中含有【divf】值的标签【div】取出来
#注意，这里取出来的是评论的集合！！！
feelings = soup.findAll('div', id=re.compile('^divf'))

#三、数据清洗
#去除所有标签，及不必要的全角标点符号
#把所有评论拼成一个大字符串！！！

#只匹配中文字符
pattern = re.compile('[\u4e00-\u9fa5]+')

#针对每一个评论体进行清洗
completed = ''
for feeling in feelings:
    washed = re.findall(pattern, feeling.text)
    #合并为一个字符串
    completed = completed + ','.join(washed)

#去掉半角逗号（生成数组时自带的）
completed = completed.replace(',', '')

#四、词频分析
#使用jieba进行分析
#segment = jieba.lcut(completed)

#统计出现频率最高的前N个词
tags = jieba.analyse.extract_tags(completed, 50)

print(",".join(tags))
