#!/usr/bin/env python
# -*- coding:UTF-8 -*-

# 目的：分析 imeituan8.7 podfile 相对于 imeituan8.4 增加的模块有哪些
# 新增模块考虑添加进tower项目中
# 实际运用效果比较满意
# 后期计划：完善一下此脚本，以后升级tower的时候可复用


import requests  # 网络库
import re  # 正则


def load_podfile_url(url):
    r = requests.get(url, auth=('xuchang08', 'KFCkfcv*259'))
    r.encoding = 'utf-8'
    return r.text


def load_podfile(branch='release/8.7'):
    url = 'http://git.sankuai.com/projects/IOS/repos/imeituan/browse/Podfile?raw&at=refs/heads/' + branch
    return load_podfile_url(url)


def regex_podfile(text):
    pattern = re.compile(r"(binary_pod|pod)\s*'([^']+)'(\s|\,)*'([^']+)'")
    result = pattern.findall(text)
    return result


def pick_pods(original):
    #     取出所有库名放入数组
    pod_names = []
    for i in original:
        pod_names.append(i[1])
    return pod_names


# 找出listA有，listB没有的元素
def check_difference(listA, listB):
    setA = set(listA)
    setB = set(listB)
    return list(setA.difference(setB))


def load_pod_list_from_url(url):
    pod_list = pick_pods(regex_podfile(load_podfile_url(url)))
    return pod_list


def main():
    pod_list_840 = load_pod_list_from_url(
        'http://git.sankuai.com/projects/IOS/repos/source-imeituan/browse/Podfile?at=8a577ee06aa459b4c55b8c556a053f809260ba62&raw')
    pod_list_870 = load_pod_list_from_url(
        'http://git.sankuai.com/projects/IOS/repos/imeituan/browse/Podfile?raw&at=refs/heads/release/8.7')
    pod_list_travel_151 = load_pod_list_from_url(
        'http://git.sankuai.com/projects/HOTEL/repos/hotel-tower-ios/browse/Podfile?at=72ce6545803f06c4bb3929895969ef5df80fefa2&raw')

    pod_list_black_list = check_difference(pod_list_840, pod_list_travel_151)
    pod_list_meituan_differ = check_difference(pod_list_870, pod_list_840)

    # 拿到differ里涉及的库，直接粘到podfile里...
    oripodfile = load_podfile_url(
        'http://git.sankuai.com/projects/IOS/repos/imeituan/browse/Podfile?raw&at=refs/heads/release/8.7')
    for i in pod_list_meituan_differ:
        a = re.findall(".*" + i + ".*", oripodfile)  # 知识点：.*不会匹配换行符
        for name in a:
            print(name)


if __name__ == '__main__':
    main()
