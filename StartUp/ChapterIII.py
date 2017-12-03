"""
第三章-开始采集

目标：用爬虫遍历多个页面、多个网站

爬虫：本质是一种递归方式 - 获取网页内容，找URL，获取网页内容，找URL...
注意：需要考虑要消耗的网络流量、尽量让被采集目标服务器负载更低一些

"""
from urllib.request import urlopen
from bs4 import BeautifulSoup


def dom3_1():
    """
    遍历单个域名

    本章目标：从一个wiki页面，按照一定规则访问到另一个wiki页面

    终极目标：从埃里克· 艾德尔的词条页面（ https://en.wikipedia.org/wiki/Eric_Idle）开始，
    经过最少的链接点击次数，找到凯文· 贝肯的词条页面（ https://en.wikipedia.org/wiki/Kevin_Bacon）
    """
    html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")
    obj = BeautifulSoup(html, "html.parser")

    def basic():
        for link in obj.find_all("a"):
            if 'href' in link.attrs:
                print(link.attrs["href"])

    # basic()

    # 通过打印的结果，发现很多链接是我们不需要的
    # 通过观察页面HTML结构发现，我们需要的词条有如下特点：
    # • 它们都在 id 是 bodyContent 的 div 标签里
    # • URL 链接不包含冒号
    # • URL 链接都以 /wiki/ 开头

    def upper():
        import re

        for link in obj.find("div", {"id": "bodyContent"}).find_all("a", href=re.compile("^(/wiki/)((?!:).)*$")):
            if 'href' in link.attrs:
                print(link.attrs['href'])

                # upper()

            # 下一步：
            # 写一个函数getLinks，入参：/wiki/<词条名称>形式的URL链接，出参：所包含的所有URL链接
            # 一个主函数，以某个词条为参数调用getLinks，直到我们主动停止，或在新页面上木有词条链接了
            # 这个程序只是为了演示从一个页面访问到另一个页面，并不完全能够解决从xxx的页面找到xxx的页面这个需求。。。还要学习点别的

    def last():
        import datetime
        import random
        import re

        random.seed(datetime.datetime.now())
        # 目的：保证每次程序运行的时候，词条的选择都是一个全新的随机路径
        # 为了可以连续的随机遍历维基百科
        def getLinks(articleUrl):
            html = urlopen("http://en.wikipedia.org" + articleUrl)
            obj = BeautifulSoup(html, "html.parser")
            return obj.find("div", {"id": "bodyContent"}).find_all("a", href=re.compile("^(/wiki/)((?!:).)*$"))

        links = getLinks("/wiki/Kevin_Bacon")
        while len(links) > 0:
            newAtrticle = links[random.randint(0, len(links) - 1)].attrs["href"]
            print(newAtrticle)
            links = getLinks(newAtrticle)

    last()


def dom3_2():
    """
    采集整个网站

    目标：需要系统把整个网站按目录分类，或者遍历网站上的所有页面。

    目的：
    1. 生成网站地图
    2. 收集数据 - 递归好多网站，只收集网站里的有用数据

    方案：
    初步版：从入口页面开始，找到上面的所有链接形成列表，作为下一轮采集的入口页面
    问题：复杂度增长太快
    分析：虽然链接多，但是大多数链接都是重复的，需要剔除掉
    进阶版：把所有已经发现的链接放在set里，只采集‘新’链接，然后再从页面中搜索其他链接
    """

    def just_capture():
        from urllib.request import urlopen
        from bs4 import BeautifulSoup
        import re

        pages = set()

        def getLinks(pageUrl):
            html = urlopen("http://en.wikipedia.org" + pageUrl)
            obj = BeautifulSoup(html, "html.parser")
            for link in obj.find_all("a", href=re.compile("^(/wiki/)")):
                if 'href' in link.attrs:
                    if link.attrs['href'] not in pages:
                        newPage = link.attrs['href']
                        print(newPage)
                        pages.add(newPage)
                        getLinks(newPage)  # python有默认递归限制 - 1000次。 可以手动调整这个数量

        getLinks("")  # 深度遍历，效率不是很好...需要访问的页面太多

        # just_capture()

    def collect_info():
        """
        用爬虫收集页面的标题、正文第一段、编辑页面的链接之类的东东

        方法:
        1. 观察页面结构
        2. 拟定采集方案

        发现规则：
        • 所有的标题（所有页面上，不论是词条页面、编辑历史页面还是其他页面）都是在
        h1 → span 标签里，而且页面上只有一个 h1 标签。
        • 前面提到过，所有的正文文字都在 div#bodyContent 标签里。但是，如果我们想更
        进一步获取第一段文字，可能用 div#mw-content-text → p 更好（只选择第一段的标
        签）。这个规则对所有页面都适用，除了文件页面（例如， https://en.wikipedia.org/wiki/
        File:Orbit_of_274301_Wikipedia.svg），页面不包含内容文字（ content text）的部分内容。
        • 编辑链接只出现在词条页面上。如果有编辑链接，都位于 li#ca-edit 标签的 li#ca
        edit → span → a 里面。
        """
        from urllib.request import urlopen
        from bs4 import BeautifulSoup
        import re

        pages = set()

        def getLinks(pageUrl):
            html = urlopen("http://en.wikipedia.org" + pageUrl)
            obj = BeautifulSoup(html, "html.parser")
            try:
                print(obj.h1.get_text())
                print(obj.find(id="mw-content-text").find_all("p")[0])
                print(obj.find(id="ca-edit").find("span").find("a").attrs['href'])
            except AttributeError:
                print("少一些属性")

            for link in obj.find_all("a", href=re.compile("^(/wiki/)")):
                if 'href' in link.attrs:
                    if link.attrs['href'] not in pages:
                        newPage = link.attrs['href']
                        print("----\n" + newPage)
                        pages.add(newPage)
                        getLinks(newPage)

        getLinks("")

    collect_info()


def dom3_3():
    """
    网际迷航...

    顺着互联网随意采集（不是之前的单域名下的采集） - 经过几跳就可以到达一些非主流网站，可以到达互联网的任何位置

    难点：不同网站的布局不同，在寻找信息和查找的时候，需要极具灵活性

    思考：
    1. 要收集哪些数据？这些数据可以通过采集几个已经确定的网站完成吗？
    2. 发现新网站以后，采取广度遍历还是深度遍历？
    3. 哪类网站不需要采集？语言有限制吗？

    这一段不是很难，没有用到新的知识点，代码就不写了...
    """


def dom3_4():
    """
    用Scrapy采集
    网络爬虫的一些简单任务：
    - 找出页面上的所有链接
    - 区分内链和外链
    - 跳转到新的页面

    Scrapy可以大幅降低网页链接查找和识别工作复杂度的Python库

    """


def main():
    print("第三章main函数")
    dom3_2()
