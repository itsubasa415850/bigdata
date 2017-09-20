# encoding=utf8
# !/usr/bin/env python


import re
import urllib2
from bs4 import BeautifulSoup as bs
import jieba.analyse

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import imread

#伪装成浏览器
headers = {
    'User-Agent':'Mozilla/5.0(Windows; U; Windows NT 6.1; en-US; '
                 'rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}
testee = ''
final = ''
dir = r'C:/Users/guopeng02/Desktop/worm/'
for num in range(2, 10):
    print('现在开始爬第' + str(num) + '页的口碑。')
    # 一，载入网页
    # 设置网址
    request = urllib2.Request(url='http://k.autohome.com.cn/spec/23721/index_' + str(num) + '.html#dataList',
                              headers=headers)
    # 使用GBK读取网页
    response = urllib2.urlopen(request)
    html_data = response.read().decode('gbk')
    # 使用BeautifulSoup的html.parser解释网页
    soup = bs(html_data, 'html.parser')
    # 二、数据抓取
    # 在汽车之家口碑频道里，所有评价都包含在
    # 属性【id】中含有【divfeeling】的【div】标签中
    # 查找属性【id】中含有【divf】值的标签【div】取出来
    # 注意，这里取出来的是评论的集合！！！
    feelings = soup.findAll('div', id=re.compile('^divf'))
    # print feelings
    # 三、数据清洗
    # 去除所有标签，及不必要的全角标点符号
    # 把所有评论拼成一个大字符串！！！
    # 只匹配中文字符和英文单词。
    pattern = re.compile(u'[0-9a-zA-Z]+|[\u4e00-\u9fa5]+')

    # 针对每一个评论体进行清洗
    completed = ''
    for feeling in feelings:
        washed = re.findall(pattern, feeling.text)
        # 合并为一个字符串并且编码为UTF-8
        completed = completed + ','.join(washed).encode('utf8')
        # 去掉半角逗号（生成数组时自带的）
        completed = completed.replace(',', '')
    # 结果合并
    testee += completed
print('分析过程开始。')
# 四、词频分析
# 统计出现频率最高的前N个词
tags = jieba.analyse.extract_tags(testee, 100)
# print('初筛之后的结果：')
# print(",".join(tags))
# 五、停用词筛出
# 载入停用词列表文件
print '停用词筛出'
stopwords = {}.fromkeys([line.rstrip() for line in open(dir + 'stop_words_zh_UTF-8.txt', mode='r')])
#, encoding='UTF-8'
for tag in tags:
    if tag not in stopwords:
        final += ' ' + tag
# 六、写入文件
# print('写入文件')
# file = open(dir + 'words200.txt', mode='w')#, encoding='UTF-8'
# file.write(" ".join(final).encode('utf8'))
#七、生成图片
back_coloring = imread.imread("C:/Users/guopeng02/Desktop/worm/bg.jpg")
wc = WordCloud(font_path= r'C:/Users/guopeng02/Desktop/worm/msyh.ttc',
                background_color="white", #背景颜色
                max_words=2000,# 词云显示的最大词数
                mask=back_coloring,#设置背景图片
                max_font_size=100, #字体最大值
                random_state=42,
                )
print '分析过程结束。'
#生成字体图片
print '生成字体图片'
wc.generate(final)
#plt.figure()
#展示图片
print '展示图片'
plt.imshow(wc)
plt.axis("off")
plt.show()
#将图片写入文件
wc.to_file('C:/Users/guopeng02/Desktop/worm/1.png')
print '全部完成。'