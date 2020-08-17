import json
import requests
import csv
import pandas as pd
import numpy as np

#/Users/liyang/desktop/comp9900/project/readbook/data.csv

####################### 数据处理 #############################

# 把书名合并，如果没有子标题就直接返回主标题
def CombineTitle(title,subtitle):
    res = title+": "+subtitle
    return res

# isbn处理
def getISBN(obj):
    for i in obj:
        if i['type']=='ISBN_13':
            return i['identifier']

# 处理图片地址
def getImageLink(obj):
    if obj['smallThumbnail']!='':
        return obj['smallThumbnail']
    else:
        return obj['thumbnail']

# 处理作者
def getAuthors(obj):
    str = ','
    return str.join(obj)

# 处理分类

def getCategories(obj):
    str=','
    return str.join(obj)

# 总处理
def process(book):
    res = dict()
    detail = book["volumeInfo"]
    res['id']=book["id"]
    if 'subtitle' in detail:    
        res['title']=CombineTitle(detail['title'],detail['subtitle'])
    else:
        res['title']=detail['title']
    if 'authors' in detail:
        res['authors']=getAuthors(detail['authors'])
    else:
        res['authors']=''
    if 'publisher' in detail: 
        res['publisher'] = detail['publisher']
    else:
        res['publisher']=''
    if 'publishedDate' in detail:
        res['publish_date'] = detail['publishedDate']
    else:
        res['publish_date'] =''
    if 'pageCount' in detail:
        res['page_count']=detail['pageCount']
    else:
        res['page_count']=''
    if 'categories' in detail:
        res['categories']= getCategories(detail['categories'])
    else:
        res['categories']=''
    if 'description' in detail:
        res['description']=detail['description']
    else:
        res['description']=''
    if 'industryIdentifiers' in detail:
        res['ISBN']=getISBN(detail['industryIdentifiers'])
    else:
        res['ISBN']=''
    if 'imageLinks' in detail:
        res['imageLink'] = getImageLink(detail['imageLinks'])
    else:
        res['imageLink']=''
    return res

#################### 写入csv ##################

    
#################### ajax ###################

def ajax(obj):
    url="https://www.googleapis.com/books/v1/volumes?q=/"+obj
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',}
    response = requests.get(url=url,headers=headers)
    data = response.text
    data = json.loads(data)
    return data


if __name__ == "__main__":

    label = ['id','title','authors','publisher','publish_date','page_count','categories','ISBN','imageLink']
    # already_input_keyword_01=['python','java','linux','harryporter','Holmes','Django','Twilight','cook',
    # 'Shakespeare','hugo','Algorithm','Vampire','Verne','Ocean','Food','Fruit','Maya','Egypt','Roma',
    # 'Carthage','United Kingdom','Blues','Rock','sex','education','love','friend','countryside','airplane','magic','speaking',
    # 'alcohol','Alexandre Dumas','Goethe','Dante','Tagore','Leo Tolstoy','Maxim Gorky','Hemingway','Balzac','Pushkin',
    # 'cat','dog','chocolate','pie','database','IBM','piano','violin','elves','tank','cake','tea','coffee','pizza','milk','rose','spring','shark','lion','cache','cpu','gpu','intel','newspaper','law','sun','moon','basketball','football']

    # item_list=[]
    # key_word=[]
    # for i in key_word:
    #     data=ajax(i)
    #     for j in data['items']:
    #         item_list.append(j)

    # df=pd.DataFrame(columns=label)
    df = pd.read_csv("data02.csv")
    # for i in item_list:
    #     temp=process(i)
    #     df = df.append(temp,ignore_index=True)

    
###### 筛选 #########
    # "~"->取反
    # df=df[~df['ISBN'].isnull()]
    # df=df[~df['authors'].isnull()]
    # df=df[~df['publisher'].isnull()]
    # df=df[~df['page_count'].isnull()]
    # df=df[~df['categories'].isnull()]
    df['page_count']=df['page_count'].astype(int)
    df['ISBN']=df['ISBN'].astype(int)
    df.to_csv("data02.csv",index=False)


# 通过 django shell插入数据，注意数据类型和model的类型是否一致
# >>> import csv
# >>> from backed.models import *
# >>>
# >>> f=open('data.csv')
# >>> reader = csv.reader(f)
# >>> for row in reader:
# ...     Book.objects.update_or_create(id=row[0],title=row[1],authors=row[2],publisher=row[3],publish_date=row[4],page_count=row[5],categories=row[6],ISBN=row[7],imageLink=row[8],description=row[9])

# 


##处理csv heder 手动删除就行了…………s