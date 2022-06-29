"""
用于知识提取-文本结构化提取展示的接口 -structured-show
"""


from flask import request, Flask, jsonify, make_response
from flask_cors import CORS
from predict import *
import json
from structured_output import *

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)
CORS(app, resources=r'/*')


@app.route('/medical_ie', methods=['POST'])
def post_Data():
    postdata = request.form['medical_content']

    if postdata:
        # 1.输入
        # (在生成输入文本的本地json文件，先清空一下的本地的历史生成文件)
        gene_path = "data/input/input_content.json"
        if os.path.exists(gene_path):
            os.remove(gene_path)

        dict1 = {"text": str(postdata)}
        with open(gene_path, "w", encoding="utf-8") as input_f:
            json.dump(dict1, input_f, ensure_ascii=False)

        # 2.
        # (在输出预测输出之前，先清空下本地的历史输出文件)
        output_path = r"output/test_predictions.json"
        if os.path.exists(output_path):
            os.remove(output_path)

        predict_re()

        with open(output_path, "r", encoding="utf-8") as ft:

            if json.load(ft)["spo_list"]:
                # 3.输出
                # output_dict：Model 原版输出，供前端反向解析
                with open(output_path, 'r', encoding="utf-8") as output_f:
                    output_dict = json.load(output_f)

                    # structured_dict:结构化输出
                    structured_dict = None
                    structured_dict = structured_output(output_dict)

                    data = {
                        "annotation": output_dict,
                        "output_dict": structured_dict

                    }
                recognize_info = {
                    "code": 200,
                    "msg": "success",
                    "data": data,
                }

                response = make_response(jsonify(recognize_info))
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,GET,POST'
                response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
                return response
            else:
                recognize_info = {
                    "code": 404,
                    "msg": "当前没有识别出任何实体关系",
                    "data": {}
                }
                response = make_response(jsonify(recognize_info))
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,GET,POST'
                response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
                return response
    else:
        recognize_info = {
            "code": 401,
            "msg": "当前无输入数据，请重新输入",
            "data": {}
        }
        response = make_response(jsonify(recognize_info))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        return response


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
