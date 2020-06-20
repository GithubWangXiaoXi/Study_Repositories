## 辨析final、finally、 finalize

## 一、考点分析

- 从**语法和使用实践角度**出发做出区别
- 以考察你对**性能**、**并发**、**对象生命周期**或**垃圾收集基本过程**等方面的理解



## 二、final、finally、 finalize的区别

### 1、final

- **final 可以用来修饰类、方法、变量，分别有不同的意义**，**final 修饰的 class 代表不可以继承扩展**，**final 的变量是不可以修改**的，而 **final 的方法也是不可以重写**的（override）。
- 推荐使用 final 关键字来明确表示我们代码的语义、逻辑意图，这已经被证明在很多场景下是非常好的实践，比如：
  - 我们可以将**方法或者类声明为 final**，这样就可以明确告知别人，**这些行为是不许修改的**。
    - 如果你关注过 Java 核心类库的定义或源码， 有没有发现 java.lang 包下面的很多类，相当一部分都被声明成为 **final class**？在第三方类库的一些基础类中同样如此，这可以**有效避免 API 使用者更改基础功能**，某种程度上，这是**保证平台安全**的必要手段。
  - 使用 **final 修饰参数**或者**变量**，也可以清楚地**避免意外赋值导致的编程错误**，甚至，有人明确**推荐将所有方法参数、本地变量、成员变量声明成 final**。
  - **final 变量**产生了某种程度的**不可变（immutable）的效果**，所以，可以用于保护只读数据，**尤其是在并发编程中**，因为明确地不能再赋值 final 变量，**有利于减少额外的同步开销**，也可以**省去一些防御性拷贝的必要**。

### 2、finally

- **finally 则是 Java 保证重点代码一定要被执行的一种机制**。我们可以使用 try-finally 或者 try-catch-finally 来进行类似关闭 JDBC 连接、保证 unlock 锁等动作。
- 对于 finally，明确知道怎么使用就足够了。
- 需要关闭的连接等资源，更推荐使用 Java 7 中添加的 **try-with-resources** 语句，因为通常 Java 平台能够更好地处理异常情况，编码量也要少很多，何乐而不为呢。

### 3、finalize

- **finalize 是基础类 java.lang.Object 的一个方法**，它的设计目的是保证对象在被垃圾收集前完成特定资源的回收。**finalize 机制现在已经不推荐使用**，并且在 **JDK 9 开始被标记为deprecated**。
- 如果没有特别的原因，不要实现finalize 方法，也**不要指望利用它来进行资源回收**。为什么呢？简单说，你无法保证 finalize 什么时候执行，执行的是否符合预期。**使用不当会影响性能，导致程序死锁、挂起**等。
- 如果确实需要额外处理，可以考虑 **Java 提供的 Cleaner 机制**或者其他替代方法

## 三、拓展知识

### 1、final和immutable的区别

```java
final List<String> strList = new ArrayList<>(); 
strList.add("Hello"); strList.add("world"); 
List<String> unmodifiableStrList = List.of("hello", "world"); 
unmodifiableStrList.add("again");
```

- **final 不等同于  immutable**:  **final** 只能**约束 strList 这个引用不可以被赋值**，但是 **strList 对象行为不被 final 影响**，添加元素等操作是完全正常的。
- 如果我们**真的希望对象本身是不可变**的，那么需要相应的类**支持不可变的行为**。在上面这个例子中，List.of 方法创建的本身就是不可变 List，**最后那句 add** 是会在运行时**抛出异常的，这才能保证strList为immutable类型**。
- Immutable 在很多场景是非常棒的选择，某种意义上说，**Java 语言目前并没有原生的不可变支持**，如果要**实现 immutable 的类**，我们需要做到：
  - 将 **class 自身声明为 final**，这样别人就不能扩展来绕过限制了。
  - 将所有成员变量定义为 private 和 final，并且**不要实现 setter** 方法。
  - 通常**构造对象**时，成员变量使用**深度拷贝来初始化**，而不是直接赋值，这是一种防御措施，因为你无法确定输入对象不被其他人修改。
  - 如果确实需要实现 getter 方法，或者其他可能会返回内部状态的方法，使用 **copy-on-write原则**，创建私有的 copy。这些原则是不是在并发编程实践中经常被提到？的确如此。

**备注：**

- 关于 **setter/getter 方法**，很多人喜欢直接用 IDE 一次全部生成，建议最好是你**确定有需要时再实现**。

  ​

### 2、finalize为何如此不堪

- finalize 还会掩盖资源回收时的出错信息，这里的**Throwable 是被生吞**了，也就意味着一旦出现异常或者出错，你得不到任何有效信息。

  ```java
  private void runFinalizer(JavaLangAccess jla) { 
    // ... 省略部分代码 
    try {
        Object finalizee = this.get(); 
        if (finalizee != null && !(finalizee instanceof java.lang.Enum)) {
  			jla.invokeFinalize(finalizee); 
          	 // Clear stack slot containing this variable, to decrease 
          	 // the chances of false retention with a conservative GC 
          	 finalizee = null; 
         } 
    } 
    catch (Throwable x) { 
      
    } 
    super.clear(); 
  }
  ```

- Java 平台目前在逐步使用` java.lang.ref.Cleaner` 来替换掉原有的 finalize 实现。**Cleaner 的实**

  **现利用了幻象引用（PhantomReference）**，这是一种常见的所谓 **post-mortem 清理机制**。

  我会在后面的专栏系统介绍 Java 的各种引用，利用幻象引用和引用队列，我们可以保证对象被

  彻底销毁前做一些类似资源回收的工作，比如关闭文件描述符（操作系统有限的资源），它**比**

  **finalize 更加轻量、更加可靠**。

  吸取了 finalize 里的教训，**每个 Cleaner 的操作都是独立的，它有自己的运行线程**，所以可以

  **避免意外死锁**等问题。

- 从可预测性的角度来判断，Cleaner 或者幻象引用改善的程度仍然是有限的，如果由于种

  种原因导致**幻象引用堆积，同样会出现问题**。所以，Cleaner 适合作为一种最后的保证手段，而

  不是完全依赖 Cleaner 进行资源回收，不然我们就要再做一遍 finalize 的噩梦了。