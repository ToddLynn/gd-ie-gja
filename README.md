# 项目说明:


# 依赖包
- python=3.6
- torch=1.7
```
 (conda环境下)- pip install -r requirements.txt
```
# 训练
```
--max_len=150 --model_name_or_path="./data/zhoujx/prev_trained_model/chinese_roberta_wwm_ext_pytorch" --per_gpu_train_batch_size=4 --per_gpu_eval_batch_size=4 --learning_rate=1e-5 --linear_learning_rate=1e-2 --num_train_epochs=4 --output_dir="./output" --weight_decay=0.01 --early_stop=2
```


# 运行
启动  
```
python app.py
--max_len=150 --model_name_or_path="./data/zhoujx/prev_trained_model/chinese_roberta_wwm_ext_pytorch" --per_gpu_eval_batch_size=2 --output_dir="./output" --fine_tunning_model="./output/best_model.pkl"
```




# 展示示例
```
1.左乳2点低回声,BI-RADS3类。
1.左乳9点低回声,BI-RADS3类。右乳外上象限无回声,BI-RADS2类。右侧腋下淋巴结肿大。
1.右乳约9-10点不均质极低回声,考虑炎性可能。2、双腋下未见明显肿大淋巴结。
1、双侧乳腺组织呈增生改变。2、右侧腋下未见明显肿大淋巴结。
1、左乳外上象限巨大低回声团,考虑BI-RADS:5类。2、右乳内上象限，BI-RADS2类。3、双侧腋下未见明显肿大淋巴结。
```










#注意
1.乳腺组织增生描述、与乳腺BI-RADS分级的描述文本，暂不可同时识别。
2.右乳、右腋。没法区分右
