## 深入理解Spring

### 一、Spring概述

#### 1、Spring的历史背景

##### 1）J2EE和EJB的关系

- 其实**j2EE就是java的企业版**，与javaSE（标准版）有是有区别的，所以运行环境会有差异(简单点可以说，这是两组不同的接口)，我们一般所熟悉的**tomcat仅仅只实现了j2ee的一小部分规范**，它只是一个**serlvet的容器（Web）容器，它不能跑J2EE的程序**

- **EJB（Enterprise JavaBean）说到底也是种规范，它是j2EE下面的一个子分类（核心类）**，所以j2ee包含EJB，同时我们都可以说**JBOSS，Weblogic，WebSphere是J2EE容器**，也可以叫**EJB容器**。因为它们能跑EJB组件。那么什么是EJB组件呢？其实就是java写出来的一段程序被打包成EAR包，这个**EAR包放在某个EJB的容器的特定目录下**启动就可以跑了。类似于互联网公司经常**使用的WAR包（部署在tomcat上）**。

  参考链接  [J2EE和EJB有什么关系？](https://www.cnblogs.com/foohack/p/5952631.html)

##### 2）J2EE和JavaWeb的关系

- **j2EE和JavaWeb说的是两个层面**，javaee是指Java的企业级应用，可以说是**一个规范，包含jdbc，EJB，RMI，JavaIDL，XML，javaMail，servlet，jsp，jndi，jms框架**，对象持久化等等组件，说白了就是用来开发服务器的程序

- **Javaweb**是指用**Java技术来解决相关web互联网领域**的**技术总和**，**其中就包含javaee的组件**。

  参考链接 https://bbs.csdn.net/topics/391906139?list=59366945

##### 3）JavaBean和POJO的区别

- POJO全称是Plain Ordinary Java Object / Pure Old Java Object，中文可以翻译成：**普通Java类，具有一部分getter/setter方法**的那种类就可以称作POJO。

- **JavaBean则比 POJO复杂很多**， Java Bean 是**可复用的组件**，对 Java Bean 并没有严格的规范，理论上讲，**任何一个 Java 类都可以是一个 Bean** 。

- **Java Bean 是不能被跨进程访问的**。

- 一般在web应用程序中建立一个**数据库的映射对象**时，我们只能称它为POJO。POJO(Plain Old Java Object)这个名字用来强调它是一个普通java对象，而不是一个特殊的对象，其主要**用来指代那些没有遵从特定的Java对象模型、约定或框架（如EJB）的Java对象**。

  参考链接 [POJO与javabean的区别](https://blog.csdn.net/u010923921/article/details/45484409)

##### 4）Spring解决的问题和演进

- 在诞生之初，创建Spring的主要目的是用来替代更加重量级的企业级Java技术，尤其是EJB。**相 对于EJB来说，Spring提供了更加轻量级和简单的编程模型**。它増强了简单老式Java对象(Plain Old Java object. POJO)的功能，使其具备了之前只有EJB和其他企业级Java规范才具有的功能。
- 随着时间的推移，**EJB以及Java 2**企业版(Java 2 Erterprise Edition. J2EE)在**不断演化**。**EJB**自身 也**提供了面向简单POJO的编程模型**。现在，**EJB也采用了依赖注入**(Dependency Injection. DI) 和**面向切面编程**(AspectOriented Programming. AOP)的理念，这毫无疑问是受到Spring成功的启发。
- 尽管J2EE（现在称之为JEE）能够赶上Spring的步伐，但Spring也没有停止前进。Spring继续在其 他领域发展，而JEE则刚刚开始涉及这些领域，或者还完全没有开始在这些领域的创新。**移动 开发、社交API集成、NoSQL数据库、云计算以及大数据都是Spring正在涉足和创新的领域**。 Spring的前景依然会很美好。





#### 3、Spring的好处

##### 1）方便解耦，简化Java开发

- Spring是为了解决企业级应用开发的复杂性而创建的。但Spring不仅仅局限于服务器端开发，**任何Java应用都能在简单性、可测试性和松耦合等 方面从Spring中获益**。


- 为了降低Java开发的开发的复杂性，Spring采取了以下4种关键策略:
  - 基于**POJO的轻量级**和**最小侵入性编程**； 
  - 通过**依赖注入**和面向接口实现**松耦合**；
  - 基于**切面**和惯例进行**声明式编程**； 
  - 通过**切面**和**模版减少**样板式代码。
- 通过**Spring提供的IoC容器**，用户可以**将对象之间的依 赖关系交由Spring进行控制**，避免硬编码所造成的过度程序耦合。有了 Spring，用户不必再为单实例模式类、属性文件解析等这些底层的需求编写代码，可以 更专注于上层的应用。

##### 2）AOP编程的支持

- 通过Spring提供的AOP功能，方便进行面向切面的编程， 很多不容易用传统OOP实现的功能可以通过AOP轻松应对。

##### 3）声明式事务的支持

- 在Spring中，用户可以从单调烦闷的事务管理代码中解脱 出来，通过声明的方式灵活地进行事务管理，提高开发效率和质量。

##### 4）方便程序的测试

- 可以用非容器依賴的編程方式进行几乎所有的测试工作。在 Spring里，测试不再是昂贵的操作，而是随手可做的事情。

##### 5）方便集成各种优秀框架

- Spring不排斥各种优秀的开源框架，相反，Spring可 以降低各种框架的使用难度。Spring提供了对各种优秀框架（如Struts、 Hibernate，Hessian，Quartz 等）的直接支持。

##### 6）降低Java EE API的使用难度

- Spring对很多难用的Java EE API （如JDBC、 JavaMail、远程调用等）提供了一个薄层封装，通过Spring的简易封装，这些 Java EE API的使用难度大大降低。 

##### 7）Spring的Java源码是经典的学习范例

- Spring的源码设计精妙、结构清晰、匠心独运， 处处体现着**大师对Java设计模式的灵活运用**及对Java技术的高深造诣。Spring 框架源码无疑是Java技术的最佳实践范例。如果想在短时间内迅速提高自己 的Java技术水平和应用开发水平，学习和研究Spring源码将会收到意想不到 的效果。



#### 4、Spring的体系结构

- **Spring的模块：**spring框架由20个不同的模块组成。

  ![8](E:\java面试\Study_Repositories\images\spring\8.jpg)


- **IoC和AOP是Spring所依赖的根本**。在此基础上，Spring整合了各种企业应用**开源框 架**和许多优秀的**第三方类库**，成为Java企业应用full-stack的开发框架。
- Spring框架的 精妙之处在于对于开发者拥有自由的选择权，Spring不会将自己的意志强加给开发者， 因为**针对某个领域的问题**，**Spring往往支持多种实现方案**。当希望选用不同的实现方案 时，Spring又能保证过渡的平滑性。

![1](E:\java面试\Study_Repositories\images\spring\1.jpg)

也可以将AOP中的instrumentation单独拆分出来：

![1](E:\java面试\Study_Repositories\images\spring\1_1.jpg)

- Spring的Instrumentation（[插桩](https://baike.baidu.com/item/Instrumentation/10402335?fr=aladdin)）模块提供了**为JVM添加代理(agent)的功能（JVM级别的AOP实现）**。具体来讲，它为Tomcat提供 了一个织入代理，能够为Tomcat传递类文件，就像这些文件是被类加载器加载的一样。参考该文档了解 [Instrumentation 介绍与使用](https://blog.csdn.net/wangming520liwei/article/details/101173111)

  ​

##### 1）IOC

- Spring核心模块实现了 loC的功能，它将类与类之间的依赖从代码中脱离出来，**用 配置的方式进行依赖关系描述** 。由**IoC容器**负责依赖类之间的**创建、拼接、管理、获取** 等工作。
- `BeanFactory`接口是**Spring框架的核心接口**，它实现了容器许多核心的功能。
- `Context`模块构建于核心模块之上，**扩展了 BeanFactory的功能**，添加了 **il8n国际 化、Bean生命周期控制、框架事件体系、资源加载透明化等多项功能**。此外，该模块 还提供了许多企业级服务的支持，如邮件服务、任务调度、JNDI获取、EJB集成、远 程访问等。
- `Applicationcontext`是`Context`模块的**核心接口**。 
- **表达式语言模块**是统一表达式语言(Unified EL)的一个扩展，**该表达式语言用于 査询和管理运行期的对象**，支持设置/获取对象属性，调用对象方法，操作数组、集合等。此外，该模块还提供了逻辑表达式运算、变量定义等功能。**可以方便地通过表达式串和 Spring IoC容器进行交互** 。

##### 2）AOP

- **AOP是继OOP之后，对编程设计思想影响极大的技术之一**。**AOP是进行横切逻辑 編程的思想**，它开拓了考虑问题的思路。在AOP模块里，Spring提供了满足AOP Alliance 规范的实现，还**整合了 AspectJ**这种AOP语言级的框架。在**Spring里实现AOP编程有众 多选择**。
- Java 5.0引入java.lang.instrument，允许在**JVM**启动时启用一个代理类，通过该 代理类**在运行期修改类的字节码（cglib）**，改变一个类的功能，从而实现AOP的功能。

##### 3）数据访问和集成

- **任何应用程序的核心问题是对数据的访问和操作**。**数据有多种表现形式**，如数据表、 XML、消息等，而**每种数据形式**又拥有**不同的数据访问技术**（如数据表的访问既可以直 接通过JDBC，也可以通过Hibernate或MyBatis）。
- 首先，Spring站在DAO的抽象层面，建立了一套面向DAO层的统一的异常体系， 同时将**各种访问数据的检査型异常转换为非检査型异常**，为整合各种持久层框架提供基 础。
- 其次，**Spring通过模板化技术对各种数据访问技术进行了薄层封装**，将模式化的代码隐藏起来，使数据访问的程序得到大幅简化。这样，Spring就建立起了和数据形式及 访问技术无关的统一的DAO层，借助AOP技术，Spring提供了声明式事务的功能。

##### 4）Web及远程操作

- 该模块建立在`Application Context`模块之上，**提供了 Web应用的各种工具类**，如**通 过Listener 或 Servlet初始化Spring容器，将Spring容器注册到Web容器中**。该模块还 提供了多项面向Web的功能，如透明化文件上传、Velocity、FmeMarker、XSLT的支持。此外，Spring可以整合Struts、WebWork等MVC框架.

##### 5）Web及远程访问

- Spring自己提供了一个完整的类似于Struts的MVC框架，称为**Spring MVC**。据说 Spring之所以也提供了一个MVC框架，是因为Rod Johnson想证明实现MVC其实是一 项简单的工作。当然，如果你不希望使用Spring MVC,那么Spring对Strats、WebWork 等MVC框架的整合,一定也可以给你带来方便。相对于Servlet的MVC, Spring在简 化Portlet的开发上也做了很多工作，开发者可以从中受益.

##### 6）WebSocket

- WebSocket提供了一个在Web应用中高效、双向的通信，需要考虑到客户端（浏览 器）和服务器之间的高频和低时延消息交换。**一般的应用场景有在线交易、游戏、协作、 数据可视化等**。

​       此外,Spring在远程访问及Web Service上提供了对很多著名框架的整合。由于 Spring框架的扩展性，特别是随着Spring框架影响性的扩大，越来越多的框架主动支持 Spring框架，使得Spring框架应用的涵盖面越来越宽广。

#### 备注：IOC和DI的区别

[控制反转（IOC）和依赖注入（DI）的区别](https://blog.csdn.net/SNOW_wu/article/details/54236374)

- **为何称为反转：**

  如果在A类中**主动获取**外部资源C（new来创建对象），则该行为方向为**正向**

  ![](http://dl.iteye.com/upload/attachment/265411/6fe19539-32ce-3a62-bc20-f8dc1e819f82.gif)

  如果A类**被动等待**IOC容器/DI容器将外部资源C注入到A类中，则该行为方向为**反转**

  ![](http://dl.iteye.com/upload/attachment/265413/e29bb428-b9f0-3465-8601-671c3fa68b8c.gif)

  ![](http://dl.iteye.com/upload/attachment/265415/2a537021-45c9-3fd3-80c5-18b9ace2b27a.gif)

- **依赖注入和控制反转**是对同一件事情的不同描述，即**主次关系**（应用程序 还是 容器）

  - **依赖注入是针对应用程序**而言的，应用程序**依赖IOC容器/DI容器**注入外部资源。
  - **控制反转是针对容器**而言的，容器控制应用程序，由容器反向的向应用程序注入应用程序所需的外部资源，**方便功能复用**。

- 小结：

  其实IoC/DI对编程带来的最大改变不是从代码上，而是**从思想上，发生了“主从换位”的变化**。应用程序原本是老大，要获取什么资源都是主动出击，但是在IoC/DI思想中，应用程序就变成被动的了，被动的等待IoC/DI容器来创建并注入它所需要的资源了。
  ​        这么小小的一个改变其实是编程思想的一个大进步，这样就有效的分离了对象和它所需要的外部资源，使得它们松散耦合，有利于功能复用，更重要的是使得程序的整个体系结构变得非常灵活

  ​

### 二、Spring核心技术解析

#### 1、激发POJO的潜能

- Spring竭力避免因自身的API而弄乱你的应用代码。Spring不会强迫你实现Spring规范的接口或 继承Spring规范的类，相反，在基于Spring构建的应用中，**它的类通常没有任何痕迹表明你使用 了Spring**。最坏的场景是，一个类或许会使用Spring注解，但它依旧是POJO。以下为简单POJO类。

  ```java
  package com.wangxiaoxi.spring;
  public class HelloWorldBean{
    public String sayHello(){
      return "Hello World";
    }
  }
  ```


-  Spring的**非侵入编程模型**意味着这个类**在Spring应用和非Spring应用中都可以发挥同样的作 用**。
- Spring赋予POJO魔力的方式之一，就是**通过DI来装配它们** ，帮助应用对象彼此之间保持松散耦合的。



#### 2、依赖注入

##### 1）没有引入DI之前是怎样的

- 任何一个有实际意义的应用（肯定比HelloWorld示例更复杂）都会由两个或者更多的类组成，这些类相互之间进行协作来完成特定的业务逻辑。按照传统的做法，**每个对象负责管理与自 己相互协作的对象（即它所依赖的对象）的引用**，这将会导致**高度耦合**和**难以测试**的代码。例如下代码

```java
package com.springincation.knights;

public class DamselRescuingKnight implements Knight{
  private RescueDamselQuest quest;
  
  public DamselRescuingKnight(){
    // DamselRescuingKnight 和 RescueDamselQuest存在紧耦合
    this.quest = new  RescueDamselQuest();
  }
  
  public void embarkOnQuest(){
    quest.embark();
  }
}
```

​	DamselRescuingKnight 和 RescueDamselQuest存在紧耦合，极大的限制了骑士执行探险的能力

##### 2）耦合的两面性

- 一方面，**紧密耦合的代码难以测试、难以复用**、难以理 解，并且典型地表现出“打地鼠'式的bug特性(修复一个bug,将会出现一个或者更多新的bug)。 
- 另一方面，**一定程度的耦合又是必须**的——完全没有耦合的代码什么也做不了。为了完成有 实际意义的功能，不同的类必须以适当的方式进行交互。总而言之，**耦合是必须的，但应当被 小心谨慎地管理**。
- 通过DI，对象的依赖关系将由系统中负责协调各对象的第三方组件在创建对象的时候进行设 定。**对象无需自行创建或管理它们的依赖关系**，如下图所示，**依赖关系将被自动注入到需要 它们的对象当中去**。

![2](E:\java面试\Study_Repositories\images\spring\2.jpg)





- **构造器注入：** 在构造的时候把冒险任务作为够着器参数传入

  ```java
  package com.springstudy.demo.pojo;

  /**
   * @author: wangxiaoxi
   * @create: 2020-04-18 23:07
   **/
  public class BraveKnight implements  Knight{

      private Quest quest;

    //
      public BraveKnight(Quest quest) {
          this.quest = quest;
      }

      public void embarkOnQuest(){
          quest.embark();
      }
  }
  ```

  传入的探险类型是Quest，也就是所有探险任务都必须**实现的一个接口**。

  ```java
  public class SlayDragonQuest implements Quest{

      private PrintStream stream;
     // SlayDragonQuest依赖于PrintStream
      public SlayDragonQuest(PrintStream stream) {
          this.stream = stream;
      }

      @Override
      public void embark() {
          System.out.println(this.stream + "SlayDragonQuest embark");
      }
  }

  ```

  ​        如果一个对象只通过接口（而不是具体实现或初始化过程）来表明依赖关系，那么**这种依赖就能够在对象本身毫不知情的情况下，用不同的具体实现进行替 换**。

- **将Quest注入到Knight中：** 

  - **配置文件：**将SlayDragonQuest注入到BraveKnight中

    ![3](E:\java面试\Study_Repositories\images\spring\3.jpg)


  - **注解开发：**

    ```java
    @Configuration
    public class KnightConfig {

        @Bean
        public BraveKnight braveKnight(){
            //通过quest()，得到IOC容器中的quest实例，再通过构造器注入的方法，封装到骑士上。
            return new BraveKnight(quest());
        }

        @Bean
        public Quest quest() {
            //System.in是输入流（InputStream），而System.out是打印流（基础输出流）
            return new SlayDragonQuest(System.out);
        }
    }
    ```

- **测试类**：

  ```java
  @SpringBootTest
  class DemoApplicationTests {

     //自动依赖注入
  	@Autowired
  	private Knight knight;

  	@Test
  	void contextLoads() {
  		System.out.println(knight);
  		knight.embarkOnQuest();
  	}
  }

  -----
  输出结果
  com.springstudy.demo.pojo.BraveKnight@2b289ac9
  java.io.PrintStream@4eb1c69SlayDragonQuest embark
  ```

  测试类也可以用`context`的`getBean()`来实现

- 小总结

  - 尽管 BraveKnight依赖于Quest,但是它并不知道传递给它的是什么类型的Quest，也不知道这 个Quest来自哪里。
  - 与之类似，SlayDragonQuest依赖于PrintStream，但是在编码时它 并不需要知道这个Printstream是什么样子的。**只有Spring通过它的配置能够了解这些组 成部分是如何装配起来的**。这样的话，就可以在**不改变所依赖的类**的情况下，修改依赖关系。
  - 如果配置了同时配置了两个Knight接口的实现类实例，系统在自动注入时就会报错`expected single matching bean but found 2`。

  ```java
    @Bean
      public BraveKnight braveKnight(){
          //通过quest()，得到IOC容器中的quest实例，封装在骑士上。
          return new BraveKnight(quest());
      }

      @Bean
      public CowardKnight cowardKnight(){
          //通过quest()，得到IOC容器中的quest实例，封装在骑士上。
          return new CowardKnight(quest());
      }

  ----
  测试结果
  type 'com.springstudy.demo.pojo.Knight' available: expected single matching bean but found 2: braveKnight,cowardKnight
  ```

  #### 

#### 3、应用切面

​	DI能够让相互协作的软件组件保持松散耦合，而面向切面编程(aspect - oriented programming, AOP)允许你把**遍布应用各处的功能分离出来形成可重用的组件**。

##### 1）为何使用面向切面编程

- 面向切面编程往往被定义为**促使软件系统实现关注点的分离一项技术**。系统由许多不同的组 件组成，每一个组件各负责一块特定功能。除了实现自身核心的功能之外，**这些组件还经常承 担着额外的职责**。诸如**日志、事务管理和安全这样的系统服务**经常**融入到自身具有核心业务 逻辑的组件**中去，**这些系统服务通常被称为横切关注点**，因为它们会跨越系统的多个组件。

- 如果将**这些关注点分散到多个组件**中去，你的**代码将会带来双重的复杂性**。 

  - 实现系统关注点功能的代码将会重复出现在多个组件中。这意味着如果你**要改变这些关 注点的逻辑，必须修改各个模块中的相关实现**。即使你把这些关注点抽象为一个独立的 模块，其他模块只是调用它的方法，但**方法的调用还是会重复出现在各个模块中**。 
  - **组件会因为那些与自身核心业务无关的代码而变得混乱。**一个向地址簿增加地址条目的 方法应该只关注如何添加地址，而不应该关注它是不是安全的或者是否需要支持事务。

  ![4](E:\java面试\Study_Repositories\images\spring\4.jpg)

- AOP能够使这些服务模块化，并**以声明的方式将它们应用到它们需要影响的组件**中去。所造 成的结果就是这些组件会具有更高的内聚性并且会更加关注自身的业务，**完全不需要了解涉 及系统服务所带来复杂性**。总之，AOP能够确保POJO的简单性。

- 如下图所示，我们可以把切面想象为覆盖在很多组件之上的一个外壳。应用是由那些实现各 自业务功能的模块组成的。**借助AOP,可以使用各种功能层去包裹核心业务层**。这些层以声明 的方式灵活地应用到系统中，你的**核心应用甚至根本不知道它们的存在**。这是一个非常强大的理念，可以**将安全、事务和日志关注点与核心业务逻辑相分离**。

![5](E:\java面试\Study_Repositories\images\spring\5.jpg)

##### 2）案例 - 诗人歌颂骑士

- **Minstrel类：** 是只有两个方法的简单类。在骑士执行毎一个探险任务之 前,` singBeforeQuest ()`方法会被调用；在骑士完成探险任务之后，`singAfterQuest () `方法会被调用。在这两种情况下，Minstrel都会通过一个`PrintStream`类来歌颂骑士的事 迹，这个类是通过构造器注入进来的。

  ```java
  /**
   * @author: wangxiaoxi
   * @create: 2020-04-19 12:07
   **/
  public class Minstrel {

      private PrintStream printStream;

      public Minstrel(PrintStream printStream){
          this.printStream = printStream;
      }

      public void singBeforeQuest(){
          System.out.println("lalala,the knight is  so brave");
      }

      public void singAfterQuest(){
          System.out.println("yes, the knight win");
      }
  }
  ```

- **BraveKnight必须调用Minstrel的方法**

  ```java
  public class BraveKnight implements  Knight{

      private Quest quest;
      private Minstrel minstrel;

      public BraveKnight(Quest quest, Minstrel minstrel) {
          this.quest = quest;
          this.minstrel = minstrel;
      }

      public void embarkOnQuest(){
          minstrel.singBeforeQuest();
          quest.embark();
          minstrel.singAfterQuest();
      }
  }
  ```

  现在，你所需要做的就是回到Spring配置中，**声明Minstrel bean并将其注入到BraveKnight的构造器之中**。但是，清稍等.. 我们似乎感觉有些东西不太对。管理他的吟游诗人真的是骑士职责范围内的工作吗？在我看 来，**吟游诗人应该做他份内的事，根本不需要骑士命令他这么做**。毕竟，用诗歌记载骑士的探 险事迹，这是吟游诗人的职责。为什么骑士还需要提醒吟游诗人去做他份内的事情呢？ 此外，因为骑士需要知道吟游诗人，所以就**必须把吟游诗人注入到BarveKnight类中。这不 仅使BraveKnight的代码复杂化了**

  而且还让我疑惑是否还需要一个不需要吟游诗人的骑 士呢？如果**Minstrel为null会发生什么呢**？我是否应该引入**一个空值校验逻辑**来覆盖该 场景？

##### 3）如何切面编程

​	依赖注入看似可达到预期的效果，但是诗人和骑士之前存在一定的耦合，需要用到前面编程来处理。

利用**配置文件将Minstrel声明为一个切面**：

![6](E:\java面试\Study_Repositories\images\spring\6.jpg)

- 这里使用了Spring的aop配置命名空间**把Minstrel bean声明为一个切面**。首先，需要把 Minstrel声明为一个bean，然后在**＜aop:aspect＞元素中引用该bean**。
- 为了进一步定义切 面，声明(使用**＜aop:before＞**)在embarkOnQuest ()方法**执行前调用Minstrel的 singBeforeQuest ()方法**。这种方式被称为**前置通知**(beforeadvice)。
- 同时声明(使 用＜**aop:after＞**)在embarkOnQuest ()方法**执行后调用singAfter Quest ()方法**。这种 方式被称为**后置通知**(after advice)。
-  在这两种方式中，pointcut-ref属性都**引用了名字为embank的切入点**。**该切入点是在前边 的＜pointcut＞元素中定义的（id）**，并配置expression属性来选择所应用的通知。
- **表达式向语 法采用的是AspectJ的切点表达式语言**。

使用spring注解进行切面编程：

- 先将 Minstrel对象注入到IOC容器中

```java
 @Bean
    public Minstrel minstrel() {
        //System.in是输入流（InputStream），而System.out是打印流（基础输出流）
        return new Minstrel(System.out);
    }
```

- 配置切面类：

  @Component，@Aspect用来配置切面类

  @Pointcut配置切入点

  @Before，@After配置通知

  更多请参照该文档  [Springboot（二十一）@Aspect 切面注解使用](https://blog.csdn.net/u012326462/article/details/82529835)

  [Spring AOP切点表达式用法总结](https://www.cnblogs.com/zhangxufeng/p/9160869.html)

```java
/**
 * @author: wangxiaoxi
 * @create: 2020-04-19 12:37
 **/
@Component
@Aspect
public class MinstrelAspect {

    //获取IOC容器中的诗人对象
    @Autowired
    private Minstrel minstrel;

    //定义切入点
    private final String POINT_CUT = "execution(public * com.springstudy.demo.pojo.BraveKnight.embarkOnQuest())";

    //用@Pointcut切点注解，想在一个空方法上面，一会儿在Advice通知中，直接调用这个空方法就行了
    //也可以把切点表达式写在Advice通知中的，单独定义出来主要是为了好管理。
    @Pointcut(POINT_CUT)
    public void pointCut(){}

    //声明前置通知
    @Before(value = "pointCut()")
    public void before(){
        minstrel.singBeforeQuest();
    }

    //声明后置通知
    @After(value = "pointCut()")
    public void after(){
        minstrel.singAfterQuest();
    }
}
```

```java
@Autowired
private Knight knight;

@Test
void contextLoads() {
  knight.embarkOnQuest();
}

----
输出结果
com.springstudy.demo.pojo.BraveKnight@97d0c06
lalala,the knight is  so brave
java.io.PrintStream@70972170SlayDragonQuest embark
yes, the knight win
```



#### 4、Spring容器

- 容器是Spring框架的核心。Spring容器**使用DI管理构成应用的组件**，它会创建相互协作的组件 之间的关联。毫无疑问，这些对象更简单干净，更易于理解，**更易于重用并且更易于进行单元 测试**。
- **Spring容器并不是只有一个**。Spring自带了多个容器实现，可以归为两种不同的类型。**bean工厂** (由org.springframework, beans. factory.eanFactory接口定义)是最简单的容 器，**提供基本的DI支持**。**应用上下文**(由org. springframework. context. ApplicationContext接口定义)**基于 BeanFactory构建**，并提供**应用框架级别的服务**，例如从属性文件解析文本信息以及发布应用 事件给感兴趣的事件监听者。

##### 1）使用应用上下文

- Spring自带了**多种类型的应用上下文**。下面罗列的几个是你最有可能遇到的。

- **Java配置加载上下文：** 

  - `AnnotationConfigApplicationContext`:从一个或多个基于**Java的配置类**中**加载 Spring应用上下文**。 

    ```java
    ApplicationContext applicationContext = new AnnotationConfigApplicationContext("com.package com.springstudy.demo.config.*");
    ```

  - `AnnotationConf igWebApplicationContext`:从一个或多个基于 **Java 的配置类**中 **加载Spring Web应用上下文**。 

- xml**配置文件加载上下文** ：

  - `ClassPathXmlApplicationContext`:从**类路径下的—或多个XML配置文件中加 载上下文定义**，把应用上下文的定义文件作为类资源。	

  - `FileSystemXmlapplicationcontext`:从**文件系统下**的一个或多个XML配置文件 中加载上下文定义。 

    ```java
    ApplicationContext applicationContext = new FileSystemXmlApplicationContext("application.xml");
    ```

  - `XmlWebApplicationContext`:从**Web应用下**的一个或多个XML配置文件中加载上下 文定义。

- 应用上下文准备就绪之后，我们就可以调用上下文的**getBean()**方法从Spring容器中获取 bean。

  ​

##### 2）Bean的生命周期

- 在传统的Java应用中，bean的生命周期很简单。使用Java关键字**new进行bean实例化**，然后该 bean就可以使用了。一旦该**bean不再被使用**，则由Java自动进行**垃圾回收**。

- 相比之下，Spring容器中的bean的生命周期就显得相对复杂多了。正确理解Springbean的生命 周期非常重要，因为你**或许要利用Spring提供的扩展点来自定义bean的创建过程**。下图展示了 bean装载到Spring应用上下文中的一个典型的生命周期过程。

  ![7](E:\java面试\Study_Repositories\images\spring\7.jpg)

##### 3）自动化装配Bean -- @Component

​	当描述 bean如何进行装配时，Spring具有非常大的灵活性，它提供了**三种主要的装配机制**： 

- 在XML中进行显式配置。 
- 在Java中进行显式（注解）配置。 
- **隐式的bean发现机制**和**自动装配**。

​       Spring的配置风格是可以互相搭配的，所以你可以选择使用 XML装配一些bean,使用Spring童于Java的配置(JavaConfig)来装配另一些bean,而将剩余的 bean让Spring去自动发现。

​	所以，尽可能地使用自动配置的机制，显示配置越少越好。

​	Spring从**两个角度来实现自动化装配**： 

- **组件扫描(component scanning):** Spring会自动发现**应用上下文中所创建的bean**。 
- **自动装配(autowiring):** Spring自动满足bean之间的依赖。 

​        组件扫描和自动装配组合在一起就能发挥出强大的威力，它们能够**将你的显式配置降低到最 少**。

还是使用之前的骑士例子（二.2.2]）：

- `Knight`接口定义了骑士的概念

  ```java
  public interface Knight{
     //不要管里面的逻辑
  }
  ```

- `Knight`接口的实现类`BraveKnight`

  ```java
  @Component
  public class BraveKnight implements  Knight{
  	//不要管里面的逻辑
  }
  ```

  上使用了**@Component注解**。这个简单的注解**表明该类会作为组件类**，并告知Spring要为这个类创建bean。**没有必要显式配置BraveKnightbean** ，因为这个类**使用了@Component注解，所以Spring会为你把事情处理妥当**

- **@ComponentScan**注解启用了组件扫描，默认会扫描与配置类相同的包

  ```java
  @Configuration
  @ComponentScan("com.springstudy.demo.*")
  public class KnightConfig {
    //不要管里面的逻辑
  }
  ```

- 测试是否自动装配Knight成功：

  ```java
  @SpringBootTest
  class DemoApplicationTests {

  	@Autowired
  	private Knight knight;

  	@Test
  	void contextLoads() {
  		System.out.println(knight);
  	}
  }

  -----
  测试结果
  com.springstudy.demo.pojo.BraveKnight@14b0e127
  ```

- **备注：**

  - 如果不是springboot项目，则需要使用`@ContextConfiguration`，告诉它需要在KnightConfig中加载配置（因为KnightConfig中有@ComponentScan，所以最终可以获得BraveKnightBean）。

    ![9](E:\java面试\Study_Repositories\images\spring\9.jpg)

  - 如果是springboot项目，在测试类中只需添加`@SpringBootTest`即可，springboot项目会**自动加载`@Configuration`下的配置类**。

    但是好奇地会发现，`@SpringBootTest`中没有类似`@ContextConfiguration`来加载配置类的注解，那测试类如何获得component组件的？。

    ```java
    @Target({ElementType.TYPE})
    @Retention(RetentionPolicy.RUNTIME)
    @Documented
    @Inherited
    @BootstrapWith(SpringBootTestContextBootstrapper.class)
    @ExtendWith({SpringExtension.class})
    ```

    其实你会发现启动类的`@SpringBootApplication`中的`@EnableAutoConfiguration`可以自动加载配置类 (具体自动装配过程请见该文档  [SpringBoot之@EnableAutoConfiguration注解](https://blog.csdn.net/zxc123e/article/details/80222967))

    ```java
    @Target({ElementType.TYPE})
    @Retention(RetentionPolicy.RUNTIME)
    @Documented
    @Inherited
    @SpringBootConfiguration
    @EnableAutoConfiguration
    @ComponentScan(
        excludeFilters = {@Filter(
        type = FilterType.CUSTOM,
        classes = {TypeExcludeFilter.class}
    ), @Filter(
        type = FilterType.CUSTOM,
        classes = {AutoConfigurationExcludeFilter.class}
    )}
    )
    ```

    在测试中，你会发现如果在运行测试类时注释掉`@SpringBootApplication`，测试会报错，解决方法不单单**要求测试类和启动类包名相同** [java.lang.IllegalStateException Unable to find a @SpringBootConfiguration错误解决方案](https://blog.csdn.net/qq_28643817/article/details/88063251)。

##### 4）自动化装配Bean -- @Bean

- @Component和@Bean的区别

  - @Component注解表**明一个类会作为组件**类，并**告知Spring要为这个类创建bean**。
  - @Bean注解告诉Spring这个**方法将会返回一个对象**，这个对象要注册为Spring应用上下文中的bean。通常方法体中包含了最终产生bean实例的逻辑。

  两者的目的是一样的，**都是注册bean到Spring容器中**。

  [SPRING中@COMPONENT与@BEAN的区别](https://www.cnblogs.com/zzw3014/p/11858508.html)