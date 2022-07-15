import re
import copy


def structured_output(output_dict):
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
        # "CDFI": {
        #     "CDFI表现": {}
        # },
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
    li_spo = output_dict["spo_list"]
    text = output_dict["text"]

    li_ss = re.split("[；。;]", text)
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
            if span in sentence and attr !="CDFI表现":
            # if span in sentence:
                if tmp == 0:
                    D[head][attr] = span
                    li_head.append(head)
                else:
                    module = head + str(dict_head[head] + 1)
                    D[module] = B[head]
                    D[module][attr] = span
                    li_head.append(head)

        # 当  一段分句中的所有属性已经填满，把这个分句里的head添加到li_head里面。
        # head = list(set(li_head))[0]
        # print(list(set(li_head)))
        try:
            head = list(set(li_head))[0]
            # print(head)
            # print(list(set(li_head)))

            li_head = []

            dict_head[head] = tmp + 1  # 完成一段的书写，追加1个头实体head的个数记录
        except:
            # print("\n"+"-"*100)
            # print("li_head = []")
            pass

    return D
if __name__ == '__main__':


    dict = {"text": "子宫大小在正常范围,边缘规则,子宫肌层回声均匀;宫腔线居中,子宫内膜厚度为12mm。左侧附件见25×34mm无回声,边界清晰,囊壁平滑。右侧附件未见明显异常。CDFI:未见异常血流信号。\n", "spo_list": [{"predicate": "子宫_大小", "object_type": {"@value": "子宫_大小"}, "subject_type": "子宫", "object": {"@value": "在正常范围"}, "subject": "子宫"}, {"predicate": "子宫_边缘", "object_type": {"@value": "子宫_边缘"}, "subject_type": "子宫", "object": {"@value": "规则"}, "subject": "子宫"}, {"predicate": "子宫内膜_厚度", "object_type": {"@value": "厚度"}, "subject_type": "子宫内膜", "object": {"@value": "12mm"}, "subject": "子宫内膜"}, {"predicate": "CDFI表现", "object_type": {"@value": "CDFI表现"}, "subject_type": "CDFI", "object": {"@value": "未见异常血流信号"}, "subject": "CDFI"}, {"predicate": "附件_侧别", "object_type": {"@value": "侧别"}, "subject_type": "附件", "object": {"@value": "右"}, "subject": "附件"}, {"predicate": "附件_侧别", "object_type": {"@value": "侧别"}, "subject_type": "附件", "object": {"@value": "左"}, "subject": "附件"}, {"predicate": "附件_回声表现", "object_type": {"@value": "附件_回声表现"}, "subject_type": "附件", "object": {"@value": "未见明显异常"}, "subject": "附件"}, {"predicate": "附件_回声大小", "object_type": {"@value": "回声大小"}, "subject_type": "附件", "object": {"@value": "25×34mm"}, "subject": "附件"}, {"predicate": "附件_回声强度", "object_type": {"@value": "回声强度"}, "subject_type": "附件", "object": {"@value": "无回声"}, "subject": "附件"}, {"predicate": "附件_边界表现", "object_type": {"@value": "边界表现"}, "subject_type": "附件", "object": {"@value": "清晰"}, "subject": "附件"}, {"predicate": "附件_囊壁表现", "object_type": {"@value": "囊壁表现"}, "subject_type": "附件", "object": {"@value": "平滑"}, "subject": "附件"}, {"predicate": "子宫肌层_边界表现", "object_type": {"@value": "边界表现"}, "subject_type": "子宫肌层", "object": {"@value": "均匀"}, "subject": "子宫肌层"}]}

    d = structured_output(dict)
    print(d)