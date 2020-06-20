如果要对ArrayList集合中的元素进行排序，需要用到java工具包中的Collections类的sort方法。

具体用法可以查看jdk帮助文档。

在这里先创建一个Person类，包含姓名，性别，年龄，身份证号，出生日期。如以下代码：

```java
public class Person {
private String name;
private String birthday;
private String idCard;
private char sex;
private int age;

//getters和setters
public String getName() {
	return name;
}
public void setName(String name) {
	this.name = name;
}
public String getBirthday() {
	return birthday;
}
public void setBirthday(String birthday) {
	this.birthday = birthday;
}
public String getIdCard() {
	return idCard;
}
public void setIdCard(String idCard) {
	this.idCard = idCard;
}
public char getSex() {
	return sex;
}
public void setSex(char sex) {
	this.sex = sex;
}
public int getAge() {
	return age;
}
public void setAge(int age) {
	this.age = age;
}
//构造函数
public Person(){}
public Person(String name,String birthday,String idCard,char sex,int age){
	this.name = name;
	this.birthday = birthday;
	this.idCard = idCard;
	this.sex = sex;
	this.age = age;
}
//输出信息
public String toString(){
	return name+","+sex+","+age+","+birthday+","+idCard;
}
}
```

然后创建排序的类（其中包括按照姓名排序，按照年龄排序，按照出生日期排序），如以下代码所示：

```java
import java.util.Comparator;

public class CompareName implements Comparator<Person>{
	//按照姓名进行排序
	@Override
	public int compare(Person p1, Person p2) {
		// TODO Auto-generated method stub
		return p1.getName().compareTo(p2.getName());
	}
}

class CompareBirthday implements Comparator<Person>{
	//按照出生日期进行排序
	@Override
	public int compare(Person p1, Person p2) {
		// TODO Auto-generated method stub
		return p1.getBirthday().compareTo(p2.getBirthday());
	}
}
```

```java
class CompareAge implements Comparator<Person>{
//按照年龄进行排序
@Override
public int compare(Person p1, Person p2) {
	// TODO Auto-generated method stub
	if(p1.getAge()>p2.getAge())
		return 1;
	else return -1;
}
}
```

最后创建一个主类（在这里我明明为First），用来调用以上所写的类并使程序可以执行。

```java
import java.util.ArrayList;
import java.util.Collections;
public class First {
public static void main(String[] args){
	ArrayList<Person> value = new ArrayList<Person>();
	Person p1 = new Person("张三","1994-3-3","45612346548",'男',26);
	Person p2 = new Person("赵四","2000-5-24","16546165746",'男',20);
	Person p3 = new Person("刘武","1997-2-3","156461656487",'男',23);
	Person p4 = new Person("丁晓晓","1996-6-13","36548588788",'女',24);
	//将创建的各元素添加到ArrayList集合中
	value.add(p1);
	value.add(p2);
	value.add(p3);
	value.add(p4);
	CompareName cn = new CompareName();
	CompareBirthday cb = new CompareBirthday();
	CompareAge ca = new CompareAge();
	System.out.println("\n按姓名排序：");//其中\n表示换行
	Collections.sort(value,cn);
	for(int i = 0; i < value.size(); i++)
		System.out.println(value.get(i).toString());
	System.out.println("\n按年龄排序：");
	Collections.sort(value,ca);
	for(int i = 0; i < value.size(); i++)
		System.out.println(value.get(i).toString());
	System.out.println("\n按生日排序：");
	Collections.sort(value,cb);
	for(int i = 0; i < value.size(); i++)
		System.out.println(value.get(i).toString());
}
}
```

最后看一下运行结果：
按姓名排序：
丁晓晓,女,24,1996-6-13,36548588788
刘武,男,23,1997-2-3,156461656487
张三,男,26,1994-3-3,45612346548
赵四,男,20,2000-5-24,16546165746


按年龄排序：
赵四,男,20,2000-5-24,16546165746
刘武,男,23,1997-2-3,156461656487
丁晓晓,女,24,1996-6-13,36548588788
张三,男,26,1994-3-3,45612346548


按生日排序：
张三,男,26,1994-3-3,45612346548
丁晓晓,女,24,1996-6-13,36548588788
刘武,男,23,1997-2-3,156461656487
赵四,男,20,2000-5-24,16546165746
