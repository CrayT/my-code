#coding:utf8
from sou_an_deng_ji import crime_form  #受案登记表
from li_an import li_an_form #立案决定书
from chuan_huan import chuan_huan_form  #传唤证
from qu_bao_hou_shen import qu_bao_form #取保候审决定书
from qi_su_yi_jian import qi_su_yi_jian
from juan_zong import juan_zong
address='E:\\魏老师\\刑事侦查卷宗目录7份\\刑事侦查卷宗目录7份\\3.txt'
#test=crime_form(address)
#test=li_an_form(address)
#test=chuan_huan_form(address)
#test=qu_bao_form(address)
#test=qi_su_yi_jian(address)
test=juan_zong(address)
print("\ntest:",test)