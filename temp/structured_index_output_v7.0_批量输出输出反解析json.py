"""
用于输出output_antiparse  反解析的json文件  [{},{},{}.....]
+  模型输出spo_list后处理把输出的作为病灶的"乳腺组织"改为"乳"
"""

import re
import copy
from predict import *

"""list去重"""


def qc(list_name):
    li = list_name
    news_li = []
    for i in li:
        if i not in news_li:
            news_li.append(i)
    return news_li


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

    li_subject, li_subject_label = [], []
    tmp = 0
    dict_sub = {}

    "遍历  每一段分句"
    for segment in li_ss:
        "遍历  每一条关系"
        for spo in li_spo:

            attr = spo["predicate"]  # "尾实体对应的属性名"

            head = spo["subject"]  # "头实体
            tail = spo["object"]["@value"]  # "尾实体
            head_label = spo["subject_type"]  # "头实体标签"
            tail_label = spo["object_type"]["@value"]  # "尾实体标签".

            tmp = dict_sub.get(head_label, 0)

            "如果字词片段span 在第一段句子中"
            if head in segment and tail in segment:
                if tmp == 0:
                    d = D[head_label]
                else:
                    module = head_label + str(tmp + 1)
                    D[module] = B[head_label]
                    d = D[module]

                """填槽，entity,label,idx"""
                d[attr]["entity"] = tail
                d[attr]["label"] = tail_label
                idx_segment = text.find(segment)
                d[attr]["idx"] = [text.find(tail, idx_segment), text.find(tail, idx_segment) + len(tail)]

                li_subject.append(head)
                li_subject_label.append(head_label)

        li_sub_qc = qc(li_subject)
        li_sub_label_qc = qc(li_subject_label)

        if li_sub_qc and li_sub_label_qc:
            sub = li_sub_qc[-1]
            sub_label = li_sub_label_qc[-1]

            d["主体"] = {}
            d["主体"]["entity"] = sub
            idx_sentence = text.find(segment)
            d["主体"]["idx"] = [text.find(sub, idx_sentence),
                              text.find(sub, idx_sentence) + len(sub)]
            d["主体"]["label"] = sub_label

            dict_sub[sub_label] = tmp + 1


        li_subject,li_subject_label =[],[]
        # li_subject,li_subject_label,li_sub_qc,li_sub_label_qc =[],[],[],[]

    D["content"] = text
    return D




def write2json(dict_name, filepath):
    with open(filepath, "w", encoding="utf-8") as fp:
        json.dump(dict_name, fp, ensure_ascii=False)


def head_value_replace_many():
    path = "../output/test_predictions.json"
    new_path = "./output/ouput_model_replace.json"
    li_dict = []

    with open(path, "r", encoding="utf-8") as fb:
        li_output = fb.readlines()  # 把json读取到li_output里面，
        for op in li_output:
            dict_op = json.loads(op)  # 把json str字符串,解码成dict : python对象。

            for spo in dict_op["spo_list"]:
                if spo["subject_type"] == "病灶":
                    spo["subject"] = "乳"  # 把subject值，不管是否是"乳腺组织"强行改为“乳”

            li_dict.append(dict_op)

    """按格式，把dict逐行写入到json文件里"""  # 将修改后的数据，存为同名的json文件。相当于是用新修改覆盖原json文件。

    with open(new_path, "w", encoding="utf-8") as fp:
        for line in li_dict:
            str1 = json.dumps(line, ensure_ascii=False)
            fp.write(str1 + "\n")


if __name__ == '__main__':

    # """ todo 把模型predict的pipeline加进来"""

    # # 单个output反解析
    # """【一】input_content """
    # """ 在data/input/input_content.json里手动复制"""
    #
    # """【二】output_model """
    # """ output_dict ={"text":"    ",spo_list:["predicate","subject","object"]}"""
    #
    # output_model_path = r"output/test_predictions.json"  # 1.在输出预测输出之前，先清空下本地的历史输出文件
    # if os.path.exists(output_model_path):
    #     os.remove(output_model_path)
    #
    # predict_re()
    #
    # with open(output_model_path, 'r', encoding="utf-8") as output_f:
    #     output_dict = json.load(output_f)
    #     print(output_dict)
    #     write2json(output_dict, "./temp/output_model.json")

    """ 【三】output_model_replace"""
    """ 对多条content的output_model的病灶值，用(乳)替换(乳腺组织)"""

    # head_value_replace_many()

    """ 【四】output_anti_parse"""

    output_model_replace_path = r"./output/ouput_model_replace.json"


    "批量"

    # with open(output_model_path, 'r', encoding="utf-8") as output_f:
    #     output_dict = json.load(output_f)
    #
    # output_anti_dict = struct_anti_parse(output_dict)
    #
    # write2json(output_anti_dict, "./temp/output_antiparse.json")
    li_output_antiparse = []

    with open(output_model_replace_path, "r", encoding="utf-8") as ft:
        for li in ft.readlines():
            output_dict = json.loads(li)

            output_anti_dict = struct_anti_parse(output_dict)
            print(output_anti_dict)
            li_output_antiparse.append(output_anti_dict)
    print(li_output_antiparse)
    output_anti_parse_file = "output/output_anti_parse_375_0411.json"
    with open(output_anti_parse_file, "w", encoding="utf-8") as fb:
        json.dump(li_output_antiparse, fb, ensure_ascii=False)


