a=[113627, 113630, 113633, 113634, 113635, 113636, 113637, 113642, 113643, 113644, 113645, 113648, 113650, 113652, 113653, 113659, 113660, 113668, 113670, 113672, 113673, 113677, 113678, 113682, 113683, 113688, 113690, 113692, 113693, 113697, 113698, 113699, 113700, 113708, 113710, 113711, 113713, 113714, 113717, 113726, 113727, 113728, 113732, 113746, 113747, 113749, 113751, 113754, 113759, 113772, 113777, 113780, 113786, 113788, 113790, 113810, 113822, 113843, 113861, 113863, 113876, 113877, 113894, 113913, 114039, 114041, 114044, 114046, 114047, 114050, 114056, 114058, 114060, 114062, 114063, 114066, 114067, 114068, 114069, 114070, 114072, 114073, 114081, 114082, 114085, 114088, 114089, 114094, 114095, 114097, 114098, 114106, 114110, 114112, 114113, 114115, 114117, 114120, 114125, 114141]
b=a.copy()
from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
digits = load_digits()
rank_rfe=a.copy()
# Plot pixel ranking
ranking_plt = np.array(rank_rfe).reshape(10,10)

# plt.matshow(ranking_plt, cmap=plt.cm.Blues)
# plt.colorbar()
# plt.title("Ranking of pixels with RFE")
# plt.show()
b=pd.DataFrame(b,columns=['a'])
b.insert(1,'iii',a)
pd.DataFrame(b).to_csv('/home/xutao/Downloads/Python/HEA-code/demo.csv',index=False)