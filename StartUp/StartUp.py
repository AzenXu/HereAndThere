from urllib.error import HTTPError
import re

__author__ = 'Azen&DK'
from urllib.request import urlopen
from bs4 import BeautifulSoup


def first_function():
    html = urlopen("http://www.pythonscraping.com/pages/page1.html")  # 这样写的问题：网页可能不存在，或服务器不存在
    obj = BeautifulSoup(html.read(), 'html.parser')
    print(obj.h1)


def error_cache():
    try:
        html = urlopen("http://www.pythonscraping.com/pages/page1.html")
    except HTTPError as e:
        print(e)
    else:
        print("done")

    if html is None:
        print("URL is not found")
    else:
        print("go on")


def css_use():
    """http://www.pythonscraping.com/pages/warandpeace.html"""
    html = urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
    obj = BeautifulSoup(html, "html.parser")

    # tag: 标签名
    # attributes：属性键值对
    # recursive：是否递归（默认是）
    # text：通过标签文本匹配
    # limit：范围限制，只取前多少个结果标签 - 值为1时等价于find()
    # keyword：选择具有指定属性的标签 - 技术上的冗余功能，尽量不用

    # findAll(tag, attributes, recursive, text, limit, keywords) 返回值：标签Tag对象
    # find(tag, attributes, recursive, text, keywords)
    name_list = obj.find_all({"h1","h2","h3","a","p"}) #tags

    name_list = obj.find_all("span",{"class":"green"})
    name_list = obj.find_all("span",{"class":{"green", "red"}}) # attributes

    name_list = obj.find_all("h1",recursive=False) # 禁止递归，只找文档一级标签

    name_list = obj.find_all(text="the prince") # text：通过标签文本匹配

    allText = obj.find_all(id="text") # 选择所有有id属性，且值为text的标签
    allText = obj.find_all("", {"id":"text"}) # 和上面的等价

    for name in name_list:
        print(name) # get_text(): 会把正在处理的HTML文档中，所有标签都清掉，返回一个字符串。一般情况下，在打印的时候才用这个函数，其他情况最好保留HTML结构，以备后续使用


def navigating_tree():
    print("导航树部分")
    html = urlopen("http://www.pythonscraping.com/pages/page3.html")
    obj = BeautifulSoup(html, "html.parser")

    # 导航树：HTML页面整个可以映射成一棵树
    # 导航树查找，用于通过标签在文档中的位置查找标签
    # 单一方向的导航树使用示例：bsObj.tag.subTag.anotherSubTag

    """子标签和后代标签"""
    # 一般，总是处理当前标签的后代标签
    obj.div.findAll("img") # 第一个div标签，后代里所有的img标签列表
    # 只找子标签，用children标签。找所有后代标签，用descendants
    for child in obj.find("table",{"id":"giftList"}).children:
        print(child)

    """兄弟标签"""
    # next_sibling
    # next_siblings()函数，获取所有此标签后面的兄弟标签
    for sibling in obj.find("table", {"id":"giftList"}).tr.next_siblings:
        print(sibling)

    # previous_sibling
    # previous_siblings()函数，获取前面的兄弟标签

    """父标签"""
    # parent
    # parents
    price = obj.find("img",{"src":"../img/gifts/img1.jpg"}).parent.previous_sibling # 打印这个图对应商品的价格
    print("---" + price.get_text() + "---")


def regular_expression():
    print("正则部分")

    html = urlopen("http://www.pythonscraping.com/pages/page3.html")
    obj = BeautifulSoup(html, "html.parser")
    # 目标：抓取所有图片链接
    images = obj.find_all("img", {"src":re.compile("\.\.\/img\/gifts\/img.*\.jpg")})
    for image in images:
        print(image["src"])


def get_attrs():
    print("获取标签属性值部分")

    # 如：获取a标签href属性
    # tag.attrs 获取全部属性，返回值为字典
    # 使用示例：tag.attrs["src"]


def lambda_load():
    print("通过lambda表达式获取")
    # 函数式编程，类似于RxSwift的filter函数 - 把所有找到的标签，传入lambda表达式中，如果返回True，则获取这个标签
    # 示例：soup.findAll(lambda tag: len(tag.attrs) == 2)
    html = urlopen("http://www.pythonscraping.com/pages/page3.html")
    obj = BeautifulSoup(html, "html.parser")
    tags = obj.find_all(lambda tag: len(tag.attrs) == 2)
    for tag in tags:
        print(tag)

def main():
    lambda_load()

if __name__ == "__main__":
    main()
