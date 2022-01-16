# 构建数据集
# train:dev:test=7:2:1
# train 479
# dev 140
# test 70
import json
import random
import pickle as pkl

wawj_file = '../My_home_data/final.json'

f = open(wawj_file, encoding='utf-8')
mos = json.load(f)

min_set = []
mid_set = []
max_set = []

for m in mos:
    i = len(m[0])
    if i <= 70:
        if i<24:
            min_set.append(m)
        elif i<47:
            mid_set.append(m)
        else:
            max_set.append(m)

train_rate = 0.7
dev_rate = 0.9
test_rate = 1

train_set = []
dev_set = []
test_set = []

random.shuffle(min_set)
random.shuffle(mid_set)
random.shuffle(max_set)

train_set = min_set[:int(len(min_set)*train_rate)] + mid_set[:int(len(min_set)*train_rate)] + max_set[:int(len(min_set)*train_rate)]
dev_set = min_set[int(len(min_set)*train_rate):int(len(min_set)*dev_rate)] + mid_set[int(len(min_set)*train_rate):int(len(min_set)*dev_rate)] + max_set[int(len(min_set)*train_rate):int(len(min_set)*dev_rate)]
test_set = min_set[int(len(min_set)*dev_rate):] + mid_set[int(len(min_set)*dev_rate):] + max_set[int(len(min_set)*dev_rate):]

random.shuffle(train_set)
random.shuffle(dev_set)
random.shuffle(test_set)


# 测试数据集比例
# relation_file = 'Orginal_data/relation/only_relation.pkl'
#
# def get_dic_relation(dataset):
#     relation_list = pkl.load(open(relation_file, 'rb'))
#     for r in relation_list:
#         relation_list[r] = 0
#     for index, m in enumerate(dataset):
#         if len(m[1]) == 0:
#             continue
#         for rl in m[1]:
#             # for r in rl['r']:
#             #     relation_list[r] = relation_list[r] + 1
#             relation_list[rl['r'][0]] = relation_list[rl['r'][0]] + 1
#     return relation_list
#
#
# A = get_dic_relation(train_set)
# B = get_dic_relation(dev_set)
# C = get_dic_relation(test_set)
#
# count = 0
# for ii,(a,b,c) in enumerate(zip(A,B,C)):
#     if B[a]/A[a]==0 or C[a]/A[a]==0:
#         count+=1
#     print(a,'\t\t',B[a]/A[a],C[a]/A[a])
# print(count)


with open('train.json', 'w', encoding='utf-8') as f:
    json.dump(train_set, f, ensure_ascii=False, indent=4)

with open('dev.json', 'w', encoding='utf-8') as f:
    json.dump(dev_set, f, ensure_ascii=False, indent=4)

with open('test.json', 'w', encoding='utf-8') as f:
    json.dump(test_set, f, ensure_ascii=False, indent=4)

