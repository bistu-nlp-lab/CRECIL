

本项目提出并描述了一个新的可自由使用的中文多方对话数据集，用于自动提取基于对话的角色关系。这些数据是从中国情景喜剧《我爱我家》(I Love My Home)的原始电视剧本中提取出来的，该电视剧以复杂的家庭为基础，用中文进行自然的对话。我们引入了全局角色关系图和角色指代关系的人工标注方法，生成了基于对话的角色关系三元组。该语料库共标注了140个实体之间的关系。我们还进行了一个数据探索实验，通过部署基于bert的模型在CRECIL语料库和另一个现有的关系抽取语料库上提取角色关系(dialgre (Yu et al.， 2020))。我们发现，在实际的汉语会话中提取人物关系比在英语会话中更具挑战性。



本项目的目录结构分为Orginal_data，My_home_data，Final_data，bert四个文件夹，具体介绍如下：

**Orginal_data**

该文件夹下保存了本项目所标注的指代数据和关系数据，共标注了140个角色实体之间关系类别，以及指代关系。

其中My_home.json 为所注释的指代信息

另外relation子目录下包含两个文件，其中：

only_relation.txt 为关系类型

relation.txt 为全局角色关系三元组

**My_home_data**

该文件夹下保存了本项目生成CRT三元组的过程以及将源文件经过的格式处理化后的数据信息。其中exportCRT.py为本文生成CRT的策略，final.json为最终格式化处理后的数据。

**Final_Data** 

该文件夹下保存了本项目划分数据集的代码以及划分数据集的结果。其中shuffle_data.py为划分数据集的策略，train.json,dev.json以及test.json为本文所使用的实验数据。

**bert** 

该文件夹下保存了本文所使用的对话关系抽取模型的相关代码，参考DialogRE数据集提供的基线模型。

实验环境：pytorch1.7  python3.8

运行模型：python run_classifier.py

验证模型：python evaluate.py

