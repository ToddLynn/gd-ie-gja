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
    d_spo_with_idx ={
        "text" :text,
        "spo_list" :li_spo_with_idx
    }
    return d_spo_with_idx



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

    D = copy.deepcopy(B)

    li_spo = dict_input["spo_list"]

    for spo in li_spo:
        predicate = spo["predicate"]  # "尾实体对应的属性名"

        tail = spo["object"]  # "尾实体
        head_idx = spo["subject_idx"]  # "头实体idx
        tail_idx = spo["object_idx"]  # "尾实体idx

        head_label = spo["subject_type"]

        """填写 头实体的属性，即，尾实体的值、标签、idx"""

        D[head_label][predicate] = tail

        # D[head_label][attr]["entity"] = tail
        # D[head_label][attr]["label"] = tail_label
        # D[head_label][attr]["idx"] = tail_idx
        #
        # D[head_label]["主体"] = {}
        # D[head_label]["主体"]["entity"] = head
        # D[head_label]["主体"]["label"] = head_label
        # D[head_label]["主体"]["idx"] = head_idx

        D["content"] = dict_input["text"]
    return D

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
    print(d_spo_with_idx)
    print("*"*100)

    d_struct_out =structured_output(d_spo_with_idx)
    print(d_struct_out)
# [
#   {
#     "subject": "子宫",
#     "subject_idx": [
#       0,
#       2
#     ],
#     "subject_type": "子宫",
#     "object": "在正常范围",
#     "object_idx": [
#       4,
#       9
#     ],
#     "object_type": "子宫_大小",
#     "predicate": "子宫_大小"
#   },
#   {
#     "subject": "子宫",
#     "subject_idx": [
#       0,
#       2
#     ],
#     "subject_type": "子宫",
#     "object": "规则",
#     "object_idx": [
#       12,
#       14
#     ],
#     "object_type": "子宫_边缘",
#     "predicate": "子宫_边缘"
#   },
#   {
#     "subject": "子宫内膜",
#     "subject_idx": [
#       30,
#       34
#     ],
#     "subject_type": "子宫内膜",
#     "object": "12mm",
#     "object_idx": [
#       37,
#       41
#     ],
#     "object_type": "厚度",
#     "predicate": "子宫内膜_厚度"
#   },
#   {
#     "subject": "CDFI",
#     "subject_idx": [
#       79,
#       83
#     ],
#     "subject_type": "CDFI",
#     "object": "未见异常血流信号",
#     "object_idx": [
#       84,
#       92
#     ],
#     "object_type": "CDFI表现",
#     "predicate": "CDFI表现"
#   },
#   {
#     "subject": "附件",
#     "subject_idx": [
#       70,
#       72
#     ],
#     "subject_type": "附件",
#     "object": "右",
#     "object_idx": [
#       68,
#       69
#     ],
#     "object_type": "侧别",
#     "predicate": "附件_侧别"
#   },
#   {
#     "subject": "附件",
#     "subject_idx": [
#       44,
#       46
#     ],
#     "subject_type": "附件",
#     "object": "左",
#     "object_idx": [
#       42,
#       43
#     ],
#     "object_type": "侧别",
#     "predicate": "附件_侧别"
#   },
#   {
#     "subject": "附件",
#     "subject_idx": [
#       70,
#       72
#     ],
#     "subject_type": "附件",
#     "object": "未见明显异常",
#     "object_idx": [
#       72,
#       78
#     ],
#     "object_type": "附件_回声表现",
#     "predicate": "附件_回声表现"
#   },
#   {
#     "subject": "附件",
#     "subject_idx": [
#       44,
#       46
#     ],
#     "subject_type": "附件",
#     "object": "25×34mm",
#     "object_idx": [
#       47,
#       54
#     ],
#     "object_type": "回声大小",
#     "predicate": "附件_回声大小"
#   },
#   {
#     "subject": "附件",
#     "subject_idx": [
#       44,
#       46
#     ],
#     "subject_type": "附件",
#     "object": "无回声",
#     "object_idx": [
#       54,
#       57
#     ],
#     "object_type": "回声强度",
#     "predicate": "附件_回声强度"
#   },
#   {
#     "subject": "附件",
#     "subject_idx": [
#       44,
#       46
#     ],
#     "subject_type": "附件",
#     "object": "清晰",
#     "object_idx": [
#       60,
#       62
#     ],
#     "object_type": "边界表现",
#     "predicate": "附件_边界表现"
#   },
#   {
#     "subject": "附件",
#     "subject_idx": [
#       44,
#       46
#     ],
#     "subject_type": "附件",
#     "object": "平滑",
#     "object_idx": [
#       65,
#       67
#     ],
#     "object_type": "囊壁表现",
#     "predicate": "附件_囊壁表现"
#   },
#   {
#     "subject": "子宫肌层",
#     "subject_idx": [
#       15,
#       19
#     ],
#     "subject_type": "子宫肌层",
#     "object": "均匀",
#     "object_idx": [
#       21,
#       23
#     ],
#     "object_type": "边界表现",
#     "predicate": "子宫肌层_边界表现"
#   }
# ]
# *******************************

"""
子宫大小在正常范围,边缘规则,子宫肌层回声均匀;宫腔线居中,子宫内膜厚度为12mm。左侧附件见25×34mm无回声,边界清晰,囊壁平滑。右侧附件未见明显异常。CDFI:未见异常血流信号。

{'subject': '子宫', 'subject_idx': [0, 2], 'object': '在正常范围', 'object_idx': [4, 9]}
{'subject': '子宫', 'subject_idx': [0, 2], 'object': '规则', 'object_idx': [12, 14]}
{'subject': '子宫内膜', 'subject_idx': [30, 34], 'object': '12mm', 'object_idx': [37, 41]}
{'subject': 'CDFI', 'subject_idx': [79, 83], 'object': '未见异常血流信号', 'object_idx': [84, 92]}
{'subject': '附件', 'subject_idx': [70, 72], 'object': '右', 'object_idx': [68, 69]}
{'subject': '附件', 'subject_idx': [44, 46], 'object': '左', 'object_idx': [42, 43]}
{'subject': '附件', 'subject_idx': [70, 72], 'object': '未见明显异常', 'object_idx': [72, 78]}
{'subject': '附件', 'subject_idx': [44, 46], 'object': '25×34mm', 'object_idx': [47, 54]}
{'subject': '附件', 'subject_idx': [44, 46], 'object': '无回声', 'object_idx': [54, 57]}
{'subject': '附件', 'subject_idx': [44, 46], 'object': '清晰', 'object_idx': [60, 62]}
{'subject': '附件', 'subject_idx': [44, 46], 'object': '平滑', 'object_idx': [65, 67]}
{'subject': '子宫肌层', 'subject_idx': [15, 19], 'object': '均匀', 'object_idx': [21, 23]}

Process finished with exit code 0
"""
