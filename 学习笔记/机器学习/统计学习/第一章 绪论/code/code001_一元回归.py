import numpy as np;
from scipy.optimize import leastsq
import matplotlib.pyplot as plt;

# 目标函数sin(2πx)
def real_func(x):
    return np.sin(2*np.pi*x)

# 关于一个变量x的(次数依次递减）多项式函数
# p是一个多项式的系数列表，次数为M，系数个数为M+1
def fit_func(p,x):
    # np.poly1d的使用
    # >>> p = np.poly1d([1, 2, 3])
    # |  >>> print(np.poly1d(p))
    # |     2
    # |  1 x + 2 x + 3
    # |
    # |  Evaluate the polynomial at :math:`x = 0.5`:
    # |
    # |  >>> p(0.5)
    # |  4.25
    f = np.poly1d(p)
    return f(x)

# 经验风险(残差函数):预测值 - 真实值
def residual_func(p,x,y):
    return fit_func(p,x) - y

# 在residual_func经验风险的基础上，加上正则化项，变成结构风险
def residuals_func_regularization(p, x, y):

    regularization = 0.0001

    # 经验风险
    ret = residual_func(p,x,y)
    print("经验风险", ret)
    # 经验风险[0.31972216 - 0.28167978 - 0.64009235 - 0.23185228
    # 0.37735337
    # 1.20983082
    # 1.89436378
    # 2.78654483
    # 3.26961043
    # 3.81895049]

    # 结构风险
    ret = np.append(ret, np.sqrt(0.5*regularization*np.square(p))) # L2范数作为正则化项
    # print(len(ret)," ", len(np.sqrt(0.5*regularization*np.square(p))))
    # ret = ret + np.sqrt(0.5*regularization*np.square(p));
    print("结构风险", ret)
    # 结构风险[3.19722159e-01 - 2.81679783e-01 - 6.40092347e-01 - 2.31852279e-01
    # 3.77353372e-01
    # 1.20983082e+00
    # 1.89436378e+00
    # 2.78654483e+00
    # 3.26961043e+00
    # 3.81895049e+00
    # 4.97801504e-04
    # 8.94357277e-04
    # 2.55965917e-03
    # 6.09320893e-03
    # 5.60403167e-03
    # 3.88778337e-04
    # 5.08172080e-03
    # 2.28874924e-03
    # 2.16380642e-03
    # 2.23093071e-03]

    return ret


# 函数参数是：M=多项式次数，x=训练集（噪点）横坐标，y=训练集（噪点）纵坐标，func=最小二乘法中选择的策略函数
# 通过产生M+1个随机的，[0,1]内的系数列表
# 使用最小二乘法的策略来避免学习到的多项式过拟合于目标函数
# 返回值是最优参数列表
def fitting(M, x, y, func):

    # dn表示数组的维度
    # out: ndarray, shape
    # ``(d0, d1, ..., dn)``
    # Random values.
    # >> > np.random.rand(3, 2)
    # array([[0.14022471, 0.96360618],  # random
    #        [0.37601032, 0.25528411],  # random
    #        [0.49313049, 0.94909878]])  # random
    p_init = np.random.rand(M + 1)
    print("初始参数列表", p_init)

    # 最小二乘法得到最优的参数向量（多项式中的系数（权值）列表）
    # leastsq()第一个参数为模型选择的策略函数：损失函数，经验风险函数，结构风险函数
    # 这里使用residual_func()，或者residuals_func_regularization作为策略函数，目的是得到最优的p_init列表,
    # args=(x,y)为residual_func()剩余的参数
    # 注意第一个参数是函数名，不带()
    p_lsq = leastsq(func,p_init,args=(x,y))
    print('最优参数列表', p_lsq[0])

    return p_lsq[0]

if __name__ == '__main__':
    # 在[0,1]区间内产生10个真实点(x,y)
    x_points = np.linspace(0,1,10)
    y_points = real_func(x_points)

    # 将真实点加上正态分布噪音的目标函数的值，作为训练集，散点表示
    # 参数loc(float)：正态分布的均值，对应着这个分布的中心。loc=0说明这一个以Y轴为对称轴的正态分布，
    # 参数scale(float)：正态分布的标准差，对应分布的宽度，scale越大，正态分布的曲线越矮胖，scale越小，曲线越高瘦。
    # 参数size(int 或者整数元组)：输出的值赋在shape里，默认为None。
    y_points = [np.random.normal(0, 0.1) + y1 for y1 in y_points]
    plt.scatter(x_points, y_points, label="noise",color="blue")

    # 在[0,1]区间内产生1000个点，汇出光滑的目标函数曲线
    x = np.linspace(0,1,1000)
    y = real_func(x)
    plt.plot(x, y, label="real curve",color="red",lw=2.0)

    # 利用噪点来训练多项式
    # 1、利用最小二乘法得到最优的参数列表  print(fitting(3,x_points,y_points))
    # 2、将最优的参数列表，噪点x代入fit_func(p, x),得到最优的多项式，即最优的模型
    y_polyld = fit_func(fitting(3,x_points,y_points,residual_func),x)
    plt.plot(x, y_polyld, label="fitted curve", color="green",lw=2.0)

    #利用噪点，通过正则化
    y_polyld_reg = fit_func(fitting(3, x_points, y_points, residuals_func_regularization), x)
    plt.plot(x, y_polyld_reg, label="regulation curve", color="cyan", lw=2.0)

    # 把所有图例放在一起
    plt.legend()
    plt.show()



