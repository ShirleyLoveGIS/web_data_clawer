# -*- coding: utf-8 -*-
#
# image spider for grabbing images from search engine, like Baidu pic;
#
# download origin image from OjbURL with multi kayword in keyword.txt



import re
import requests
from urllib import error
from bs4 import BeautifulSoup
import os
 
num = 0
numPicture = 0

keyword_file = "./keyword.txt"
folder_total = "./img_spider_v4_folder"

List = []
 
 
def Find(url):
    global List

    print ("calculate image total number, wait...")
    t = 0
    i = 1
    s = 0
    while t < 1000:
        Url = url + str(t)
        try:
            Result = requests.get(Url, timeout=7)
        except BaseException:
            t = t + 60
            continue
        else:
            result = Result.text
            pic_url = re.findall('"objURL":"(.*?)",', result, re.S)
            s += len(pic_url)
            if len(pic_url) == 0:
                break
            else:
                List.append(pic_url)
                t = t + 60
    return s
 
 
def recommend(url):
    Re = []
    try:
        html = requests.get(url)
    except error.HTTPError as e:
        return
    else:
        html.encoding = 'utf-8'
        bsObj = BeautifulSoup(html.text, 'html.parser')
        div = bsObj.find('div', id='topRS')
        if div is not None:
            listA = div.findAll('a')
            for i in listA:
                if i is not None:
                    Re.append(i.get_text())
        return Re
 
 
def dowmloadPicture(html, keyword):
    global num
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)
    
    print("images with keyword:" + keyword + ", read to download")
    for each in pic_url:
        print ("downloading id: " + str(num + 1) + " image with URL: " + str(each))
        try:
            if each is not None:
                pic = requests.get(each, timeout=7)
            else:
                continue
        except BaseException:
            print ("wrong image, ignore")
            continue
        else:
            string = os.path.join(folder_total, (keyword + '_' + str(num) + '.jpg'))
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            num += 1
        if num >= numPicture:
            return
 
 
if __name__ == '__main__':
    
    img_num_each_cls = 1000
    numPicture = img_num_each_cls

    if not os.path.exists(folder_total):
        os.mkdir(folder_total)

    line_list = []
    with open(keyword_file, encoding='utf-8') as f_read:
        line_list = [k.strip() for k in f_read.readlines()]
 
    for word in line_list:
        url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&pn='
        tot = Find(url)
        Recommend = recommend(url)
        print ("class: {0}, total image: {1}".format(word, tot))

        t = 0
        tmp = url
        while t < numPicture:
            try:
                url = tmp + str(t)
                result = requests.get(url, timeout=10)
                print (url)
            except error.HTTPError as e:
                print ("network error, try again")
                t = t + 60
            else:
                dowmloadPicture(result.text, word)
                t = t + 60
        numPicture = numPicture + img_num_each_cls
