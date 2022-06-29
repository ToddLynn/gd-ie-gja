import re
import copy

dict1 = {"text": "1、左乳外上象限巨大低回声团,考虑BI-RADS:5类。2、右乳内上象限，BI-RADS2类。3、双侧腋下未见明显肿大淋巴结。", "spo_list": [
    {"predicate": "病灶_侧别", "object_type": {"@value": "侧别"}, "subject_type": "病灶", "object": {"@value": "右"},
     "subject": "乳"},
    {"predicate": "病灶_侧别", "object_type": {"@value": "侧别"}, "subject_type": "病灶", "object": {"@value": "左"},
     "subject": "乳"},
    {"predicate": "病灶_象限", "object_type": {"@value": "象限定位"}, "subject_type": "病灶", "object": {"@value": "内上象限"},
     "subject": "乳"},
    {"predicate": "病灶_象限", "object_type": {"@value": "象限定位"}, "subject_type": "病灶", "object": {"@value": "外上象限"},
     "subject": "乳"}, {"predicate": "病灶_评估分类", "object_type": {"@value": "BI-RADS分类_超声"}, "subject_type": "病灶",
                       "object": {"@value": "BI-RADS2类"}, "subject": "乳"},
    {"predicate": "病灶_评估分类", "object_type": {"@value": "BI-RADS分类_超声"}, "subject_type": "病灶",
     "object": {"@value": "BI-RADS:5类"}, "subject": "乳"},
    {"predicate": "腋窝_侧别", "object_type": {"@value": "侧别"}, "subject_type": "腋窝", "object": {"@value": "双侧"},
     "subject": "腋下"}, {"predicate": "腋窝_淋巴结表现", "object_type": {"@value": "淋巴结表现"}, "subject_type": "腋窝",
                        "object": {"@value": "未见明显肿大淋巴结"}, "subject": "腋下"}]}


def ie_index_output(output_dict):
    B =    {
        "增生腺体": {
            "增生_侧别": None,
            "增生_表现": None
        },
        "导管": {
            "导管_侧别": None,
            "导管_表现": None
        },
        "病灶": {
            "病灶_侧别": None,
            "病灶_象限": None,
            "病灶_钟面": None,
            "病灶_评估分类": None,
            "病灶_回声强度": None,

        },
        "腋窝": {
            "腋窝_侧别": None,
            "腋窝_淋巴结表现": None,
            "腋窝_评估分类": None
        },
        "锁骨上侧": {
            "锁骨上侧_侧别": None,
            "锁骨上_淋巴结表现": None,
            "锁骨上_评估分类": None
        },
        "锁骨下侧": {
            "锁骨下_侧别": None,
            "锁骨下_淋巴结表现": None,
            "锁骨下_评估分类": None
        },
        "内乳": {
            "内乳_侧别": None,
            "内乳_淋巴结表现": None,
            "内乳_评估分类": None
        }
    }
    D = copy.deepcopy(B)

    # 获取spo_list,text文本
    li_spo = output_dict["spo_list"]
    text = output_dict["text"]

    # 把一条文本，用“；。”分成多段的分句,并去掉空值
    li_ss = re.split("[；。]", text)
    li_ss = [i for i in li_ss if i != '']

    # 遍历 五元组列表里的每一个元组
    li_head = []
    dict_head = {}
    tmp = 0
    # li_total_head = []

    "遍历  每一段分句"
    for sentence in li_ss:
        "遍历  每一条关系"
        for spo in li_spo:
            span = spo["object"]["@value"]  # "尾实体对应的文本-字词片段"

            attr = spo["predicate"]  # "尾实体对应的属性名"
            head = spo["subject_type"]  # "尾实体对应的头实体"

            tmp = dict_head.get(head, 0)  # 获取 -当前字典中头实体head的个数

            "如果词语在第一段句子中"
            if span in sentence:
                if tmp == 0:
                    D[head][attr] = span
                    li_head.append(head)
                else:
                    module = head + str(dict_head[head] + 1)
                    D[module] = B[head]
                    D[module][attr] = span
                    li_head.append(head)

        # 当  一段分句中的所有属性已经填满，把这个分句里的head添加到li_head里面。
        try:
            head = list(set(li_head))[0]
            li_head = []
            dict_head[head] = tmp + 1  # 完成一段的书写，追加1个头实体head的个数记录
        except:
            pass

    return D


if __name__ == '__main__':
    dic1 = {"text": "1、左乳外上象限巨大低回声团,考虑BI-RADS:5类。2、右乳内上象限，BI-RADS2类。3、双侧腋下未见明显肿大淋巴结。", "spo_list": [
        {"predicate": "病灶_侧别", "object_type": {"@value": "侧别"}, "subject_type": "病灶", "object": {"@value": "右"},
         "subject": "乳"},
        {"predicate": "病灶_侧别", "object_type": {"@value": "侧别"}, "subject_type": "病灶", "object": {"@value": "左"},
         "subject": "乳"},
        {"predicate": "病灶_象限", "object_type": {"@value": "象限定位"}, "subject_type": "病灶", "object": {"@value": "内上象限"},
         "subject": "乳"},
        {"predicate": "病灶_象限", "object_type": {"@value": "象限定位"}, "subject_type": "病灶", "object": {"@value": "外上象限"},
         "subject": "乳"}, {"predicate": "病灶_评估分类", "object_type": {"@value": "BI-RADS分类_超声"}, "subject_type": "病灶",
                           "object": {"@value": "BI-RADS2类"}, "subject": "乳"},
        {"predicate": "病灶_评估分类", "object_type": {"@value": "BI-RADS分类_超声"}, "subject_type": "病灶",
         "object": {"@value": "BI-RADS:5类"}, "subject": "乳"},
        {"predicate": "腋窝_侧别", "object_type": {"@value": "侧别"}, "subject_type": "腋窝", "object": {"@value": "双侧"},
         "subject": "腋下"}, {"predicate": "腋窝_淋巴结表现", "object_type": {"@value": "淋巴结表现"}, "subject_type": "腋窝",
                            "object": {"@value": "未见明显肿大淋巴结"}, "subject": "腋下"}]}
    d = {"output_dict": {
            "内乳": {
                "内乳_侧别": None,
                "内乳_淋巴结表现": None,
                "内乳_评估分类": None
            },
            "增生腺体": {
                "增生_侧别": None,
                "增生_表现": None
            },
            "导管": {
                "导管_侧别": None,
                "导管_表现": None
            },
            "病灶": {
                "病灶_侧别": "左",
                "病灶_回声强度": None,
                "病灶_评估分类": "BI-RADS:5类",
                "病灶_象限": "外上象限",
                "病灶_钟面": None
            },
            "病灶2": {
                "病灶_侧别": "右",
                "病灶_回声强度": None,
                "病灶_评估分类": "BI-RADS2类",
                "病灶_象限": "内上象限",
                "病灶_钟面": None
            },
            "腋窝": {
                "腋窝_侧别": "双侧",
                "腋窝_淋巴结表现": "未见明显肿大淋巴结",
                "腋窝_评估分类": None
            },
            "锁骨上侧": {
                "锁骨上_淋巴结表现": None,
                "锁骨上_评估分类": None,
                "锁骨上侧_侧别": None
            },
            "锁骨下侧": {
                "锁骨下_侧别": None,
                "锁骨下_淋巴结表现": None,
                "锁骨下_评估分类": None
            }
        }}
    print(ie_index_output(dic1))
