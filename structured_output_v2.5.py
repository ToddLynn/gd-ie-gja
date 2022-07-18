# -*- coding:utf-8 -*-

"""
宫颈癌-后结构化展示的反解析脚本：model_out(predict_spo_list)-->struct_out
structured_output_v2.5
新增功能：
分组；附件1，附件2
"""

import re
import copy

"尝试一"
# li_x = [
#     ["子宫", 0],
#     ["附件", 70],
#     ["附件", 44],
#     ["子宫肌层", 15],
# ]

"尝试二"

"生成模块1、模块2"

# li_name = []
# for x in li_x:
#     name =x[0]
#     li_name.append(name)
#
# print(li_name)

"既定模块名"
# li_name_standard =["子宫", "子宫内膜","CDFI","附件","子宫肌层","宫颈"]
# li_name_new = []
#
# d_head = {}
# for i in li_name_standard:
#     name_raw =i
#     num = d_head.get(name_raw,0) #"子宫", "子宫内膜","CDFI","附件","子宫肌层","宫颈"
#
#
#     for x in li_x:
#         if num == 0:
#             name_new =x[0]
#             d_head[name_raw]= num +1
#             li_name_new.append(name_new)
#         else:
#             name_new = x[0]+str(num)
#             d_head[name_raw] = num + 1
#             li_name_new.append(name_new)
# print(li_name_new)


"尝试三"
li_x = [
    ["子宫", 0],
    ["附件", 70],
    ["附件", 44],
    ["附件", 43],
    ["附件", 45],
    ["子宫肌层", 15]
]

d_head = {}

li_head_new = []

for x in li_x:
    head = x[0]
    if head not in d_head:
        name = head
        d_head[head] = 1
    else:
        d_head[head] += 1
        name = head + str(d_head[head])
    li_head_new.append(name)

# print(li_head_new)

"['子宫', '附件', '附件', '子宫肌层']"
"['子宫', '附件', '附件2', '附件3', '附件4', '子宫肌层']"


# 封装成函数
def name_new(li):
    #    li = [
    #     ["子宫", 0],
    #     ["附件", 70],
    #     ["附件", 44],
    #     ["附件", 43],
    #     ["附件", 45],
    #     ["子宫肌层", 15]
    # ]
    d_head = {}
    li_head_new = []

    for x in li:
        head = x[0]
        if head not in d_head:
            name = head
            d_head[head] = 1
        else:
            d_head[head] += 1
            name = head + str(d_head[head])
        li_head_new.append(name)
    return li_head_new

def name_new_with_idx(li):

    d_head = {}
    d = {}

    for x in li:
        head = x[0]
        if head not in d_head:
            name = head
            d_head[head] = 1
            d[name]= x[-1]
        else:
            d_head[head] += 1
            name = head + str(d_head[head])
            d[name] = x[-1]
    return d

if __name__ == '__main__':
    li_x = [
        ["子宫", 0],
        ["附件", 70],
        ["附件", 44],
        ["附件", 43],
        ["附件", 45],
        ["子宫肌层", 15]
    ]
    # print(name_new(li_x))
    print(name_new_with_idx(li_x))
    "{'子宫': 0, '附件': 70, '附件2': 44, '附件3': 43, '附件4': 45, '子宫肌层': 15}"