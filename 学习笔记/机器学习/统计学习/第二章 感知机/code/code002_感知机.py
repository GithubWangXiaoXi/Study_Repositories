import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
import sklearn
import matplotlib.pyplot as plt

# ----------------------------------数据预处理------------------------------------
"""
 The iris dataset is a classic and very easy multi-class classification
 dataset.
 =================   ==============
    Classes                          3
    Samples per class               50
    Samples total                  150
    Dimensionality                   4
    Features            real, positive
    =================   ==============
data : Bunch(结构化数据）
        Dictionary-like object, the interesting attributes are:
        'data', the data to learn,
        'target', the classification labels,
        'target_names', the meaning of the labels,
        'feature_names', the
        meaning of the features, and 'DESCR', the
        full description of the dataset.
  [5.1 3.5 1.4 0.2]
  [4.9 3.  1.4 0.2]
  [4.7 3.2 1.3 0.2]
  [4.6 3.1 1.5 0.2]
  [5.  3.6 1.4 0.2]
"""
iris = load_iris()
# Numpy是以矩阵为基础的数学计算模块，纯数学。
# Scipy基于Numpy，科学计算库，有一些高阶抽象和物理模型。比方说做个傅立叶变换，这是纯数学的，用Numpy；做个滤波器，这属于信号处理模型了，在Scipy里找。
# Pandas提供了一套名为DataFrame的数据结构，比较契合统计分析中的表结构，并且提供了计算接口，可用Numpy或其它方式进行计算。
df = pd.DataFrame(iris.data, columns=iris.feature_names)

# print(df['sepal length (cm)'])
# print(df.columns)

"""
dataFrame的特征选择：如果没有该特征‘label’，则在dataFrame表末追加一列,给实例添加标注
"""
df['label'] = iris.target
df.columns = ['sepal length', 'sepal width', 'petal length', 'petal width', 'label']
# print(df)
# 每种标签数据量有多少
# print(df.label.value_counts())

# 0~49为0类，50~99为1类，100~149为2类
# plt.scatter(df[:50]['sepal length'], df[:50]['sepal width'], label='0')
# plt.scatter(df[50:100]['sepal length'], df[50:100]['sepal width'], label='1')
# plt.xlabel('sepal length')
# plt.ylabel('sepal width')

# --------------------------------数据输入：确定输入变量（特征向量），以及输出变量的真实值（类别）-----------------------------------------------
# While standard Python / Numpy expressions for selecting and setting are intuitive and
# come in handy for interactive work, for production code, we recommend the optimized pandas
# data access methods, .at, .iat, .loc and .iloc.
# 获取特征为'sepal length', 'sepal width', 'label'的前100条数据,是ndarray类型的二维数组
"""
我们选取0,1两类的数据，并提取特征：'sepal length'，'sepal width'作为实例x，'label'作为标记y
"""
data = np.array(df.iloc[:100, [0, 1, -1]])
# 对data再筛选，得到数据集X和真实值y
X, y = data[0:100, [0, 1]], data[0:100, -1]

# <https://blog.csdn.net/qq_38402294/article/details/95763489>
"""
在标签数组y中，如果i = 1,则将该位置的值重置为1，如果i！=1（else），则将该位置的值重置为-1
其实不用把类别规定死，只要有个类别为+1，另一个类别为-1，或者说两个类别的值互为相反数即可。
"""
y = np.array([1 if i == 1 else -1 for i in y])
# print(y)

"""
梯度下降的原始形式
"""
class Model:

    """
    将w,b分别初始化为元素均为0的向量,b = 0，并且初始化学习率l_rate
    """
    def __init__(self):
        self.w = np.zeros(len(data[0]) - 1)
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
                    # print("真实类别:",y,end="---")
                    # print("sign(w·x + b)的值:",self.sign(x,self.w,self.b),end="---")
                    wrong_count += 1
                    # 更新w，b
                    self.w = self.w + self.l_rate * np.dot(x,y)
                    self.b = self.b + self.l_rate * y
                    print("将w更新为:",self.w,end="---")
                    print("将b更新为:", self.b)
            if wrong_count == 0:
                is_wrong = False

"""
梯度下降的对偶形式（耗时大）
"""
class Model1:
    """
    对偶形式是针对所有实例x，标记y进行迭代计算a，进而得到w
    假设样本有100个实例，正类和负类均有50个，则a是100个元素的向量
    初始化：a所有元素为0，b为0
    """
    def __init__(self):
        self.a = np.zeros(len(data))
        self.b = 0
        self.l_rate = 1
        self.w = []

    """
    将w转化成 1~N个aj*xj*yj累加来计算，但是不要单独计算w，因为计算w后需要和xi求内积，出现重复计算，
    所以使用Gram矩阵，w·xi同时计算，减少计算耗时。
    """
    def sign(self,a,X_train,Y_train,b,x):

        w_ = np.zeros(len(X_train[0]))
        for j in range(0,len(X_train)):
            w_ += a[j] * X_train[j] * Y_train[j]
        self.w = w_
        temp = np.dot(x, w_) + b
        print("w_x + b",temp)
        return temp


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

                    # print("y",y)
                    # print("真实类别:", y, end="---")
                    # print("sign(w·x + b)的值:", self.sign(self.a, X_train,Y_train,self.b,x), end="---")
                    wrong_count += 1
                    # 更新w，b
                    self.a[i] = self.a[i] + self.l_rate
                    self.b = self.b + self.l_rate * y
                    print("将w更新为:", self.w, end=' ')
                    print("将b更新为:", self.b)
            # 注意a更新完后，需要更新w
            if wrong_count == 0:
                self.sign(self.a, X_train, Y_train, self.b, x)
                is_wrong = False

class Model2:
    """
    对偶形式是针对所有实例x，标记y进行迭代计算a，进而得到w
    假设样本有100个实例，正类和负类均有50个，则a是100个元素的向量
    初始化：a所有元素为0，b为0
    """
    def __init__(self):
        self.a = np.zeros(len(data))
        self.b = 0
        self.l_rate = 1
        self.w = np.zeros(2)
        #初始化N * N维的Gram矩阵,注意Gram矩阵精度
        self.Gram = np.array([len(data) * [0]] * len(data),dtype=np.float64)
        # print(self.Gram)


    # 计算上三角元素即可，将元素拷贝到下三角
    # 注意Gram矩阵的精度，避免计算误差（数据越多，误差越大）
    def calGram(self,X_train):
        # for i in range(0,len(self.Gram)):
        #     for j in range(i,len(self.Gram[0])):
        #         self.Gram[i][j] = np.dot(X_train[i], X_train[j])
        #         self.Gram[j][i] = self.Gram[i][j]
        self.Gram = np.dot(X_train,X_train.T)
        print(self.Gram)


    """
        sign函数的功能是返回超平面S
        将w转化成 1~N个aj*xj*yj累加来计算，但是不要单独计算w，因为计算w后需要和xi求内积，出现重复计算，
        所以使用Gram矩阵，w·xi同时计算，减少计算耗时。
    """
    def sign(self,a,Y_train,i,b):
        w_x = 0
        for j in range(0,len(Y_train)):
            w_x += a[j] * Y_train[j] * self.Gram[i][j]

        print("w_x + b",w_x + b)
        return w_x + b

    def fitting(self,X_train,Y_train):
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

                if y * self.sign(self.a,Y_train,i,self.b) <= 0:
                    # print("y",y)
                    # print("真实类别:", y, end="---")
                    # print("sign(w·x + b)的值:", self.sign(self.a, X_train,Y_train,self.b,x), end="---")
                    wrong_count += 1
                    for i in range(0, len(X_train)):
                        self.w += np.dot(self.a[i], X_train[i]) * Y_train[i]

                    # 更新w，b
                    self.a[i] = self.a[i] + self.l_rate
                    self.b = self.b + self.l_rate * y

                    print("将w更新为:", self.w, end=' ')
                    print("将b更新为:", self.b)

            if wrong_count == 0:
                # 注意最后一趟a更新完后，需要更新w,w = sum{ai*xi*yi)*(x1,x2,x3)
                for i in range(0, len(X_train)):
                    self.w += np.dot(self.a[i], X_train[i]) * Y_train[i]
                is_wrong = False

if __name__ == "__main__":

    # 绘制iris数据的散点图(前50条数据是1类，50~100数据为2类）
    plt.scatter(X[:50,0],X[:50,1],color='blue')
    plt.scatter(X[50:100,0], X[50:100, 1], color='orange')

    """
    采用学习算法的原始形式，得到感知机模型的w，b,将函数方程转化为一次函数
    """
    perception = Model1()
    perception.fitting(X,y)
    x_points = np.linspace(4,7,2)
    y_ = -(perception.b + perception.w[0] * x_points)/perception.w[1]
    plt.plot(x_points,y_,color='cyan',lw=2.0)
    plt.legend()
    plt.show()

    """
    采用学习算法的对偶形式，得到感知机模型的系数ai，b,将函数方程转化为一次函数
    """
    perception1 = Model2()
    perception1.fitting(X,y)
    x_points = np.linspace(4,7,2)
    y_ = -(perception1.b + perception1.w[0] * x_points)/perception1.w[1]
    plt.plot(x_points,y_,color='cyan',lw=2.0)
    plt.legend()
    plt.show()