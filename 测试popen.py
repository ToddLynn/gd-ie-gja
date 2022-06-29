import os

golden_file="./data/kt_dev_196.json"
predict_file="./output/eval_predictions.json"


r = os.popen(
    'python ./re_official_evaluation.py --golden_file={} --predict_file={}'.
        format(golden_file, predict_file))
result = r.read()
print("**************")
print(result)