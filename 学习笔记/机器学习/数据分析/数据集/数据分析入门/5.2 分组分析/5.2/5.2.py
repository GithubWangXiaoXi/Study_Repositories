import numpy
import pandas

data = pandas.read_csv(
    'D:\\PDA\\5.2\\data.csv'
)

aggResult = data.groupby(
    by=['class']
)['score'].agg({
    '总分': numpy.sum, 
    '人数': numpy.size, 
    '平均值': numpy.mean
})
