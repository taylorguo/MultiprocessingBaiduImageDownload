# -*- coding:utf-8 -*-
import re,os
import requests
from pypinyin import lazy_pinyin
import unicodedata


def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def hanzi_pinyin(word):
    p_dict = lazy_pinyin(word)
    p=""
    for i in p_dict:
        p = p+i+"_"
    return p[:-1]

def dowmloadPic(html, keyword, nb_page=1):
    # if is_Chinese(keyword):
    if 0:
        pinyin_word = hanzi_pinyin(keyword)

        if not os.path.exists("../datasets"):
            os.mkdir("../datasets")
        if not os.path.exists("../datasets/"+pinyin_word):
            os.mkdir("../datasets/"+pinyin_word)

        sub_folder = pinyin_word
    else:
        sub_folder = keyword
        if not os.path.exists("../datasets/"+keyword):
            os.mkdir("../datasets/"+keyword)

    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)
    i = 1
    print('找到关键词:' + keyword + '的图片，现在开始下载图片...')
    for each in pic_url:
        print('正在下载第' + str(i) + '张图片，图片地址:' + str(each))
        try:
            pic = requests.get(each, timeout=10)
        except requests.exceptions.ConnectionError:
            print('【错误】当前图片无法下载')
            continue

        dir = '../datasets/' + sub_folder + '/'+ keyword + '_' + str(nb_page) +'_'+str(i) + '.jpg'
        fp = open(dir, 'wb')
        fp.write(pic.content)
        fp.close()
        i += 1

def DownloadImage(each, i, ):
    pass

def dowmload_pic(html, keyword, nb_page=1):
    # if is_Chinese(keyword):
    if 0:
        pinyin_word = hanzi_pinyin(keyword)

        if not os.path.exists("../datasets"):
            os.mkdir("../datasets")
        if not os.path.exists("../datasets/"+pinyin_word):
            os.mkdir("../datasets/"+pinyin_word)

        sub_folder = pinyin_word
    else:
        sub_folder = keyword
        if not os.path.exists("../datasets/"+keyword):
            os.mkdir("../datasets/"+keyword)

    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)
    i = 1
    print('      找到关键词:' + keyword + '的图片，现在开始下载图片...')
    for each in pic_url:
        dir = '../datasets/' + sub_folder + '/'+ hanzi_pinyin(keyword) + '_' + str(nb_page) +'_'+str(i) + '.jpg'
        if not os.path.exists(dir):
            
            print('      正在下载第' + str(i) + '张图片，图片地址:' + str(each))
            try:
                pic = requests.get(each, timeout=30)
            except requests.exceptions.ConnectionError:
                print('      【错误】当前图片无法下载')
                continue

            fp = open(dir, 'wb')
            fp.write(pic.content)
            fp.close()
        i += 1

def get_urls(word):
    url1 = "http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word="+word+"&pn=0&gsm=50&ct=&ic=0&lm=-1&width=0&height=0"
    url2 = "http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word="+word+"&pn=80&gsm=78&ct=&ic=0&lm=-1&width=0&height=0"
    url3 = "http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word="+word+"&pn=120&gsm=a0&ct=&ic=0&lm=-1&width=0&height=0"
    url4 = "http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word="+word+"&pn=180&gsm=dc&ct=&ic=0&lm=-1&width=0&height=0"
    url5 = "http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word="+word+"&pn=240&gsm=118&ct=&ic=0&lm=-1&width=0&height=0"
    url6 = "http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word="+word+"&pn=300&gsm=0&ct=&ic=0&lm=-1&width=0&height=0"
    return [url1, url2, url3, url4, url5, url6]

def down_keyword_images(item):
    (num, word) = item
    print(" ********** Processing No. %d keyword : %s"%(num+1, word))
    for n, url in enumerate(get_urls(word)):
        try:
            result = requests.get(url)
            dowmload_pic(result.text, word, nb_page=n+1)
        except Exception as e:
            print(e)
            return

if __name__ == '__main__':
    get_more_than_300_images = 1
    
    if not get_more_than_300_images:
        word = input("Input key word: ")
        url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&ct=201326592&v=flip'
        result = requests.get(url)
        dowmloadPic(result.text, word)
    else:
        lines = []
        with open("keydirs.txt", "r", encoding="utf-8") as txtfile:
            for n, line in enumerate(txtfile.readlines()):
                lines.append((n, line.strip()))
        from tqdm import tqdm
        import multiprocessing
        #for num, word in enumerate(lines):
        pool = multiprocessing.Pool(processes=8)
        with tqdm(total=len(lines)) as bar:
            for _ in pool.imap_unordered(down_keyword_images, lines):
                bar.update(1)
    
    # cn_char = "你好"
    #
    # # if is_Chinese(cn_char):
    # #     p_dict = lazy_pinyin(cn_char)
    # #     p=""
    # #     for i in p_dict:
    # #         p = p+i+"_"
    # # p = p[:-1]
    # p =  hanzi_pinyin(cn_char)
    #
    # print("Unicodedata: ", p)