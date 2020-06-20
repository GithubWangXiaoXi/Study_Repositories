转载自：<http://linuxperformance.top/>

### java诊断工具

工欲善其事，必先利其器，本文将本人在上次定位问题中用到的工具都列了出来，后续根据使用情况再会更新。

1. #### jps

   jps(Java Virtual Machine Process Status Tool)**类似于Linux中的ps命令**。

   jps主要用来输出**JVM中运行的进程状态信息**。
   \#jps
   常用参数如下：

   - -q 只显示pid，不显示class名称,jar文件名和传递给main 方法的参数
   - -m 输出传递给main 方法的参数，在嵌入式jvm上可能是null
   - -l 输出应用程序main class的完整package名 或者 应用程序的jar文件完整路径名
   - -v 输出传递给JVM的参数

2. #### jstack

   jstack主要用来查看**某个Java进程内的线程堆栈信息**。可以**定位到线程堆栈**，根据堆栈信息定位到具体代码，在JVM性能调优中使用得非常多。

   主要参数如下：
   Options:

   - -F to force a thread dump. Use when jstack does not respond (process is hung)

   - -m to print both java and native frames (mixed mode)

   - -l long listing. Prints additional information about locks

   - -h or -help to print this help message

   - 通过#top –H获得最费资源线程PID

   - $printf "%x\n" [pid]

     - 例如：
     - $printf "%x\n" 128044
     - 1dd52

   - 然后执行如下(127853为进程PID)：

     $./jstack -l 127853 | grep 1f42c

     ```java
     "Thread-6" #31 prio=5 os_prio=0 tid=0x00007f7d1f5b7800 nid=0x1f42c runnable [0x00007f7cfd7fe000]
     ```

     可以查看到该线程的状态和正在执行的代码行。
     如果不加grep就可以看到所有的进程状态。

   ​

3. #### jmap

   jmap（Memory Map）用来查看**堆内存**使用状况，一般**结合jhat**（Java Heap Analysis Tool）

   常用的是使用**jmap -heap pid**查看进程堆内存使用情况，包括使用的**GC算法、堆配置参数**和**各代中堆内存使用情况**。

   - $./jmap -heap 135210

     ```java
     Attaching to process ID 135210, please wait...

     Debugger attached successfully.

     Server compiler detected.

     JVM version is 25.112-b6

     …

     4380 interned Strings occupying 418376 bytes.

     ```

   - 此外可以**用jmap把进程内存使用情况dump到文件中**，再**用jhat分析**查看。

   - jmap进行dump命令格式如下：

     jmap -dump:format=b,file=dumpFileName pid

     例如：

     \#jmap -dump:format=b,file=/tmp/dump.dat 11611
     dump出来的文件可以用MAT、VisualVM等工具查看，这里用jhat查看：
     \#jhat -port 9998 /tmp/dump.dat
     注意如果Dump文件太大，可能需要加上-J-Xmx512m这种参数指定最大堆内存。然后在浏览器中输入主机地址:9998查看

   - jmap是jdk自带的。一些常用用法如下：

     - 查看jvm内存使用状况：jmap -heap
     - 查看jvm内存存活的对象：jmap -histo:live
     - 把heap里所有对象都dump下来，无论对象是死是活：jmap -dump:format=b,file=xxx.hprof
     - 先做一次full GC，再dump，只包含仍然存活的对象信息：jmap -dump:format=b,live,file=xxx.hprof

   ​

4. #### jstat

   当JVM存在内存问题或者垃圾回收问题时候，使用linux系统自带的top是满足不了这样的需求，top主要监控的是总体的系统资源，很难定位到java应用程序。
   而jstat是JDK自带的一个轻量级小工具。全称“**Java Virtual Machine statistics monitoring tool**”，它位于java的bin目录下，主要**利用JVM内建的指令对Java应用程序的资源和性能进行实时的命令行的监控**，包括了对Heap size和垃圾回收状况的监控。可见，Jstat是轻量级的、专门针对JVM的工具，非常适用。
   jstat使用
   使用语法如下：
   Usage: jstat -help|-options
   jstat -

5. #### javap

   javap是一个Java**类文件反汇编程序**，可以查看Java编译器生成的字节码，是分析代码的一个好工具。

6. #### jprofiler

   JProfiler是一个商业授权的Java剖析工具，由EJ技术有限公司，针对的Java EE和Java SE应用程序开发的。
   **JProfiler 可对 CPU、堆、内存进行分析**，功能强大。同时结合压测工具，可以对代码耗时采样统计
   下载地址如下

   http://www.ej-technologies.com/download/jprofiler/files
   是个开发调试工具，不适合非开发阶段的使用。

7. #### jcmd

   **Java 命令行**(Java Command)，用于向正在运行的JVM发送诊断命令请求。

8. #### jconsole

   图形化用户界面的监测工具，主要用于监测并显示运行于Java平台上的应用程序的性能和资源占用等信息。

9. #### MAT(Memory Analyzer Tool)

   ​    **MAT(Memory Analyzer Tool)**，一个基于Eclipse的内存分析工具，是一个快速、功能丰富的Java heap分析工具，它可以帮助我们查找内存泄漏和减少内存消耗。使用内存分析工具从众多的对象中进行分析，快速的计算出在内存中对象的占用大小，看看是谁阻止了垃圾收集器的回收工作，并可以通过报表直观的查看到可能造成这种结果的对象。

10. #### jvisualvm

    **JDK自带的JAVA性能分析工具**。它已经在你的JDK bin目录里了，只要你使用的是JDK1.6 Update7之后的版本。点击一下j**visualvm.exe图标**它就可以运行了。当然前提是ORACLE 的JDK。

11. #### Btrace

    BTrace是一个非常不错的java诊断工具。BTrace 中的B表示bytecode，它是在字节码层面上对代码进行trace ，通过在运行中的java类中注入trace代码， 并对运行中的目标程序进行热交换(hotswap)来达到对代码的跟踪 。
    下载链接如下：
    http://hg.openjdk.java.net/code-tools/btrace/

12. #### Jwebap

    Jwebap是一个用于J2EE工程（EJB以及WebModule系统）进行性能监控的组件.

13. #### JMC

    作为JVM融合战略的一部分，主要用来统一HotSpot、JRockit VMs。目前，JRockit Mission Control在标准版Java SE中已经可以使用。Java Mission Control（JMC）与Java Flight Recorder一起工作，适用于HotSpot JVM，用来记录核心数据和事件。它是一个调优工具，并且适用于Oracle JDK。一旦出现问题，这些数据就可以用来分析。 

    开发者可以使用jmc命令来创建JMC工具。

14. #### SJK开源JAVA工具

    这里推荐一个能实现Java诊断、性能排查、优化工具sjk,全称Swiss Java Knife 

    使用sjk对Java诊断、性能排查、优化工具

    - ttop:类似linux的top命令，监控指定jvm进程的各个线程的cpu使用情况
    -  jps: 类似linux的ps命令
    - hh: 类似jmap –histo命令
    - gc: 实时报告垃圾回收信息

    如果不使用Awesome，可以从如下连接下载。
    https://github.com/aragozin/jvm-tools
    或者直接下载jar包
    https://repo1.maven.org/maven2/org/gridkit/jvmtool/sjk/0.6/sjk-0.6.jar
    sjk sjk --commands sjk --help 
    例如：跟踪进程6344的JVM中， CPU使用率的20个线程。(默认就是20个现场，按CPU排序)
    java -jar sjk.jar ttop -p 6344 -n 20 -o CPU
    可以看到GC时间利用率，每秒堆栈分配速率。

15. #### perfj

    在定位java问题的时候特别希望有一个类似perf的工具，现在终于有了，真是纵里寻她千百度，蓦然回首，那人却在灯火阑珊处。下载链接如下：

    https://github.com/coderplay/perfj
    可以直接下载二进制包
    https://github.com/coderplay/perfj/releases
    需要先安装linxu自带的perf
    yum install perf
    tar zxvf perf-*.tgz
    解压后运行：
    \#bin/perfj record -e sched:sched_switch -F 99 -g -p 159667 sleep 5
    \#bin/perfj script > out.perfj
    查看监控数据：
    $bin/perfj report --stdio
    在当前目录下保存perf.data文件。

16. #### 火焰图

    perfj看到的是文本的，如何通过图形化直观观测呢？可以使用brendangregg 分享的火焰图

    链接如下：
    https://github.com/brendangregg/FlameGraph
    火焰图绘制如下：
    先抓取数据,在perfj目录下执行如下：
    \#bin/perfj record -e sched:sched_switch -F 99 -g -p 159667 sleep 5
    sudo perf script > out.perfj
    然后在FlameGraph目录下合并栈采样到单独行，执行如下：
    $./stackcollapse-perf.pl ../perfj-1.0/out.perfj > out.folded
    最后绘制火焰图
    \#./flamegraph.pl out.folded > kernel.svg
    可以通过浏览器打开。
    手动一个一个执行略显麻烦，为此可以使用如下脚本，前提是将FlamgeGraph文件中内容复制到perfj文件夹中，脚本放在perfj文件夹中执行即可。
    export JAVA_HOME=~/jdk8u60
    if [ $# != 4 ] ; then
    echo "USAGE: $0 event_name test_name pid duration"
    echo " e.g.: $0 cpu-clock testname 6643 10"
    exit 1;
    fi
    \#bin/perfj record -e cpu-clock,context-switches,cpu-migrations,task-clock -F 99 -g -p 6643 sleep 30
    echo "perfj record..."
    bin/perfj record -e $1 -F 99 -g -p $3 sleep $4
    sudo perf script > out_${2}.perfj
    echo "fold stack samples"
    ./stackcollapse-perf.pl ../perfj-1.0/out_${2}.perfj > out_${2}.folded
    echo "create flamegraph ${2}.svg"
    ./flamegraph.pl out_${2}.folded > ${2}.svg

17. #### Awesome-java开源项目

    Awesome-java可以来得到常用的JAVA第三方库。Awesome-java将JAVA中那些最常用的第三方库按照分类整理成了一个列表，堪称java第三方库大全，如果项目中使用哪一个库不确定,都可以到awesome-java上进行参考。

    工具下载链接如下：
    https://github.com/superhj1987/awesome-scripts
    解压后执行
    $sudo make install
    会在/usr/local/bin下创建opscripts.然后可以直接使用opscripts,通过opscripts工具可以关联到其他著名的第三方java库。其中包含了sjk命令参数。

18. #### JAVA压测工具JMH

    JMH下载链接：

    http://hg.openjdk.java.net/code-tools/jmh/

#### 参考链接

http://www.importnew.com/13954.html
http://blog.csdn.net/chen77716/article/details/569589
http://java.sun.com/javase/technologies/hotspot/gc/gc_tuning_6.html
http://www.cnblogs.com/zhguang/p/Java-JVM-GC.html
http://www.oracle.com/technetwork/cn/java/javase/tech/index-jsp-136373-zhs.html
http://java-performance.info/jmh/
http://blog.csdn.net/sunny243788557/article/details/52796904
http://www.cnblogs.com/whgw/archive/2011/09/29/2194997.html
http://blog.csdn.net/zhengchao1991/article/details/53188629