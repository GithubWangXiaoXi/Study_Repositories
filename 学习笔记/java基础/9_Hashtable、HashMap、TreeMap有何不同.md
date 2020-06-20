## Hashtable、HashMap、TreeMap有何不同

### 一、考点分析

- 理解**Map**相关类似的**整体结构**，尤其是有序数据结构的一些要点
- 从源码去分析HashMap的设计和实现要点，理解**容量，负载因子**等，以及**为什么需要这些参数**，如何**影响Map的性能**，实践中如何取舍
- 理解**树化改造**的相关原理和改进原因



### 二、广义集合框架

#### 1、Hashtable、HashMap、TreeMap有何不同

​	Hashtable，HashMap、TreeMap都是最常见的**一些Map实现**，是以**键值对**的形式**存储和操作数据**的容器类型.

##### **Hashtable：**

- Hashtable是早期Java类库提供一个**哈希表**实现，本身是**同步的**，不支持null键和值, 由 于**同步导致的性能开销**，所以已经很少被推荐使用。

##### **HashMap：**

- 行为上大致和Hashtable一致，主要区别于**HashMap不是同步**的，支持null键和值等。
- HashMap进行put或者get操 作，可以达到常数时间的性能，所以它是**绝大部分利用键值对存取场景**的首选。

##### **TreeMap：**

- TreeMap则是**基于红黑树的一种提供顺序访问的Map** ,和HashMap不同，它的**get、 put、remove之类都是O (log(n)) 的时间复杂度**，具体**顺序可以由指定的Comparator来决 定**，或者根据**键的自然顺序**来判断。



##### **LinkedHashMap：**

- **HashMap和双向链表合二为一即是LinkedHashMap**，当我们要用**LinkedHashMap实现LRU算法时，就需要调用该构造方法并将accessOrder置为true。**
- 当**accessOrder为true**时，get方法和put方法都会调用**recordAccess()**方法使得**最近使用的Entry移到双向链表的末尾**；当accessOrder为默认值false时，从源码中可以看出recordAccess方法什么也不会做。[彻头彻尾理解 LinkedHashMap](https://blog.csdn.net/justloveyou_/article/details/71713781)


- **应用场景：**我们构建一个空间占用敏感的资源池，希望可以**自动 将最不常被访问的对象释放掉**，这就可以利用**LinkedHashMap提供的机制**来实现，参考下面 的示例：

  ```java
  @Test
  public void test(){
    LinkedHashMap<String,String> linkedHashMap = new LinkedHashMap(16,0.75f,true){
      @Override
      protected boolean removeEldestEntry(Map.Entry eldest) {
        //父类的size对于子孙类可见，对其他package不可见
        return size() > 3;
      }
    };

    linkedHashMap.put("project1","world");
    linkedHashMap.put("project2","world");
    linkedHashMap.put("project3","world");
    linkedHashMap.forEach((k,v) ->{
      System.out.println(k + ' ' + v);
    });
    System.out.println("-----------------------------------");

    //模拟访问
    linkedHashMap.get("project1");
    linkedHashMap.get("project1");
    linkedHashMap.get("project2");
    linkedHashMap.forEach((k,v) ->{
      System.out.println(k + ' ' + v);
    });

    System.out.println("-----------------------------------");
    //触发删除
    linkedHashMap.put("project4","Mission control");
    System.out.println("oldest entry should ne removed:");
    linkedHashMap.forEach((k,v) ->{
      System.out.println(k + ' ' + v);
    });
  }

  ---------
  输出结果：
  project1 world
  project2 world
  project3 world
  -----------------------------------
  project3 world
  project1 world
  project2 world
  -----------------------------------
  oldest entry should ne removed:
  project1 world
  project2 world
  project4 Mission control
  ```

- 重写LinkedHashMap的removeEldestEntry方法，其中eldest在文档中的意思如下：*The least recently inserted entry in the map, or **if this is an access-ordered map, the least recently accessed entry**.  **This is the entry that will be removed** it this method returns*

  ```java
  protected boolean removeEldestEntry(Map.Entry<K,V> eldest) {
         return false;
  }
  ```

  

**备注：**

- 在《Vector，ArrayList，LinkedList区别》中有对HashMap和TreeMap进行简单的区分

- **LinkedHashMap与TreeMap区别：**

  - 虽然LinkedHashMap和TreeMap都可 以**保证某种顺序**，但二者还是非常不同的。

     LinkedHashMap通常提供的是**遍历顺序符合插入顺序**，它的实现是通过为条目（键值对） 维护一个双向链表。注意，通过特定构造函数，我们可以创建反映访问顺序的实例，**所谓的put、get、compute等，都算作“访问”**

  - 构建一个具有**优先级的调度系统**的问题，其本质就是个典型 的优先队列场景，Java标准库提供了基于**二叉堆实现的PriorityQueue** ,它们都是依赖于同一 种排序机制，当然也**包括TreeMap**的马甲**TreeSet**。

  -  类似hashCode和equals的约定，为了避免模棱两可的情况,自然顺序同样需要符合一个约 定，就是**compareTo的返回值需要和equals 一致，否则就会出现模棱两可情况**。

  

#### 2、Map的整体结构

![13](..\..\images\java基础\13.jpg)

- Map是**广义上的集合框架**，**不是狭义上的集合类型（Collection）**

- **Hashtable**比较特别，作为类似Vector、Stack的早期集合相关类型，它是**扩展了 Dictionary 类**的，**类结构上与HashMap之类明显不同**.

- **HashMap**等其他Map实现则是**扩展了 AbstractMap** ,里面包含了通用方法抽象。不同 Map的用途，从类图结构就能体现出来，设计目的已经体现在不同接口上。

- **HashMap的性能表现非常依赖于哈希码的有效性**，请务必掌握**hashCode和equals的一些基本约定**，比如: 

  - **equals 相等，hashCode —定相等**。
  - 重写了 hashCode 也要重写equals。 
  - **hashCode**需要**保持一致性**，状态改变返回的哈希值仍然要一致；**equals保持唯一性**。 
  - equals的对称、反射、传递等特性（？？？）。

  

#### 3、HashMap源码分析

##### **HashMap内部的结构**

- 它可以看作是**数组(Node<K,V>D table)和 链表结合**组成的复合结构，数组被分为一个个桶(bucket)，通过**哈希值**决定了健值对在这个 **数组的寻址**；**哈希值相同的鍵值对，则以链表形式存储。**你可以参考下面的示意图.这里需要注 意的是，**如果链表大小超过阈值(TREEIFY_THRESHOLD, 8)，图中的链表就会改造为树形结构**。

  ![14](..\..\images\java基础\14.jpg)

##### **HashMap的putVal方法**

- HashMap的主要密码隐藏在**putVal**里面：putVal方法本身逻辑非常集中，从**初始化、扩容**到**树化**，全部都和它有关。

  ```java
  public V putIfAbsent(K var1, V var2) {
    return this.putVal(hash(var1), var1, var2, true, true);
  }
  ```

  ```java
  final V putVal(int var1, K var2, V var3, boolean var4, boolean var5) {
    HashMap.Node[] var6 = this.table;
    int var8;
    //hashMap默认大小
    if (this.table == null || (var8 = var6.length) == 0) {
      var8 = (var6 = this.resize()).length;
    }

    Object var7;
    int var9;
    if ((var7 = var6[var9 = var8 - 1 & var1]) == null) {
      var6[var9] = this.newNode(var1, var2, var3, (HashMap.Node)null);
    } else {
      //...
      if (((HashMap.Node)var7).next == null) {
        ((HashMap.Node)var7).next = this.newNode(var1, var2, var3, (HashMap.Node)null);
        if (var12 >= 7) {
          //树化
          this.treeifyBin(var6, var1);
        }
        break;
      }
      //...
    }
    ++this.modCount;
    if (++this.size > this.threshold) {
      this.resize();
    }
    //...
    this.afterNodeInsertion(var5);
    return null;
  } 
  ```

  从putVal方法最初的几行，我们就可以发现几个有意思的地方: 

  - 如果表格是null, resize方法会负责初始化它，这从**tab = resize()**可以看出。

  - resize方法兼顾两个职责，创建初始存储表格，或者在**容量不满足需求的时候，进行扩容 (resize)**。

  - 在放置新的键值对的过程中，如果发生下面条件，也会发生扩容。

    ```java
    if (++this.size > this.threshold) {
      this.resize();
    }
    ```

  - 具体**键值对在哈希表中的位置**（数组index）取决于下面的**位运算**：

    ```java
    i = (n - 1) & hash
    ```

  - 我前面提到的**链表结构**（这里叫bin ）,会在**达到一定门限值**时，发生**树化**。

##### **HashMap的resize方法：**

以JDK8源码为例：

```java
final HashMap.Node<K, V>[] resize() {
  HashMap.Node[] var1 = this.table;
  int var2 = var1 == null ? 0 : var1.length;
  int var3 = this.threshold;
  int var5 = 0;
  int var4;
  if (var2 > 0) {
    if (var2 >= 1073741824) {
      this.threshold = 2147483647;
      return var1;
    }

    if ((var4 = var2 << 1) < 1073741824 && var2 >= 16) {
      var5 = var3 << 1;
    }
  } else if (var3 > 0) {
    var4 = var3;
  } else {
    var4 = 16;
    var5 = 12;
  }

  if (var5 == 0) {
    float var6 = (float)var4 * this.loadFactor;
    var5 = var4 < 1073741824 && var6 < 1.07374182E9F ? (int)var6 : 2147483647;
  }

  this.threshold = var5;
  HashMap.Node[] var14 = (HashMap.Node[])(new HashMap.Node[var4]);
  this.table = var14;
  if (var1 != null) {
    for(int var7 = 0; var7 < var2; ++var7) {
      HashMap.Node var8;
      if ((var8 = var1[var7]) != null) {
        var1[var7] = null;
        if (var8.next == null) {
          var14[var8.hash & var4 - 1] = var8;
        } else if (var8 instanceof HashMap.TreeNode) {
          ((HashMap.TreeNode)var8).split(this, var14, var7, var2);
        } else {
          HashMap.Node var9 = null;
          HashMap.Node var10 = null;
          HashMap.Node var11 = null;
          HashMap.Node var12 = null;

          HashMap.Node var13;
          do {
            var13 = var8.next;
            if ((var8.hash & var2) == 0) {
              if (var10 == null) {
                var9 = var8;
              } else {
                var10.next = var8;
              }

              var10 = var8;
            } else {
              if (var12 == null) {
                var11 = var8;
              } else {
                var12.next = var8;
              }

              var12 = var8;
            }

            var8 = var13;
          } while(var13 != null);

          if (var10 != null) {
            var10.next = null;
            var14[var7] = var9;
          }

          if (var12 != null) {
            var12.next = null;
            var14[var7 + var2] = var11;
          }
        }
      }
    }
  }

  return var14;
}
```

​	不考虑极端情况（容量理论最大极限由MAXIMUM_CAPACITY指定，数值 为1 <<30 ,也就是2的30次方），我们可以归纳为： 

- **门限值等于（负载因子）x （容量）**，如果构建HashMap的时候没有指定它们,那么就是依 据相应的默认常量值。 
- **门限通常是以倍数进行调整（newThr = oldThr << 1 ）**，我前面提到，根据putVal中的逻 辑，当元素个数超过门限大小时，则调整Map大小。
- 扩容后，需要将老的数组中的元素重新放置到新的数组，这是扩容的一个主要开销来源。
- 

#### 4、容量，负载因子和树化

##### 容量和负载因子

- **负载因子 * 容量 > 元素数量**
- 负载因子不要轻易更改，建议**不要设置  超过 0.75数值，因为会显著增加冲突**，降低HashMap 的性能。若使用**太小的负载因子**，按照上面的公式，预设容量值也进行调整，否则可能会导致**更加 频繁的扩容，增加开销**。



##### 树化

- 为什么HashMap要树化？

  - **本质上这是个安全问题。  **因为在元素放置过程中，如果一个对象哈希冲突，者都被放置到同一个桶里，则会形成一个链表，我们知道**链表査询是线性的，会严重影响存取的性能**。
  - 而在现实世界，构造哈希冲突的数据并不是非常复杂的事情，**恶意代码**就可以利用这些数据大量 与服务器端交互，**导致服务器端CPU大量占用，这就构成了哈希  碰撞拒绝服务攻击**，国内一线 互联网公司就发生过类1以攻击事件。

- 由treeifyBin源码可知，当**bin的数量大于TREEIFYJHRESHOLD**时：

  ```java
  static final int MIN_TREEIFY_CAPACITY = 64;

  static final int MIN_TREEIFY_CAPACITY = 64;
  final void treeifyBin(HashMap.Node<K, V>[] var1, int var2) {
    int var3;
    if (var1 != null && (var3 = var1.length) >= 64) {
      int var4;
      HashMap.Node var5;
      if ((var5 = var1[var4 = var3 - 1 & var2]) != null) {
        HashMap.TreeNode var6 = null;
        HashMap.TreeNode var7 = null;

        do {
          HashMap.TreeNode var8 = this.replacementTreeNode(var5, (HashMap.Node)null);
          if (var7 == null) {
            var6 = var8;
          } else {
            var8.prev = var7;
            var7.next = var8;
          }

          var7 = var8;
        } while((var5 = var5.next) != null);

        if ((var1[var4] = var6) != null) {
          var6.treeify(var1);
        }
      }
    } else {
      this.resize();
    }
  }
  ```

  - 如果**容量小于MIN_TREEIFY_CAPACITY** ,只会进行**简单的扩容**。
  - 如果**容量大于MIN TREEIFY CAPACITY**，则会进行**树化改造**。



### 三、知识拓展

#### 1、解决hash冲突的方法：

- **开放定址法**（线性探测 ，平方探测，双散列探测）[参考文档](https://blog.csdn.net/qq_30091945/article/details/78044445)

  基本思想是：当关键字key的哈希地址p=H ( key)出现冲突时，以p为基础，产生另一个哈 希地址p1 ,如果p1仍然冲突，再以p为基础，产生另一个哈希地址p2，…，直到找岀一个不 冲突的哈希地址pi ,将相应元素存入其中，

- **再哈希法**

  这种方法是同时构造多个不同的哈希函数： Hi=RH1 (key) i=1 , 2 ...k 当哈希地址Hi=RH1 ( key)发生冲突时，再计算Hi=RH2 (key)... ， 直到冲突不再产生。这种方法不易产生聚集，但增加了计算时间。

- **链地 址法**

  这种方法的基本思想是将所有哈希地址为i的元素构成一个称为**同义词链的单链表**，并将单链 表的头指针存在哈希表的第i个单元中，因而査找、插入和删除主要在同义词链中进行。**链地 址法适用于经常进行插入和删除的情况。**

- **建立公共溢出区**

   这种方法的基本思想是:将哈希表分为**基本表和溢出表**两部分，凡是和基本表发生冲突的元 素，一律填入溢出表。



### 四、参考文档

1、极客时间《Java核心技术36讲》第9讲

