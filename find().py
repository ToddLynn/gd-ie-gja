str1 = "1、双侧乳腺组织增生。双侧乳腺多发囊性结节,BI-RADS3类,建议定期复查。2、双侧腋下未见明显肿大淋巴结。"

# aaa =str1.find("BI-RADS3类")
aaa =str1.find("腋下")
seg =str1.find("2、双侧腋下未见明显肿大淋巴结。")
print("2、双侧腋下未见明显肿大淋巴结。",seg)


bbb =str1.find("双侧")
print("双侧   :",bbb)


ccc = str1.find("双侧",seg)
ddd = str1.find("腋下",seg)
eee = str1.find("未见明显肿大淋巴结",seg)

print("双侧   :",ccc)
print("腋下   :",ddd)
print("未见明显肿大淋巴结   :",eee)
