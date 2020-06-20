## BIO、NIO的整体理解

## 一、考点分析

### 1、考察点

- 基础 API 功能与设计，**InputStream/OutputStream 和 Reader/Writer 的关系和区别**。 

- **NIO、NIO2**的基本组成. 

- 给定场景，分别用不同模型实现，分析**BIO， NIO等模式的设计和实现原理**. 

- NIO提供的高性能数据操作方式是基于什么原理。如何使用? 

- 或者，从开发者的角度来看，你觉得**NIO自身实 现存在哪些问题**？有什么改进的想法吗? 

  

### 2、java.io 必备知识

-  IO不仅仅是**对文件的操作**，网络编程中，比如**Socket通信**, 都是**典型的IO操作**目标。 

- **输入流，输出流**（Inputstream/Outputstream）是用于**读取或写入字节**的，例如操作图片 文件。 

- 而**Reader/Writer**则是用于**操作字符**，增加了字符编解码等功能，适用于类似**从文件中读取 或者写入文本信息**。**本质上计算机操作的都是字节**，不管是网络通信还是文件读取， Reader/Writer相当于构建了**应用逻辑**和**原始数据  之间的桥梁**。

-  **BufferedOutputStream**等带缓冲区的实现，可以**避免频繁的磁盘读写**，进而提高IO处理 效率。这种设计利用了缓冲区，将批量数据进行一次操作，但在使用中**千万别忘了 flush**.

- 参考下面这张类图。**很多IO工具类都实现了 Closeable接口**，因为需要迸行资源的释放。 比如，打开Fileinputstream ,它就会获取相应的文件描述符(FileDescriptor)，需要利用 **try-with-resources** ， **try-finally**等机制**保证FilelnputStream被明确关闭**，进而相应文件 描述符也会失效，否则将导致资源无法被释放。利用**Cleaner或 finalize机制作为资源释放的最后把关**，也是必要的。

  ![16](..\..\images\java基础\16.jpg)



## 二、知识拓展

### 1、基础概念

#### 同步和异步，阻塞和非阻塞

- 区分同步和异步( synchronous/asynchronous)。简单来说，**同步是一种可靠的有序运行 机制**；而异步 则相反,其他任务不需要等待当前调用返回,**通常依靠事件、回调等机制实现任务间次序关系**
- 区分阻塞与非阻塞(blocking/non-blocking )。在进行阻塞操作时，当前线程会处于阻塞 状态，无法从事其他任务，只有当条件就绪才能继续，比如**Serversocket新连接建立完毕，或数据读取、写入操作完成**；而非阻塞则是不管IO操作是否结束，直接返回，相应操作在后台继续处理。
- **不能一概而论认为同步或阻塞就是低效**，具体还要着应用和系统特征。

### 2、BIO（传统IO）

- 首先，**传统的 java.io**包，它基于流模型实现，提供了我们最熟知的一些IO功能，比如**File抽 象、输入输出流**等。**交互方式是同步、阻塞的方式**，也就是说，在读取输入流或者写入输出流 时，在读、写动作完成之前，线程会一直阻塞在那里，它们之间的调用是可靠的线性顺序。
- java.io包的好处是代码比较简单、直观，缺点则是**IO效率和扩展性存在局限性**,容易成为应用性能的瓶颈。
- 很多时候，人们也把**java.net**下面提供的部分网络API，比如**Socket, ServerSocket，HttpURLConnection**也归类到**同步阻塞IO类库**，因为网络通信同样是IO行为.
- 请跳转到这里 [IO详解之BIO](https://blog.csdn.net/u012250875/article/details/78341874?depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-1&utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-1)



### 3、NIO

#### 1）NIO概览

-  在 Java 1.4 中引入了 NIO 框架(**java.nio 包**)，提供了 **Channel、Selector、 Buffer 等 新的抽象**，可以**构建多路复用**的、**同步非阻塞IO程序**，同时提供了更接近操作系统底层的高性能数据操作方式

   ![19](..\..\images\java基础\19.jpg)

- **NIO的主要组成部分：**
  - **Buffer**：高效的**数据容器**，除了布尔类型，所有**原始数据类型都有相应的Buffer实现**。

  - **Channel**：类似在Linux之类操作系统上看到的文件描述符，是NIO中被用来**支持批量式IO操作**的一种抽象。

  - **File成者Socket**：通常被认为是比较**高层次的抽象**。而**Channel**则是更加操作**系统底层的 一种抽象**，这也使得NIO得以充分利用现代操作系统底层机制,获得特定场景的性能优化,，例如，**DMA** ( Direct Memory Access)等。不同层次的抽象是相互关联的，我们可以**通过 Socket获取Channel**，反之亦然， 

  - **Selector**： 是NIO实现**多路复用的基础**，它提供了一种高效的机制，**可以检测**到注册在 **Selector上的多个Channel**中，**是否有Channel处于就绪状态** ，进而实现了**单线程对多 Channel的高效管理**。

    **Selector**同样是**基于底层**操作系统机制，**不同模式，不同版本都存在区別**，例如，在最新的 代码库里，相关实现如下：

    - Linux上依赖于 **epoll** (http://hg.openjdk.java.net/jdk/jdk/file/d8327f838b88/src/iava.base/linux/classes/sun/nio/ch/EPollSelectorlmpl.java)

    - Windows 上 NIO2 ( AIO)模式依赖于

       **iocp** ( http://hg.openjdk.java.net/jdk/jdk/fiIe/d8327f838b88/src/java.base/windows/classes/sun/nio/ch/locp.java). 

  - **Charset**：提供Unicode 字符串定义，NlO 也提供了相应的编解码器等，例如通过下面的方式进行**字符串到ByteBuffer的转换**： 

    ```java
    Charset.defaultCharset().encode("Hello world!")；
    ```



#### 2）NIO可解决什么问题

##### 场景描述：

- 我们需要实 现**一个服务器应用**，只简单要求能够**同时服务多个客户端请求**即可。

##### 方法1：BIO实现

- 使用java.io和java.net中的同步、阻塞式API,可以简单实现.

  ```java
  public class DemoServer extends Thread{

      //服务端线程
      private ServerSocket serverSocket;

      public int getPort(){
          return serverSocket.getLocalPort();
      }

      @Override
      public void run() {
          try{
              //设置端口
              serverSocket = new ServerSocket(0);
              while(true){
                  //调用accept方法，阻塞等待客户端连接.
                  Socket socket = serverSocket.accept();
                  RequestHandler requestHandler = new RequestHandler(socket);
                  requestHandler.start();
              }

          }catch (IOException e) {
              e.printStackTrace();
          }
      }

      public static void main(String[] args) throws Exception {
          DemoServer demoServer = new DemoServer();
          demoServer.start();
          for (int i = 0; i < 6 ; i++) {
              //客户端线程：主机地址，端口号连接服务端
              try(Socket client = new Socket(InetAddress.getLocalHost(),demoServer.getPort())){
                  BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(client.getInputStream()));
                  bufferedReader.lines().forEach(s->{
                      System.out.println(s);
                  });
              }
          }
      }
  }

  //简化实现，不做读取，直接发送字符串
  class RequestHandler extends Thread{
      private Socket socket;
      RequestHandler(Socket socket){
          this.socket = socket;
      }

      @Override
      public void run() {
          try(PrintWriter out = new PrintWriter(socket.getOutputStream());){
              out.println("hello world");
              out.flush();
          }catch (Exception e){
              e.printStackTrace();
          }
      }
  }

  输出结果
  ---------
  hello world
  hello world
  hello world
  hello world
  hello world
  hello world
  (服务器继续阻塞等待socket客户端发来请求)
  ```

- **其实现要点是：**

  - 服务端启动ServerSocket，端口 **0表示自动绑定一个空闲端口**。
  - 调用accept方法，**阻塞等待客户端连接**. 
  - 利用Socket模拟了一个简单的客户端，只进行连接、读取、打印。 
  - 当连接建立后，**启动一个单独线程负责回复（RequstHandler）**客户端请求.

- **出现的问题：**

  - Java语言目前的**线程**实现是比较**重置级**的，**启动或者销毁一个线程有明显开销的**， 每个线程都有单独的线程栈等结构，需要占用非常明显的内存，所以，**每一个Client启动一个 线程似乎都有些浪费**。

    

##### 方法2：关于BIO线程池机制

- 引入**线程池机制的BIO避免线程销毁**，减少重新创建启动线程，销毁线程带来的浪费

  ```java
  ExecutorService executors = Executors.newFixedThreadPool(8);

   //利用线程池机制,为requestHandler分配线程，来处理client请求
  while(true){
    Socket socket = serverSocket.accept();
    RequestHandler requestHandler = new RequestHandler(socket);
    //requestHandler.start();
    executors.execute(requestHandler);
  }
  ```

- **实现要点：**

  通过一个固定大小的线程池，来负责管理工作线程，避免频繁创建，销毁线程的开销，这是我们构建并发服务的典型方式。这种工作方式，可以参考下图来理解。

  ![17](..\..\images\java基础\17.jpg)

- **存在的问题：**

  如果连接数并不是非常多，只有最多几百个连接的普通应用，这种模式往往可以工作的很好。但 是,如果连接数量急剧上升，这种实现方式就无法很好地工作了，因为**线程上下文切换开销会在 高并发时变得很明显**，这是**同步阻塞方式的低扩展性劣势**。


##### 方法3：NIO的多路复用机制

```java
public class NIOServer extends Thread{

  @Override
  public void run() {

    try(Selector selector = Selector.open()){

      //创建server的channel
      ServerSocketChannel serverSocket = ServerSocketChannel.open();
      serverSocket.bind(new InetSocketAddress(InetAddress.getLocalHost(),8888));
      //设置server的channel非阻塞。阻塞模式下，注册操作是不允许的
      serverSocket.configureBlocking(false);

      //将serverChannel注册到selector，并说明关注点
      serverSocket.register(selector, SelectionKey.OP_ACCEPT);

      //轮询访问selector
      while (true){
        //阻塞并等待就绪的socket Channel，这是关键点之一
        selector.select();
        //在这段时间内，得到所有访问selector的socket channel（socketChannel（多个）和serverSocketChannel（一个）是一对）
        Set<SelectionKey> selectionKeys = selector.selectedKeys();
        Iterator<SelectionKey> iterator = selectionKeys.iterator();
        while(iterator.hasNext()){
          SelectionKey next = iterator.next();
          sayHelloWorld((ServerSocketChannel)next.channel());
          iterator.remove();
        }
      }

    } catch (IOException e) {
      e.printStackTrace();
    }

  }

  //client利用socket高层抽象对服务器发出请求，服务器用底层的抽象socketChannel，selector进行处理
  private  void sayHelloWorld(ServerSocketChannel serverSocketChannel){
    //
    try(SocketChannel socketChannel = serverSocketChannel.accept()) {
      //处理socketChannel：服务器端将字符串写入byteBuff
      socketChannel.write(Charset.defaultCharset().encode("hello wangxiaoxi"));
    } catch (IOException e) {
      e.printStackTrace();
    }
  }

  public static void main(String[] args) throws Exception{
    NIOServer nioServer = new NIOServer();
    nioServer.start();

    for (int i = 0; i < 6; i++) {
      try(Socket socket = new Socket(InetAddress.getLocalHost(),8888)){

        //服务端已将字符串写入byteBuff，客户端读取byteBuff里的数据
        BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        bufferedReader.lines().forEach(s->{
          System.out.println(s);
        });
      }
    }
  }
}

输出结果
-------------
hello wangxiaoxi
hello wangxiaoxi
hello wangxiaoxi
hello wangxiaoxi
hello wangxiaoxi
hello wangxiaoxi

```

- 首先，通过**Selector.open()创建一个Selector**，作为类似调度员的角色.

- 然后，创建一个**ServerSocketChannel,并且向Selector注册**,通过指定 **SelectionKey.OP_ACCEPT** ,告诉调度员，它**关注的是新的连接请求**. 

  注意,为什么我们要明确配宜非阻塞模式呢？这是因为**阻塞模式下，注册操作是不允许的**，会抛出 IllegalBlockingModeException 异常. 

- **Selector阻塞在select操作**，当有Channel 发送接入请求，就会被唤醒. 

- 在sayHelloWorld方法中，通过**Socketchannel和Buffer进行数据操作**，在本例中是发送 了一段字符串。

- NIOServer 和 BIOServer的main方法类似


**备注：**

- **基本抽象很相似：SocketChannel（N） 和ServerSocketChannel（1）是一对** ，他们是java.nio下面实现通信的类，支持异步通信。就好比**java.net下，Socket 和ServerSocket** 是一对。
- **什么是多路复用**：很多个网络I/O复用**一个或少量的线程**来处理这些连接。





#### 3）NIO与BIO的区别

- 可以看到，在前面两个样例中，IO都是同步阻塞模式，所以需要多线程以实现多任务处理。而 NIO则是利用了**单线程轮询事件的机制（事件驱动）**，通过高效地**定位就绪的Channel** ，来决定做什么，**仅 仅select阶段是阻塞**的，可以有效**避免大量客户端连接时，频繁线程切换带来的问题**，应用的 扩展能力有了非常大提高。下面这张图对这种实现思路进行了形象地说明。

  ![18](..\..\images\java基础\18.jpg)





#### 4）Netty与Java的NIO的区别

- 请跳转至这里 [Java标准NIO类库与Netty的区别](https://blog.csdn.net/qq_33934427/article/details/105427550)



### 4、NIO2（AIO）

- 在**Java 7**中，NIO有了进一步改进，也就是**NIO 2**，引入了**异步非阻塞**方式，也 有很多人叫它AIO (Asynchronous IO)。异步IO操作**基于事件和回调的机制**，可以简 单理解为，**应用操作直接返回，而不会阻塞**那里，当**后台处理完成，操作系统会通知相应线程进行后续工作。**
- NIO2利用事件和回调，处理 Accept、Read等操作。AIO实现看起来是类似这样子：
- **NIO和NIO2的区别：**
  - **基本抽象很相似**：AsynchronousServerSocketChannel对应于上面例子中的 ServerSocketChannel; AsynchronousSocketChannel 则对应 Socketchannel。
  - 业务逻辑的关键在于，通过指定**CompletionHandler回调接口**，在**accept/read/write等 关键节点**，通过**事件机制调用**，这是非常不同的一种编程思路。




### 5、小总结

​	比较了BIO，NIO，NIO2的设计思路，在我看来，以烤串店为例（假设只有一个卖串口。在大东北有些热闹片区，外面就有这样的小店）

- **BIO：**烤肉店老板雇了很多员工，一个员工为一个顾客拿串串（那么小一个地方，哪能容得下那么多员工，效率太低了）
- **NIO：**烤肉店老板解雇了所有的员工，夫妻两人开店，丈夫烤肉，妻子到外面卖肉（减少了大量的人工成本，效率提高了不少）
- **NIO2：**自从有了美团，烤肉店老板常常接到网上订购烤串客户的电话，生意又好了不少。

所以要结合具体场景，选择是使用BIO，NIO还是NIO2，使系统效能达到更高，不能一概而论，但在理论上，对于高并发场景，NIO2效率更高。


## 三、参考文档

1、极客时间《Java核心技术36讲》第11讲

2、 [【java】IO详解之BIO](https://blog.csdn.net/u012250875/article/details/78341874?depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-1&utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-1)