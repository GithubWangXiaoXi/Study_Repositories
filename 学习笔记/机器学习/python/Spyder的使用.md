### Spyder的使用

#### 备注：

##### 1、代码编写方面

- 使用了spyder学习一段时间的机器学习，我爱上了它的**逐行解析（不用print，就能输出变量）**。

  其实jupyter notebook也行，**但我更喜欢spyder**，而且**变量可视化更清晰**

- 但是**spyder的诟病是代码提示问题**，如果没有导入文件中的module，就无法代码提示。eg：**`DataFrame.groupby()`有提示**，但是如果是通过`read_csv()`将读取的数据转化成DataFrame对象，并取名为df后，**`df.groupby()`没有提示**

- pycharm在导入项目文件时，会像IDEA一样，产生一个`.idea`文件夹

  而spyder导入项目时会产生`.ipynb_checkpoints`和`.spyproject`项目文件夹

  这**两个IDE可以同时打开同一个项目**，这样spyder的缺点可以用pycharm来弥补

- **用pycharm(社区版)编程，用spyder逐行运行调试代码**（如果在spyder中写代码，注意`ctrl+s`保存文件，pycharm才可看到，而对于pycharm，则是实时保存文件的）

##### 2、帮助文档方面（第三方库）

- 首先采用spyder的可视化help文档
- 其次，如果出现`No documentation available`，优先使用`help()`函数
- 最后使用[zeal离线文档](https://blog.csdn.net/qq_33934427/article/details/107454461)

#### 以下是spyder的一些使用说明：

##### 1、注释

行注释：快捷键`ctrl + 1`

块注释：快捷键`ctrl + 4`

##### 2、代码提示（×）

- 快捷键：`Tab`。
- 但有些时候，如果这些module不在\Lib\site-packages\spyder\utils\introspection路径下的**module_completion.py**文件，spyder是不会给出提示的。<https://blog.csdn.net/ZMT1849101245/article/details/79034729>
- 尝试了很多方法，比如
  - 修改preference中的Ipython console -> 无效；
  - 通过升级conda，进而升级spyder3到spyder4，但是conda升级太卡了，[换了镜像](https://blog.csdn.net/mywmy/article/details/96994065)也卡。<https://www.cnblogs.com/pyme/p/12816754.html>

##### 3、运行代码

- 快捷键`ctrl + enter`，可以运行一个语句中某个代码片段

- 可以像jupiter notebook一样**运行指定的代码片段**。但是当变量值被修改时，需要**运行变量值被修改的语句**，否则变量值仍然是旧值

##### 4、清缓存

运行指定行的代码之前，注意**清除控制台缓存变量**，否则打印输出和自己设想的不一致（看Variable explorer中的数据）：

- 法1：在console中输入：`reset`，得到提示输入y确认即可
- 法2：在控制台输入`clear`即可，或者快捷键`ctrl + L`

##### 5、格式化代码

pep8时python代码样式规范

- **安装autopep8**：打开anaconda prompt，输入

  `pip install --upgrade autopep8`，如果安装不了，更换pip镜像

- **安装spyder的autopep8插件**：github网址<https://github.com/spyder-ide/spyder-autopep8#readme>

- 解压包，然后将文件包中的**spyder_autopep8文件夹**复制至spyder.exe的目录下，我的spyder地址如下：`D:\programmingSoftware\Anaconda\Anaconda\Scripts`

  ![](https://img-blog.csdnimg.cn/20191124180858496.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzQxNjY2OTg3,size_16,color_FFFFFF,t_70)

参考文档

[spyder安装autopep8插件:自动代码排版](https://blog.csdn.net/weixin_44321080/article/details/103494592)

[如何让spyder编写的代码自动格式化](https://blog.csdn.net/qq_41666987/article/details/103226754)

##### 6、查看函数的帮助文档（×）

- 快捷键`Ctrl+I` 

- 但是有些时候查出的结果是`No documentation available`，举个栗子：

  ```python
  from pandas import read_csv
  df = read_csv(open('E://python//数据集//数据分析入门//1.csv'))
  
  from pandas import DataFrame
  #1) Ctrl+I可查help文档 
  DataFrame.to_csv()
  #2) Ctrl+I不可查help文档， 结果是`No documentation available`
  df.to_csv(
          'E://python//数据集//数据分析入门//2.csv'
          #不打印索引列
          index=False
  )
  df1 = DataFrame(df)
#3) Ctrl+I可查help文档 
  df1.to_csv(...)
  ```
  
  我猜测原因是`read_csv`返回值为`DataFrame or TextParser`，所以`df.to_csv`不知道是`DataFrame`还是`TextParser`的方法，如果不`import DataFrame`，无法查看其help文档
  
- 如果出现`No documentation available`，优先使用`help()`函数，其次使用[zeal离线文档](https://blog.csdn.net/qq_33934427/article/details/107454461)

