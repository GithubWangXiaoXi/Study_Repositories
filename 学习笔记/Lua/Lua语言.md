## Lua语言

### 一、Lua语言的应用场景

先看一看lua的创始人们是怎么说的吧  

**如何定义 Lua ？**

- Luiz：lua是一种可嵌入，轻量，快速，功能强大的脚本语言
- Lua 是一种脚本语言，这种语言通常用来控制其它语言编写的其他组件

**在使用lua注意什么？**

- luiz：我想应该是用lua的方式做事。不建议去模拟出所有你在其他语言中用到的东西。你应该真的去用这个语言提供的特性。
- 就lua来讲，语言的特性主要指用**table**表示所有的东西，用**metamathod**做出优雅的解决方案。

**lua的用户是哪些人？**

- 应用程序设计者应该从一开始就考虑脚本，这会带来更多的灵活性，把握性能问题
- 性能不太重要之处，就交给脚本处理，开发周期短，速度快。

更多采访请参照该文档 [云风的 BLOG: 采访 Lua 发明人的一篇文章](https://blog.codingnow.com/2010/06/masterminds_of_programming_7_lua.html)



### 二、Lua的安装，配置与运行

请参照该文档  [Lua在Windows下的安装、配置、运行](https://blog.csdn.net/ChinarCSDN/article/details/78667262)

当然用一个顺手的IDE方便的lua代码的编写，这里我是用IDEA（社区版，最终版都行）

1、先在IDEA中安装Lua语言提示插件（这里我已经安装好了）

![1](E:\java面试\Study_Repositories\images\lua\1.jpg)



2、安装Lua二进制包（我是在window运行的）

![2](E:\java面试\Study_Repositories\images\lua\2.jpg)



3、配置IDEA进行运行调试：指定lua.exe解释器的位置，和运行调试文件的位置

![3](E:\java面试\Study_Repositories\images\lua\3.jpg)



运行效果

![4](E:\java面试\Study_Repositories\images\lua\4.jpg)



### 三、Lua基本概念

#### 1、值与类型

​	lua是动态类型的语言，所以变量没有类型，只有值才有类型。lua语言没有类型的定义，所有的值都有它们各自的类型。

​	Lua中有8个基本类型：*nil*, *boolean*, *number*, *string*, *function*, *userdata*, *thread*, and *table*。

- **nil：** 代表该值是否有效存在；nil可作为条件判断中的false
- **boolean：** false / true作为条件判断
- **number：** 可以是整型，也可以是浮点型数
- **string：**
  - 不可变的字节序列；
  - 可以存放 8bit 的值，包括'\0'；
  - 无需指定String的编码格式
- **function：**  lua可以回调或者操纵lua或C写的方法
- **userdata： ** 
  - full userdata是由lua管理的存储块的对象；
  - light userdata是简单的C指针的值；
  - 通过metatables可以为full userdata的值定义操作；
  - userdata的值不能被创建，也不能被修改，只能通过C的API调用。
- **thread：**
  - thread是独立的可执行线程，它常用来实现多线程编程
  - Lua的thread不依赖于操作系统的thread，
  - Lua的多线程可以支持所有操作系统，即使该系统不支持原生的线程。
- **table：**
  - table实现了综合性的数组，该数组（有索引）不仅可以存数值（numbers），还可以存除了nil和NaN的任何Lua值

**备注：**

-  标准的Lua采用64位integer，和64位双精度的float；而小型机器和嵌入式系统需要32位的integer和32位的单精度float

- table，functions，threads，和full userdata的值是对象，变量不能直接存储这些值，只能引用它们。在赋值，传参以及函数返回时，都是操作这些值的引用，不会复制这些值。

  ​

#### 2、环境和全局环境

#### 3、错误处理

#### 4、元表格和元方法

#### 5、垃圾收集

- 垃圾收集的元方法
- 虚表格

#### 6、多线程编程





### 四、Lua语法

#### 1、数据类型

- 整型：十进制，十六进制（以"`0x` or `0X`"为开头）
- 浮点型：

```lua
a = 0xf
print(a,"type",type(a))

a = 123
print(a,"type",type(a))

a = 34e1
print(a,"type",type(a))

a = 314.16e-2
print(a,"type",type(a))

a = 0x0.1E
print(a,"type",type(a))

---
输出结果
15	type	number
123	type	number
340.0	type	number
3.1416	type	number
0.1171875	type	number
162.1875	type	number
```

#### 2、变量

- Lua有三种类型的变量：全局变量，局部变量和表中的域

  ```lua
  a = 5
  function test()
      local b = 10
  end

  print("a=",a,"b=",b)

  ----
  输出结果
  a=	5	b=	nil
  ```

  ​



#### 3、字符串

- 字符串主要有三种表示方式：‘xxx’，"xxx"，[[xxx]]，[==[xxx]==]  ...

- 以`--`开头的字符串表示文本

- 转译字符

  - '`\a`' (bell)，
  - '`\b`' (backspace),
  -  '`\f`' (form feed), 
  - '`\n`' (newline), 
  - '`\r`' (carriage return), 
  - '`\t`' (horizontal tab),
  -  '`\v`' (vertical tab),
  -  '`\\`' (backslash),
  -  '`\"`' (quotation mark [double quote]),
  - '`\'`' (apostrophe [single quote]). 

- 以下5个string意味着同一个string

  ```lua
  a = 'alo\n123"'
  a = "alo\n123\""
  a = '\97lo\10\04923"'
  a = [[alo
  123"]]
  a = [==[
  alo
  123"]==]
  a = [[alo
  	123"]]


  ---
  输出结果(以后三个为例)
  alo
  123"	
  	---------------
  alo
  123"	
  	---------------
  alo
  	123"	
  	---------------
  ```

  备注：

  - [[xxx]]在使用时**不会忽略空格和换行**，[[xxx]]内部的格式即为打印输出的格式



#### 4、 表达式

##### 1）块（chunks）

- lua的块可作为可变数量参数的匿名的方法
- 为了避免语句歧义，句末加‘’ ; ‘’
- 块内可定义局部变量，接收参数，返回值
- 块内若要引用外部变量，使用_ENV方法
- 表达式（stat）的写法：
  - `stat ::= do block end`
  - `chunk ::= block`

```lua
a = 5;
do
    a = 6
end
print(a);

do
    _ENV.a = 7
end
print(a);

------
输出结果
6
7
```



##### 2）赋值

- lua支持多种赋值
- lua原地交换值

```lua
x = 2;
y = 3;
z = 4
x, y, z = y, z, x

print(x,y,z)

---
输出结果
3	4	2
```



##### 3）控制结构

- 注意**nil，false**在表达式中视为**false**；
- **不同于nil，false**的值在表达式中都视为**true** ,(即使是**数字0还是空串都表示true**)
- while：`stat ::= while exp do block end`
- repeat： `stat ::= repeat block until exp`
- if： `stat ::= if exp then block {elseif exp then block} [else block] end`
- break：`stat ::= break`
- return：`stat ::= return [explist][‘;’]`

###### if

```lua
a = 0;
if(a < 5) then
    print("if");
    a = a + 1;
elseif a < 3 then
    print("elseif");
end

----
输出结果
if
```



###### while

```lua
a = 0;
while(a < 5) do
    print(a)
    a = a + 1;
end

----
输出结果
0
1
2
3
4
```



###### repeat

```lua
a = 0;
repeat
    print(a)
    a = a + 1;
until(a >= 5)   ---除非a >= 5才跳出循环

----
输出结果
0
1
2
3
4
```



##### 4）迭代器

###### for

- `stat ::= for Name ‘=’ exp ‘,’ exp [‘,’ exp] do block end`

- ` for var_1, ···, var_n in explist do block end`

  其中的explist的值是第一个迭代器变量中的迭代函数，状态和初始值。

- `for i,v in ipairs(t) do body end` ，Lua 默认提供的**迭代函数 ipairs**

```lua
for a,b,c  in ipairs({"a","b",5,9,16}) do
    print(a,b);  ---索引和值
    print(c);  ---多出的值为nil
end
---
输出结果
1	a
nil
2	b
nil
3	5
nil
4	9
nil
5	16
nil
```



#### 5、运算符

##### 1）算术运算符

- **+: **addition
- **-: **subtraction
- ***: **multiplication
- **/: **float division
- **//: **floor division
- **%: **modulo
- **^: **exponentiation
- **-: **unary minus

##### 2）位运算符

- **&: **bitwise AND

- **|: **bitwise OR

- **~: **bitwise exclusive OR

- **>>: **right shift

- **<<: **left shift

- **~: **unary bitwise NOT

  ​

##### 3）关系运算符

- **==: **equality
- **~=: **inequality
- **<: **less than
- **>: **greater than
- **<=: **less or equal
- **>=: **greater or equal



##### 4）逻辑运算符

- lua的逻辑运算符只有`and`，`or`,`not`



##### 5）其他运算符

###### 长度运算符

- 如果t是一个序列，则`#t`返回该序列的长度
- 如果t是一个字符串，则`string.len`获取字符串的长度，也可以用`#t`

```lua
arrays = {"a","b",5,9,16};
print("length",#arrays)

str = "helloWangxiaoxi"
print(string.len(str));
print(#str);
---
输出结果
length	5
15
15
```



#### 6、函数

##### 1）函数定义

```lua
function f(a, b) end
function g(a, b, ...) end
```

##### 2）返回多值

```lua
function r()
    ---返回多值
    return 1,2,3
end

a,b,c = r();
print(a,b,c);

---
输出结果
1  2  3
```

##### 3）可变参数

​	举个例子，考虑以下函数定义

```lua
function f(a, b) end
function g(a, b, ...) end
function r() return 1,2,3 end
```

​	则在调用函数时，映射的参数实际为：

```lua
CALL            PARAMETERS
     
f(3)             a=3, b=nil
f(3, 4)          a=3, b=4
f(3, 4, 5)       a=3, b=4
f(r(), 10)       a=1, b=10
f(r())           a=1, b=2

g(3)             a=3, b=nil, ... -->  (nothing)
g(3, 4)          a=3, b=4,   ... -->  (nothing)
g(3, 4, 5, 8)    a=3, b=4,   ... -->  5  8
g(5, r())        a=5, b=1,   ... -->  2  3
```

```lua
function f(a, b)
    print(a,b);
end
function g(a,b,...)
    print(a,b,...);
end
function r()
    ---返回多值
    return 1,2,3
end

f(r(),10);
g(5,r());

---
输出结果
1	10
5	1	2	3
```

**备注：**

- `...`表示多参数

##### 4）可见原则

```lua
 x = 10                -- global variable
do                    -- new block
  local x = x         -- new 'x', with value 10
  print(x)            --> 10
  x = x+1
  do                  -- another block
    local x = x+1     -- another 'x'
    print(x)          --> 12
  end
  print(x)            --> 11
end
print(x)              --> 10  (the global one)

---
输出结果
10
12
11
10
```



