# --*-- coding: utf-8 --*--
# @Time     : 2020/3/14 11:24
# @Author   : mrqinglang
# @software : PyCharm

import requests
import re

def first_url(name):
    # 初始网址生成
    novel = name.encode("gbk")
    new_novel = str(novel).replace("\\x", "%")
    url = "https://www.52bqg.com/modules/article/search.php?searchkey="
    url += new_novel[2:-1]
    return url
def decide(title, url1):
    # 小说章节网址生成
    text = re.match("(\w*?).html$", title)
    if text==None:
        return "no"
    else:
        new_url = url1 + text.group()
        return new_url

def contents(url):
    # 解析第一个网页内容返回新网址
    res = requests.get(url)
    res.encoding = "gbk"
    # 正则表达式提取小说目录
    pat = re.compile("<meta.*?url=(.*?)\">")
    pattern = re.compile('<dd><a href=.(.*?).>(.*?)</a></dd>', re.S)
    # 书名和html
    titles = re.findall(pattern, res.text)
    # 网站url
    webname = re.findall(pat, res.text)
    url1 = webname[0]
    # 计数器
    print("共计%d章小说" % len(titles))
    i = 1
    for title in titles:
        list(title)
        new_url = decide(title[0], url1)
        if new_url == "no":
            pass
        else:
            number = i/(len(titles))*100
            print("\r已完成%.2f%%"%number, end="")
            work(new_url, title[1])
            i += 1


def work(new_url,bookname):
    # 解析每章节内容
    response = requests.get(new_url)
    response.encoding = "gbk"
    res = response.text
    a = re.compile("&nbsp;&nbsp;&nbsp;&nbsp;(.*?)<", re.S)
    titles = re.findall(a, res)
    name = bookname+".txt"
    with open(name,"a+") as file:

        for title in titles:
            file.write(title)
            file.write("\r\n")

def main():
    name = input("请输入你想看的小说")
    url = first_url(name)
    contents(url)


if __name__ == '__main__':
    main()
