"""
用于标注助手-反解析-模型自动标注新样本的接口 -
"""

import re
import copy
from predict import *


def struct_anti_parse(output_dict):
    B = {
        "增生腺体": {
            "增生_侧别": {},
            "增生_表现": {}
        },
        "导管": {
            "导管_侧别": {},
            "导管_表现": {}
        },
        "病灶": {
            "病灶_侧别": {},
            "病灶_象限": {},
            "病灶_钟面": {},
            "病灶_评估分类": {},
            "病灶_回声强度": {},

        },
        "腋窝": {
            "腋窝_侧别": {},
            "腋窝_淋巴结表现": {},
            "腋窝_评估分类": {}
        },
        "锁骨上侧": {
            "锁骨上侧_侧别": {},
            "锁骨上_淋巴结表现": {},
            "锁骨上_评估分类": {}
        },
        "锁骨下侧": {
            "锁骨下_侧别": {},
            "锁骨下_淋巴结表现": {},
            "锁骨下_评估分类": {}
        },
        "内乳": {
            "内乳_侧别": {},
            "内乳_淋巴结表现": {},
            "内乳_评估分类": {}
        }
    }

    D = copy.deepcopy(B)

    li_spo = output_dict["spo_list"]
    text = output_dict["text"]

    li_ss = re.split("[；。]", text)
    li_ss = [i for i in li_ss if i != '']

    # 遍历 五元组列表里的每一个元组
    li_head = []
    li_head_entity = []
    dict_head = {}
    tmp = 0
    # li_total_head = []

    "遍历  每一段分句"
    for sentence in li_ss:
        "遍历  每一条关系"
        for spo in li_spo:
            span = spo["object"]["@value"]  # "尾实体对应的文本-字词片段"

            attr = spo["predicate"]  # "尾实体对应的属性名"
            head = spo["subject_type"]  # "尾实体对应的头实体标签"
            label = spo["object_type"]["@value"]  # "尾实体对应的头实体"

            head_entity = spo["subject"]
            tmp = dict_head.get(head, 0)  # 获取 -当前字典中头实体head的个数

            "如果字词片段span 在第一段句子中"
            if span in sentence:
                if tmp == 0:
                    d = D[head]

                else:
                    module = head + str(dict_head[head] + 1)
                    D[module] = B[head]
                    d = D[module]
                d[attr]["entity"] = span
                d[attr]["label"] = label
                idx_sentence = text.find(sentence)
                d[attr]["idx"] = [text.find(span, idx_sentence), text.find(span, idx_sentence) + len(span)]

                li_head.append(head)
                li_head_entity.append(head_entity)

            # li_spo.remove(spo)

        # 当  一段分句中的所有属性已经填满，把这个分句里的head添加到li_head里面。

        try:
            li_sort_head = list(set(li_head))
            li_sort_head.sort(key=li_head.index)
            head = li_sort_head[-1]
            # head = li_sort_head[0]

            li_sort_head_entity = list(set(li_head_entity))
            li_sort_head_entity.sort(key=li_head_entity.index)

            head_entity = li_sort_head_entity[-1]
            # head_entity = li_sort_head_entity[0]

            d["主体"] = {}
            d["主体"]["entity"] = head_entity
            idx_sentence = text.find(sentence)
            d["主体"]["idx"] = [text.find(head_entity, idx_sentence),
                              text.find(head_entity, idx_sentence) + len(head_entity)]
            d["主体"]["label"] = head

            # li_head
            #
            # li_head = []
            # li_head_entity = []
            dict_head[head] = tmp + 1  # 完成一段的书写，追加1个头实体head的个数记录

        except:
            # print("\n"+"-"*100)
            # print("li_head = []")
            pass

    D["content"] = text
    return D


if __name__ == '__main__':
    # 单个output反解析
    output_dict = {'text': '1、双侧乳腺组织增生。2、右侧乳腺低回声结节,BI-RADS3类;建议定期复查。3、双侧腋下未见明显肿大淋巴结。', 'spo_list': [
        {'predicate': '增生_侧别', 'object_type': {'@value': '侧别'}, 'subject_type': '增生腺体', 'object': {'@value': '双侧'},
         'subject': '乳腺组织'},
        {'predicate': '增生_表现', 'object_type': {'@value': '乳腺组织改变'}, 'subject_type': '增生腺体', 'object': {'@value': '增生'},
         'subject': '乳腺组织'},
        {'predicate': '病灶_侧别', 'object_type': {'@value': '侧别'}, 'subject_type': '病灶', 'object': {'@value': '右侧'},
         'subject': '乳腺组织'},
        {'predicate': '病灶_回声强度', 'object_type': {'@value': '回声强度'}, 'subject_type': '病灶', 'object': {'@value': '低回声'},
         'subject': '乳腺组织'}, {'predicate': '病灶_评估分类', 'object_type': {'@value': 'BI-RADS分类_超声'}, 'subject_type': '病灶',
                              'object': {'@value': 'BI-RADS3类'}, 'subject': '乳腺组织'},
        {'predicate': '腋窝_侧别', 'object_type': {'@value': '侧别'}, 'subject_type': '腋窝', 'object': {'@value': '双侧'},
         'subject': '腋下'}, {'predicate': '腋窝_淋巴结表现', 'object_type': {'@value': '淋巴结表现'}, 'subject_type': '腋窝',
                            'object': {'@value': '未见明显肿大淋巴结'}, 'subject': '腋下'}]}
    result = struct_anti_parse(output_dict)
    print(output_dict)
    print(result)

    # """批量"""
    # """【一、input_content】 模型原始输入 {"text": "1、双侧乳腺组织增生。2、双侧腋下未见明显肿大淋巴结。"}"""
    #
    # """【二、output_dict】  模型原始输出dict {"text": "1、双侧乳腺组织增生。2、双侧腋下未见明显肿大淋巴结。"}"""
    #
    # # (在输出预测输出之前，先清空下本地的历史输出文件)
    # output_path = r"output/test_predictions.json"
    # if os.path.exists(output_path):
    #     os.remove(output_path)
    #
    # predict_re()
    # with open(output_path, "r", encoding="utf-8") as fb:
    #     for li in fb.readlines():
    #         output_dict = json.loads(li)
    #         result = struct_anti_parse(output_dict)
    #
    #         print(output_dict)
    #         print(result)
    #         print("-"*100)
    #
    #
