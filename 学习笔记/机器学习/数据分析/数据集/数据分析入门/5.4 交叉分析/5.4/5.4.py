import numpy
import pandas

data = pandas.read_csv(
    'D:\\PDA\\5.4\\data.csv'
)

bins = [
    min(data.年龄)-1, 20, 30, 40, max(data.年龄)+1
]
labels = [
    '20岁以及以下', '21岁到30岁', '31岁到40岁', '41岁以上'
]

data['年龄分层'] = pandas.cut(
    data.年龄, 
    bins, 
    labels=labels
)

ptResult = data.pivot_table(
    values=['年龄'], 
    index=['年龄分层'], 
    columns=['性别'], 
    aggfunc=[numpy.size]
)
