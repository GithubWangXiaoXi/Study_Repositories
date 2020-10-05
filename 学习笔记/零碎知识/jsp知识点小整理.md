## jsp知识点小整理

​		由于好久之前学的jsp，现在已经基本忘了，但是老师要求我们用jsp做项目，我也没辙，只能一点点回顾这些知识点。

1、[JSP中如何导入JAVA包](https://zhidao.baidu.com/question/505228113.html)，这个不能用普通java项目那样的方式打包，IDEA的jsp页面虽然有显示包存在，但是在编译时会出错（当时我用的是fastjson.jar时出现了问题），主要方式是**把jar包复制到WEB-INF下的lib文件夹**。

2、**JSP表达式，EL表达式以及一些标签**，请参考这两个博客

- [JSP基础知识](https://blog.csdn.net/pengzhisen123/article/details/80366278)

- [JSP基本语法小结](https://www.cnblogs.com/yunqing/p/6186583.html)

3、jsp和js在一起使用过程中，难免会互相取值的问题，但是由于jsp引擎在执行过程中，先是执行java，**将jsp变成servlet**，后再执行js，**使得js可以获得java的值，但是java获取不到js的值**。（那时我是想通过js获取后台传过来的值，然后通过dom，来给jsp页面上添加多个表单的js效果）

参考[jsp代码和js代码执行的顺序](https://www.cnblogs.com/qingxinblog/articles/3370520.html)

4、js获取java数组（先将**java数组转换成json字符串**，js才能获取，否则js获取的数组为`undefined`）

```jsp
<%
DataSet curds=list.get(list.size()-1);
		inputdata.setdata(curds.getData(),		//用备选数据集中的指定数据替换掉当前数据
		 			curds.getSetname(),
		 			curds.getColname(),
		  			curds.getPercent(),
					curds.getSetinfo());

	String featureName =  JSON.toJSONString(curds.getColname());  //fastjson将字符串数组转换成json
	System.out.println(featureName);
%>

<script type="text/javascript">

	//将java数组转化成json，可和js进行类型转换
    var featureName = <%= featureName%>;  //不知道为啥子不能用el表达式，只能用jsp表达式
</script>
```

