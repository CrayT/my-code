# HEA-code
## HEA_1:
 - Gao做训练集，Ye做预测集。

## HEA_2:
 - Gao+Ye合并作为整个数据集,只选取部分特征。

## HEA_3:
 - Gao+Ye合并作为整个数据集，lda降维。准确率最高KNC:89%

## HEA_4_featuretool:
 - Gao+Ye合并作为整个数据集，可通过feature_create扩维函数扩充特征维度。

## feature_create:
 - 扩维函数：
 - create_features：用featuretool工具包进行扩维，不适合本例的单个数据集；
 - generate_feature：对本例的单个数据集进行扩维；
 
## add_feature:
 - 扩维：任意两个特征通过乘除，然后取倒数来扩充维度，然后再lda降维，然后训练测试。准确率最高95%。

## HEA_4-jupyter:
 - 数据集经过扩维后，然后再经LDA降维，分为训练和测试集。类似HEA_4_featuretool。若不经过降维直接训练预测，准确率最高DTC:85%

## HEA_5:
 - 数据经过扩维后，分为训练和测试集，在训练集上进行LDA的降维模型fit，然后在训练集和测试集进行转换。-----效果很差，准确率不到60。
 - 原始数据不经过处理，直接分类预测。最高DTC 83%，综合效果不好。


## HEA_7:
- 已经得到在rfc的RFE的特征排序的前100个特征列标,在此基础上进行其他操作,得到各个算法的准确率。

# HEA_8:
 - 根据得到的准确率绘制曲线。


