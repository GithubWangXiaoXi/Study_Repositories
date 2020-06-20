## Spring Boot与Kubernetes云原生微服务实践

### 一、课程介绍和案例需求

#### Ⅰ、课程目标和主要内容 

##### **1、Dev**（编码）

![1](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\1.jpg)

##### **2、OPS**（运维）

![2](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\2.jpg)

##### 3、备注

- **SaaS应用**是当前行业创新的热点
- 大学生在大学项目开发中，与企业级开发脱节，**对可运维性没有严格要求，对生产级，可运维架构理念理解不足**（监控，报警，部署等）
- **软件工程流程**（传统 -》 敏捷 -》云时代）
- **Dev-Ops研发运维一体化**很重要



#### Ⅱ、课程案例需求

##### 1、Staffjoy公司背景

![3](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\3.jpg)

##### 2、功能和非功能需求

![4](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\4.jpg)

##### 3、界面展示

![5](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\5.jpg)

![6](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\6.jpg)

![7](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\7.jpg)

![8](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\8.jpg)

##### 4、课程先决条件

![9](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\9.jpg)

##### 5、额外说明

![10](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\10.jpg)

![11](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\11.jpg)

### 二、系统架构设计和技术栈选型

#### Ⅰ、架构选择

##### 1、为什么用微服务架构

![12](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\12.jpg)

![13](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\13.jpg)

**备注：**

- 微服务可以更高层度的**抽象管理软件的复杂性**
- 易于开发更加复杂的系统，**应对不同的需求**。



##### 2、staffjoy的架构设计思想

![14](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\14.jpg)

**备注：**

- 分而治之
- 单一职责
- 关注分离

##### 3、技术栈选型

![15](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\15.jpg)

##### 4、SaaS多租户设计

![16](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\16.jpg)

#### Ⅱ、数据和接口模型设计

##### 1、账户数据模型和接口设计

**账户数据模型**

![17](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\17.jpg)

**账户接口**

![18](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\18.jpg)

##### 2、公司数据模型和接口设计

**公司数据模型**

![19](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\19.jpg)

![20](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\20.jpg)

**公司接口**

![21](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\21.jpg)

##### 3、admin接口

![22](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\22.jpg)

##### 4、团队Team接口

![23](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\23.jpg)

##### 5、雇员worker接口

![24](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\24.jpg)

##### 6、任务Job接口

![25](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\25.jpg)

##### 7、班次Shift接口

![26](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\26.jpg)

#### Ⅲ、Dubbo、Spring Cloud和Kubernetes如何选择

![27](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\27.jpg)

![28](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\28.jpg)

![29](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\29.jpg)

![30](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\30.jpg)

**备注：**

- kubernetes是**完整的基础设施解决方案**，而dubbo，springcloud是部分基础设施的解决方案
- Kubernetes**偏DevOps和运维，技术门槛高**
- Dubbo好比平台机，开箱即用，**一般不用替换里面的组件**。
- Spring Cloud好比组装机，可灵活替换扩展。
- **不建议混搭**，两者体系不一致（及spring cloud混搭dubbo等，如果混搭，有些技术栈的服务需要退化）

#### Ⅳ、技术中台

![31](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\31.jpg)

![32](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\32.jpg)

![33](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\33.jpg)

![34](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\34.jpg)

**备注：**

- **中台和前台、后台对应**，指的是在一些系统中，**被共用的中间件的集合**。


- **中台架构具有通用性**的，互联网公司发展到一定阶段都会呈现出这样类似的架构

- staffjoy的**技术中台是构建在第三方的公有设施服务之上**，而不是自己接底层的基础设施平台

  ​

### 三、服务开发框架设计和实践

#### Ⅰ、staffjoy项目组织

![35](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\35.jpg)

**备注：**

- staffjoy虽然采用微服务，但是所**有代码都在一个仓库中**，这种结构组织是**单体仓库**。
- 多个spring项目以module进行组织
- 父pom规定了整个项目的依赖，每个模块**优先使用父pom的依赖**，**再根据需要引入自己定制的模块的依赖**。
- 每个模块都有**接口模块**和**接口实现模块**。
- 私密数据（阿里云连接，SWT安全等）放在**config模块**中。
- **frontend为前端模块**应用。

#### Ⅱ、谷歌为什么采用单体仓库（Mono-Repo）

![36](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\36.jpg)

备注：

- **多仓库**的问题：职责单一，**但项目代码不容易规范**，开发人员不能对整体项目有个整体的认知等。
- **单体仓库**：不用集中管理，**方便一键部署**和code review，**但业务越复杂，单体仓库的项目也越复杂**。

![37](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\37.jpg)

#### Ⅲ、微服务接口参数校验

![38](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\38.jpg)

![39](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\39.jpg)

**备注：**

- **微服务接口参数校验**十分重要！！！


- **@min(0)**：接口参数最小值不能为0

- **@NotBlank**：接口参数不能为空

- 如何**自定义标注**：**先建标注，再建标注的实现**。（在common-lib中）

  如何实现，请查看参考文档：

  [自定义注解实现接口参数校验](https://www.baidu.com/link?url=Mjz3owZIkO6mPcYSSXpPvMNtqKXnlUS0c-zD2luOfq__F_qpgCp1FAZEOMBPbZpY_Vq3B-hhErma3hFRJ21PcVGOhI6DeOKL385lB-8UTUm&wd=&eqid=94443a88003ef637000000065e8b3d3f)

  [使用自定义注解实现接口参数校验](https://blog.csdn.net/qq_24629159/article/details/86568104)

  ![40](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\40.jpg)

![42](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\42.jpg)

![41](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\41.jpg)

#### Ⅳ、如何实现统一异常和错误处理

##### 1、RestFul统一异常处理

![43](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\43.jpg)

![44](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\44.jpg)

![45](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\45.jpg)

![46](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\46.jpg)

![47](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\47.jpg)

**备注：**

- **GlobalException**进行**统一的RestFul异常处理**
- **所有的捕获信息被封装成BaseResponse**，以**json数据**进行返回（return BaseResponse）。

##### 2、SpringMVC统一错误处理

![49](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\49.jpg)

![48](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\48.jpg)

![50](E:\java面试\Study_Repositories\images\springboot\springboot和kubernetes云原生微服务实践\50.jpg)

备注：

- spring MVC**通过获取错误码和异常（statusCode，exception），配置统一的错误页面进行展示**（是page Not Found页面还是Internal Server Error页面）

