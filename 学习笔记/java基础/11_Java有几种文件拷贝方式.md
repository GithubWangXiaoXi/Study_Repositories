## Java有几种文件拷贝方式

## 一、考点分析

### 1、考察方向

- **不同的copy**方式，**底层机制**有什么区别？ 
- 为什么**零拷贝**(zero-copy)可能有**性能优势**? 
- **Buffer分类与使用** 。
- **Direct Buffer**对**垃圾收集**等方面的影响与实践选择。



**备注：**

- **NIO不止多路复用，NIO2也不只是异步IO**



### 2、典型回答

**java有多种比较典型的文件拷贝实现方式：**

- 利用**java.io**类库，直接为源文件构建一个**FilelnputStream读取**，然后再为目标文件构建一个 **FileOutputStream ,完成写入工作**。
- 利用**java.nio**类库提供的**transferTo**或**transferFrom**方法实现
- 对于Copy的效率，**理论上来说**，NIO transferTo/From的方式可能更快（**从实践角度**，并没有明确说NIO transfer的方案最快，真实情况也确实未必如此），因为它更能利用现代操作系统底层机制，**避免不必要拷贝 和上下文切换**。



## 二、知识拓展

### 1、拷贝实践机制分析

- 当我们使用输入输出流逬行读写时，实际上是进行了**多次上下文切换**。比如应用读取数据时,先 在**内核态将数据从磁盘读取到内核缓存**，再**切换到用户态**将数据从内核缓存**读取到用户缓存**。 写入操作也是类似，仅仅是步骤相反。

  ![23](..\..\images\java基础\23.png)

- 而基于NIO transferTo的实现方式，在Linux和Unix上，则会使用到**零拷贝**技术，**数据传输 并不需要用户态参与，省去了上下文切换的开销和不必要的内存拷贝** ，进而可能提高应用拷贝性 能。注意，**transferTo**不仅仅是可以用在**文件拷贝**中，与其类似的，例如读取磁盘文件，然后 **进行Socket发送**，同样可以享受这种机制带来的性能和扩展性提高。[零拷贝](https://www.jianshu.com/p/275602182f39)

  ![24](..\..\images\java基础\24.png)



### 2、Java IO/NIO源码结构

##### 不同的copy方式的底层机制：

```java
private static long copy(InputStream source, OutputStream sink)
        throws IOException
```

```java
public static long copy(InputStream in, Path target, CopyOption... options)
        throws IOException
```

```java
public static long copy(Path source, OutputStream out) throws IOException
```

- **后面两种copy**实现，能  够在方法实现里直接看到使用的是**InputStream.transferTo()** (应该是java8以后的版本才有)

- **copy不仅仅是支持文件之间操作**，没有人限定输入输出流一定是针对文件的，这时两个很实用的工具方法。

  

##### 如何提高类似拷贝等IO操作的性能：

有一些宽泛的原则：

-  在程序中，**使用缓存**等机制，合理**减少IO次数**（在网络通信中，如TCP传输，window大 小也可以看作是类似思路）。
- 使用**transferTo**等机制，**减少上下文切换**和额外IO操作。 
- 尽量**减少不必要的转换过程**，比如编解码；对象序列化和反序列化，比如操作文本文件或者 网络通信，**如果不是过程中需要使用文本信息**,可以考虑不要将二进制信息转换成字符串，**直接传输二进制信息**，

### 3、掌握NIO Buffer

##### 使用Buffer的重要性：

- **Buffer是NIO操作数据的基本工具** 。Java为每种**原始数据类型都提供了相应 的Buffer**实现（布尔除外），所以掌握和使用Buffer是十分必要的。

  ![25](..\..\images\java基础\25.png)

- 尤其是涉及**Direct Buffer**等使用，因为其在**垃圾收集**等方面的特殊性，更要重点掌握。

##### Buffer几个基本属性：

-  **capcity**： 它反映这个Buffer到底有多大，也就是**数组的长度**。

- **position**：要操作的数据起始位置。

- **limit**：相当于操作的限额。在读取或者写入时，limit的意义很明显是不一样的。比如,读取 操作时，很可能将limit设置到所容数据的上限；而在写入时，则会设置容量或容量以下的可写限度 。

- **mark** ：记录**上一次postion的位置**，默认是0,算是—便利性的考虑，往往不是必须的。

  

##### Buffer的基本操作:

-  我们创建了一个ByteBuffer，准备放入数据， capcity当然就是缓冲区大小，而position就 是0 , limit默认就是capcity的大小.。

- 当我们写入几个字节的数据时，**position**就会跟着水涨船高，但是它**不可能超过limit**的大 小。

- 如果我们想**把前面写入的数据读出来**，需要调用**flip()**，将**position设置为0 , limit设 置为以前的position那里**。

- 如果还想从头再读一遍，可以调用**rewind()** ,让limit不变，position再次设置为0。

  

### 4、Direct Buffer和垃圾收集

##### Direct Buffer（堆外缓存）

- 如果我们看Buffer的方法定义，你会发现它定义了 **isDirect()**方法，**返回当 前Buffer是否是Direct类型** 。这是因为Java提供**了堆内和堆外(Direct) Buffer** ，我们可 以以它的allocate或者allocateDirect方法直接创建 



##### MappedByteBuffer:

- 它将文件按照指定大小直接映射为内存区域，当**程序访问**这个内存区 域时将**直接操作这块儿文件数据**，省去了将数据从内核空间向用户空间传输的损耗。我们可 以**使用FileChannel.map创建 MappedByteBuffer** ，**它本质上也是种 Direct Buffer** 。



##### Direct Buffer的优势

- Java会尽量对Direct Buffer仅做本地IO 操作，对于很多**大数据量的IO密集操作**,可能会带来非常大的性能优势，因为：  
  - Direct Buffer生命周期内**内存地址都不会再发生更改**，进而**内核可以安全地对其进行访问**， 很多IO操作会很高效。
  -  **减少了堆内对象存储**的可能**额外维护**工作,所以访问效率可能有所提高。
- 但是请注意，Direct Buffer创建和销毁过程中，都会比一般的的堆内Buffer増加部分开销，所以 **通常都建议Direct Buffer用于长期使用、数据较大的场景。**



##### Direct Buffer和垃圾收集

- 使用Direct Buffer,我们需要清楚它对内存和JVM参数的影响。首先，因为它不在堆上，所以 **Xmx**之类参数，其实并**不能影响Direct Buffer**等堆外成员的内存额度，我们可以使用下面参数设置大小: -XX:MaxDirectMemorySize=512M 

  [JVM参数调优总结请看这](https://blog.csdn.net/unixboy_xujf/article/details/83224043?depth_1-utm_source=distribute.pc_relevant.none-task-blog-OPENSEARCH-1&utm_source=distribute.pc_relevant.none-task-blog-OPENSEARCH-1)

- 从参数设置和内存问题排査角度来看，这意味着我们在计算Java可以使用的内存大小的时候， 不能只考虑堆的需要，还有Direct Buffer等一系列堆外因素。如果**岀现内存不足，堆外内存占 用也是一种可能性**。

- 另外，大多数垃圾收集过程中，都**不会主动收集Direct Buffer**，它的垃圾收集过程，就是基于 **Cleaner (一个内部实现)和幻象引用(Phantom Reference )机制**，其本身不是public类型，内部实现了一个Deallocator负责销毁的逻辑。对它的销毁往往要拖到 full GC的时候。所以使用不当很容易袒导致OutOfMemoryError.

- 对于Direct Buffer的回收的几个建议: 

  - 在应用程序中，显式地调用System.gc()来强制触发。 

  - 另外一种思路是，在大量使用Direct Buffer的部分框架中，**框架会自己在程序中调用释放方 法**，Netty就是这么做的，有兴趣可以参考其实现(PlatformDependent0 )。

  -  重复使用 Direct Buffer。

    

### 5、跟踪和诊断Direct Buffer内存占用

- 因为通常的**垃圾收集日志等记录，并不包含Direct Buffer等信息**，所以Direct Buffer内存诊 断也是个比较头疼的事情。幸好，在JDK 8之后的版本，我们可以方便地使用**Native Memory Tracking ( NMT)**	特性来进行诊断，你可以在程序启动时加上下面参数：

  ```java
  -XX:NativeMemoryTracking={summary|detail)
  ```

- 注意，激活NMT通常都会导致JVM出现5%~10%的性能下降，请谨慎考虑。运行时，可以采用下面命令进行交互式対比： 

  ```java
  //打印NMT信息
  jcmd <pid> VM.native_memory detail

  //进行baseline，以对比分配内存变化
  jcmd <pid> VM.native_memnory baseline

  //进行baseline,以对比分配内存変化
  jcmd <pid> VM.native_memory detail.diff
  ```

  我们可以在Internal部分发现Direct Buffer内存使用的信息，这是因为其底层实际是利用 unsafe_allocatememory.严格说,这**不是JVM内部使用的内存**。所以在JDK11以后，其实 它是**归类在other部分**里。

  [Java调试工具](https://blog.csdn.net/notbaron/article/details/76284046)



**备注：**

- JVM的**堆外内存远不止Direct Buffer**, NMT输出的信息当然也远不止这些。



## 三、问答环节

**Q：**如果我们需要在channel读取 的过程中,将不同片段写入到相应的Buffer里面（类似二进制**消息分拆成消息头、消息体** 等），可以采用NIO的什么机制做到呢？

**A：**可以利用**NIO分散-scatter机制**来写入不同buffer。

 Code: 

ByteBuffer header = ByteBuffer.allocate(128); 

ByteBuffer body = ByteBuffer.allocate(1024);

 ByteBuffer bufferArray = {header, body); 

channel.read(bufferArray); 

注意: 该方法适用于请求头长度固定



## 四、参考文档

1、极客时间《Java核心技术36讲》第12讲

2、[零拷贝](https://www.jianshu.com/p/275602182f39)

3、[NIO中的heap Buffer和direct Buffer区别](https://www.cnblogs.com/winner-0715/p/8590910.html)

4、[初探Java的Buffer类](https://blog.csdn.net/czx2018/article/details/89502699)

