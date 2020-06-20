## 深入理解Java高并发

原版图书链接  [Mastering_Concurrency_Programming_with_Java_8](https://book.douban.com/subject/26760497/)

遗留问题（过后解决）**

- 一.5.2）
- 一.5.5）
- 一.7.6）

### 一、并发的设计原则

#### 1、基础的并发概念

##### 1）基础概念

- **并发（Concurrency）：** 
  - 多任务在单核单CPU的调度下，似乎同时运行（在用户可接受的一段时间内）
  - 对于不同方法和机制的程序员，必须对共享资源进行**同步任务和同步访问权限**
- **并行（parallelism）：** 
  - **多任务**在不同的机器上，或者不同的处理器上（或核上），同一时刻同时运行
  - **同一任务不同实例**，在同一时刻同时运行在不同的数据集上。
- **同步（synchronization）：**
  - 任务B依赖于另一个任务A，只有当A运行后，B才可以运行
  - **引入同步可以解决并发出错问题**，但同时也带来了算法的开销
  - 但如果有**细粒度**的同步方法（小任务，高互通），由于同步带来的开销会很高，算法吞吐率会不好。
- **互斥（mutual exclusion）:**
  - 是一机制，该机制保证在同一时刻，只有一个任务访问**共享资源**。
  - 互斥有多种实现方法

##### 2）同步的方法

- **信号量**：
  - 可以控制对一个或多个单元的资源的访问控制
  - 需要有**一个变量**来存储可以访问资源的数目
  - 需要有**两个原子操作**来管理这个变量
  - 互斥锁mutex就是一个特殊的信号量，只有两个值（free和busy）
- **监视器：**
  - 可以互斥访问共享资源
  - 有一个**互斥锁mutex**，和一个**条件变量**，和两个操作（等待该条件（出阻塞队列）或者唤起该条件（入阻塞队列））

##### 3）线程安全

- 如果用户的共享数据由同步机制保护着，那么该代码片段（方法或对象）就是线程安全的
- 无阻塞的比较和交换原语（**compare-and-swap**  CAS），以及**数据的不可变性**（String），也是线程安全的    （不知理解是否正确）
- 区别CAS和volatile [CAS原理](https://www.jianshu.com/p/ab2c8fce878b)
- **原子变量**：是指通过**原子操作**去获得和设置值，该原子操作可以是**同步机制**，也可以是用**CAS的上锁-开锁**行为



#### 2、在并发应用中可能发生的问题

##### 1）资源竞争

##### 2）死锁

**死锁的必要条件：**

- **互斥：** 同一时刻只能有一个任务使用资源
- **请求和保持：** 一个任务在使用互斥资源的同时，请求另一个互斥资源
- **非抢占：**只有使用该资源的任务才可以去释放资源
- **环路等待：**任务A等待获取任务B中的资源，而任务B等待C中的资源，...，而任务N等待A的资源

**避免死锁的方法：** 

- **死锁忽视（ignore）：** 最常用的机制，认为死锁不会发生，如果发生，则重启应用
- **死锁检测与解除（Detection）：**如果分析检测到出现死锁，则可以采用完成该任务，或者强迫其资源释放
- **死锁预防（Prevention）：**破坏死锁的4个必要条件
- **死锁避免（Avoidance）：**通过分析比较该空闲资源与任务所需资源，判断该操作是否要启动 

更详细的避免死锁的方法请看 [死锁的四个必要条件和解决办法]( https://blog.csdn.net/guaiguaihenguai/article/details/80303835)

##### 3）资源饥饿

- 线程长时间不能得到该资源导致饿死
- 公平是解决饥饿的办法

##### 4）优先级抢占

- 高优先级的任务可以抢占低优先级任务的资源（Priority inversion）

#### 3、并发算法的设计

##### 起始：串行算法

- 利用**串行算法**，检测**该并发算法**是否根据输入的数据产生**正确的输出**

  检测**一系列并发算法**根据相同的输入是否产生**相同的输出**
- 计算两个算法的**吞吐量**，去比较并发算法是否改善了响应时间，或者是否在一定量的数据下及时处理完毕。

##### 1）分析

- 我们需要分析这些算法，去寻找可以并行运行的代码片段。
- 我们要特别关注那些**运行时间占很大部分**的代码（逻辑部分）
- 通过对这些**占很大时间的部分**进行**并发处理**，才能获得较好的性能。
- 好的例子是：这两部分**代码或步骤互相独立**的循环运行（比如建立数据库连接，加载配置文件，初始化一些对象，这些步骤相互不影响）

##### 2）设计

​	一旦知道哪些部分可以处理成并行之后，需要对其设计

- 代码的改变会影响应用的改变
  - 代码的结构
  - 数据结构的组织
- 两种方法改变代码
  - **任务的分解：**
    - 将代码**分解成2个或2个以上独立运行的任务**
    - 也许一些任务之间需要按一定顺序执行，或者必须等待相同时间（wait at the same point），那么必须有**同步机制**来处理。
  - **数据的分解：**
    - 当你拥有同一个任务的多个实例，并且该任务在**数据集的子集**工作时，那么**该数据是共享资源**，就有必要数据分解
    - 需要对共享数据的临界区进行保护
- 解决方案中的**粒度**也是重点
  - 使用所有可以使用的处理器和核数
  - 在使用同步机制时，会**引入额外的必须执行的指令**。
    - 如果切分的**粒度过细**，则额外代码同步时会使**性能退化**
    - 如果切分的**粒度过粗**，则**无法充分利用所有的资源**。
  - 在多线程处理任务时，一定要考虑**粗粒度和细粒度之间的平衡**

##### 3）实现

##### 4）测试

##### 5）调优

​	最后一步是比较**并行算法和顺序算法的吞吐量(throughput)** ，也可以去**比较不同参数**（粒度或者任务数量等）

**度量标准：**

- **加速比（SpeedUp）：** 
  $$
  SpeedUp = \frac{T_{sequential}}{T_{concurrency}}
  $$
  

  优化前系统耗时/优化后系统耗时。

- **Amdahl定律：** 计算并行计算的**最大预期改进**。

- **Gustafson-Barsis定律：** 

  - Amdahl定律有限制：在相同的数据集下增加核心数
  - 但通常情况下，**多核**你就想处理**更多数据**。

备注：

- 这两个定律从不同的角度诠释了加速比与**系统串行化程度**、**cpu核心数**之间的关系，它们是我们在做高并发程序设计时的理论依据。

详细请参考这  [Amdahl's law and Gustafson's law](https://blog.csdn.net/qq_34594236/article/details/79674204?depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-1&utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-1)

##### 6）小总结

- **并不是所有的算法都可以并行处理**。例如循环计数，该数依赖于之前的数，就不能对循环进行并行处理。
- 在设计并行算法之前，一定要有一个**好的性能的串行算法**为开始。
- 在设计并行算法时，要考虑以下指标：
  - **效率（Efficiency）：**  并行算法的结束时间一定要比串行算法的**时间更短**
  - **简单（Simplicity）：** 无论你是用的是并行还是串行算法，你必须**尽可能保证其简单。这将会方便实现，测试，调试和维护**。
  - **可移植性（Portability）：** 需要保证在其他平台上，小改一下也可以运行（java不用考虑这些）
  - **可拓展性（Scalability）：** 如果增加了核心数，该算法会发生什么。所以在**设计并行算法时，需要去利用所有可用的资源。**



#### 4、Java并发API

##### 1）基础并发类

- `Thread`类：该类代表执行并发程序的线程
- `Runnable`接口：另一种方式创建java并发程序
- `ThreadLocal`类：为thread**存储局部变量**的类
- `ThreadFactory`接口：是一种设计模式，可以创建**自定义的thread**

##### 2）同步机制

- 作用：
  - 定义访问共享资源的临界区
  - 在同一时间同步不同的任务
- `synchronized`关键字：可以定义**代码块**的临界区
- `Lock`接口：
  - 提供比`synchronized`更加灵活的同步操作（synchronization）
  - `ReentrantLock`实现了可以关联条件的Lock
  - `ReentrantReadWriteLock`将操作分成读和写操作
  - `StampedLock`是Java8的新特性，对于控制读写访问，包含3种模式。
- `Semaphore`类：该类实现了经典的信号量方法来实现同步问题。java支持**二进制或普通的信号量**。
- `CountDownLatch`类：该类允许任务等待多操作后的结束
- `CyclicBarrier`类：该类允许多线程同步在同一时间上。
- `Phaser`类：该类允许我们**将执行的任务划分成多个阶段**。没有任务可以提前到下一阶段直至所有任务都完成当前阶段

##### 3）执行器（Executors）

​	**执行器框架是一种机制**，该机制可以允许我们在实现并发任务时，将**线程创建和管理拆分开**来。

- `Executor`和`ExecutorService`接口：它们包含的方法和executors类似。
- `ThreadPoolExecutor` ：该类可以允许我们得到伴有**线程池的executor**，以及自定义**并行任务的最大数目**。
- `ScheduledThreadPoolExecutor` ：是特殊的executor，可以**延迟或者定期执行任务。**
- `Executors` ：该类简化了executor的创建
- `Callable`接口：可以**替代Runnable接口**，拆分的任务可以**返回值**
- `Future`接口：该接口**包含Callable接口的值的方法** ，并且该方法可以**控制该值的状态**。

##### 4）Fork/Join框架

​	Fork/Join框架定义了一种专门用来**解决分而治之问题的executor**

- `ForkJoinPool`  ：该类实现了跑多任务的executor
- `ForkJoinTask` ：该类是一个可以**在`ForkJoinPool`中执行**的任务。
- `ForkJoinWorkerThread`：该类是一个可以**在`ForkJoinPool`中执行**的线程。

##### 5）并行流（Parallel Streams）

​	流和Lamda表达式是java8的新特性。流作为一种方法添加到`Collection`接口和其他数据源上，并且允许处理数据结构的所有元素，生成新的结构，过滤数据和通过map和reduce来实现算法

​	并行流是一种特殊的流，可以实现并行操作。

- `Stream`接口：定义了**执行流的所有操作**
- `Optional`： 是一个容器对象，可能或不可能包含非空值
- `Collectors` ：该类实现了规约（reduce）操作，该操作可用来**对流序列的操作**
- Lamda表达式：流和lamda表达式一起工作。大部分**流接受lamda表达式作为参数**，进而实现更精简的操作

##### 6）并发数据结构

​	Java的ArrayList, Hashtable等不能实现并发编程除非使用外部同步机制，但是会带来额外计算开销。

​	如果你在多线程中修改了它们，会抛出异常（eg：`ConcurrentModificationException` 和
`ArrayIndexOutOfBoundsException`）

Java API中支持并发的数据结构分类： 

- **阻塞数据结构： **如果数据结构空但你想要值的时候，它拥有阻塞任务的方法
  - `LinkedBlockingDeque`: This is a blocking list
  - `LinkedBlockingQueue`： This is a blocking queue
  - `PriorityBlockingQueue` ：This is a blocking queue that orders its elements based on its priority
- **非阻塞数据结构：** 如果操作要立刻执行，则返回null或者抛异常
  - `ConcurrentLinkedDeque`: This is a non-blocking list
  - `ConcurrentLinkedQueue`: This is a non-blocking queue
  - `ConcurrentSkipListMap`: This is a non-blocking navigable map
  - `ConcurrentHashMap`: This is a non-blocking hash map
- Java基本类型的原子实现
  - `AtomicBoolean`, `AtomicInteger`, `AtomicLong`, 和 `AtomicReference`


#### 5、并发设计模式

​	在软件工程中，**设计模式**是普通问题的**一种解决方案**。这种方案被使用很多次，足够证明它是该问题的**最优解决方案**，你可以使用它，避免造轮子。

##### 1）唤起（Signaling）：

- 实现了一个任务**唤起另一个任务的事件**。
- 这里的section2一定是在section1之后执行

```java
public void task1(){
  section1();
  commonObject.notify();
}
public void task2(){
  commonObject.wait();
  section2();
}
```



##### 2）约会（Rendezvous）：

###### 概念：

- **唤起模式的一种泛化形式**，任务A等待任务B唤起某个事件，任务B等待A唤起某个事件

  [TensorFlow中的通信机制——Rendezvous（二）gRPC传输](https://www.cnblogs.com/deep-learning-stacks/p/10355770.html)

```java
public void task1(){
  section1_1();
  commonObject1.notify();
  commonObject2.wait();
  section1_2();
}
public void task2(){
  section2_1();
  commonObject2.notify();
  commonObject1.wait();
  section2_2();
}

-------------
感觉书中代码有点怪，有些时候会产生死锁，也会出现一个线程没有执行完。
个人觉得应该下面这种，可以执行完，但也有可能发生死锁；
public void task1(){
  section1_1();
  commonObject2.wait();
  commonObject1.notify();
  section1_2();
}
public void task2(){
  section2_1();
  commonObject2.notify();
  commonObject1.wait();
  section2_2();
}

```

###### 小实验：(以后回来验证)

- 实现A，B交替执行


- 注意**不是只有commonObject一个对象**，进行唤起、等待操作

- 假设只有一个对象，如果不对其进行同步操作（synchronized），以java8为例，会抛出`illigalMonitorStateException()`

  [诡异的java.lang.IllegalMonitorStateException](https://blog.csdn.net/historyasamirror/article/details/6709693)

  ```java
  public void task1() throws InterruptedException {
    System.out.println("section1_1");
    synchronized(commonObject){commonObject.notify();}
    synchronized(commonObject){commonObject.wait();}
    System.out.println("section1_2");
  }
  public void task2() throws InterruptedException {
    System.out.println("section2_1");
    synchronized(commonObject){commonObject.notify();}
    synchronized(commonObject){commonObject.wait();}
    System.out.println("section2_2");
  }

  ---
  输出结果
  section1_1
  section2_1
  section1_2
  （线程2一直等待）
  ```

- 假设有两个对象，**以Java8的Object对象的wait，notify方法为例** （事实上**应该用lock进行锁的释放和获取**）

  ```java
  public void task1() throws InterruptedException {
    System.out.println("section1_1");
    synchronized (commonObject1){
      System.out.println(Thread.currentThread().getName() + "唤起1");
      commonObject1.notify();
    }
    synchronized (commonObject2){
      System.out.println(Thread.currentThread().getName() + "等待2");
      commonObject2.wait();
    }
    System.out.println("section1_2");
  }
  public void task2() throws InterruptedException {
    System.out.println("section2_1");
    synchronized (commonObject2){
      System.out.println(Thread.currentThread().getName() + "唤起2");
      commonObject2.notify();
    }
    synchronized (commonObject1){
      System.out.println(Thread.currentThread().getName() + "等待1");
      commonObject1.wait();
    }
    System.out.println("section2_2");
  }
  ```

  - 如果A唤起对象1，而此时B没有等待对象1，则B永远得不到对象1；死锁

  - 如果B唤起对象2，而此时A没有等待对象2，则A永远得不到对象2；死锁

  - 如果A唤起对象1，此时B等待对象1，则B可以获得对象1；有一方结束

    真就验证了**约会随缘**

  ```java
  ---
  输出结果
  test1：
  section1_1
  Thread-0唤起1
  Thread-0等待2
  section2_1
  Thread-1唤起2
  Thread-1等待1
  section1_2  

  test2:
  section1_1
  section2_1
  Thread-0唤起1
  Thread-1唤起2
  Thread-1等待1
  Thread-0等待2
  （死锁）
  ```

- 如果使用lock的condition的await，signal方法，也会出现`illigalMonitorStateException()`  [ReentrantLock（二）：正确使用Condition实现等待与通知](https://blog.csdn.net/zhang199416/article/details/70771238)

  - 在使用内置监视器锁时，返回的 Condition 实例支持与 Object 的监视器方法（wait、notify 和 notifyAll）相同的用法。
  - 在Condition.await()方法调用之前使用lock.lock()获得同步监视器 

  ```java
  public void task1() throws InterruptedException {
        System.out.println("section1_1");

        lock.tryLock();
        System.out.println(Thread.currentThread().getName() + "唤起1");
        commonObject1.signal();
        lock.unlock();
        lock.tryLock();
      System.out.println(Thread.currentThread().getName() + "等待2");
      commonObject2.await();
      lock.unlock();
  
      System.out.println("section1_2");
  }
  public void task2() throws InterruptedException {
      System.out.println("section2_1");
      lock.tryLock();
      System.out.println(Thread.currentThread().getName() + "唤起2");
      commonObject2.signal();
      lock.unlock();
  
      //必须在Condition.await()方法调用之前使用lock.lock()获得同步监视器
      lock.tryLock();
      System.out.println(Thread.currentThread().getName() + "等待1");
      commonObject1.await();
      lock.unlock();
  
  	System.out.println("section2_2");
      
  ```



    
  }

------
  输出结果
  section1_1
  Thread-0唤起1
  Thread-0等待2
  section2_1
  Thread-1唤起2
  Thread-1等待1
  section1_2
  Thread-0等待2
  （Thread-0未结束）
  ```



##### 3）互斥锁（Mutex）：

- 互斥锁是一种可以**实现临界区，保证互斥**的一种机制
- java中，可以使用 `synchronized`，
  `ReentrantLock`类或者`Semaphore`类来实现互斥锁

​```java
public void task() {
  preCriticalSection();
  lockObject.lock() // The critical section begins
  criticalSection();
  lockObject.unlock(); // The critical section ends
  postCriticalSection();
}
  ```



##### 4）多元访问（Multiplex）：

- 是互斥锁的一种泛化
- 允许一定数量的任务在临界区同时执行（eg：有相同的**资源拷贝**）
- java中，使用`Semaphore`来**初始化任务的数量**

```java
public void task() {
  preCriticalSection();
  semaphoreObject.acquire();
  criticalSection();
  semaphoreObject.release();
  postCriticalSection();
}
```



##### 5）双重检查加锁（Double-checked locking）：

- 当你获得锁后，需要检查状态。如果状态会false，此时就会增加获得锁的开销
- **懒加载**时会用到该设计模式
- java中没有`Singleton`可以实现该模式，需要自己编写

法一：

```java
public class Singleton{
private Object reference;
  private Lock lock=new ReentrantLock();
  public Object getReference() {
    if (reference==null) {
      lock.lock();
      try {
        if (reference == null) {
          reference=new Object();
        }
      } finally {
        lock.unlock();
      }
    }
    return reference;
  }
}

```

如果两个任务同时判断条件，将会产生两个Object（疑问：不是加锁了吗，怎么可能会有两个任务同时检查判断？？？）



法二：

如果要**提高性能，则不要使用显性的同步机制**。

```java
class Singleton {
    private static class LazySingleton {
        private static final Singleton INSTANCE = new Singleton();
    }
    public static Singleton getSingleton() {
        return LazySingleton.INSTANCE;
    }
}
```

##### 6）读写锁（Read-write lock）

- **普通锁对于读操作来说太影响性能**，因为并发读是没有问题的
- 读写锁内部有两把锁，一把处理读，一把处理写
- 主要操作如下
  - A正在读，B想读，可以
  - A正在读，B想写，不可以，直到所有任务读完为止
  - A正在写，B想写，不可以，直到该任务写完为止
- java8中的` ReentrantReadWriteLock`可以实现该模式
- 使用时需要**认真考虑读写的优先级**，如果太多读任务，写任务会等很久

##### 7）线程池（Thread pool）

- 为了减少为任务创建线程的开销
- 线程集合**一般是固定数量**，它会到等待队列中去获取任务并执行，不会摧毁线程
- java8中用`ExecutorService`来实现该模式

##### 8）线程局部存储器（Thread local storage）

- 该模式为任务定义了如何**局部地使用全局或静态的变量**。
- 对于一个类的静态变量，所有的类对象有可能同时访问该变量，如果使用Thread local storage，每个线程都会获得**该变量的不同的实例**。
- java8中用`ThreadLocal`来实现该模式



#### 6、Java内存模型

##### 1）缓存，指令重排带来的问题

- **缓存**可以有效的增加应用的性能，但是它会导致数据的不一致性。当一个任务**在缓存中修改**变量的值，**没有及时写回主内存**。那么**其他任务**读的值也许是更新之前的**旧的值**。
- 为了提高应用的性能，编译器和代码优化器对**代码指令**进行**重排**优化。在串行应用中，这不会发生问题，但是在并发应用中，会引起意料之外的结果。

为了解决这些问题，编程语言引入内存模型，

- 该模型描述**独立的任务之间**如何**通过主存来通信**，**当一个任务导致主存某一数据发生变化**，该**变化对其他任务可见（visible to another）**。
- 该模型还定义了**什么代码的优化是被允许**的，以及在哪**些场合是被允许**的。

##### 2）内存模型的种类

​	有些比较**严格**（所有任务总可以访问同样的值），有些**不那么严格**（只有一些指令可以更新主存中的值）

​	java的原始内存模型存在一些问题，后来在java5重新定义。该模型和java8相同，定义在JSR133。基础定义如下

-  定义了关键字`volatile`, `synchronized`, 和 `final` 的行为。
- **保证同步并发程序**在该架构（JMM + JVM）上运行正确，不用考虑操作系统，CPU架构核数等
- 创建了一种命名为“**之前发生（happens-before）**“的`volatile read`, `volatile write`,` lock`, 和 `unlock`的命令的偏序关系
- 如果一个事件在另一个之前发生，那么前一个是可见的，并且顺序在后者之前。
- 如果一个任务**获得监视器**（monitor），那么**缓存是无效**的。
- 如果一个任务**释放监视器**（monitor），那么**缓存中的值会flush到主内存**中
- 对编码者透明

  

#### 7、并发设计的小技巧

##### 1）识别正确的独立任务

**不适合：**

- 如果你有多个任务，这些任务有顺序依赖性，也许你**没有兴趣去并发执行**它们，也**没有兴趣用同步机制**去保证它们的顺序。让它们串行运行即可。
- 如果是**循环，则不能使用并发**，因为所有的步骤产生的数据依赖于前一个步骤，或者存在某些状态信息从某一步到另一步。

**适合：**

- 如果这些任务有一些先决条件（ prerequisites

  ），并且这些**先决条件彼此相互独立**，那么可以**并发运行**这些先决条件，然后使用**同步机制**来控制在完成所有先决条件之后的任务的运行。

  

##### 2）高水准机制实现并发

- Java并发API中，我们可以使用`Thread`，`Lock`类来创建和同步线程

- 同时它提供了**高水平的并发对象**，例如`executors` 和 `Fork/Join` 框架，允许我们**执行多并发的任务**。这些高水平的并发机制有如下好处：

  - 你不用担心线程的创建和管理（Java API做的事），你**只需创建任务**，并**将它们发送给execution**即可。
  - 它比直接使用线程有**更高的性能**。例如线程池
  - 有**高级特征**使API功能更强大。例如使用executors，你能**获取任务的返回值**，封装在`Future`对象中。
  - 应用有**更好的移植性和可扩展性**。
  - 在未来的Java版本中，应用也许会更快，因为**Java 的内核，JVM的优化**，会使JDK API更加合身（tailored）

- 总之，在**实现并发算法之前一定要先分析Java API提供的高水平的同步机制。**

  

##### 3）考虑可扩展性

- 当你使用并发算法时，主要的**目的是为了利用计算机的所有资源**，特别是**处理器和核数的数量**。但是这些资源的数目也许会改变。

- 当你通过**分解数据**设计并发算法时，**不要提前假设该应用将会执行的处理器和核数的数量**。而是动态使用系统信息，例如使用Java的`Runtime.getRuntime().availableProcessors())`来获取处理器数，并利用它计算要执行的任务的个数。**虽然这么做会带来开销，但提高了算法的可扩展性**。

- 当你通过**分解任务**设计并发算法时，这种情况会更加困难，你需要**依赖独立任务的数量**，而且如果分解的**任务数量过多会增加同步机制带来的开销，**系统的全局性能会更加糟糕。

  所以需要认真分析算法决定是否**使用动态的任务数量**。



##### 4）使用线程安全（thread-safe）的API

- 如果有线程安全的API，直接用；如果没有，加上必要的同步机制，特别是在资源竞争的时候。
- 例如要使用list，而**ArrayList线程不安全**，所以**优先使用线程安全的list**，`ConcurrentLinkedDeque`,`CopyOnWriteArrayList`, 或者 `LinkedBlockingDeque`



##### 5）不要假设执行顺序

- 任务的执行顺序依赖于处理机的调度。

- 假设的结果常用来处理资源竞争的问题。而算法的最终结果依赖于任务的执行顺序。

  **很难去检测**资源竞争条件的原因，所以**必须认真仔细，不要忘了加上所有必要的同步元素**。

  

##### 6）宁愿使用局部线程变量

[ThreadLocal理解及应用](https://blog.csdn.net/zzg1229059735/article/details/82715741)

[ThreadLocal](https://www.jianshu.com/p/3c5d7f09dfbd)

​	相比静态和共享变量，宁愿使用局部线程变量

- 使用`ThreadLocal`类保证**每一个线程**能够不通过锁，信号量等类来**访问自己的实例变量**。而是通过为每个线程单独一份存储空间，**牺牲空间来解决冲突，不存在竞争关系**。

- ThreadLocal中保存着Thread_id，每个**Thread中有ThreadLocalMap**，用来存储线程的所有局部变量，而**ThreadLocal负责访问和维护ThreadLocalMap**。

- 另一种使用方法是采用` ConcurrentHashMap<Thread, MyType>`，并用`var.put(Thread.currentThread(), newValue)`来**绑定线程和值**。但存在竞争，效率比`ThreadLocal`低。

  但它也有好处，就是可以完全**清理掉map，使得Thread中的value消失**。

  疑问：ThreadLocal与之对比，为什么没有这个效果，用得不好会发生[内存泄漏](https://baijiahao.baidu.com/s?id=1633148445526799229&wfr=spider&for=pc)？？

  参考[ThreadLocal理解及应用](https://blog.csdn.net/zzg1229059735/article/details/82715741)

  

##### 7）寻找更加简单的并行算法

- 对于同样的问题，往往有不同的方法。有些算法更快，有些使用更少的资源，有些适合特殊的输入数据（例如归并排序）
- 在设计并行算法之前，建议**先设计串行算法**
  - 可以检测并行算法的正确性
  - 可以衡量并行算法带来的性能改进
- **并非所有的算法都可以并行**，或者说不简单！！！**所以最好的开始是，在设计串行算法时，还要考虑到（该算法的）并行处理的最优效能和吞吐量，并选出合适的串行算法**。



##### 8）尽量使用不可变对象

- 在处理资源竞争的问题时，特别是对于面向对象的语言来说，每个对象都有get，set。多线程操作会出现数据不一致。而**不可变对象一旦初始化，就不能修改，如果修改它，就会产生新的对象**（eg：String类，+=会产生新的String）

- 在并发应用中使用不可变对象的好处

  - 你**无需同步机制**去保护该类该方法。如果多个任务修改同一个值，**会产生新的对象**。所以不存在多任务同时对同一个对象进行操作
  - 不存在数据不一致性的问题

- 同时，它有缺点。如果产生**太多的对象**，这会**影响吞吐量和内存使用**。

  如果**简单的对象没有内部数据结构，则通常无需让其不可变（immutable）**。

  让和其他对象不合并的集合对象变成不可变型，会带来严重性能问题



##### 9）锁的顺序使用时避免死锁

- 最好避免死锁的机制是使**所有任务按照相同的顺序访问共享资源**。最简单的方法是**为资源赋值**。当**一个任务需要多个资源**时，需要**按顺序获取该资源**（例如先访问R1资源，再访问R2资源）。

  ```java
  //不会发生死锁
  public void operation1() {
  lock1.lock();
  lock2.lock();
  ….
  }
  public void operation2() {
  lock1.lock();
  lock2.lock();
  …..
  }
  ```

- 如果T1先访问R1，再访问R2，而T2先访问R2，再访问R1，就会死锁



##### 10）能使用原子变量不要用同步机制

- 在一些情况下，使用**volatile**，而不使用同步机制，例如只有**一个写，多个读**的时候。

  而其他场景，使用`lock`, `synchronized`
  或其他同步方法。

- java5中，API提供源自变量，支持变量的原子操作，它们有一个方法` compareAndSet(oldValue, newValue)`，该机制可以**检测该值是否已经被赋上新的值**。如果该值和原来的值不同，则将该值变新，并返回true。

  还有其他原子性方法：`getAndIncrement() `和`getAndDecrement()`。

- 该方法是“**不使用锁（*lock-free*）**”的，所以性能优于同步机制

- 常见的原子变量

  - `AtomicInteger`
  - `AtomicLong`
  - `AtomicReference`
  - `AtomicBoolean`
  - `LongAdder`
  - `DoubleAdder`

  

##### 11）竟可能短时间上锁

- **锁**和同步机制一样，**可以定义一个临界区**，只允许同一时刻一个任务运行此处，**其他任务只能阻塞**在这，等待锁的释放。

- 为了不退化应用的性能，必须**使临界区尽可能的小**，只有和其他任务共享的资源的指令才必须上锁。

- **避免执行临界区中你无法控制的代码**。例如，你想将数据写入数据库中，并等待用户自定义的Callable，但你不知道Callable中究竟是什么，也许会阻塞输入输出。

  对你而言，如果该算法必须这么做的话，那么在库文档中具体化这个行为，并且**限制用户提供的代码（例如它无需使用锁）**， 	`ConcurrentHashMap`类中的compute()是个好的文档例子

  

##### 12）利用懒加载来预防

- 懒加载：延迟对象创建直到你第一次要使用该对象。
- **懒加载在并发应用中会出问题**：多个任务同时调用该对象的初始化方法。
- 这个问题已得到解决，请见[Initialization-on-demand holder idiom](https://en.wikipedia.org/wiki/Initialization-on-demand_holder_idiom)



##### 13）在临界区中避免阻塞操作

- **临界区内**任务在等待I/O输入而**阻塞**，而**临界区外**的任务在等待临界区资源而**阻塞**，会**降低系统的性能**。

