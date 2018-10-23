import os
import itchat
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import jieba
from pyecharts import WordCloud
from collections import Counter

class WeChat(object):
    def __init__(self):
        itchat.login ()
        self.friends = itchat.get_friends ( update=True )[0:]
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        # print ( self.friends )
        # print ( self.friends[0] )

    def save_info(self,NickName,Sex,Province,City,Signature):
        list=[]
        for i in self.friends:
            dict={}
            dict["NickName"]=i[NickName]
            if i[Sex]==1:
                dict["Sex"]="男"
            elif i[Sex]==2:
                dict["Sex"]="女"
            else:
                dict["Sex"]="不明性别"
            dict["Province"]=i[Province]
            dict["City"]=i[City]
            dict["Signature"]=i[Signature]
            list.append(dict)
        return list
    def save_csv(self):
        list=self.save_info("NickName","Sex","Province","City","Signature")
        # print(list)
        pf=pd.DataFrame(list)
        print(pf)
        try:
            pf.to_csv("wechat.csv",index=True,encoding="gb18030")
        except Exception as ret:
            print(ret)
        return pf

    def anysys(self,pf):
        res_sex = pd.DataFrame(pf["Sex"].value_counts())
        res_province =  pd.DataFrame(pf["Province"].value_counts()[:15])
        res_signature=pd.DataFrame(pf["Signature"][:50])
        index_list = []
        for i in list(res_province.index):
            if i=="":
                i="未知"
            index_list.append(i)
        res_province.index=index_list
        print(res_sex,res_province,res_signature,type(res_province),type(res_sex),type(res_signature))
        return res_sex,res_province,res_signature

    def get_chart(self,train_data, feature_list, x_feature, chart_type, width_bar=None):
        """折线图、散点图、条形图绘制：
        parameters:
            train_data:DataFrame类型
            x_feature：特征，要统计的x轴的数据类别名称
            feature_list:特征列表 
            chart_type: 
                0 : 折线图
                1：散点图
                2：条形图
            width_bar:num类型，条形图条的宽度，必须传值，否则多组数据统计时图形会覆盖                
        """
        try:
            if x_feature and len(feature_list) > 0:
                for i in range(len(feature_list)):
                    feature = feature_list[i]
                    # 设置x轴刻度
                    x_labels = list(train_data.index)
                    x = range(len(x_labels))
                    plt.xticks(x, x_labels)
                    y = train_data[feature]
                    if chart_type == 0:
                        y = train_data[feature]
                        plt.plot(x, y, label=x_feature)
                    elif chart_type == 1:
                        y = train_data[feature]
                        plt.scatter(x, y, label=x_feature)
                    elif chart_type == 2:
                        x = [j + width_bar * i for j in x]
                        plt.bar(x, y, width=width_bar, label=x_feature)
                plt.legend()
                plt.show()
        except Exception as e:
            print(e)


    def get_sign(self,res_signature):
        cut_words_list=[]
        for i in res_signature["Signature"]:
            cut_words=list(jieba.cut(i))
            print(222,cut_words)
            cut_words_list.extend(cut_words)
        print(cut_words_list)
        stop_words=pd.read_table("stopwords_dict.txt")
        print(stop_words)
        for i in stop_words["stop_words"]:
            while i in cut_words_list:
                print(333,i)
                cut_words_list.remove(i)
        print(cut_words_list)
        print(len(cut_words_list))

        k_list=[]
        v_list=[]
        for k,v in Counter(cut_words_list).items():
            k_list.append(k)
            v_list.append(v)
        print(k_list,v_list,len(k_list),len(v_list))
        return k_list,v_list

    def wordcloud(self,x, y, label):
        wordcloud = WordCloud(width=1300, height=620)
        wordcloud.add(label, x, y, word_size_range=[20, 100], shape="star")
        wordcloud.render()
        os.system(r"render.html")

if __name__ == '__main__':
    wechat = WeChat()
    pf = wechat.save_csv()
    res_sex, res_province,res_signature=wechat.anysys(pf)
    # wechat.get_chart(res_sex, ["Sex"],"性别", 2, width_bar=0.2)
    # wechat.get_chart(res_province, ["Province"], "省份", 2, width_bar=0.2)
    k_list, v_list=wechat.get_sign(res_signature)
    label = "词云"
    wechat.wordcloud(k_list, v_list, label)


