## Java标准NIO类库与Netty的区别

### 一、考点分析

#### 1、考察方面

- 对 Netty 进行整体理解，了解其**基本组成**。
- 基于 IO、NIO 等标准 API 的实例，**分析Netty的技术要点**。

#### 2、典型问答

单独从**性能角度**，Netty 在基础的 NIO 等类库之上进行了很多改进，例如：

- 更加优雅的 **Reactor 模式**实现、**灵活的线程模型**、利用 **EventLoop** 等创新性的机制，可以**非常高效地管理成百上千的 Channel**。


- 充分利用了 Java 的 **Zero-Copy 机制**，并且从多种角度，“斤斤计较”般的降低内存分配和回收的开销。例如，使用**池化的 Direct Buffer** 等技术，在提高 IO 性能的同时，**减少了对象的创建和销毁**；
- **利用反射**等技术直接**操纵 SelectionKey**，使用数组而不是 Java 容器等。


- 使用更多本地代码。例如，直接利用 **JNI 调用 Open SSL** 等方式，获得比 Java 内建 SSL 引擎更好的性能。


- 在通信协议、序列化等其他角度的优化。

总的来说，Netty 并没有 Java 核心类库那些强烈的通用性、跨平台等各种负担，针对性能等特定目标以及 Linux 等特定环境，采取了一些极致的优化手段。



### 二、知识拓展

#### 1、概念

##### 整体概念：

- 它是一个**异步的、基于事件 Client/Server**的网络框架，目标是提供一种简单、快速构建网络应用的方式，同时保证**高吞吐量、低延时、高可靠性**。

  

##### 核心概念：

![20](..\..\images\java基础\20.png)

- **ServerBootstrap：** **服务器端程序的入口**，这是 Netty 为**简化网络程序配置和关闭等生命周期管理**，所引入的 Bootstrapping 机制。我们**通常要做的创建 Channel、绑定端口、注册Handler 等，都可以通过这个统一的入口**，以Fluent API 等形式完成，相对简化了 API 使用。

- **Bootstrap**则是 **Client 端的通常入口**。

- **Channel：** **作为一个基于 NIO 的扩展框架，Channel 和 Selector 等概念仍然是 Netty 的基础组件**，但是针对应用开发具体需求，提供了相对易用的抽

- **EventLoop**：这是 Netty **处理事件的核心机制**。例子中使用了EventLoopGroup。我们在NIO 中通常要做的几件事情，如**注册感兴趣的事件、调度相应的 Handler** 等，**都是EventLoop 负责**。

- **ChannelFuture**： 这是 Netty 实现异步 IO 的基础之一，保证了同一个 Channel 操作的调用顺序。**Netty 扩展了 Java 标准的 Future**，提供了针对自己场景的特有Future定义。

- **ChannelHandler：**  这是应用开发者**放置业务逻辑**的主要地方，也是我上面提到的“Separation Of Concerns”原则的体现。

- **ChannelPipeline：** 它是 **ChannelHandler 链条的容器**，**每个 Channel** 在创建后，**自动被分配一个 ChannelPipeline**。在上面的示例中，我们通过 ServerBootstrap 注册了ChannelInitializer，并且实现了 **initChannel** 方法，而在该方法中则**承担了向ChannelPipleline 安装其他 Handler** 的任务。

  ![21](..\..\images\java基础\21.png)



#### 2、Netty 与 Java 自身的 NIO 框架相比有哪些不同呢？

-  **Java 的标准类库**，由于其**基础性、通用性**的定位，往往过于关注技术模型上的抽象，而**不是从一线应用开发者的角度去思考**。


- 为什么要引入Netty，而不用Java的NIO类库。

  这里以Thread线程为例，引入并发包的一个重要原因就是，应用开发者使用 Thread API 比较痛苦，需要操心的不仅仅是业务逻辑，而且还要自己负责将其映射到Thread 模型上。**Java NIO** 的设计也有类似的特点，**开发者需要深入掌握线程、IO、网络等相关概念，学习路径很长**，很容易导致代码复杂、晦涩。即使是有经验的工程师，也难以快速地写出高可靠性的实现。

- Netty 将业务逻辑和无关技术逻辑进行隔离，并通过各种方便的抽象，一定程度上**填补了了基础平台**和**业务开发之间的鸿沟**，更**有利于在应用开发中普及业界的最佳实践**。

- 另外，Netty > java.nio + java. net！

- 除了**核心的事件机制**等，Netty 还额外提供了很多功能，例如：

  - 从网络协议的角度，Netty 除了支持传输层的 **UDP、TCP、SCTP**协议，也支持 **HTTP(s)、WebSocket** 等多种**应用层协议**，它并不是单一协议的 API。

  - 在应用中，需要将数据从 Java 对象转换成为各种应用协议的数据格式，或者进行反向的转换，Netty 为此提供了一系列扩展的**编解码框架**，与应用开发场景无缝衔接，并且性能良好。

  - 它**扩展了 Java NIO Buffer**，提供了自己的 Byte Buffer实现，并且**深度支持 Direct Buffer 等技术**，甚至 hack 了 Java 内部对 Direct Buffer 的分配和销毁等。同时，**Netty 也提供了更加完善的 Scatter/Gather 机制**实现。

    ![22](..\..\images\java基础\22.png)

- 对比 Java 标准 NIO 的代码，Netty 提供的相对高层次的封装，**减少了对 Selector 等细节的操纵**，而 **EventLoop、Pipeline 等机制则简化了编程模型**，开发者不用担心并发等问题，在一定程度上简化了应用代码的开发。最难能可贵的是，这一切并没有以可靠性、可扩展性为代价，反而将其大幅度提高。

  

### 三、深入自学方向

##### 学习小建议：

- 想系统学习 Netty，Norman Maurer 等编写的《Netty 实战》（Netty In

  Action）是个很好的入门参考。

- 针对 **Netty 的一些实现原理**，很可能成为面试中的考点，例如：

  - **Reactor 模式**和 **Netty 线程模型**。
  - **Pipelining、EventLoop** 等部分的**设计实现细节**。
  - Netty 的内存管理机制、引用计数等特别手段。

- 有的时候面试官也喜欢**对比 Java 标准 NIO API**，例如，你是否知道 Java NIO 早期版本中的**Epoll空转**问题，以及 **Netty 的解决方式**等。

  

**注意点：**

- 在学习时希望你不要一开始就被复杂的细节弄晕，可以结合实例，逐步、有针对性的进行学习。
- 试着画出相应的示意图，非常有助于理解并能清晰阐述自己的看法。



### 四、问答环节

**Q：**Netty 的线程模型是什么样的？

**A：** netty线程模型一般分为**监听线程**和**I/O处理线程**，也即bossGroup和workerGroup，属于多Reactor模型。



### 五、参考文档

1、极客时间《Java核心技术36讲》第12讲

2、[Netty线程模型](https://www.jianshu.com/p/738095702b75)

