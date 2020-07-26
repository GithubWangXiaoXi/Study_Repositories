import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
import sklearn
import matplotlib.pyplot as plt

#注意要将一般的数组转化成numpy的ndarray数组，否则会报TypeError: 'numpy.float64' object cannot be interpreted as an integer
x1,x2,x3 = np.array([3.0,3.0]),np.array([4.0,3.0]),np.array([1.0,1.0])
y1,y2,y3  = 1,1,-1

X_train = np.array([x1,x2,x3])
Y_train = np.array([y1,y2,y3])
"""
梯度下降的原始形式
"""
class Model:

    """
    将w,b分别初始化为元素均为0的向量,b = 0，并且初始化学习率l_rate
    """
    def __init__(self):
        self.w = np.zeros(2)
        self.b = 0
        self.l_rate = 1

    """
    感知机模型虽然是sign(w·x + b),但实际上我们要训练的是w，b，所以使用分离超平面S作为目标函数即可
    """
    def sign(self,x,w,b):
        return np.dot(x,w) + b

    def fitting(self,X_train,Y_train):
        is_wrong = True

        # 直到没有误分类点，则找到分类直线
        while is_wrong:
            wrong_count = 0

            # 循环遍历训练集，寻找误分类点
            for i in range(len(X_train)):
                x = X_train[i]
                y = Y_train[i]

                if y * self.sign(x,self.w,self.b) <= 0:
                    print("真实类别:",y,end="---")
                    print("sign(w·x + b)的值:",self.sign(x,self.w,self.b),end="---")
                    wrong_count += 1
                    # 更新w，b
                    self.w = self.w + self.l_rate * np.dot(x,y)
                    self.b = self.b + self.l_rate * y
                    print("将w更新为:",self.w,end="---")
                    print("将b更新为:", self.b)
            if wrong_count == 0:
                is_wrong = False

"""
梯度下降的对偶形式
"""
class Model1:
    """
    对偶形式是针对所有实例x，标记y进行迭代计算a，进而得到w
    假设样本有100个实例，正类和负类均有50个，则a是100个元素的向量
    初始化：a所有元素为0，b为0
    """
    def __init__(self):
        self.a = np.zeros(len(X_train))
        self.b = 0
        self.l_rate = 1
        self.w = []

    """
    将w转化成 1~N个aj*xj*yj累加来计算
    """
    def sign(self,a,X_train,Y_train,b,x):

        w_ = np.zeros(len(X_train[0]))
        print("误分条件中w部分的运算:",end=" ")
        for j in range(0,len(X_train)):
            if j != len(X_train) - 1:
                print(a[j],"*", X_train[j], "*", Y_train[j],"+",end=" ")
            else:
                print(a[j], "*", X_train[j], "*", Y_train[j])
            w_ += a[j] * X_train[j] * Y_train[j]
        self.w = w_
        return np.dot(x, w_) + b


    def fitting(self,X_train,Y_train):
        is_wrong = True

        # 直到没有误分类点，则找到分类直线
        while is_wrong:
            wrong_count = 0

            # 循环遍历训练集，寻找误分类点
            for i in range(len(X_train)):
                x = X_train[i]
                y = Y_train[i]

                if y * self.sign(self.a, X_train,Y_train,self.b,x) <= 0:
                    print("误分类点:", x, end="---")
                    # print("真实预测值:", y, end="---")
                    # print("sign(w·x + b)的值:", self.sign(self.a, X_train,Y_train,self.b,x), end="---")
                    wrong_count += 1
                    # 更新w，b
                    self.a[i] = self.a[i] + self.l_rate
                    self.b = self.b + self.l_rate * y
                    print("将a更新为:", self.a,end="---")
                    print("将b更新为:", self.b)
            if wrong_count == 0:
                is_wrong = False

class Model2:
    """
    对偶形式是针对所有实例x，标记y进行迭代计算a，进而得到w
    假设样本有100个实例，正类和负类均有50个，则a是100个元素的向量
    初始化：a所有元素为0，b为0
    """
    def __init__(self):
        self.a = np.zeros(len(X_train))
        self.b = 0
        self.l_rate = 1
        self.w = np.zeros(2)
        # 初始化N * N维的Gram矩阵
        self.Gram = np.array([len(X_train) * [0]] * len(X_train))
        # print(self.Gram)

    # 计算上三角元素即可，将元素拷贝到下三角
    def calGram(self, X_train):
        # for i in range(0, len(self.Gram)):
        #     for j in range(i, len(self.Gram[0])):
        #         self.Gram[i][j] = np.dot(X_train[i], X_train[j])
        #         self.Gram[j][i] = self.Gram[i][j]
        # X_train必须是numpy的ndarray类型，才能用.T表示转置
        self.Gram = np.dot(X_train,X_train.T)
        print(self.Gram)

    """
        sign函数的功能是返回超平面S
        将w转化成 1~N个aj*xj*yj累加来计算，但是不要单独计算w，因为计算w后需要和xi求内积，出现重复计算，
        所以使用Gram矩阵，w·xi同时计算，减少计算耗时。
    """
    def sign(self, a, Y_train, i, b):
        w_x = 0
        for j in range(0, len(Y_train)):
            w_x += a[j] * Y_train[j] * self.Gram[i][j]
        return w_x + b

    def fitting(self, X_train, Y_train):
        is_wrong = True

        # 先计算Gram矩阵
        self.calGram(X_train)

        # 直到没有误分类点，则找到分类直线
        while is_wrong:
            wrong_count = 0

            # 循环遍历训练集，寻找误分类点
            for i in range(len(X_train)):
                x = X_train[i]
                y = Y_train[i]

                if y * self.sign(self.a, Y_train, i,self.b) <= 0:
                    # print("真实类别:", y, end="---")
                    # print("sign(w·x + b)的值:", self.sign(self.a, X_train,Y_train,self.b,x), end="---")
                    wrong_count += 1
                    # 更新w，b
                    self.a[i] = self.a[i] + self.l_rate
                    self.b = self.b + self.l_rate * y
                    print("将a更新为:", self.a, end=' ')
                    print("将b更新为:", self.b)

            if wrong_count == 0:
                # 注意最后一趟a更新完后，需要更新w,w = sum{ai*xi*yi)*(x1,x2,x3)
                for i in range(0,len(X_train)):
                    self.w += np.dot(self.a[i], X_train[i]) * Y_train[i]
                is_wrong = False

if __name__ == "__main__":

    # 绘制iris数据的散点图(前50条数据是1类，50~100数据为2类）
    plt.scatter(x1[0],x1[1],color='blue')
    plt.scatter(x2[0], x2[1], color='blue')
    plt.scatter(x3[0], x3[1], color='orange')

    """
    采用学习算法的原始形式，得到感知机模型的w，b,将函数方程转化为一次函数
    """
    perception = Model()
    perception.fitting(X_train,Y_train)
    x_points = np.linspace(0,5,2)
    y_ = -(perception.b + perception.w[0] * x_points)/perception.w[1]
    plt.plot(x_points,y_,color='cyan',lw=2.0)
    plt.legend()
    plt.show()

    # 绘制iris数据的散点图(前50条数据是1类，50~100数据为2类）
    plt.scatter(x1[0], x1[1], color='blue')
    plt.scatter(x2[0], x2[1], color='blue')
    plt.scatter(x3[0], x3[1], color='orange')
    """
    采用学习算法的对偶形式，得到感知机模型的系数ai，b,将函数方程转化为一次函数
    """
    perception1 = Model2()
    perception1.fitting(X_train,Y_train)
    x_points = np.linspace(0,5,2)
    y_ = -(perception1.b + perception1.w[0] * x_points)/perception1.w[1]
    plt.plot(x_points,y_,color='cyan',lw=2.0)
    plt.legend()
    plt.show()