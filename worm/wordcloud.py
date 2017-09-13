#encoding=utf8
from os import path  
import codecs
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import imread
d = 'C:/Users/guopeng02/Desktop/worm'
#使用UTF-8格式打开文本文件
text = codecs.open(d + '/words200.txt', 'r', 'utf-8').read()
#print(text)
#print(d + "/bg.jpg")
#在背景图的文字里显示词语，首先要保证
#背景图中文字是黑色，底色是白色，
#然后在下面的设置中【背景颜色】一项设置为
#白色，这样出来的效果就是：
#背景是白色，在【背景图】中黑色的文字被词语覆盖。
back_coloring = imread.imread(d + "/bg.jpg")
wc = WordCloud(font_path= r'C:/Users/guopeng02/Desktop/worm/msyh.ttc',
                background_color="white", #背景颜色  
                max_words=2000,# 词云显示的最大词数  
                mask=back_coloring,#设置背景图片  
                max_font_size=100, #字体最大值  
                random_state=42,
                )
#生成字体图片
wc.generate(text)
#plt.figure() 
#展示图片
plt.imshow(wc)  
plt.axis("off")  
plt.show()
#将图片写入文件  
wc.to_file(path.join(d + "/1.png"))  
