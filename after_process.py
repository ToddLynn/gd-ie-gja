"""模型输出spo_list后处理"""
"""把输出的作为病灶的"乳腺组织"改为"乳"""



import json


"""对单条content的output_model的病灶值，用(乳)替换(乳腺组织)"""
def head_value_replace():
    path = "./output/test_predictions.json"

    with open(path, "r", encoding="utf-8") as fr:
        dict1 = json.load(fr)

    # print(dict1)

    for spo in dict1["spo_list"]:
        if spo["subject_type"] == "病灶":
            spo["subject"] = "乳"

    with open(path, "w", encoding="utf-8") as fw:
        json.dump(dict1, fw, ensure_ascii=False)


"""对多条content的output_model的病灶值，用(乳)替换(乳腺组织)"""

def head_value_replace_many():
    path = "./output/test_predictions.json"
    new_path = "./output/ouput_model_replace.json"
    li_dict = []

    with open(path, "r", encoding="utf-8") as fb:
        li_output = fb.readlines()          #把json读取到li_output里面，
        print(len(li_output))
        for op in li_output:
            dict_op =json.loads(op)         #把json str字符串,解码成dict : python对象。

            for spo in dict_op["spo_list"]:
                if spo["subject_type"] == "病灶":
                    spo["subject"] = "乳"            #把subject值，强行改为“乳”

            li_dict.append(dict_op)


    """按格式，把dict逐行写入到json文件里"""    #将修改后的数据，存为同名的json文件。相当于是用新修改覆盖原json文件。

    with open(new_path, "w", encoding="utf-8") as fp:
        for line in li_dict:
            str1 = json.dumps(line, ensure_ascii=False)
            fp.write(str1 + "\n")

if __name__ == '__main__':
    head_value_replace_many()