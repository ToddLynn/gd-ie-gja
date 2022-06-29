# str1 =  "1、左乳外上象限巨大低回声团,考虑BI-RADS:5类。2、右乳内上象限，BI-RADS2类。3、双侧腋下未见明显肿大淋巴结。"
str1 =  "1、甲状腺大部切除术后,残余甲状腺未见明显异常声像。2、双侧颈部未见肿大淋巴结声像。3、双侧乳腺组织未见异常肿块声像。4、双腋下未见明显肿大淋巴结。"

# idx1 = str1.find("内",4)
# idx1 = str1.find("1")
# idx1 = str1.find("双")

idx1 = str1.find("4、双腋下未见明显肿大淋巴结。")
print(idx1)

idx2 = str1.find("颈部",idx1)

print("idx2:  {}".format(idx2))

