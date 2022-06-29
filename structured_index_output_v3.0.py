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

    """句子用。；分段"""
    li_ss = re.split("[；。]", text)
    li_ss = [i for i in li_ss if i != '']

    tmp = 0
    dict_group ={}
    li_head,li_head_label =[],[]


    "遍历  每一段分句"
    for segment in li_ss:
        "遍历  每一条关系"
        for spo in li_spo:

            attr = spo["predicate"]  # "尾实体对应的属性名"

            head = spo["subject"]  # "头实体
            tail = spo["object"]["@value"]  # "尾实体
            head_label = spo["subject_type"]  # "头实体标签"
            tail_label = spo["object_type"]["@value"]  # "尾实体标签".

            "如果字词片段span 在第一段句子中"
            if head in segment and tail in segment:
                if tmp == 0:
                    d = D[head_label]

                else:
                    module = head_label + str(dict_group[head_label] + 1)
                    D[module] = B[head]
                    d = D[module]


                """填槽，entity,label,idx"""
                d[attr]["entity"] = tail
                d[attr]["label"] = tail_label
                idx_segment = text.find(segment)
                d[attr]["idx"] = [text.find(tail, idx_segment), text.find(tail, idx_segment) + len(tail)]

                li_head.append(head)
                li_head_label.append(head_label)

        # dict_group[head_label] = tmp + 1

        try:
            li_sort_head = list(set(li_head))
            li_sort_head.sort(key=li_head.index)
            head = li_sort_head[-1]

            li_sort_head_label = list(set(li_head_label))
            li_sort_head_label.sort(key=li_head_label.index)
            head_label = li_sort_head_label[-1]

            d["主体"] = {}
            d["主体"]["entity"] = head
            idx_sentence = text.find(segment)
            d["主体"]["idx"] = [text.find(head, idx_sentence),
                              text.find(head, idx_sentence) + len(head)]
            d["主体"]["label"] = head

            # li_head
            #
            # li_head = []
            # li_head_entity = []
            dict_group[head_label] = tmp + 1  # 完成一段的书写，追加1个头实体head的个数记录

        except:
            # print("\n"+"-"*100)
            # print("li_head = []")
            pass


    D["content"] = text
    return D


def write2json(dict_name, filepath):
    with open(filepath, "w", encoding="utf-8") as fp:
        json.dump(dict_name, fp, ensure_ascii=False)


if __name__ == '__main__':

    # 单个output反解析
    """【一】input_content """
    """ 在data/input/input_content.json里手动复制"""

    """【二】output_model """
    """ output_dict ={"text":"    ",spo_list:["predicate","subject","object"]}"""

    # 1.在输出预测输出之前，先清空下本地的历史输出文件
    output_model_path = r"output/test_predictions.json"
    if os.path.exists(output_model_path):
        os.remove(output_model_path)

    predict_re()

    with open(output_model_path, 'r', encoding="utf-8") as output_f:
        output_dict = json.load(output_f)
        print(output_dict)
        write2json(output_dict, "./temp/output_model.json")

    output_anti_dict = struct_anti_parse(output_dict)
    write2json(output_anti_dict, "./temp/output_antiparse.json")

    # output_dict
    print("\n")
    print(output_dict)
    print("\n")
    print(output_anti_dict)
