# import numpy as np
# from tensorboardX import SummaryWriter
#
#
# # D = {
# #     "增生腺体": {
# #         "增生_侧别": {},
# #         "增生_表现": {}
# #     },
# #     "导管": {
# #         "导管_侧别": {},
# #         "导管_表现": {}
# #     },
# #     "病灶": {
# #         "病灶_侧别": {},
# #         "病灶_象限": {},
# #         "病灶_钟面": {},
# #         "病灶_评估分类": {},
# #         "病灶_回声强度": {},
# #
# #     },
# #     "腋窝": {
# #         "腋窝_侧别": {},
# #         "腋窝_淋巴结表现": {},
# #         "腋窝_评估分类": {}
# #     },
# #     "锁骨上侧": {
# #         "锁骨上侧_侧别": {},
# #         "锁骨上_淋巴结表现": {},
# #         "锁骨上_评估分类": {}
# #     },
# #     "锁骨下侧": {
# #         "锁骨下_侧别": {},
# #         "锁骨下_淋巴结表现": {},
# #         "锁骨下_评估分类": {}
# #     },
# #     "内乳": {
# #         "内乳_侧别": {},
# #         "内乳_淋巴结表现": {},
# #         "内乳_评估分类": {}
# #     }
# # }
# # # # D["科比"] = "mvp"
# # # #
# # # # D["内乳"]["曼巴"] ="champion"
# # # # d = D["内乳"]
# # # # print(d)
# # # # d["内乳_评估分类"]["new_key"] = [1,23,4]
# # # # D["内乳"]["内乳_评估分类"]["index"] = 123
# # # #
# # # # # print(d)
# # # # print(D)
# # #
# # # dict_new = {"key1":123,"key2":"中文word","key3":{}}
# # # # dict_new["key3"]= "kd"
# # # dict_new["key3"]["name"]= "kd"
# # #
# # # # dict_sub = dict_new["key3"]
# # # #
# # # # dict_sub["sub_key1"] = 456
# # # #
# # # print(dict_new)
# # # # print(dict_sub)
# #
#
#
# # list1 = [0, 3, 2, 3, 1, 0, 9, 8, 9, 7]
# # list2 = list(set(list1))
# # print(list2)        # [0, 1, 2, 3, 7, 8, 9]
# # list2.sort(key = list1.index)
# # print(list2)
#
#
# # text ="1、左乳外上象限巨大低回声团,考虑BI-RADS:5类。2、右乳内上象限，BI-RADS2类。3、双侧腋下未见明显肿大淋巴结。"
#
# # text =  "1.左乳9点低回声,BI-RADS3类。右乳外上象限无回声,BI-RADS2类。右侧腋下淋巴结肿大。"
# #
# # print(text.find("腋下",4))
#
#
# #
# # writer = SummaryWriter(comment='base_scalar')
# # for epoch in range(100):
# #
# #     # 将我们所需要的数据保存在文件里面供可视化使用。 这里是Scalar类型，所以使用writer.add_scalar()
# #     # 第一个参数可以简单理解为保存图的名称，第二个参数是可以理解为Y轴数据，第三个参数可以理解为X轴数据
# #     writer.add_scalar('scalar/test', np.random.rand(), epoch)
# #     # writer.add_scalars('scalar/scalars_test', {'xsinx': epoch * np.sin(epoch), 'xcosx': epoch * np.cos(epoch)}, epoch)
# #     # writer.add_scalars('scalar/okc_test', {'xsinx': epoch **2}, epoch)
# #     # 当Y轴数据不止一个时，可以使用writer.add_scalars().运行代码之后生成文件之后，我们在runs同级目录下使用命令行
# # writer.close()
# #
# str1 = "1、双侧乳腺组织增生。2、双侧腋下未见明显肿大淋巴结。"
# num = str1.find("")


li =  []

print(li[0])