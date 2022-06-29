# 项目说明:


### 1. 从阿里云Registry中拉取镜像

```
docker pull registry.cn-shenzhen.aliyuncs.com/space_gd_medical_ie/ck_gd_ie
```
### 2. 启动
启动  
```
docker run -p 8080:8080 --name container_gd_ie -v 预训练模型绝对路径:/app/data registry.cn-shenzhen.aliyuncs.com/space_gd_medical_ie/ck_gd_ie

```
脚本示例
```
docker run -p 8080:8080 --name container_gd_ie -v F:/workspace_dl_env/gd_medical_ie/data:/app/data registry.cn-shenzhen.aliyuncs.com/space_gd_medical_ie/ck_gd_ie
```


###*** 乳腺超声结构化抽取展示示例
```
1、双侧乳腺组织呈增生改变。2、右侧腋下未见明显肿大淋巴结。
1、左乳外上象限巨大低回声团,考虑BI-RADS:5类。2、右乳BI-RADS2类。3、双侧腋下未见明显肿大淋巴结。
1、双侧乳腺组织增生。2、左侧乳腺2点极低回声:BI-RADS3类。3、右侧腋下淋巴结可见。
1、双侧乳腺组织增生。BI-RADS3类。右乳导管局限性扩张。 2、左侧腋下未见明显肿大淋巴结。
1、双侧乳腺组织增生。2、左乳低回声结节,BI-RADS3类。3、右乳多发囊性暗区,BI-RADS2类。
```

