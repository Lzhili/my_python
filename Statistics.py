# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:10:09 2020

@author: Lzhili
"""

import jieba
import wordcloud
import matplotlib.pyplot as plt

with open('r.json', 'r', encoding='utf-8') as f:
    strs = f.read()
for ch in r':"¥,{}./【】0123456789abcdefghijklmnopqrstuvwxyz ':
    strs = strs.replace(ch, '')        
words = jieba.lcut(strs)
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
provinces = {}
txt = ''
includes = {'北京','天津','上海','重庆','河北','山西','辽宁','吉林','黑龙江',
            '浙江','江苏','安徽','福建','江西','山东','河南','河北','湖北',
            '湖南','广东','海南','四川','贵州','陕西','云南','甘肃','青海'}
for province in includes:
    if province in counts.keys():
        provinces[province] = counts[province]
provinces = list(provinces.items())
provinces.sort(key = lambda x : x[1], reverse = True)
num = 0
print('4400件商品中货源前10的省份：')
for i in range(1,11):
    key, value = provinces[i-1]
    print("{:<5}{:>5}".format(key, value))
    key1 = key +' '
    txt += key1 * value
    num += value
w = wordcloud.WordCloud(height = 1000, width = 1500, font_path='msyh.ttc', collocations=False)
w.generate(txt)
w.to_file('wordcloud.png')
print('-' * 50) 
print('根据上述结果生成词云！')

labels = []
sizes = []
plt.rcParams['font.family']='SimHei'
for province, number in provinces[:10]:
    labels.append(province)
    scale = number/num
    sizes.append(round(scale * 100))   
explode = (0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
plt.title('货源前10商品的饼状图')    
plt.axis('equal')
plt.savefig('pie', dpi=800)
plt.show()        