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









###*** 宫颈癌超声结构化抽取
```
子宫大小65x64x56mm,边缘规则,子宫肌层回声均匀;宫腔线居中,子宫内膜厚度为8.5mm。右侧附件见19x18mm无回声,边界清晰,囊壁平滑。左侧附件未见明显异常。CDFI:未见异常血流信号。

子宫大小在正常范围,边缘规则,子宫肌层回声均匀;宫腔线居中,子宫内膜厚度为5mm。CDFI:未见异常血流信号。左侧附件见17×13mm无回声,边界清晰,囊壁平滑。右侧附件未见明显异常。

子宫大小在正常范围,边缘规则,子宫肌层回声均匀;宫腔线居中,子宫内膜厚度为12mm。左侧附件见25×34mm无回声,边界清晰,囊壁平滑。右侧附件未见明显异常。CDFI:未见异常血流信号。



子宫大小在正常范围,边缘规则,子宫肌层回声稍粗、不均匀,后壁可见大小约9×7mm的低回声,边界欠清;宫腔线居中,子宫内膜厚度为5.6mm。双侧附件区未见明显异常包块回声。CDFI:未见异常血流信号显示。
子宫大小在正常范围,边缘规则,子宫肌层回声均匀;宫腔线居中,子宫内膜厚度为8mm。宫颈可见数个无回声,较大的约10x8mm。双侧附件未见明显异常包块。CDFI:未见明显异常血流信号。

