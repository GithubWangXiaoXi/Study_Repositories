## Postman的使用

请参考postman [官方文档](https://learning.postman.com/docs/postman/launching-postman/introduction/) 进行学习

### 一、postman的安装

**https://learning.postman.com/docs/postman/launching-postman/installation-and-updates/**

### 二、接口测试

#### 1、什么是接口测试

​	接口测试就是针**对软件对外提供服务的接口的输入输出**进行测试，以及接口间相互逻辑的测试，验证接口功能与接口描述文档的一致性。

​	接口请求部分包括：**URL，方法，头域，参数**

![5](E:\java面试\Study_Repositories\学习笔记\postman\5.jpg)

#### 2、为什么做接口测试

​	接口测试通常能够对系统测试得更为彻底，**越早越底层的发现问题，修改和维护的代价也越小**。从分层测试角度来说，接口测试是相对来说性价比最高。常见的接口测试工具很多，比如：jmeter、soapui、postman等

#### 3、如何做接口测试

- **获取接口信息**：通过**接口文档和抓包**（F12 + network，对浏览器动作进行抓包）来获取接口的基本调用方式和返回
- **接口测试用例设计**：根据获取到的接口信息，按照接口测试用例设计方法，**设计参数和预期返回结果**。
- 接口发包：使用工具或者编程**向接口传递参数**。
- 根据接口文档设计用例，**调用接口，验证结果**。

#### 4、接口收发包

​	以postman接口请求和响应为例

- postman接口请求过程：

  | web      | 快递     |
  | -------- | ------ |
  | 填写接口URL  | 获取对方地址 |
  | 设置HTTP方法 | 选择快递公司 |
  | 设置请求头域   | 填写快递单  |
  | 填写请求参数   | 寄送物品打包 |

- postman接口响应验证

  | web     | 快递       |
  | ------- | -------- |
  | HTTP状态码 | 是否成功收到回件 |
  | 收到接口响应  | 获取返回     |
  | 检查头域    | 检查快递单    |
  | 查看主体内容  | 拆快递查看内容  |


### 三、postman的基本使用

#### 1、简单入门

##### 1）发送第一个请求

​	使用**New** > **Request**来创建请求，还可以设置该请求的**Collections**每个API请求用到HTTP方法。最常用的方法有 `GET`, `POST`, `PATCH`, `PUT`, 和 `DELETE` 。

- `GET` 方法用来获取API接口返回的数据。
- `POST`发送新数据给API接口。
- `PATCH` 和 `PUT` 方法更新已存在的数据。
- `DELETE` 删除已存在的数据。

这里用 http://postman-echo.com/get的API接口来测试`GET`请求

**备注：**

- 左边栏：**History** and **Collections** 。
- 可以使用**Collections**来管理api接口请求的测试 

![8](E:\java面试\Study_Repositories\学习笔记\postman\8.jpg)

##### 2）参数排列组合

​	通过对参数进行排列组合，**判断哪些参数是必须写的**，从而来设计测试用例

![3](E:\java面试\Study_Repositories\学习笔记\postman\3.jpg)

#### 2、基本属性

##### 1）普通的request请求

- **添加一个request**：需要`URL`，`method`和其他`可选值`（参数或者身份验证）
- **url的构成：** 在`https://api-test-fun.glitch.me/info`中，`https://api-test-fun.glitch.me`是基本URL，而`/info`是挂载路径（endpoint path）。
- **request发送参数：** URL后使用`?`进行衔接，不同参数用`&`分开，例如`?id=1&type=new`。

如果你的请求**无需主体内容(body)，身份验证(auth)或者头域(header)**，则直接发送测试即可，如果需要，则再考虑设置以下属性

- **request的body：** 发送不同类型的，适应API接口的主体数据。这时需要**设置正确的头域**，保证发送的数据可以由API来处理。为request body选择需要的data type（请求体可以为[form data](https://learning.postman.com/docs/postman/sending-api-requests/requests/#form-data), [URL-encoded](https://learning.postman.com/docs/postman/sending-api-requests/requests/#url-encoded), [raw](https://learning.postman.com/docs/postman/sending-api-requests/requests/#raw-data), [binary](https://learning.postman.com/docs/postman/sending-api-requests/requests/#binary-data), 或[GraphQL](https://learning.postman.com/docs/postman/sending-api-requests/requests/#graphql)）

  ![7](E:\java面试\Study_Repositories\学习笔记\postman\7.jpg)

  - **form data表单数据**：支持发送键值对；content type使用`multipart/form-data`;支持文件上传；不支持多个文件上传。
  - **URL-encoded：**使用`x-www-form-urlencoded` ，当你在发送请求填写键值对时，postman会在发送之前**对参数编码**。
  - raw，binary，GraphQL就详见文档吧

##### 2）带cookie的request请求

​	有些时候，request请求需要登录帐号，获得Cookie后，才可以访问系统内部的页面。在postman请求中，需要在头域中加上cookie标识。

- 先在浏览器登录页面，然后F12 + 刷新，获取Cookie对应的SESSIONID值

  ![9](E:\java面试\Study_Repositories\学习笔记\postman\9.jpg)

- 在postman的header中添加cookie以及SESSIONID

  ![10](E:\java面试\Study_Repositories\学习笔记\postman\10.jpg)

### 四、参考文档

1、[postman简介及基本用法](https://www.cnblogs.com/imyalost/p/8480288.html)

2、https://www.bilibili.com/video/BV134411v7Sj