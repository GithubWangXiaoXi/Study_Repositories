## int和Integer有什么区别

### 一、考点分析

##### 1、考点

- **原始数据类型**和**包装类**

- **自动装箱**和**拆箱**机制

  

##### 2、常见问题

- Java使用的不同阶段：编译阶段、运行时, 而**自动装箱/自动拆箱 发生在什么阶段**？ 
- 静态工厂方法valueOf会使用到缓存机制，那么**自动装箱的时候，缓存机 制起作用吗**？ 
- **为什么我们需要原始数据类型**，java对象似乎也很高效，应用中具体会产生哪些异? 
- 阅读过**Integer源码**吗？分析下类或某些方法的设计要点。



### 二、知识拓展

##### 1、int和Integer有什么区别

- Java语言号称**一切都是对象，但原始数据类型除外**。
- 关于**Integer的值缓存**，构建Integer对象的传统方式是直接调用构造器，直接new一个对象。但是根据实践，我们发现大**部分数据操作都是集中在有限的较小的数值范围**。因而Java5中新增了**静态工厂方法valueOf**，在调用它的时候会利用一个**缓存机制**，带来明显的性能改进。这个值**默认缓存是-128到127**之间，而且该值可以修改 `-XX:AutoBoxCacheMax=N`。

##### 2、理解自动装箱、拆箱

- 比如整数，**javac**替我们自动把**装箱转换为Integer.valueOf()** ,把**拆箱替换为 Intege.intValue()** ,这似乎这也顺道回答了另一个可题,既然调用的是Integer.valueOf, 自然 能够到缓存的好处（可以通过反编译验证）

- 这种**缓存机制并不是只有Integer**才有，同样存在于其他的一些包装类，比如

  - **Boolean**：缓存true/false 对应实例，确切说，只会返回两个常量实例 Boolean.TRUE/FALSE。
  -  **Short** ：同样是缓存了 -128到127之间的数值。
  - **Byte** ：故值有限，所以全部都被缓存。
  - **Character**：缓存范围'\u0000`到'\u007F'。

- 原则上，**建议避免无意中的装箱、拆箱行为**，尤其是在性能敏感场合，创建10万个Java对 象和10万个整数的开销可不是一个数量级的,不管是内存使用还是处理速度，**光是对象头的空 间占用就已经是数量级的差距了**。

- **原始数据类型、数组**甚至本地代码实现等，在性能极度敏感的场景往往具有比较大的优势，用其**替换包装类，动态数组（ArrayList）**等可以作为性能优化的备选项。

  例如 以下代码，用long原始数据类型代替包装类Long，并保证线程安全。

  ```java
  class Counter {
    private final AtomicLong counter = new AtonicLong();
      public void increase() {
         counter.incrementAndGet();
      }
  } 
  ```

  ```java
  class CompactCounter {
    private volatile long counter;
    private static final AtomicLongFieldUpdater<CompactCounter> updater = AtomicLongFieldUpdater.newUpdater(CompactCounter.class,"counter")
    public void increase() {
      updater.incrementAndGet(this);
    }
  ```

##### 3、Integer源码分析

- **包装类里存储数值的成员变量"value"**（不管是Integer还是Boolean等），都被声明为“**private final**”，所以，它们同样是不可变类型。

- 举个例子

  ![11](..\..\images\java基础\11.jpg)



##### 4、原始数据类型线程安全

- 原始数据类型的变量，显然要使用并发相关手段，才能保证线程安全。建议考虑**AtomicInteger、AtomicLong线程安全类**
- 特别的是，**部分较宽**的数据类型，**比如float，double**，甚至**不能保证更新操作的原子性**，可能出现程序读取到只更新一半数据位的数值。



##### 5、Java原始数据类型和引用类型局限性

- **原始数据类型和java泛型并不能配合使用**

  ![9](..\..\images\java基础\9.jpg)

- **无法高效的表达数据**

  ![10](..\..\images\java基础\10.jpg)



##### 6、补充：java对象的内存结构是怎样的？

- 网友1 ![6](..\..\images\java基础\6.jpg)

- 网友2

  ![8](..\..\images\java基础\8.jpg)

- 网友3

  ![7](..\..\images\java基础\7.jpg)

  

  