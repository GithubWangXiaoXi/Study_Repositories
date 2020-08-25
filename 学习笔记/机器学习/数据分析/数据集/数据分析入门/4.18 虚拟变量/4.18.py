# -*- coding: utf-8 -*-
import pandas

data = pandas.read_csv(
    'D:\\PDA\\4.18\\data.csv', 
    encoding='utf8'
)

data['Education Level'].drop_duplicates()

"""
博士后    Post-Doc
博士      Doctorate
硕士      Master's Degree
学士      Bachelor's Degree
副学士    Associate's Degree
专业院校  Some College
职业学校  Trade School
高中      High School
小学      Grade School
"""
educationLevelDict = {
    'Post-Doc': 9,
    'Doctorate': 8,
    'Master\'s Degree': 7,
    'Bachelor\'s Degree': 6,
    'Associate\'s Degree': 5,
    'Some College': 4,
    'Trade School': 3,
    'High School': 2,
    'Grade School': 1
}

data['Education Level Map'] = data[
    'Education Level'
].map(
    educationLevelDict
)

data['Gender'].drop_duplicates()

dummies = pandas.get_dummies(
    data, 
    columns=['Gender'],
    prefix=['Gender'],
    prefix_sep="_",
    dummy_na=False,
    drop_first=False
)

dummies['Gender'] = data['Gender']