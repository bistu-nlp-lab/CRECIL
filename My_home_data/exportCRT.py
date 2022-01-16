import json
import pickle as pkl

key_character = {"fm": "傅明", "hp": "和平", "jzg": "贾志国", "jzx": "贾志新", "jyy": "贾圆圆",
                 "jxf": "贾小凡", "mcy": "孟朝阳", "zfg": "张凤姑", "xxg": "薛晓桂","mzy": "孟朝阳"}

alternative_name = {
    "圆圆": "贾圆圆",
    "志新": "贾志新",
    "小凡": "贾小凡",
    "和平": "和平",
    "志国": "贾志国",
    "傅老": "傅明",
    "小张": "张凤姑",
}

maybe_trigger = ['爸','爸爸','爸爸爸','妈','妈妈','爷爷','姑姑','公公','儿媳',
                 '大哥','爹','二叔','娘','哥','女朋友','好儿子','儿子','女儿']
pron = ['我','你','他','咱','俺','您']

colls = ['众人']


# step1 将neo4j中的关系数据导出 并存储成pkl文件
# step2 读取已经存储在本地的pkl文件
# step3 读取我爱我家文件,关系数据 生成 Argument pair
def read_wawj(wawj_file, re_dict, only_re_dict, speaker_hidden=True):
    f = open(wawj_file, encoding='utf-8')
    mos = json.load(f)

    all_data = []
    for i in range(0, 120):
        ep = mos['episodes'][i]

        for scene in ep['scenes']:
            print('============', scene['scene_id'], '============')
            utterances = []

            # 对话中的任务角色存储在 speaker_list 和entity_list 中
            # 发言人词典 以及 发言人列表
            speaker_list = []
            speaker_dict = {}
            speaker_index = 1
            # 话语中角色实体词典  以及 角色实体列表
            entity_list = []
            entity_dict = {}

            for utr in scene["utterances"]:
                # 清洗utterance
                utr['transcript'] = utr['transcript'].replace('/', '').replace('【', '').replace('】', '')
                utterance = utr['transcript']

                # 将speaker替换为人物真实名称
                if utr['speakers'] in alternative_name:
                    utr['speakers'] = alternative_name[utr['speakers']]

                # 将发言人掩住 真实姓名替换为speaker N
                speaker = utr["speakers"]
                if speaker not in speaker_dict:
                    speaker_dict[speaker] = 'S ' + str(speaker_index)
                    speaker_list.append('S ' + str(speaker_index))
                    speaker_index += 1

                if speaker_hidden:
                    utterances.append(speaker_dict[speaker] + ': ' + utterance)
                else:
                    utterances.append(speaker + ': ' + utterance)

                # 获取scene中出现的角色
                characters = utr["character_entities"]

                # 此处获取到了单句的token 和 单句的指代 以及 单句的发言人
                # 人物包括  说话人和指代的人
                # 将这部分角色生成 关系三元组

                # 从对话中抽取关系
                tokens = utr['tokens']
                for character in characters:
                    # maybe_trigger是为了去掉一些广义的mention
                    if tokens[character[2]] not in maybe_trigger and sum([1 if i in character[0] else 0 for i in pron])==0:
                        if tokens[character[2]] == character[0]:
                            if character[0] not in entity_list:
                                entity_list.append(character[0])
                            if character[1] in key_character:
                                entity_dict[tokens[character[2]]] = key_character[character[1]]
                            else:
                                entity_dict[tokens[character[2]]] = character[1]
                        else:
                            print('token和character 没有对应上')
                            print(character,tokens)
                            print()
                    else:
                        pass

            people_list = speaker_list + entity_list
            speaker_reserve_dict = dict(zip(speaker_dict.values(), speaker_dict.keys()))
            people_dict = {**speaker_reserve_dict,**entity_dict}
            print(len(entity_list), entity_list)
            print(len(speaker_dict),speaker_dict.keys())
            relation_pair_list = []
            # 要过滤掉同样的mention指向不同的角色
            for x in people_list:
                for y in people_list:
                    if x != y:
                        p1 = people_dict[x]
                        p2 = people_dict[y]
                        if (p1,p2) in re_dict:
                            r = re_dict[(p1,p2)]
                            rid = [only_re_dict[rel] for rel in r]
                            relation_pair = {'x': x, 'y': y, 'r': r[:1], 'rid': rid[:1]}
                        else:
                            if p1 == p2:
                                relation_pair = {'x': x, 'y': y, 'r': ['per:alternate_name'],'rid':[0]}
                            else:
                                relation_pair = {'x': x, 'y': y, 'r': ['unanswerable'],'rid':[31]}

                        relation_pair_list.append(relation_pair)

            # 取到了所有的角色|关系列表
            # print(relation_pair_list)
            # scene_information_list = [utterances,relation_pair_list,scene]
            scene_information_list = [utterances, relation_pair_list]
            # print(scene_information_list)
            all_data.append(scene_information_list)

    with open('final_0.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':

    relation_tuple_file = '../Orginal_data/relation/relation.pkl'
    relation_file = '../Orginal_data/relation/only_relation.pkl'
    wawj_file = '../Orginal_data/My_home.json'

    relation = pkl.load(open(relation_tuple_file, 'rb'))
    only_relation = pkl.load(open(relation_file, 'rb'))

    read_wawj(wawj_file, relation, only_relation)
