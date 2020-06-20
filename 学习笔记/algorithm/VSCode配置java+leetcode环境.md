## VSCode配置基于java + LeetCode环境

#### 一、VSCode安装

​	在此处https://code.visualstudio.com/安装，安装后点击VSCodeSetUp.exe，一路安装即可，注意勾选上path自动配置（默认是勾选的）。

#### 二、VSCode配置java环境

##### 1、VSCode汉化 & 颜色主题 & 字体设置

- **VSCode汉化**

![1](\vscode\1.jpg)

- **颜色主题**

  我喜欢使用亮一点的颜色，黑色主题盯久了容易犯困。。。。

![15](\vscode\15.jpg)

![16](\vscode\16.jpg)

- **字体设置**

  在setting.json中配置 **"editor.mouseWheelZoom": true**，就可以用鼠标滚动调整字体大小

![19](E:\java面试\Study_Repositories\学习笔记\algorithm\vscode\19.gif)

##### 2、配置VSCode的java基础环境

​	安装jdk步骤这里就省了，网上资源挺多，这里只关注一下VSCode的setting.json文件中java home的配置。

![3](\vscode\9.jpg)

![3](\vscode\10.jpg)

![3](\vscode\11.jpg)

##### 3、安装java扩展插件

​	安装该插件，及**一次性安装**如下6个java扩展插件

![3](\vscode\3.jpg)

##### 4、运行一波

​	先写一个HelloWorld.java文件，注意此时工作区中还没有launch.json文件

![4](\vscode\4.jpg)

​	再点击“小昆虫“，创建launch.json文件，**这时工作区中有了.vscode文件夹和launch.json文件**。

![5](\vscode\5.jpg)

![6](\vscode\6.jpg)

​	此时运行文件，会提示报错：`No delegateCommandHandler for vscode.java.resolveMainMethod`，怎么办？重启VSCode即可，参照该文档 <http://gochannel.org/links/link/snapshot/12049>，所以在VSCode中，**一旦修改了配置文件，建议重启。**

![7](\vscode\7.jpg)

​	重启之后的样子。。。

![08](\vscode\8.jpg)

**5、调试一波**

![17](\vscode\17.jpg)

##### 6、备注：

- 注意创建的是java文件，不是class文件，java文件需要编译成class文件，不要把IDEA中Class类误认为是class文件。
- 如果写代码时没有提示，检查“Language support for Java ™ for Visual Studio Code”是否启用，setting.json配置文件是否格式正确

#### 三、VSCode配置LeetCode环境

##### 1、安装leetcode插件

​	安装leetcode插件，安装成功后，左边有小图标

![08](\vscode\12.jpg)

##### 2、登录帐号

​	登录国外的leetCode可能会连不上，修改挂载点，使用国内LeetCode。

![08](\vscode\13.jpg)

##### ![14](\vscode\14.jpg)	

##### 3、开始答题

![18](\vscode\18.gif)