## 理解Exception和Error（待跟进）

## 一、Throwable、Exception、Error 的设计和分类

### 1、Exception和Error的区别

- **`Exception` 和 `Error` 都是继承了 `Throwable` 类**，在 Java 中**只有` Throwable` 类型的实例才可以被抛出（throw）或者捕获（catch）**，它是异常处理机制的基本组成类型。
- `Exception` 和 `Error` 体现了 Java 平台设计者对不同异常情况的分类。`Exception` 是程序**正常运行**中，可以预料的意外情况，可能并且应该被捕获，进行相应处理。
- `Error` 是指在正常情况下，不大可能出现的情况，绝大部分的 `Error` 都会导致程序（比如 JVM自身）处于**非正常的**、**不可恢复状态**。既然是**非正常情况，所以不便于也不需要捕获**，常见的比如 `OutOfMemoryError` 之类，都是 `Error` 的子类
- `Exception` 又分为**检查型（checked）异常**和**非检查（unchecked）异常**，可检查异常**在源代码里必须显式地进行捕获处理**，这是**编译期检查的一部分**。
- **不检查异常**就是所谓的**运行时异常**，类似 **`NullPointerException`、`ArrayIndexOutOfBoundsException`** 之类，通常是可以编码避免的逻辑错误，具体根据需要来判断是否需要捕获，**并不会在编译期强制要求**。



### 2、经典题目

**Ⅰ、`NoClassDefFoundError`** 和**`ClassNotFoundException`** 有什么区别？

- **`NoClassDefFoundError`是一个错误(Error)，**而**`ClassNotFoundException`是一个异常**，在Java中对于错误和异常的处理是不同的，我们**可以从异常中恢复程序**但却**不应该尝试从错误中恢复程序**。

- **`ClassNotFoundException`的产生原因**：

  Java支持使用**Class.forName方法来动态地加载类**，任意一个类的类名如果被作为参数传递

  给这个方法都将导致**该类被加载到JVM内存**中，如果**这个类在类路径中没有被找到**，那么此时就会在运行时抛出`ClassNotFoundException`异常。

- **`NoClassDefFoundError`产生原因**：

  如果JVM或者**ClassLoader实例尝试加载**（可以通过正常的方法调用，也可能是使用new来创建新的对象）**类**的时候却**找不到类的定义**。要查找的类在**编译的时候是存在的，运行的时候却找不到了**。这个时候就会导致`NoClassDefFoundError`.

  造成该问题的原因可能是打包过程漏掉了部分类，或者**jar包出现损坏或者篡改**。解决这个问题的办法是查找那些在开发期间存在于类路径下但在运行期间却不在类路径下的类



**Ⅱ、**了解**哪些` Error`、`Exception` 或者`RuntimeException`**？

![2](..\images\java基础\2.jpg)

- **Error:**
  - LinkageError:
    - ![img](https://pic.rmb.bdstatic.com/023a8f8414cfabda8f3d3d99b0734b2e.png)
  - VirtualMachineError:虚拟机错误。用于指示虚拟机被破坏或者继续执行操作所需的资源不足的情况。
    - OutOfMemoryError: 内存溢出错误
    - StackOverflowError：栈溢出错误
- **Exception**
  - **检查型异常 (checked exception)**
    - IOException
    - ClassNotFoundException
    - InstantiationException
    - SQLException
  - **非检查型异常 (unchecked exception)**
    - RuntimeException
      - NullPointerException
      - ClassCastException
      - SecurityException
      - ArithmeticException
      - IndexOutOfBoundsException

**Ⅲ、异常方法 ：**

下面是 Throwable 类的主要方法:（[java.lang.Throwable](https://docs.oracle.com/javase/8/docs/api/index.html?java/lang/Exception.html)）

- ***public String getMessage()*** 返回关于发生的异常的详细信息
- ***public Throwable getCause()***：返回一个Throwable 对象代表异常原因
- ***public void printStackTrace()***：打印toString()结果和栈层次到System.err，即错误输出流。
- ***public String toString()***：Returns a short description of this throwable.



## 二、异常处理的实践

### 1、 try-catch-finally 块

```java
try {
    execute(); //exception might be thrown
} catch (IOException ex) {
    LOGGER.error(ex);
    throw new SpecialException();
} catch (SQLException ex) {
    LOGGER.error(ex);
    throw new SpecialException();
} 
```

- 在 finally 里面做一些资源回收工作。


- 这种处理方式使得代码过于繁琐，如果需要关闭的资源少一点还好，要是**关闭超过三个，代码就会比较繁琐**。

### 2、try-with-resources和multi-catch的使用

```java
try {
    execute(); //exception might be thrown
} catch (IOException | SQLExceptionex ex) {// Multiple catch
    LOGGER.log(ex);
    throw new SpecialException();
}
```

**语法如下：**

```java
try(  这里面的资源会自动关闭，前提是这些资源必须实现了Closeable接口或者AutoCloseable接口){

    //这里面是你的其他代码
} catch(捕获的异常){
    //打印异常信息
}
```

备注：

- 在编译时期，会自动生成相应的处理逻辑，

  比如，自动按照约定俗成 **close 那些扩展了 AutoCloseable 或者 Closeable 的对象**。

  

### 3、异常处理的基本原则

- 尽量**不要捕获**类似 **`Exception`** 这样的**通用异常**，而是**应该捕获特定异常**

  - 这是因为在日常的开发和合作中，我们**读代码的机会往往超过写代码**
  - 软件工程是门协作的艺术，所以我们**有义务让自己的代码能够直观地体现出尽量多的信息**，而泛泛的**`Exception`** 之类，恰恰隐藏了我们的目的。
  - 除非深思熟虑了，否则**不要捕获 `Throwable` 或者 `Error`**，这样很难保证我们能够正确程序处理**`OutOfMemoryError`** 。

- **不要生吞（swallow）异常**。

  - 如果我们不把异常抛出来，或者也没有输出到日志（Logger）之类，**程序可能在后续代码以不可控的方式结束。**没人能够轻易判断究竟是哪里抛出了异常，以及是什么原因产生了异常。

- **不要使用*e.printStackTrace()***输出异常

  - printStackTrace()的文档，开头就*“Prints this throwable and its backtrace to the standard error stream”*。问题就在这里，在稍微复杂一点的生产系统中，标准出错（STERR）不是个合适的输出选项，因为你**很难判断出到底输出到哪里去了**。
  - 尤其是**对于分布式系统**，如果发生异常，但是**无法找到堆栈轨迹**（stacktrace），这纯属是为诊断设置障碍。
  - **最好使用产品日志，详细地输出到日志系统里**。

- **Throw early, catch late 原则**：*"you should throw an exception as soon as you can, and catch it late as much as possible. You should wait until you have all the information to handle it properly."*

  - 看下面的代码段：

    ```java
    public void readPreferences(String fileName){
        //...perform operations...
        InputStream in = new FileInputStream(fileName);
        //...read the preferences file...
    }
    ```

    上段代码中如果 fileName 为 `null`，那么程序就会抛出 `NullPointerException`，但是由于没有第一时间暴露出问题，堆栈信息可能非常令人费解，往往需要相对复杂的定位。在发现问题的时候，第一时间抛出，能够更加清晰地反映问题。

    修改一下上面的代码，让问题 “throw early”，对应的异常信息就非常直观了。

    ```java
    public void readPreferences(String filename) {
        Objects. requireNonNull(filename);   // throw NullPointerException
        //...perform other operations...
        InputStream in = new FileInputStream(filename);
        //...read the preferences file...
    }
    ```

    上面这段代码使用了`Objects.requireNonNull()`方法，下面是它在`java.util.Objects`里的具体实现：

    ```java
    public static <T> T requireNonNull(T obj) {
            if (obj == null)
                throw new NullPointerException();
            return obj;
        }
    ```

    至于 `catch late`，捕获异常后，需要怎么处理呢？最差的处理方式，就是的“生吞异常”，本质上其实是掩盖问题。如果实在不知道如何处理，可以选择**保留原有异常的 `cause` 信息，直接再抛出或者构建新的异常抛出去**。在更高层面，因为有了清晰的（业务）逻辑，往往会更清楚合适的处理方式是什么。

### 4、异常处理的性能开销

- try-catch 代码段会产生额外的性能开销，或者换个角度说，它往往会影响 JVM 对代码进行优化，所以建议仅捕获有必要的代码段，**尽量不要一个大的 try 包住整段的代码**
- 与此同时，**利用异常控制代码流程，也不是一个好主意**，远比我们通常意义上的条件语句（if/else、switch）要低效。
- **Java 每实例化一个 Exception，都会对当时的栈进行快照**，这是一个相对比较重的操作。如果**发生的非常频繁，这个开销可就不能被忽略了**。



## 三、关于checked Exception的槽点

**1、反对者**

- 业界有一种争论（甚至可以算是某种程度的共识），Java 语言的 Checked Exception 也许是个Checked Exception 的假设是我们捕获了异常，然后恢复程序。但是，其实我们**大多数情况下，根本就不可能恢复**。Checked Exception 的使用，已经大大偏离了最初的设计目的。
- **Checked Exception 不兼容 functional 编程，如果你写过 Lambda/Stream 代码**，相信深有体会。很多开源项目，已经采纳了这种实践，比如 Spring、Hibernate 等，甚至反映在新的编程语言设计中，比如 Scala 等。 如果有兴趣，你可以参考：http://literatejava.com/exceptions/checked-exceptions-javas-biggest-mistake/。

**2、中立态度**

- 当然，很多人也觉得没有必要矫枉过正，因为确实有一些异常，**比如和环境相关的 IO、网络等，其实是存在可恢复性的**，而且 Java 已经通过业界的海量实践，证明了其构建高质量软件的能力。我就不再进一步解读了，感兴趣的同学可以[点击链接](https://v.qq.com/x/page/d0635rf5x0o.html?)，观看 Bruce Eckel 在 2018 年全球软件开发大会 QCon 的分享 Failing at Failing: How and Why We've Been NonchalantlyMoving Away From Exception Handling。





## 四、优质问答(知识拓展)

**Ⅰ、网友1**

- 1.异常：这种情况下的异常，可以通过**完善任务重试机制，当执行异常时，保存当前任务信息加入重试队列**。重试的策略根据业务需要决定，**当达到重试上限依然无法成功，记录任务执行失败，同时发出告警**。
- 2.日志：类比消息中间件，处在不同线程之间的同一任务，简单高效一点的做法可能是用traceId/requestId串联。有些日志系统本身支持MDC/NDC功能，可以串联相关联的日志。

**Ⅱ、网友2**

- 对于日志里面我们看到的往往是特定 executor 的堆栈，而不是业务方法调用关系这种情况，我在公司推行的是**自定义异常，自定义的异常有一个错误码**，这个错误码需要细到某个业务的某个方法的某种错，这样**排查问题会很方便**，但是写的时候就比较麻烦，文档也比较多

**Ⅲ、网友3**

- 1.Error:系统错误，虚拟机出错，我们处理不了，也不需要我们来处理。
- 2.Exception，可以捕获的异常，且作出处理。也就是要么捕获异常并作出处理，要么继续抛出异常。


- 3.RuntimeException，经常性出现的错误，可以捕获，并作出处理，可以不捕获，也可以不用抛出。ArrayIndexOutOfBoundsException像这种异常可以不捕获，为什么呢？在一个程序里，使用很多数组，如果使用一次捕获一次，则很累。

- 4.继承某个异常时，重写方法时，要么不抛出异常，要么抛出一模一样的异常。

- 5.当一个try后跟了很多个catch时，必须先捕获小的异常再捕获大的异常。

- 6.假如一个异常发生了，控制台打印了许多行信息，是因为程序中进行多层方法调用造成的。关键是看类型和行号。

- 7.上传下载不能抛异常。上传下载一定要关流。

  

## 五、参考文档

1、[[浅析Java异常处理机制](https://segmentfault.com/a/1190000017320437)](https://segmentfault.com/a/1190000017320437)

2、Exception和Error有什么区别？ - Java核心技术36讲