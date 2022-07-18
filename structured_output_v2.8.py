# -*- coding:utf-8 -*-

"""
宫颈癌-后结构化展示的反解析脚本：model_out(predict_spo_list)-->struct_out
structured_output_v2.0
新增功能：
根据带index的spo，套原来的方法，实现struct_out；
    同时保证按头实体的idx，分模块1、模块2
"""

import re
import copy


def get_entity_index(output_dict):
    "对模型输出的dict中的spo_list,获取其中head/tail entity的准确idx"

    # 1.得到list_spo text
    li_spo = output_dict["spo_list"]
    text = output_dict["text"]
    print(text)

    # 2.分句
    li_sentence = re.split("[；。;]", text)
    li_sentence = [i for i in li_sentence if i != '']
    """['子宫大小在正常范围,边缘规则,子宫肌层回声均匀', '宫腔线居中,子宫内膜厚度为12mm', '左侧附件见25×34mm无回声,边界清晰,囊壁平滑', '右侧附件未见明显异常', 'CDFI:未见异常血流信号', '\n']"""

    # 3.开始获取entity的index

    li_spo_with_idx = []
    for spo in li_spo:
        tail = spo["object"]["@value"]  # 尾实体的具体文本
        head = spo["subject"]  # 头实体的具体文本
        label_tail = spo["object_type"]["@value"]  # 尾实体的标签
        label_head = spo["subject_type"]  # 头实体的标签
        predicate = spo["predicate"]

        for sentence in li_sentence:
            idx_sentence = text.find(sentence)
            if tail in sentence and head in sentence:
                idx_tail = [text.find(tail, idx_sentence), text.find(tail, idx_sentence) + len(tail)]
                idx_head = [text.find(head, idx_sentence), text.find(head, idx_sentence) + len(head)]
                spo_with_idx = {
                    "subject": head,
                    "subject_idx": idx_head,
                    "subject_type": label_head,
                    "object": tail,
                    "object_idx": idx_tail,
                    "object_type": label_tail,
                    "predicate": predicate
                }
                # print(d_new_idx)
                li_spo_with_idx.append(spo_with_idx)
    d_spo_with_idx = {
        "text": text,
        "spo_list": li_spo_with_idx
    }
    return d_spo_with_idx


def qc(list_name):
    li = list_name
    news_li = []
    for i in li:
        if i not in news_li:
            news_li.append(i)
    return news_li


def name_new_with_idx(li):
    d_head = {}
    d = {}

    for x in li:
        head = x[0]
        if head not in d_head:
            name = head
            d_head[head] = 1
            d[name] = x[-1]
        else:
            d_head[head] += 1
            name = head + str(d_head[head])
            d[name] = x[-1]
    return d


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

def structured_output(dict_input):
    B = {
        "子宫": {
            "子宫_大小": {},
            "子宫_边缘": {},
            "子宫_位置": {},
            "子宫_形状": {},
            "子宫_回声均匀度": {}
        },
        "子宫内膜": {
            "子宫内膜_厚度": {}
        },
        "CDFI": {
            "CDFI表现": {}
        },
        "附件": {
            "附件_侧别": {},
            "附件_回声表现": {},
            "附件_回声数量": {},
            "附件_回声强度": {},
            "附件_回声大小": {},
            "附件_回声均匀度": {},
            "附件_回声类型": {},
            "附件_边界表现": {},
            "附件_囊壁表现": {},
            "卵巢大小": {}
        },
        "子宫肌层": {
            "子宫肌层_边界表现": {},
            "子宫肌层_囊壁表现": {},
            "子宫肌层_回声数量": {},
            "子宫肌层_回声强度": {},
            "子宫肌层_回声大小": {},
            "子宫肌层_回声类型": {},
            "回声均匀度": {}
        },
        "宫颈": {
            "宫颈_回声数量": {},
            "宫颈_回声强度": {},
            "宫颈_回声大小": {},
            "宫颈_边界表现": {}
        }
    }

    li_spo = dict_input["spo_list"]
    li_x = []
    '[["子宫", 0], ["附件", 70], ["附件", 44], ["子宫肌层", 15]]'

    for spo in li_spo:
        head_idx = spo["subject_idx"]  # "头实体idx

        head_label = spo["subject_type"]

        li_x.append([head_label, head_idx])
    li_x_qc = qc(li_x)
    "经过去重以后的所有head"
    "[['子宫', [0, 2]], ['子宫内膜', [30, 34]], ['CDFI', [79, 83]], ['附件', [70, 72]], ['附件', [44, 46]], ['子宫肌层', [15, 19]]]"

    "命名附件1、附件2"
    d_head_new = name_new_with_idx(li_x_qc)

    "开始填槽或扩槽"
    # D = copy.deepcopy(B)
    # for spo in li_spo:
    #     head_label = spo["subject_type"]
    #     predicate = spo["predicate"]  # "尾实体对应的属性名"
    #     tail = spo["object"]  # "尾实体
    #
    #     head_idx = spo["subject_idx"]
    #
    #     for key in d_head_new:
    #         if head_idx ==key.values():
    #             D[key][predicate] = tail
    #             pass
    #         # else:

    return d_head_new


if __name__ == '__main__':
    dict = {"text": "子宫大小在正常范围,边缘规则,子宫肌层回声均匀;宫腔线居中,子宫内膜厚度为12mm。左侧附件见25×34mm无回声,边界清晰,囊壁平滑。右侧附件未见明显异常。CDFI:未见异常血流信号。\n",
            "spo_list": [{"predicate": "子宫_大小", "object_type": {"@value": "子宫_大小"}, "subject_type": "子宫",
                          "object": {"@value": "在正常范围"}, "subject": "子宫"},
                         {"predicate": "子宫_边缘", "object_type": {"@value": "子宫_边缘"}, "subject_type": "子宫",
                          "object": {"@value": "规则"}, "subject": "子宫"},
                         {"predicate": "子宫内膜_厚度", "object_type": {"@value": "厚度"}, "subject_type": "子宫内膜",
                          "object": {"@value": "12mm"}, "subject": "子宫内膜"},
                         {"predicate": "CDFI表现", "object_type": {"@value": "CDFI表现"}, "subject_type": "CDFI",
                          "object": {"@value": "未见异常血流信号"}, "subject": "CDFI"},
                         {"predicate": "附件_侧别", "object_type": {"@value": "侧别"}, "subject_type": "附件",
                          "object": {"@value": "右"}, "subject": "附件"},
                         {"predicate": "附件_侧别", "object_type": {"@value": "侧别"}, "subject_type": "附件",
                          "object": {"@value": "左"}, "subject": "附件"},
                         {"predicate": "附件_回声表现", "object_type": {"@value": "附件_回声表现"}, "subject_type": "附件",
                          "object": {"@value": "未见明显异常"}, "subject": "附件"},
                         {"predicate": "附件_回声大小", "object_type": {"@value": "回声大小"}, "subject_type": "附件",
                          "object": {"@value": "25×34mm"}, "subject": "附件"},
                         {"predicate": "附件_回声强度", "object_type": {"@value": "回声强度"}, "subject_type": "附件",
                          "object": {"@value": "无回声"}, "subject": "附件"},
                         {"predicate": "附件_边界表现", "object_type": {"@value": "边界表现"}, "subject_type": "附件",
                          "object": {"@value": "清晰"}, "subject": "附件"},
                         {"predicate": "附件_囊壁表现", "object_type": {"@value": "囊壁表现"}, "subject_type": "附件",
                          "object": {"@value": "平滑"}, "subject": "附件"},
                         {"predicate": "子宫肌层_边界表现", "object_type": {"@value": "边界表现"}, "subject_type": "子宫肌层",
                          "object": {"@value": "均匀"}, "subject": "子宫肌层"}]}

    d_spo_with_idx = get_entity_index(dict)
    # print(d_spo_with_idx)
    print("*" * 100)

    d_struct_out = structured_output(d_spo_with_idx)
    print(d_struct_out)
