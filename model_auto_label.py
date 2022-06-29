from predict import *
from structured_index_output import *

"""定义输入 到底是json、还是多个txt?"""
r"data/input/input_content.json"


# (在输出预测输出之前，先清空下本地的历史输出文件)
output_path = r"output/test_predictions.json"
if os.path.exists(output_path):
    os.remove(output_path)


# """模型原始output"""
predict_re()


li_index_output = []
# """structure_index_output"""
with open(output_path, "r", encoding="utf-8") as ft:
    for li in ft.readlines():

        # 3.输出
        # output_dict：Model 原版输出，供前端反向解析
        with open(output_path, 'r', encoding="utf-8") as output_f:
            output_dict = json.loads(li)

            # structured_dict:结构化输出
            structured_dict = None
            structured_dict = structured_index_output(output_dict)

        li_index_output.append(structured_dict)


"""定义输出"""


print(li_index_output)
output_auto_label_file = "output/output_auto_500.json"
with open(output_auto_label_file, "w", encoding="utf-8") as fb:
    json.dump(li_index_output[:500],fb,ensure_ascii=False)
    # json.dump(li_index_output[:3],fb,ensure_ascii=False)