### java类中私有对象可以直接初始化吗？

今天碰到一个比较奇怪的初始化问题。

#### case1：

```java
package test;

public class test {
    public static void main(String[] args) {
        MyClass myClass = new MyClass();
        myClass.init();
    }
}

class MyClass{
    private double [][]e = new double[2][3];

    public void init(){
        int k = 0;
        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 3; j++) {
                e[i][j] = k++;
            }
        }
    }
}
---
Process finished with exit code 0
```

这里发现e数组可以在类内，而不用在方法内初始化，不会报空指针异常。

#### case2：

```java
package test;

public class test {
    public static void main(String[] args) {
        MyClass myClass = new MyClass();
        myClass.init();
    }
}

class MyClass{
    private int dimensions;
    private int TIMES;
    private double [][]e = new double[TIMES][dimensions];

    public void init(){

        //初始化dimensions，TIMES
        this.dimensions = 3;
        this.TIMES = 4;

        int k = 0;
        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 3; j++) {
                e[i][j] = k++;
            }
        }
    }
}
---
Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: 0
	at test.MyClass.init(test.java:24)
	at test.test.main(test.java:6)    
```

由于**dimensions，TIMES没有初始化**，e数组在一开始加载时不能初始化，会报空指针异常。

#### case3：

是否有个疑问：类在加载过程中，初始化的顺序是怎样的？如果将dimensions，TIMES放在e数组后面初始化，会不会有问题呢？

```java
 private double [][]e = new double[TIMES][dimensions];
    private int dimensions = 3;
    private int TIMES = 4;
```

**IDEA自动报错**：`illegal forward referance`

#### case4：

如果将属性定义为**static类型**，可以放在e数组创建之后吗？这样是可以的

```java
public class test {
    public static void main(String[] args) {
        MyClass myClass = new MyClass();
        myClass.init();
    }
}

class MyClass{

    private double [][]e = new double[TIMES][dimensions];
    private static int dimensions = 3;
    private static int TIMES = 4;

    public void init(){

        int k = 0;
        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 3; j++) {
                e[i][j] = k++;
            }
        }
    }
}
---
Process finished with exit code 0    
```

#### 总结：类中属性在JVM中初始化的顺序