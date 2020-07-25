### Python基础语法（待更新）

##### 一、输入输出

###### 1、基本输入输出

```python
a1 = input("input:")
print("a1=",a1,end='')
print(" b1:上面的老弟，别换行")
```

###### 2、文件输出和读取

```python
#2.1 文件输出
file1 = open("data.txt","w")
print("hello python",file=file1)
file1.close() #注意需要关闭文件后，才能读取到文件里的内容
 
#2.2 文件读取
#2.2.1 txt文件读取
print(open("data.txt").read())
#2.2.2 csv文件读取
print(open("iris.csv").read())
```

##### 二、运算

###### 1、算术运算符

```python
#1.1 整除
a2 = 12 / 5
b2 = 12 // 5
print("a2=",a2,",b2=",b2)
 
#1.2 求余
a2_1 = 12 % -7 # 12 - （-2 * -7） = -2
b2_1 = 12 % 7
print("a2_1=",a2_1,end=" ")
print(",b2_1=",b2_1) #注意两个结果是不同的，在C/Java中的输出结果都是5，而Python输出的结果分别是-2,5
```

###### 2、关系运算符

```python
print("布尔值True是否等于1:",True == 1)
print("布尔值True是否是int类型的实例:",isinstance(True,int))
print("布尔值True和1是否是同一个对象:",True is 1)
```

###### 3、逻辑运算符

```python
a2_3 = True or False
b2_3 = True and False
c2_3 = not False
print("True or False:",a2_3)
print("True and False:",b2_3)
print("not False:",c2_3)
```

###### 4、类型转换

```python
#4.1 字符串转整型
a2_4 = "11"
print("十进制:",int(a2_4,10),",二进制:",int(a2_4,2)) #把字符串看成是十进制或者二进制的形式，输出结果为十进制
 
#4.2 整型转字符串
b2_4 = str(11)
print("b2_4的类型:",type(b2_4))
 
#4.3 类型转换报错
b2_4 = "11.0"
print(int(b2_4))
c2_4 = "11abc"
print(int(c2_4))
```

##### 三、基本语句

###### 1、条件语句

```python
a3_1 = input("input a3_1:") #注意输入的是一个字符串，想对变量进行运算时，需要进行类型转换
a3_1 = int(a3_1)
if a3_1 == 10:
	print("Bingo")
	elif a3_1 < 10:
		print("less")
	else:
		print("more")
```

###### 2、循环语句

- **for循环**

```python
#3.2.1 for循环
for i in range(0,3): #如果第一个参数没写，默认从0开始取数，依次递增，数的个数为3
	print(i,end=" ")
 
set1 = {1, 2, 4}
for i in set1: #从集合中取数（不单单是集合，元组，列表都行）,相当于java的for(Integer i : set1){}
	print(i,end=" ") 
```

- **while循环**

```python
#3.2.2 while循环
index3 = 0
while index3 < 5:
index3 += 1
print(index3,end=" ")
print()
```

##### 四、函数使用

###### 1、自定义函数和函数调用

```python
def add(a,b):
return a+b
 
result = add(10,20)
print("10+20=",result)
```

###### 2、常见函数的使用

```python
import math as m
a4_2 = 10
#特殊
print("10*2+1:",eval("a4_2 * 2 + 1"))
print("1,2,3,4中最大值为:",max(1,2,3,4))
#常见
print("-5取绝对值:",m.fabs(-5))
print("-5.5取向上取整:",m.ceil(-5.5))
print("-5.5取向下取整:",m.floor(-5.5))
```

##### 五、数据结构

###### 1、集合

```python
#5.1 集合（元素唯一且不可以修改，但可以添加，删除元素。对于可变对象（集合，字典，列表），不能加入(add)到集合当中）
set5 = {1,2,2}
#集合的复制
set5_1 = set5.copy()
#加入一个元素，该元素不能是可变类型的
set5.add("abc")
#一次性加入多个对象
set5.update({"aaa","1.8"})
#如果集合中没有该元素，则会抛出异常
set5.remove("1.8")
 
print("集合a:",set5)
print("集合b:",set5_1)
```

###### 2、列表

```python
#5.2 列表(还有复制copy，对字符串，数字排序sort)
list5 = [1,2]
#添加一个元素
list5.append("3")
#添加多个元素
list5.extend([4,5])
#在指定位置插入元素（index从0开始）
list5.insert(1,"1.5")
print("list:",list5)
#指定位置删除元素
del list5[0:2]
print("从第一个元素开始删除2个后的list:",list5)
```

###### 3、元组

```python
#5.3 元组(大小不能改变，不能进行添加，删除操作)
tuple5 = ("length","width","weight","height")
print("tuple5:",tuple5)
```

###### 4、字典

```python
#5.4 字典(括号和集合的一样，但是元素不同，是键值对的方式)
dict5 = {"height":170,"weight":65}
print("dict5:",dict5)
print("dict5 keys:",dict5.keys())
print("dict5 values:",dict5.values())
```

##### 六、其他零碎知识点

```python
#6.1 计算程序运行时间
def func():
for i in range(10000):
None
  
import time
start = time.time()
func()
end = time.time()
print("func函数运行时间:",end-start)
 
#6.2 随机数
import random
#输出0~9的随机整数
print(random.randint(0,9))
 
```

