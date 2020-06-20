## JVM知识点总结

转载于https://blog.csdn.net/huyuyang6688/article/details/81490570

本文是学习了《深入理解Java虚拟机》之后的总结，主要内容都来自于书中，也有作者的一些理解。一是为了梳理知识点，归纳总结，二是为了分享交流，如有错误之处还望指出。（本文以jdk1.7的规范为基础）。

文章对JVM内存区域分布、JVM内存溢出分析、JVM垃圾回收算法/垃圾收集器、JVM性能调优工具及技巧、类加载等部分做了详细描述。

用XMind画了一张导图（源文件对部分节点有详细备注和参考资料，需要的朋友可以扫描二维码直接回复“JVM思维导图”获取，）：






一、JVM内存区域
Java虚拟机在运行时，会把内存空间分为若干个区域，根据《Java虚拟机规范（Java SE 7 版）》的规定，Java虚拟机所管理的内存区域分为如下部分：方法区、堆内存、虚拟机栈、本地方法栈、程序计数器。


1、方法区
方法区主要用于存储虚拟机加载的类信息、常量、静态变量，以及编译器编译后的代码等数据。在jdk1.7及其之前，方法区是堆的一个“逻辑部分”（一片连续的堆空间），但为了与堆做区分，方法区还有个名字叫“非堆”，也有人用“永久代”（HotSpot对方法区的实现方法）来表示方法区。

从jdk1.7已经开始准备“去永久代”的规划，jdk1.7的HotSpot中，已经把原本放在方法区中的静态变量、字符串常量池等移到堆内存中，（常量池除字符串常量池还有class常量池等），这里只是把字符串常量池移到堆内存中；在jdk1.8中，方法区已经不存在，原方法区中存储的类信息、编译后的代码数据等已经移动到了元空间（MetaSpace）中，元空间并没有处于堆内存上，而是直接占用的本地内存（NativeMemory）。根据网上的资料结合自己的理解对jdk1.3~1.6、jdk1.7、jdk1.8中方法区的变迁画了张图如下（如有不合理的地方希望读者指出）：

去永久代的原因有：
（1）字符串存在永久代中，容易出现性能问题和内存溢出。
（2）类及方法的信息等比较难确定其大小，因此对于永久代的大小指定比较困难，太小容易出现永久代溢出，太大则容易导致老年代溢出。
（3）永久代会为 GC 带来不必要的复杂度，并且回收效率偏低。

2、堆内存
堆内存主要用于存放对象和数组，它是JVM管理的内存中最大的一块区域，堆内存和方法区都被所有线程共享，在虚拟机启动时创建。在垃圾收集的层面上来看，由于现在收集器基本上都采用分代收集算法，因此堆还可以分为新生代（YoungGeneration）和老年代（OldGeneration），新生代还可以分为Eden、From Survivor、To Survivor。

3、程序计数器
程序计数器是一块非常小的内存空间，可以看做是当前线程执行字节码的行号指示器，每个线程都有一个独立的程序计数器，因此程序计数器是线程私有的一块空间，此外，程序计数器是Java虚拟机规定的唯一不会发生内存溢出的区域。

4、虚拟机栈
虚拟机栈也是每个线程私有的一块内存空间，它描述的是方法的内存模型，直接看下图所示：

虚拟机会为每个线程分配一个虚拟机栈，每个虚拟机栈中都有若干个栈帧，每个栈帧中存储了局部变量表、操作数栈、动态链接、返回地址等。一个栈帧就对应Java代码中的一个方法，当线程执行到一个方法时，就代表这个方法对应的栈帧已经进入虚拟机栈并且处于栈顶的位置，每一个Java方法从被调用到执行结束，就对应了一个栈帧从入栈到出栈的过程。

5、本地方法栈
本地方法栈与虚拟机栈的区别是，虚拟机栈执行的是Java方法，本地方法栈执行的是本地方法（Native Method）,其他基本上一致，在HotSpot中直接把本地方法栈和虚拟机栈合二为一，这里暂时不做过多叙述。

6、元空间
上面说到，jdk1.8中，已经不存在永久代（方法区），替代它的一块空间叫做“元空间”，和永久代类似，都是JVM规范对方法区的实现，但是元空间并不在虚拟机中，而是使用本地内存，元空间的大小仅受本地内存限制，但可以通过-XX:MetaspaceSize和-XX:MaxMetaspaceSize来指定元空间的大小。


二、JVM内存溢出
1、堆内存溢出
堆内存中主要存放对象、数组等，只要不断地创建这些对象，并且保证GC Roots到对象之间有可达路径来避免垃圾收集回收机制清除这些对象，当这些对象所占空间超过最大堆容量时，就会产生OutOfMemoryError的异常。堆内存异常示例如下：

/**
 * 设置最大堆最小堆：-Xms20m -Xmx20m
 * 运行时，不断在堆中创建OOMObject类的实例对象，且while执行结束之前，GC Roots(代码中的oomObjectList)到对象(每一个OOMObject对象)之间有可达路径，垃圾收集器就无法回收它们，最终导致内存溢出。
    */
    public class HeapOOM {
    static class OOMObject {
    }
    public static void main(String[] args) {
        List<OOMObject> oomObjectList = new ArrayList<>();
        while (true) {
            oomObjectList.add(new OOMObject());
        }
    }
    }
    运行后会报异常，在堆栈信息中可以看到 java.lang.OutOfMemoryError: Java heap space 的信息，说明在堆内存空间产生内存溢出的异常。

新产生的对象最初分配在新生代，新生代满后会进行一次Minor GC，如果Minor GC后空间不足会把该对象和新生代满足条件的对象放入老年代，老年代空间不足时会进行Full GC，之后如果空间还不足以存放新对象则抛出OutOfMemoryError异常。常见原因：内存中加载的数据过多如一次从数据库中取出过多数据；集合对对象引用过多且使用完后没有清空；代码中存在死循环或循环产生过多重复对象；堆内存分配不合理；网络连接问题、数据库问题等。

2、虚拟机栈/本地方法栈溢出
（1）StackOverflowError：当线程请求的栈的深度大于虚拟机所允许的最大深度，则抛出StackOverflowError，简单理解就是虚拟机栈中的栈帧数量过多（一个线程嵌套调用的方法数量过多）时，就会抛出StackOverflowError异常。最常见的场景就是方法无限递归调用，如下：

/**
 * 设置每个线程的栈大小：-Xss256k
 * 运行时，不断调用doSomething()方法，main线程不断创建栈帧并入栈，导致栈的深度越来越大，最终导致栈溢出。
    */
    public class StackSOF {
    private int stackLength=1;
    public void doSomething(){
            stackLength++;
            doSomething();
    }
    public static void main(String[] args) {
        StackSOF stackSOF=new StackSOF();
        try {
            stackSOF.doSomething();
        }catch (Throwable e){//注意捕获的是Throwable
            System.out.println("栈深度："+stackSOF.stackLength);
            throw e;
        }
    }
    }
    ​
    上述代码执行后抛出：Exception in thread “Thread-0” java.lang.StackOverflowError的异常。

（2）OutOfMemoryError：如果虚拟机在扩展栈时无法申请到足够的内存空间，则抛出OutOfMemoryError。我们可以这样理解，虚拟机中可以供栈占用的空间≈可用物理内存 - 最大堆内存 - 最大方法区内存，比如一台机器内存为4G，系统和其他应用占用2G，虚拟机可用的物理内存为2G，最大堆内存为1G，最大方法区内存为512M，那可供栈占有的内存大约就是512M，假如我们设置每个线程栈的大小为1M，那虚拟机中最多可以创建512个线程，超过512个线程再创建就没有空间可以给栈了，就报OutOfMemoryError异常了。

栈上能够产生OutOfMemoryError的示例如下：

/**
 * 设置每个线程的栈大小：-Xss2m
 * 运行时，不断创建新的线程（且每个线程持续执行），每个线程对一个一个栈，最终没有多余的空间来为新的线程分配，导致OutOfMemoryError
    */
    public class StackOOM {
    private static int threadNum = 0;
    public void doSomething() {
        try {
            Thread.sleep(100000000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
    public static void main(String[] args) {
        final StackOOM stackOOM = new StackOOM();
        try {
            while (true) {
                threadNum++;
                Thread thread = new Thread(new Runnable() {
                    @Override
                    public void run() {
                        stackOOM.doSomething();
                    }
                });
                thread.start();
            }
        } catch (Throwable e) {
            System.out.println("目前活动线程数量：" + threadNum);
            throw e;
        }
    }
    }
    ​
    上述代码运行后会报异常，在堆栈信息中可以看到 java.lang.OutOfMemoryError: unable to create new native thread的信息，无法创建新的线程，说明是在扩展栈的时候产生的内存溢出异常。

总结：在线程较少的时候，某个线程请求深度过大，会报StackOverflow异常，解决这种问题可以适当加大栈的深度（增加栈空间大小），也就是把-Xss的值设置大一些，但一般情况下是代码问题的可能性较大；在虚拟机产生线程时，无法为该线程申请栈空间了，会报OutOfMemoryError异常，解决这种问题可以适当减小栈的深度，也就是把-Xss的值设置小一些，每个线程占用的空间小了，总空间一定就能容纳更多的线程，但是操作系统对一个进程的线程数有限制，经验值在3000~5000左右。在jdk1.5之前-Xss默认是256k，jdk1.5之后默认是1M，这个选项对系统硬性还是蛮大的，设置时要根据实际情况，谨慎操作。

3、方法区溢出
前面说到，方法区主要用于存储虚拟机加载的类信息、常量、静态变量，以及编译器编译后的代码等数据，所以方法区溢出的原因就是没有足够的内存来存放这些数据。

由于在jdk1.6之前字符串常量池是存在于方法区中的，所以基于jdk1.6之前的虚拟机，可以通过不断产生不一致的字符串（同时要保证和GC Roots之间保证有可达路径）来模拟方法区的OutOfMemoryError异常；但方法区还存储加载的类信息，所以基于jdk1.7的虚拟机，可以通过动态不断创建大量的类来模拟方法区溢出。

/**
 * 设置方法区最大、最小空间：-XX:PermSize=10m -XX:MaxPermSize=10m
 * 运行时，通过cglib不断创建JavaMethodAreaOOM的子类，方法区中类信息越来越多，最终没有可以为新的类分配的内存导致内存溢出
    */
    public class JavaMethodAreaOOM {
    public static void main(final String[] args){
       try {
           while (true){
               Enhancer enhancer=new Enhancer();
               enhancer.setSuperclass(JavaMethodAreaOOM.class);
               enhancer.setUseCache(false);
               enhancer.setCallback(new MethodInterceptor() {
                   @Override
                   public Object intercept(Object o, Method method, Object[] objects, MethodProxy methodProxy) throws Throwable {
                       return methodProxy.invokeSuper(o,objects);
                   }
               });
               enhancer.create();
           }
       }catch (Throwable t){
           t.printStackTrace();
       }
    }
    }
    ​
    上述代码运行后会报“java.lang.OutOfMemoryError: PermGen space”的异常，说明是在方法区出现了内存溢出的错误。

4、本机直接内存溢出
本机直接内存（DirectMemory）并不是虚拟机运行时数据区的一部分，也不是Java虚拟机规范中定义的内存区域，但Java中用到NIO相关操作时（比如ByteBuffer的allocteDirect方法申请的是本机直接内存），也可能会出现内存溢出的异常。


三、JVM垃圾回收
垃圾回收，就是通过垃圾收集器把内存中没用的对象清理掉。垃圾回收涉及到的内容有：1、判断对象是否已死；2、选择垃圾收集算法；3、选择垃圾收集的时间；4、选择适当的垃圾收集器清理垃圾（已死的对象）。

1、判断对象是否已死
判断对象是否已死就是找出哪些对象是已经死掉的，以后不会再用到的，就像地上有废纸、饮料瓶和百元大钞，扫地前要先判断出地上废纸和饮料瓶是垃圾，百元大钞不是垃圾。判断对象是否已死有引用计数算法和可达性分析算法。

（1）引用计数算法

给每一个对象添加一个引用计数器，每当有一个地方引用它时，计数器值加1；每当有一个地方不再引用它时，计数器值减1，这样只要计数器的值不为0，就说明还有地方引用它，它就不是无用的对象。如下图，对象2有1个引用，它的引用计数器值为1，对象1有两个地方引用，它的引用计数器值为2 。


这种方法看起来非常简单，但目前许多主流的虚拟机都没有选用这种算法来管理内存，原因就是当某些对象之间互相引用时，无法判断出这些对象是否已死，如下图，对象1和对象2都没有被堆外的变量引用，而是被对方互相引用，这时他们虽然没有用处了，但是引用计数器的值仍然是1，无法判断他们是死对象，垃圾回收器也就无法回收。



（2）可达性分析算法

了解可达性分析算法之前先了解一个概念——GC Roots，垃圾收集的起点，可以作为GC Roots的有虚拟机栈中本地变量表中引用的对象、方法区中静态属性引用的对象、方法区中常量引用的对象、本地方法栈中JNI（Native方法）引用的对象。
当一个对象到GC Roots没有任何引用链相连（GC Roots到这个对象不可达）时，就说明此对象是不可用的，是死对象。如下图：object1、object2、object3、object4和GC Roots之间有可达路径，这些对象不会被回收，但object5、object6、object7到GC Roots之间没有可达路径，这些对象就被判了死刑。

上面被判了死刑的对象（object5、object6、object7）并不是必死无疑，还有挽救的余地。进行可达性分析后对象和GC Roots之间没有引用链相连时，对象将会被进行一次标记，接着会判断如果对象没有覆盖Object的finalize()方法或者finalize()方法已经被虚拟机调用过，那么它们就会被行刑（清除）；如果对象覆盖了finalize()方法且还没有被调用，则会执行finalize()方法中的内容，所以在finalize()方法中如果重新与GC Roots引用链上的对象关联就可以拯救自己，但是一般不建议这么做，周志明老师也建议大家完全可以忘掉这个方法~

（3）方法区回收

上面说的都是对堆内存中对象的判断，方法区中主要回收的是废弃的常量和无用的类。
判断常量是否废弃可以判断是否有地方引用这个常量，如果没有引用则为废弃的常量。
判断类是否废弃需要同时满足如下条件：

该类所有的实例已经被回收（堆中不存在任何该类的实例）

加载该类的ClassLoader已经被回收

该类对应的java.lang.Class对象在任何地方没有被引用（无法通过反射访问该类的方法）

2、常用垃圾回收算法
常用的垃圾回收算法有三种：标记-清除算法、复制算法、标记-整理算法。

（1）标记-清除算法：分为标记和清除两个阶段，首先标记出所有需要回收的对象，标记完成后统一回收所有被标记的对象，如下图。

缺点：标记和清除两个过程效率都不高；标记清除之后会产生大量不连续的内存碎片。


（2）复制算法：把内存分为大小相等的两块，每次存储只用其中一块，当这一块用完了，就把存活的对象全部复制到另一块上，同时把使用过的这块内存空间全部清理掉，往复循环，如下图。

缺点：实际可使用的内存空间缩小为原来的一半，比较适合。


（3）标记-整理算法：先对可用的对象进行标记，然后所有被标记的对象向一段移动，最后清除可用对象边界以外的内存，如下图。


（4）分代收集算法：把堆内存分为新生代和老年代，新生代又分为Eden区、From Survivor和To Survivor。一般新生代中的对象基本上都是朝生夕灭的，每次只有少量对象存活，因此采用复制算法，只需要复制那些少量存活的对象就可以完成垃圾收集；老年代中的对象存活率较高，就采用标记-清除和标记-整理算法来进行回收。


在这些区域的垃圾回收大概有如下几种情况：

大多数情况下，新的对象都分配在Eden区，当Eden区没有空间进行分配时，将进行一次Minor GC，清理Eden区中的无用对象。清理后，Eden和From Survivor中的存活对象如果小于To Survivor的可用空间则进入To Survivor，否则直接进入老年代）；Eden和From Survivor中还存活且能够进入To Survivor的对象年龄增加1岁（虚拟机为每个对象定义了一个年龄计数器，每执行一次Minor GC年龄加1），当存活对象的年龄到达一定程度（默认15岁）后进入老年代，可以通过-XX:MaxTenuringThreshold来设置年龄的值。

当进行了Minor GC后，Eden还不足以为新对象分配空间（那这个新对象肯定很大），新对象直接进入老年代。

占To Survivor空间一半以上且年龄相等的对象，大于等于该年龄的对象直接进入老年代，比如Survivor空间是10M，有几个年龄为4的对象占用总空间已经超过5M，则年龄大于等于4的对象都直接进入老年代，不需要等到MaxTenuringThreshold指定的岁数。

在进行Minor GC之前，会判断老年代最大连续可用空间是否大于新生代所有对象总空间，如果大于，说明Minor GC是安全的，否则会判断是否允许担保失败，如果允许，判断老年代最大连续可用空间是否大于历次晋升到老年代的对象的平均大小，如果大于，则执行Minor GC，否则执行Full GC。

当在java代码里直接调用System.gc()时，会建议JVM进行Full GC，但一般情况下都会触发Full GC，一般不建议使用，尽量让虚拟机自己管理GC的策略。

永久代（方法区）中用于存放类信息，jdk1.6及之前的版本永久代中还存储常量、静态变量等，当永久代的空间不足时，也会触发Full GC，如果经过Full GC还无法满足永久代存放新数据的需求，就会抛出永久代的内存溢出异常。

大对象（需要大量连续内存的对象）例如很长的数组，会直接进入老年代，如果老年代没有足够的连续大空间来存放，则会进行Full GC。

3、选择垃圾收集的时间
当程序运行时，各种数据、对象、线程、内存等都时刻在发生变化，当下达垃圾收集命令后就立刻进行收集吗？肯定不是。这里来了解两个概念：安全点(safepoint)和安全区(safe region)。
安全点：从线程角度看，安全点可以理解为是在代码执行过程中的一些特殊位置，当线程执行到安全点的时候，说明虚拟机当前的状态是安全的，如果有需要，可以在这里暂停用户线程。当垃圾收集时，如果需要暂停当前的用户线程，但用户线程当时没在安全点上，则应该等待这些线程执行到安全点再暂停。举个例子，妈妈在扫地，儿子在吃西瓜（瓜皮会扔到地上），妈妈扫到儿子跟前时，儿子说：“妈妈等一下，让我吃完这块再扫。”儿子吃完这块西瓜把瓜皮扔到地上后就是一个安全点，妈妈可以继续扫地（垃圾收集器可以继续收集垃圾）。理论上，解释器的每条字节码的边界上都可以放一个安全点，实际上，安全点基本上以“是否具有让程序长时间执行的特征”为标准进行选定。
安全区：安全点是相对于运行中的线程来说的，对于如sleep或blocked等状态的线程，收集器不会等待这些线程被分配CPU时间，这时候只要线程处于安全区中，就可以算是安全的。安全区就是在一段代码片段中，引用关系不会发生变化，可以看作是被扩展、拉长了的安全点。还以上面的例子说明，妈妈在扫地，儿子在吃西瓜（瓜皮会扔到地上），妈妈扫到儿子跟前时，儿子说：“妈妈你继续扫地吧，我还得吃10分钟呢！”儿子吃瓜的这段时间就是安全区，妈妈可以继续扫地（垃圾收集器可以继续收集垃圾）。

4、常见垃圾收集器
现在常见的垃圾收集器有如下几种

新生代收集器：Serial、ParNew、Parallel Scavenge

老年代收集器：Serial Old、CMS、Parallel Old

堆内存垃圾收集器：G1

每种垃圾收集器之间有连线，表示他们可以搭配使用。


（1）Serial 收集器

Serial是一款用于新生代的单线程收集器，采用复制算法进行垃圾收集。Serial进行垃圾收集时，不仅只用一条线程执行垃圾收集工作，它在收集的同时，所有的用户线程必须暂停（Stop The World）。就比如妈妈在家打扫卫生的时候，肯定不会边打扫边让儿子往地上乱扔纸屑，否则一边制造垃圾，一遍清理垃圾，这活啥时候也干不完。
如下是Serial收集器和Serial Old收集器结合进行垃圾收集的示意图，当用户线程都执行到安全点时，所有线程暂停执行，Serial收集器以单线程，采用复制算法进行垃圾收集工作，收集完之后，用户线程继续开始执行。


适用场景：Client模式（桌面应用）；单核服务器。可以用-XX:+UserSerialGC来选择Serial作为新生代收集器。

2）ParNew 收集器

ParNew就是一个Serial的多线程版本，其它与Serial并无区别。ParNew在单核CPU环境并不会比Serial收集器达到更好的效果，它默认开启的收集线程数和CPU数量一致，可以通过-XX:ParallelGCThreads来设置垃圾收集的线程数。
如下是ParNew收集器和Serial Old收集器结合进行垃圾收集的示意图，当用户线程都执行到安全点时，所有线程暂停执行，ParNew收集器以多线程，采用复制算法进行垃圾收集工作，收集完之后，用户线程继续开始执行。

适用场景：多核服务器；与CMS收集器搭配使用。当使用-XX:+UserConcMarkSweepGC来选择CMS作为老年代收集器时，新生代收集器默认就是ParNew，也可以用-XX:+UseParNewGC来指定使用ParNew作为新生代收集器。

（3）Parallel Scavenge 收集器

Parallel Scavenge也是一款用于新生代的多线程收集器，与ParNew的不同之处是，ParNew的目标是尽可能缩短垃圾收集时用户线程的停顿时间，Parallel Scavenge的目标是达到一个可控制的吞吐量。吞吐量就是CPU执行用户线程的的时间与CPU执行总时间的比值【吞吐量=运行用户代代码时间/（运行用户代码时间+垃圾收集时间）】，比如虚拟机一共运行了100分钟，其中垃圾收集花费了1分钟，那吞吐量就是99% 。比如下面两个场景，垃圾收集器每100秒收集一次，每次停顿10秒，和垃圾收集器每50秒收集一次，每次停顿时间7秒，虽然后者每次停顿时间变短了，但是总体吞吐量变低了，CPU总体利用率变低了。

收集频率	每次停顿时间	吞吐量
每100秒收集一次	10秒	91%
每50秒收集一次	7秒	88%
可以通过-XX:MaxGCPauseMillis来设置收集器尽可能在多长时间内完成内存回收，可以通过-XX:GCTimeRatio来精确控制吞吐量。

如下是Parallel收集器和Parallel Old收集器结合进行垃圾收集的示意图，在新生代，当用户线程都执行到安全点时，所有线程暂停执行，ParNew收集器以多线程，采用复制算法进行垃圾收集工作，收集完之后，用户线程继续开始执行；在老年代，当用户线程都执行到安全点时，所有线程暂停执行，Parallel Old收集器以多线程，采用标记整理算法进行垃圾收集工作。

适用场景：注重吞吐量，高效利用CPU，需要高效运算且不需要太多交互。可以使用-XX:+UseParallelGC来选择Parallel Scavenge作为新生代收集器，jdk7、jdk8默认使用Parallel Scavenge作为新生代收集器。

（4）Serial Old收集器

Serial Old收集器是Serial的老年代版本，同样是一个单线程收集器，采用标记-整理算法。

如下图是Serial收集器和Serial Old收集器结合进行垃圾收集的示意图：

适用场景：Client模式（桌面应用）；单核服务器；与Parallel Scavenge收集器搭配；作为CMS收集器的后备预案。

（5）CMS(Concurrent Mark Sweep) 收集器

CMS收集器是一种以最短回收停顿时间为目标的收集器，以“最短用户线程停顿时间”著称。整个垃圾收集过程分为4个步骤：

① 初始标记：标记一下GC Roots能直接关联到的对象，速度较快
② 并发标记：进行GC Roots Tracing，标记出全部的垃圾对象，耗时较长
③ 重新标记：修正并发标记阶段引用户程序继续运行而导致变化的对象的标记记录，耗时较短
④ 并发清除：用标记-清除算法清除垃圾对象，耗时较长

整个过程耗时最长的并发标记和并发清除都是和用户线程一起工作，所以从总体上来说，CMS收集器垃圾收集可以看做是和用户线程并发执行的。

CMS收集器也存在一些缺点：

对CPU资源敏感：默认分配的垃圾收集线程数为（CPU数+3）/4，随着CPU数量下降，占用CPU资源越多，吞吐量越小

无法处理浮动垃圾：在并发清理阶段，由于用户线程还在运行，还会不断产生新的垃圾，CMS收集器无法在当次收集中清除这部分垃圾。同时由于在垃圾收集阶段用户线程也在并发执行，CMS收集器不能像其他收集器那样等老年代被填满时再进行收集，需要预留一部分空间提供用户线程运行使用。当CMS运行时，预留的内存空间无法满足用户线程的需要，就会出现“Concurrent Mode Failure”的错误，这时将会启动后备预案，临时用Serial Old来重新进行老年代的垃圾收集。

因为CMS是基于标记-清除算法，所以垃圾回收后会产生空间碎片，可以通过-XX:UserCMSCompactAtFullCollection开启碎片整理（默认开启），在CMS进行Full GC之前，会进行内存碎片的整理。还可以用-XX:CMSFullGCsBeforeCompaction设置执行多少次不压缩（不进行碎片整理）的Full GC之后，跟着来一次带压缩（碎片整理）的Full GC。
适用场景：重视服务器响应速度，要求系统停顿时间最短。可以使用-XX:+UserConMarkSweepGC来选择CMS作为老年代收集器。

（6）Parallel Old 收集器

Parallel Old收集器是Parallel Scavenge的老年代版本，是一个多线程收集器，采用标记-整理算法。可以与Parallel Scavenge收集器搭配，可以充分利用多核CPU的计算能力。

适用场景：与Parallel Scavenge收集器搭配使用；注重吞吐量。jdk7、jdk8默认使用该收集器作为老年代收集器，使用 -XX:+UseParallelOldGC来指定使用Paralle Old收集器。

（7）G1 收集器

G1 收集器是jdk1.7才正式引用的商用收集器，现在已经成为jdk9默认的收集器。前面几款收集器收集的范围都是新生代或者老年代，G1进行垃圾收集的范围是整个堆内存，它采用“化整为零”的思路，把整个堆内存划分为多个大小相等的独立区域（Region），在G1收集器中还保留着新生代和老年代的概念，它们分别都是一部分Region，如下图：

每一个方块就是一个区域，每个区域可能是Eden、Survivor、老年代，每种区域的数量也不一定。JVM启动时会自动设置每个区域的大小（1M~32M，必须是2的次幂），最多可以设置2048个区域（即支持的最大堆内存为32M*2048=64G），假如设置-Xmx8g -Xms8g，则每个区域大小为8g/2048=4M。

为了在GC Roots Tracing的时候避免扫描全堆，在每个Region中，都有一个Remembered Set来实时记录该区域内的引用类型数据与其他区域数据的引用关系（在前面的几款分代收集中，新生代、老年代中也有一个Remembered Set来实时记录与其他区域的引用关系），在标记时直接参考这些引用关系就可以知道这些对象是否应该被清除，而不用扫描全堆的数据。

G1收集器可以“建立可预测的停顿时间模型”，它维护了一个列表用于记录每个Region回收的价值大小（回收后获得的空间大小以及回收所需时间的经验值），这样可以保证G1收集器在有限的时间内可以获得最大的回收效率。

如下图所示，G1收集器收集器收集过程有初始标记、并发标记、最终标记、筛选回收，和CMS收集器前几步的收集过程很相似：

① 初始标记：标记出GC Roots直接关联的对象，这个阶段速度较快，需要停止用户线程，单线程执行
② 并发标记：从GC Root开始对堆中的对象进行可达新分析，找出存活对象，这个阶段耗时较长，但可以和用户线程并发执行
③ 最终标记：修正在并发标记阶段引用户程序执行而产生变动的标记记录
④ 筛选回收：筛选回收阶段会对各个Region的回收价值和成本进行排序，根据用户所期望的GC停顿时间来指定回收计划（用最少的时间来回收包含垃圾最多的区域，这就是Garbage First的由来——第一时间清理垃圾最多的区块），这里为了提高回收效率，并没有采用和用户线程并发执行的方式，而是停顿用户线程。

适用场景：要求尽可能可控GC停顿时间；内存占用较大的应用。可以用-XX:+UseG1GC使用G1收集器，jdk9默认使用G1收集器。

四、JVM性能调优
1、JVM调优目标：使用较小的内存占用来获得较高的吞吐量或者较低的延迟。
程序在上线前的测试或运行中有时会出现一些大大小小的JVM问题，比如cpu load过高、请求延迟、tps降低等，甚至出现内存泄漏（每次垃圾收集使用的时间越来越长，垃圾收集频率越来越高，每次垃圾收集清理掉的垃圾数据越来越少）、内存溢出导致系统崩溃，因此需要对JVM进行调优，使得程序在正常运行的前提下，获得更高的用户体验和运行效率。

这里有几个比较重要的指标：

内存占用：程序正常运行需要的内存大小。

延迟：由于垃圾收集而引起的程序停顿时间。

吞吐量：用户程序运行时间占用户程序和垃圾收集占用总时间的比值。

当然，和CAP原则一样，同时满足一个程序内存占用小、延迟低、高吞吐量是不可能的，程序的目标不同，调优时所考虑的方向也不同，在调优之前，必须要结合实际场景，有明确的的优化目标，找到性能瓶颈，对瓶颈有针对性的优化，最后进行测试，通过各种监控工具确认调优后的结果是否符合目标。

2、JVM调优工具

（1）调优可以依赖、参考的数据有系统运行日志、堆栈错误信息、gc日志、线程快照、堆转储快照等。

① 系统运行日志：系统运行日志就是在程序代码中打印出的日志，描述了代码级别的系统运行轨迹（执行的方法、入参、返回值等），一般系统出现问题，系统运行日志是首先要查看的日志。

② 堆栈错误信息：当系统出现异常后，可以根据堆栈信息初步定位问题所在，比如根据“java.lang.OutOfMemoryError: Java heap space”可以判断是堆内存溢出；根据“java.lang.StackOverflowError”可以判断是栈溢出；根据“java.lang.OutOfMemoryError: PermGen space”可以判断是方法区溢出等。

③ GC日志：程序启动时用 -XX:+PrintGCDetails 和 -Xloggc:/data/jvm/gc.log 可以在程序运行时把gc的详细过程记录下来，或者直接配置“-verbose:gc”参数把gc日志打印到控制台，通过记录的gc日志可以分析每块内存区域gc的频率、时间等，从而发现问题，进行有针对性的优化。
比如如下一段GC日志：

2018-08-02T14:39:11.560-0800: 10.171: [GC [PSYoungGen: 30128K->4091K(30208K)] 51092K->50790K(98816K), 0.0140970 secs] [Times: user=0.02 sys=0.03, real=0.01 secs] 
2018-08-02T14:39:11.574-0800: 10.185: [Full GC [PSYoungGen: 4091K->0K(30208K)] [ParOldGen: 46698K->50669K(68608K)] 50790K->50669K(98816K) [PSPermGen: 2635K->2634K(21504K)], 0.0160030 secs] [Times: user=0.03 sys=0.00, real=0.02 secs] 
2018-08-02T14:39:14.045-0800: 12.656: [GC [PSYoungGen: 14097K->4064K(30208K)] 64766K->64536K(98816K), 0.0117690 secs] [Times: user=0.02 sys=0.01, real=0.01 secs] 
2018-08-02T14:39:14.057-0800: 12.668: [Full GC [PSYoungGen: 4064K->0K(30208K)] [ParOldGen: 60471K->401K(68608K)] 64536K->401K(98816K) [PSPermGen: 2634K->2634K(21504K)], 0.0102020 secs] [Times: user=0.01 sys=0.00, real=0.01 secs] 

上面一共是4条GC日志，来看第一行日志，“2018-08-02T14:39:11.560-0800”是精确到了毫秒级别的UTC 通用标准时间格式，配置了“-XX:+PrintGCDateStamps”这个参数可以跟随gc日志打印出这种时间戳，“10.171”是从JVM启动到发生gc经过的秒数。第一行日志正文开头的“[GC”说明这次GC没有发生Stop-The-World（用户线程停顿），第二行日志正文开头的“[Full GC”说明这次GC发生了Stop-The-World，所以说，[GC和[Full GC跟新生代和老年代没关系，和垃圾收集器的类型有关系，如果直接调用System.gc()，将显示[Full GC(System)。接下来的“[PSYoungGen”、“[ParOldGen”表示GC发生的区域，具体显示什么名字也跟垃圾收集器有关，比如这里的“[PSYoungGen”表示Parallel Scavenge收集器，“[ParOldGen”表示Serial Old收集器，此外，Serial收集器显示“[DefNew”，ParNew收集器显示“[ParNew”等。再往后的“30128K->4091K(30208K)”表示进行了这次gc后，该区域的内存使用空间由30128K减小到4091K，总内存大小为30208K。每个区域gc描述后面的“51092K->50790K(98816K), 0.0140970 secs”进行了这次垃圾收集后，整个堆内存的内存使用空间由51092K减小到50790K，整个堆内存总空间为98816K，gc耗时0.0140970秒。

④ 线程快照：顾名思义，根据线程快照可以看到线程在某一时刻的状态，当系统中可能存在请求超时、死循环、死锁等情况是，可以根据线程快照来进一步确定问题。通过执行虚拟机自带的“jstack pid”命令，可以dump出当前进程中线程的快照信息，更详细的使用和分析网上有很多例，这篇文章写到这里已经很长了就不过多叙述了，贴一篇博客供参考：http://www.cnblogs.com/kongzhongqijing/articles/3630264.html

⑤ 堆转储快照：程序启动时可以使用 “-XX:+HeapDumpOnOutOfMemory” 和 “-XX:HeapDumpPath=/data/jvm/dumpfile.hprof”，当程序发生内存溢出时，把当时的内存快照以文件形式进行转储（也可以直接用jmap命令转储程序运行时任意时刻的内存快照），事后对当时的内存使用情况进行分析。

（2）JVM调优工具

① 用 jps（JVM process Status）可以查看虚拟机启动的所有进程、执行主类的全名、JVM启动参数，比如当执行了JPSTest类中的main方法后（main方法持续执行），执行 jps -l可看到下面的JPSTest类的pid为31354，加上-v参数还可以看到JVM启动参数。

3265 
32914 sun.tools.jps.Jps
31353 org.jetbrains.jps.cmdline.Launcher
31354 com.danny.test.code.jvm.JPSTest
380 
1
2
3
4
5
② 用jstat（JVM Statistics Monitoring Tool）监视虚拟机信息
jstat -gc pid 500 10 ：每500毫秒打印一次Java堆状况（各个区的容量、使用容量、gc时间等信息），打印10次

S0C    S1C    S0U    S1U      EC       EU        OC         OU       MC     MU    CCSC   CCSU   YGC     YGCT    FGC    FGCT     GCT   
11264.0 11264.0 11202.7  0.0   11776.0   1154.3   68608.0    36238.7     -      -      -      -        14    0.077   7      0.049    0.126
11264.0 11264.0 11202.7  0.0   11776.0   4037.0   68608.0    36238.7     -      -      -      -        14    0.077   7      0.049    0.126
11264.0 11264.0 11202.7  0.0   11776.0   6604.5   68608.0    36238.7     -      -      -      -        14    0.077   7      0.049    0.126
11264.0 11264.0 11202.7  0.0   11776.0   9487.2   68608.0    36238.7     -      -      -      -        14    0.077   7      0.049    0.126
11264.0 11264.0  0.0    0.0   11776.0   258.1    68608.0    58983.4     -      -      -      -        15    0.082   8      0.059    0.141
11264.0 11264.0  0.0    0.0   11776.0   3076.8   68608.0    58983.4     -      -      -      -        15    0.082   8      0.059    0.141
11264.0 11264.0  0.0    0.0   11776.0    0.0     68608.0     390.0      -      -      -      -        16    0.084   9      0.066    0.149
11264.0 11264.0  0.0    0.0   11776.0    0.0     68608.0     390.0      -      -      -      -        16    0.084   9      0.066    0.149
11264.0 11264.0  0.0    0.0   11776.0   258.1    68608.0     390.0      -      -      -      -        16    0.084   9      0.066    0.149
11264.0 11264.0  0.0    0.0   11776.0   3012.8   68608.0     390.0      -      -      -      -        16    0.084   9      0.066    0.149

S0C：第一个幸存区的大小
S1C：第二个幸存区的大小
S0U：第一个幸存区的使用大小
S1U：第二个幸存区的使用大小
EC：伊甸园区的大小
EU：伊甸园区的使用大小
OC：老年代大小
OU：老年代使用大小
MC：方法区大小
MU：方法区使用大小
CCSC:压缩类空间大小
CCSU:压缩类空间使用大小
YGC：年轻代垃圾回收次数
YGCT：年轻代垃圾回收消耗时间
FGC：老年代垃圾回收次数
FGCT：老年代垃圾回收消耗时间
GCT：垃圾回收消耗总时间
jstat还可以以其他角度监视各区内存大小、监视类装载信息等，具体可以google jstat的详细用法。
jstat命令使用 https://www.cnblogs.com/lizhonghua34/p/7307139.html

③ 用jmap（Memory Map for Java）查看堆内存信息
执行jmap -histo pid可以打印出当前堆中所有每个类的实例数量和内存占用，如下，class name是每个类的类名（[B是byte类型，[C是char类型，[I是int类型），bytes是这个类的所有示例占用内存大小，instances是这个类的实例数量：

num     #instances         #bytes  class name
----------------------------------------------
   1:          2291       29274080  [B
   2:         15252        1961040  <methodKlass>
   3:         15252        1871400  <constMethodKlass>
   4:         18038         721520  java.util.TreeMap$Entry
   5:          6182         530088  [C
   6:         11391         273384  java.lang.Long
   7:          5576         267648  java.util.TreeMap
   8:            50         155872  [I
   9:          6124         146976  java.lang.String
  10:          3330         133200  java.util.LinkedHashMap$Entry
  11:          5544         133056  javax.management.openmbean.CompositeDataSupport

执行 jmap -dump 可以转储堆内存快照到指定文件，比如执行 jmap -dump:format=b,file=/data/jvm/dumpfile_jmap.hprof 3361 可以把当前堆内存的快照转储到dumpfile_jmap.hprof文件中，然后可以对内存快照进行分析。

④ 利用jconsole、jvisualvm分析内存信息(各个区如Eden、Survivor、Old等内存变化情况)，如果查看的是远程服务器的JVM，程序启动需要加上如下参数：

"-Dcom.sun.management.jmxremote=true" 
"-Djava.rmi.server.hostname=12.34.56.78" 
"-Dcom.sun.management.jmxremote.port=18181" 
"-Dcom.sun.management.jmxremote.authenticate=false" 
"-Dcom.sun.management.jmxremote.ssl=false"
1
2
3
4
5
下图是jconsole界面，概览选项可以观测堆内存使用量、线程数、类加载数和CPU占用率；内存选项可以查看堆中各个区域的内存使用量和左下角的详细描述（内存大小、GC情况等）；线程选项可以查看当前JVM加载的线程，查看每个线程的堆栈信息，还可以检测死锁；VM概要描述了虚拟机的各种详细参数。（jconsole功能演示）


下图是jvisualvm的界面，功能比jconsole略丰富一些，不过大部分功能都需要安装插件。概述跟jconsole的VM概要差不多，描述的是jvm的详细参数和程序启动参数；监视展示的和jconsole的概览界面差不多（CPU、堆/方法区、类加载、线程）；线程和jconsole的线程界面差不多；抽样器可以展示当前占用内存的类的排行榜及其实例的个数；Visual GC可以更丰富地展示当前各个区域的内存占用大小及历史信息（下图）。（jvisualvm功能演示）


⑤ 分析堆转储快照

前面说到配置了 “-XX:+HeapDumpOnOutOfMemory” 参数可以在程序发生内存溢出时dump出当前的内存快照，也可以用jmap命令随时dump出当时内存状态的快照信息，dump的内存快照一般是以.hprof为后缀的二进制格式文件。
可以直接用 jhat（JVM Heap Analysis Tool） 命令来分析内存快照，它的本质实际上内嵌了一个微型的服务器，可以通过浏览器来分析对应的内存快照，比如执行 jhat -port 9810 -J-Xmx4G /data/jvm/dumpfile_jmap.hprof 表示以9810端口启动 jhat 内嵌的服务器：

Reading from /Users/dannyhoo/data/jvm/dumpfile_jmap.hprof...
Dump file created Fri Aug 03 15:48:27 CST 2018
Snapshot read, resolving...
Resolving 276472 objects...
Chasing references, expect 55 dots.......................................................
Eliminating duplicate references.......................................................
Snapshot resolved.
Started HTTP server on port 9810
Server is ready.

在控制台可以看到服务器启动了，访问 http://127.0.0.1:9810/ 可以看到对快照中的每个类进行分析的结果（界面略low），下图是我随便选择了一个类的信息，有这个类的父类，加载这个类的类加载器和占用的空间大小，下面还有这个类的每个实例（References）及其内存地址和大小，点进去会显示这个实例的一些成员变量等信息：


jvisualvm也可以分析内存快照，在jvisualvm菜单的“文件”-“装入”，选择堆内存快照，快照中的信息就以图形界面展示出来了，如下，主要可以查看每个类占用的空间、实例的数量和实例的详情等：


还有很多分析内存快照的第三方工具，比如eclipse mat，它比jvisualvm功能更专业，出了查看每个类及对应实例占用的空间、数量，还可以查询对象之间的调用链，可以查看某个实例到GC Root之间的链，等等。可以在eclipse中安装mat插件，也可以下载独立的版本（http://www.eclipse.org/mat/downloads.php ），我在mac上安装后运行起来老卡死~下面是在windows上的截图（MAT功能演示）：



（3）JVM调优经验
垃圾收集器方面，Serial可以直接排除掉，现在最普通的服务器也有双核64位\8G内存，默认的收集器是PS Scavenge和PS MarkSweep。所以在并行(Parallel)和并发(Concurrent)两者之间选择。如果系统对峰值处理要求不高，而对一两秒的停顿可以接受，则使用(-XX:+UseParallelGC)；如果应用对响应有更高的要求，停顿最好小于一秒，则使用(-XX:+UseConcMarkSweepGC)。

JVM配置方面，一般情况可以先用默认配置（基本的一些初始参数可以保证一般的应用跑的比较稳定了），在测试中根据系统运行状况（会话并发情况、会话时间等），结合gc日志、内存监控、使用的垃圾收集器等进行合理的调整，当老年代内存过小时可能引起频繁Full GC，当内存过大时Full GC时间会特别长。

那么JVM的配置比如新生代、老年代应该配置多大最合适呢？答案是不一定，调优就是找答案的过程，物理内存一定的情况下，新生代设置越大，老年代就越小，Full GC频率就越高，但Full GC时间越短；相反新生代设置越小，老年代就越大，Full GC频率就越低，但每次Full GC消耗的时间越大。建议如下：

-Xms和-Xmx的值设置成相等，堆大小默认为-Xms指定的大小，默认空闲堆内存小于40%时，JVM会扩大堆到-Xmx指定的大小；空闲堆内存大于70%时，JVM会减小堆到-Xms指定的大小。如果在Full GC后满足不了内存需求会动态调整，这个阶段比较耗费资源。
新生代尽量设置大一些，让对象在新生代多存活一段时间，每次Minor GC 都要尽可能多的收集垃圾对象，防止或延迟对象进入老年代的机会，以减少应用程序发生Full GC的频率。
老年代如果使用CMS收集器，新生代可以不用太大，因为CMS的并行收集速度也很快，收集过程比较耗时的并发标记和并发清除阶段都可以与用户线程并发执行。
方法区大小的设置，1.6之前的需要考虑系统运行时动态增加的常量、静态变量等，1.7只要差不多能装下启动时和后期动态加载的类信息就行。
代码实现方面，性能出现问题比如程序等待、内存泄漏除了JVM配置可能存在问题，代码实现上也有很大关系：

避免创建过大的对象及数组：过大的对象或数组在新生代没有足够空间容纳时会直接进入老年代，如果是短命的大对象，会提前出发Full GC。

避免同时加载大量数据，如一次从数据库中取出大量数据，或者一次从Excel中读取大量记录，可以分批读取，用完尽快清空引用。

当集合中有对象的引用，这些对象使用完之后要尽快把集合中的引用清空，这些无用对象尽快回收避免进入老年代。

可以在合适的场景（如实现缓存）采用软引用、弱引用，比如用软引用来为ObjectA分配实例：SoftReference objectA=new SoftReference(); 在发生内存溢出前，会将objectA列入回收范围进行二次回收，如果这次回收还没有足够内存，才会抛出内存溢出的异常。
避免产生死循环，产生死循环后，循环体内可能重复产生大量实例，导致内存空间被迅速占满。

尽量避免长时间等待外部资源（数据库、网络、设备资源等）的情况，缩小对象的生命周期，避免进入老年代，如果不能及时返回结果可以适当采用异步处理的方式等。

（4）JVM问题排查记录案例

JVM服务问题排查 https://blog.csdn.net/jacin1/article/details/44837595

次让人难以忘怀的排查频繁Full GC过程 http://caogen81.iteye.com/blog/1513345

线上FullGC频繁的排查 https://blog.csdn.net/wilsonpeng3/article/details/70064336/

【JVM】线上应用故障排查 https://www.cnblogs.com/Dhouse/p/7839810.html

一次JVM中FullGC问题排查过程 http://iamzhongyong.iteye.com/blog/1830265

JVM内存溢出导致的CPU过高问题排查案例 https://blog.csdn.net/nielinqi520/article/details/78455614

一个java内存泄漏的排查案例 https://blog.csdn.net/aasgis6u/article/details/54928744

Java内存泄露的问题调查定位 https://www.cnblogs.com/2714585551summer/p/5745748.html

（5）常用JVM参数参考：

参数	说明	实例
-Xms	初始堆大小，默认物理内存的1/64	-Xms512M
-Xmx	最大堆大小，默认物理内存的1/4	-Xms2G
-Xmn	新生代内存大小，官方推荐为整个堆的3/8	-Xmn512M
-Xss	线程堆栈大小，jdk1.5及之后默认1M，之前默认256k	-Xss512k
-XX:NewRatio=n	设置新生代和年老代的比值。如:为3，表示年轻代与年老代比值为1：3，年轻代占整个年轻代年老代和的1/4	-XX:NewRatio=3
-XX:SurvivorRatio=n	年轻代中Eden区与两个Survivor区的比值。注意Survivor区有两个。如:8，表示Eden：Survivor=8:1:1，一个Survivor区占整个年轻代的1/8	-XX:SurvivorRatio=8
-XX:PermSize=n	永久代初始值，默认为物理内存的1/64	-XX:PermSize=128M
-XX:MaxPermSize=n	永久代最大值，默认为物理内存的1/4	-XX:MaxPermSize=256M
-verbose:class	在控制台打印类加载信息	
-verbose:gc	在控制台打印垃圾回收日志	
-XX:+PrintGC	打印GC日志，内容简单	
-XX:+PrintGCDetails	打印GC日志，内容详细	
-XX:+PrintGCDateStamps	在GC日志中添加时间戳	
-Xloggc:filename	指定gc日志路径	-Xloggc:/data/jvm/gc.log
-XX:+UseSerialGC	年轻代设置串行收集器Serial	
-XX:+UseParallelGC	年轻代设置并行收集器Parallel Scavenge	
-XX:ParallelGCThreads=n	设置Parallel Scavenge收集时使用的CPU数。并行收集线程数。	-XX:ParallelGCThreads=4
-XX:MaxGCPauseMillis=n	设置Parallel Scavenge回收的最大时间(毫秒)	-XX:MaxGCPauseMillis=100
-XX:GCTimeRatio=n	设置Parallel Scavenge垃圾回收时间占程序运行时间的百分比。公式为1/(1+n)	-XX:GCTimeRatio=19
-XX:+UseParallelOldGC	设置老年代为并行收集器ParallelOld收集器	
-XX:+UseConcMarkSweepGC	设置老年代并发收集器CMS	
-XX:+CMSIncrementalMode	设置CMS收集器为增量模式，适用于单CPU情况。	
五、类加载
编写的Java代码需要经过编译器编译为class文件（从本地机器码转变为字节码的过程），class文件是一组以8位字节为基础的二进制流，这些二进制流分别以一定形式表示着魔数（用于标识是否是一个能被虚拟机接收的Class文件）、版本号、字段表、访问标识等内容。代码编译为class文件后，需要通过类加载器把class文件加载到虚拟机中才能运行和使用。

####1、类加载步骤
类从被加载到内存到使用完成被卸载出内存，需要经历加载、连接、初始化、使用、卸载这几个过程，其中连接又可以细分为验证、准备、解析。


（1）加载

在加载阶段，虚拟机主要完成三件事情：
① 通过一个类的全限定名（比如com.danny.framework.MyClassLoader）来获取定义该类的二进制流；
② 将这个字节流所代表的静态存储结构转化为方法区的运行时存储结构；
③ 在内存中生成一个代表这个类的java.lang.Class对象，作为程序访问方法区中这个类的外部接口。

（2）验证

验证的目的是为了确保class文件的字节流包含的内容符合虚拟机的要求，且不会危害虚拟机的安全。

文件格式验证：主要验证class文件中二进制字节流的格式，比如魔数是否已0xCAFEBABY开头、版本号是否正确等。

元数据验证：主要对字节码描述的信息进行语义分析，保证其符合Java语言规范，比如验证这个类是否有父类（java.lang.Object除外），如果这个类不是抽象类，是否实现了父类或接口中没有实现的方法，等等。

字节码验证：字节码验证更为高级，通过数据流和控制流分析，确保程序是合法的、符合逻辑的。

符号引用验证：对类自身以外的信息进行匹配性校验，举个栗子，比如通过类的全限定名能否找到对应类、在类中能否找到字段名/方法名对应的字段/方法，如果符号引用验证失败，将抛出“java.lang.NoSuchFieldError”、“java.lang.NoSuchMethodError”等异常。

（3）准备

正式为【类变量】分配内存并设置类变量【初始值】，这些变量所使用的内存都分配在方法区。注意分配内存的对象是“类变量”而不是实例变量，而且为其分配的是“初始值”，一般数值类型的初始值都为0，char类型的初始值为’\u0000’（常量池中一个表示Nul的字符串），boolean类型初始值为false，引用类型初始值为null。
但是加上final关键字比如public static final int value=123;在准备阶段会初始化value的值为123；

（4）解析

解析是将常量池中【符号引用】替换为【直接引用】的过程。

符号引用是以一组符号来描述所引用的目标，符号引用与虚拟机实现的内存布局无关，引用的目标不一定已经加载到内存中。比如在com.danny.framework.LoggerFactory类引用了com.danny.framework.Logger，但在编译期间是不知道Logger类的内存地址的，所以只能先用com.danny.framework.Logger（假设是这个，实际上是由类似于CONSTANT_Class_info的常量来表示的）来表示Logger类的地址，这就是符号引用。

直接引用可以是直接指向目标的指针、相对偏移量或是一个能间接定位到目标的句柄。直接引用和虚拟机实现的内存布局有关，如果有了直接引用，那引用的目标一定在内存中存在。

解析的时候class已经被加载到方法区的内存中，因此要把符号引用转化为直接引用，也就是能直接找到该类实际内存地址的引用。

（5）初始化

在准备阶段，已经为类变量赋了初始值，在初始化阶段，则根据程序员通过程序定制的主观计划去初始化类变量的和其他资源，也可以从另一个角度来理解：初始化阶段是执行类构造器()方法的过程，那()到底是什么呢？
我的理解是，java在生成字节码时，如果类中有静态代码块或静态变量的赋值操作，会将类构造器()方法和实例构造器 () 方法添加到语法树中（可以理解为在编译阶段自动为类添加了两个隐藏的方法：类构造器——()方法和实例构造器——()方法，可以用javap命令查看），()主要用来构造类，比如初始化类变量(静态变量)，执行静态代码块(statis{})等，该方法只执行一次；()方法主要用来构造实例，在构造实例的过程中，会首先执行()，这时对象中的所有成员变量都会被设置为默认值（每种数据类型的默认值和类加载准备阶段描述的一样），然后才会执行实例的构造函数（会先执行父类的构造方法，再执行非静态代码块，最后执行构造函数）。

下面看段代码来理解下：

public class Parent {
    static {
        System.out.println("Parent-静态代码块执行");
    }
    
    public Parent() {
        System.out.println("Parent-构造方法执行");
    }
    
    {
        System.out.println("Parent-非静态代码块执行");
    }
}

public class Child extends Parent{
    private static int staticValue = 123;
    private int noStaticValue=456;
    
    static {
        System.out.println("Child-静态代码块执行");
    }
    
    public Child() {
        System.out.println("Child-构造方法执行");
    }
    
    {
        System.out.println("Child-非静态代码块执行");
    }
    
    public static void main(String[] args) {
        Child child = new Child();
    }
}

看下面的运行结果之前可以先猜测一下结果是什么，运行结果如下：

Parent-静态代码块执行
Child-静态代码块执行
Parent-非静态代码块执行
Parent-构造方法执行
Child-非静态代码块执行
Child-构造方法执行

上面的例子中可以看到一个类从加载到实例化的过程中，静态代码块、构造方法、非静态代码块的加载顺序。无法看到静态变量和非静态变量初始化的时间，静态变量的初始化和静态代码块的执行都是在类的初始化阶段（()）完成，非静态变量和非静态代码块都是在实例的初始化阶段（()）完成。

2、类加载器
（1）类加载器的作用

加载class：类加载的加载阶段的第一个步骤，就是通过类加载器来完成的，类加载器的主要任务就是“通过一个类的全限定名来获取描述此类的二进制字节流”，在这里，类加载器加载的二进制流并不一定要从class文件中获取，还可以从其他格式如zip文件中读取、从网络或数据库中读取、运行时动态生成、由其他文件生成（比如jsp生成class类文件）等。
从程序员的角度来看，类加载器动态加载class文件到虚拟机中，并生成一个java.lang.Class实例，每个实例都代表一个java类，可以根据该实例得到该类的信息，还可以通过newInstance()方法生成该类的一个对象。

确定类的唯一性：类加载器除了有加载类的作用，还有一个举足轻重的作用，对于每一个类，都需要由加载它的加载器和这个类本身共同确立这个类在Java虚拟机中的唯一性。也就是说，两个相同的类，只有是在同一个加载器加载的情况下才“相等”，这里的“相等”是指代表类的Class对象的equals()方法、isAssignableFrom()方法、isInstance()方法的返回结果，也包括instanceof关键字对对象所属关系的判定结果。

（2）类加载器的分类

以开发人员的角度来看，类加载器分为如下几种：启动类加载器（Bootstrap ClassLoader）、扩展类加载器（Extension ClassLoader）、应用程序类加载器（Application ClassLoader）和自定义类加载器（User ClassLoader），其中启动类加载器属于JVM的一部分，其他类加载器都用java实现，并且最终都继承自java.lang.ClassLoader。

① 启动类加载器（Bootstrap ClassLoader）是由C/C++编译而来的，看不到源码，所以在java.lang.ClassLoader源码中看到的Bootstrap ClassLoader的定义是native的“private native Class findBootstrapClass(String name);”。启动类加载器主要负责加载JAVA_HOME\lib目录或者被-Xbootclasspath参数指定目录中的部分类，具体加载哪些类可以通过“System.getProperty(“sun.boot.class.path”)”来查看。

② 扩展类加载器（Extension ClassLoader）由sun.misc.Launcher.ExtClassLoader实现，负责加载JAVA_HOME\lib\ext目录或者被java.ext.dirs系统变量指定的路径中的所有类库，可以用通过“System.getProperty(“java.ext.dirs”)”来查看具体都加载哪些类。

③ 应用程序类加载器（Application ClassLoader）由sun.misc.Launcher.AppClassLoader实现，负责加载用户类路径（我们通常指定的classpath）上的类，如果程序中没有自定义类加载器，应用程序类加载器就是程序默认的类加载器。

④ 自定义类加载器（User ClassLoader），JVM提供的类加载器只能加载指定目录的类（jar和class），如果我们想从其他地方甚至网络上获取class文件，就需要自定义类加载器来实现，自定义类加载器主要都是通过继承ClassLoader或者它的子类来实现，但无论是通过继承ClassLoader还是它的子类，最终自定义类加载器的父加载器都是应用程序类加载器，因为不管调用哪个父类加载器，创建的对象都必须最终调用java.lang.ClassLoader.getSystemClassLoader()作为父加载器，getSystemClassLoader()方法的返回值是sun.misc.Launcher.AppClassLoader即应用程序类加载器。

（3）ClassLoader与双亲委派模型

ClassLoader主要负责的是类加载过程中的第一个步骤——加载，下面看一下类加载器java.lang.ClassLoader中的核心逻辑loadClass()方法：

protected Class<?> loadClass(String name, boolean resolve)
        throws ClassNotFoundException
    {
        synchronized (getClassLoadingLock(name)) {
            // 检查该类是否已经加载过
            Class c = findLoadedClass(name);
            if (c == null) {
                long t0 = System.nanoTime();
                try {
                    if (parent != null) {//如果父加载器不为空，就用父加载器加载类
                        c = parent.loadClass(name, false);
                    } else {//如果父加载器为空，就用启动类加载器加载类
                        c = findBootstrapClassOrNull(name);
                    }
                } catch (ClassNotFoundException e) {
                }
    
                if (c == null) {//如果上面用父加载器还没加载到类，就自己尝试加载
                    long t1 = System.nanoTime();
                    c = findClass(name);
                    sun.misc.PerfCounter.getParentDelegationTime().addTime(t1 - t0);
                    sun.misc.PerfCounter.getFindClassTime().addElapsedTimeFrom(t1);
                    sun.misc.PerfCounter.getFindClasses().increment();
                }
            }
            if (resolve) {
                resolveClass(c);
            }
            return c;
        }
    }
这段代码的主要意思就是当一个类加载器加载类的时候，如果有父加载器就先尝试让父加载器加载，如果父加载器还有父加载器就一直往上抛，一直把类加载的任务交给启动类加载器，然后启动类加载器如果加载不到类就会抛出ClassNotFoundException异常，之后把类加载的任务往下抛，如下图：


通过上图的类加载过程，就引出了一个比较重要的概念——双亲委派模型，如下图展示的层次关系，双亲委派模型要求除了顶层的启动类加载器之外，其他的类加载器都应该有一个父类加载器，但是这种父子关系并不是继承关系，而是像上面代码所示的组合关系。


双亲委派模型的工作过程是，如果一个类加载器收到了类加载的请求，它首先不会加载类，而是把这个请求委派给它上一层的父加载器，每层都如此，所以最终请求会传到启动类加载器，然后从启动类加载器开始尝试加载类，如果加载不到（要加载的类不在当前类加载器的加载范围），就让它的子类尝试加载，每层都是如此。

那么双亲委派模型有什么好处呢？最大的好处就是它让Java中的类跟类加载器一样有了“优先级”。前面说到了对于每一个类，都需要由加载它的加载器和这个类本身共同确立这个类在Java虚拟机中的唯一性，比如java.lang.Object类（存放在JAVA_HOME\lib\rt.jar中），如果用户自己写了一个java.lang.Object类并且由自定义类加载器加载，那么在程序中是不是就是两个类？所以双亲委派模型对保证Java稳定运行至关重要。


