import json
import numpy as np
import argparse
from sklearn.metrics import accuracy_score,f1_score,precision_score,recall_score
import pickle as pkl

relation_file = '../../Orginal_data/relation/only_relation.pkl'
only_relation = pkl.load(open(relation_file, 'rb'))

relation_id = {}
for ors in only_relation:
        relation_id[only_relation[ors]] = ors

def getresult(fn):
    result = []
    with open(fn, "r") as f:
        l = f.readline()
        while l:
            l = l.strip().split()
            for i in range(len(l)):
                l[i] = float(l[i])
            result += [l]
            l = f.readline()
    result = np.asarray(result)
    return list(1 / (1 + np.exp(-result)))


def getpredict(result, T1 = 0.5, T2 = 0.4):
    for i in range(len(result)):
        r = []
        maxl, maxj = -1, -1
        for j in range(len(result[i])):
            if result[i][j] > T1:
                r += [j]
            if result[i][j] > maxl:
                maxl = result[i][j]
                maxj = j
        if len(r) == 0:
            if maxl <= T2:
                r = [32]
            else:
                r += [maxj]
        result[i] = r
    return result


def evaluate(devp, data):
    index = 0
    correct_sys, all_sys = 0, 0
    correct_gt = 0

    for i in range(len(data)):
        for j in range(len(data[i][1])):
            for id in data[i][1][j]["rid"]:
                if id != 32:
                    #
                    correct_gt += 1
                    if id in devp[index]:
                        # TP
                        correct_sys += 1
            for id in devp[index]:
                if id != 32:
                    # TP + FN
                    all_sys += 1
            index += 1

    precision = correct_sys/all_sys if all_sys != 0 else 1
    recall = correct_sys/correct_gt if correct_gt != 0 else 0
    f_1 = 2*precision*recall/(precision+recall) if precision+recall != 0 else 0

    return precision, recall, f_1


def evaluate2(devp, data):
    labels = []
    preds = []
    for i in range(len(data)):
        for j in range(len(data[i][1])):
            labels.append(data[i][1][j]["rid"][0])

    for dp in devp:
        preds.append(dp[0])


    for c in range(32):
        compute_label = c
        labels_ = [0 if l!=compute_label else 1 for l in labels]
        preds_ = [0 if p!=compute_label else 1 for p in preds]

        f_1_binary = f1_score(labels_, preds_, pos_label=1,average='binary')
        print(compute_label,'label=',relation_id[compute_label],' f1=',f_1_binary)


    return precision, recall, f_1

def evaluate3(devp, data):
    index = 0
    correct_sys, all_sys = 0, 0
    correct_gt = 0
    clist = [0,1,2,13,31]
    for i in range(len(data)):
        for j in range(len(data[i][1])):
            for id in data[i][1][j]["rid"]:
                if id not in clist:
                    correct_gt += 1
                    if id in devp[index]:
                        correct_sys += 1
            for id in devp[index]:
                if id not in clist:
                    all_sys += 1
            index += 1

    precision = correct_sys/all_sys if all_sys != 0 else 1
    recall = correct_sys/correct_gt if correct_gt != 0 else 0
    f_1 = 2*precision*recall/(precision+recall) if precision+recall != 0 else 0

    return precision, recall, f_1



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--f1dev",
                        default='../../bert/bert_today/logits_dev.txt',
                        type=str,
                        # required=True,
                        help="Dev logits (f1).")
    parser.add_argument("--f1test",
                        default='../../bert/bert_today/logits_test.txt',
                        type=str,
                        # required=True,
                        help="Test logits (f1).")

    args = parser.parse_args()

    f1dev = args.f1dev
    f1test = args.f1test

    with open("../../Final_Data/dev.json", "r", encoding='utf8') as f:
        datadev = json.load(f)
    with open("../../Final_Data/test.json", "r", encoding='utf8') as f:
        datatest = json.load(f)

    bestT2 = bestf_1 = 0
    for T2 in range(51):
        dev = getresult(f1dev)
        devp = getpredict(dev, T2=T2/100.)
        precision, recall, f_1 = evaluate(devp, datadev)
        if f_1 > bestf_1:
            bestf_1 = f_1
            bestT2 = T2/100.

    print("best T2:", bestT2)
    dev = getresult(f1dev)
    devp = getpredict(dev, T2=bestT2)
    test = getresult(f1test)
    testp = getpredict(test, T2=bestT2)
    print('======================================================')
    precision, recall, f_1 = evaluate(devp, datadev)
    print("dev (P R F1)", precision, recall, f_1)
    precision, recall, f_1 = evaluate(testp, datatest)
    print("test (P R F1)", precision, recall, f_1)
    print('======================================================')
    evaluate2(devp, datadev)
    evaluate2(testp, datatest)
    print('=======================================================')
    precision, recall, f_1 = evaluate3(devp, datadev)
    print("other dev (P R F1)", precision, recall, f_1)
    precision, recall, f_1 = evaluate3(testp, datatest)
    print("other test (P R F1)", precision, recall, f_1)

