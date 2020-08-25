import numpy
import pandas

data = pandas.read_csv(
    'D:\\PDA\\5.3\\data.csv'
)

aggResult = data.groupby(
    by=['年龄']
)['年龄'].agg({
    '人数': numpy.size
})

data.年龄.hist()

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

aggResult = data.groupby(
    by=['年龄分层']
)['年龄'].agg({
    '人数': numpy.size
})

pAggResult = round(
    aggResult/aggResult.sum(), 
    2
)*100
pAggResult['人数'].map('{:,.2f}%'.format)