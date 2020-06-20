### 二、用Executors管理多线程

#### 1、executors的介绍

##### 1）基本特征：

- 要执行并发任务，创建**实现`Runnable`接口的任务实例**，并**发送给executors**即可，executors会帮忙管理运行任务的线程。
- 减少线程创建的开销，重复使用线程。
- **限制executor工作线程的数目**。如果你发送的任务超出工作线程的数目，**该任务会放在等待队列中**。
- 需要**显示结束executor的运行**。需要向executor指明结束运行并杀死线程

##### 2）基本组件

​	**executor框架提供**了很多实现executors提供的所有功能的**接口和类**

- **`Executor`接口**：它只定义了一个方法 -- 允许我们将`Runnable`对象发送给executor
- **`ExecutorService`接口**：继承`Executor`接口，相比于`Executor`接口，提供了更多功能，如下：
  - 执行任务并返回结果。**Runnable接口中的run方法不返回值**，但是**使用executors**后，你能**得到任务返回值**。
  - 使用单个方法调用来执行一系列的任务
  - 结束executor的运行并等待它终止。
- **`ThreadPoolExecutor `类**：实现了`Executor`和`ExecutorService`接口。并且有额外的方法**获得executor的状态**（工作线程的数量，运行任务的数量等），**设置executor的参数**（工作线程的最大最小值，空闲线程等待新任务的时长等）
- **`Executors`类**：该类提供有效的方法去创建Executor对象和其他相关类。



#### 2、例子1 - k近邻算法

​	k近邻算法是简单的机器学习算法，被用作监督式分类。

- **训练集：**该数据集由**一个或多个属性的实例构成**，这些属性定义了每一个实例，以及**定义了确定实例的例子和标签的特殊属性**。
- **距离度量：**用来计算训练集中**各实例间的距离**（相似度），以及你想分类的新实例。这里采用**欧几里得距离**。
- **测试集：**用来衡量算法的行为

##### 1）串行算法

- *KnnClassifier*该类存储了训练集和样例数目k（k可以用来确定距离标签）

- *KnnClassifier*只实现了*classify*方法，用来存储包含距离的样本，该方法有主要三个部分：

  - 计算输入数据和训练数据的距离，使用*EuclideanDistanceCalculator*来计算欧几里得距离  
    $$
    E(p,q) = \sqrt{(p_1−q_1)^2+(p_2−q_2)^2+…+(p_n−q_n)^2)} = \sqrt{\sum_{i=1}^{n}(p_i - q_i)^2}
    $$

  - 对样本按距离从低到高排序

  - 计算算法例子中最多实例的标签

```java
public class KnnClassifier {
  private List <? extends Sample> dataSet;
  private int k;
  public KnnClassifier(List <? extends Sample> dataSet, int k) {
    this.dataSet=dataSet;
    this.k=k;
  }

  public String classify (Sample example) {
    
    Distance[] distances=new Distance[dataSet.size()];
    int index=0;
    //计算输入数据和训练数据的距离
    for (Sample localExample : dataSet) {
      distances[index]=new Distance();
      distances[index].setIndex(index);
      distances[index].setDistance (EuclideanDistanceCalculator.calculate(localExample, example));
      index++;
 	}

    //对样本按距离从低到高排序
  	Arrays.sort(distances);

    Map<String, Integer> results = new HashMap<>();
    for (int i = 0; i < k; i++) {
      Sample localExample = dataSet.get(distances[i].getIndex());
      String tag = localExample.getTag();
      results.merge(tag, 1, (a, b) -> a+b);
    }
    return Collections.max(results.entrySet(),
    Map.Entry.comparingByValue()).getKey();
  }

  
  public class EuclideanDistanceCalculator {
    
    public static double calculate (Sample example1, Sample example2) {
      double ret=0.0d;
      double[] data1=example1.getExample();
      double[] data2=example2.getExample();
      if (data1.length!=data2.length) {
        throw new IllegalArgumentException ("Vector doesn't have the same
        length");
      }

      for (int i=0; i<data1.length; i++) {
        ret+=Math.pow(data1[i]-data2[i], 2);
      }
      return Math.sqrt(ret);
  	}
  }

```





##### 2）细粒度并发算法





##### 3）粗粒度并发算法















#### 3、例子2 - 并发环境下的客户端/服务器

