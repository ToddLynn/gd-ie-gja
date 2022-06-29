--max_len=150 --model_name_or_path="./data/zhoujx/prev_trained_model/chinese_roberta_wwm_ext_pytorch" --learning_rate=1e-5 --linear_learning_rate=1e-2 --num_train_epochs=10 --output_dir="./output" --weight_decay=0.01 --early_stop=2 --per_gpu_eval_batch_size=2  --per_gpu_train_batch_size=2





#预测 python predict.py
--max_len=150 --model_name_or_path="./data/zhoujx/prev_trained_model/chinese_roberta_wwm_ext_pytorch" --per_gpu_eval_batch_size=2 --output_dir="./output" --fine_tunning_model="./output/best_model.pkl"

#python app.py 添加header-2.py --max_len=150 --model_name_or_path="./data/zhoujx/prev_trained_model/chinese_roberta_wwm_ext_pytorch" --per_gpu_eval_batch_size=2 --output_dir="./output" --fine_tunning_model="./output/best_model.pkl"
