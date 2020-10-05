## SQL常用语句整理（待更新）

### 1、Select语句

参考[MySQL查询语句(select)详解（1）](https://www.cnblogs.com/drake-guo/p/6104654.html)

注意

- `where`条件用`and`并列

```sql
---wrong---
select height,times,threshold,correctRate,dataset 
from boost 
where height=3,times=40,threshold=0.2,dataset='classical model'
[Err] 1064 - You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'times=40,threshold=0.2,dataset='classical model'' at line 3

---right---
select height,times,threshold,correctRate,dataset 
from boost 
where height=3 and times=40 and threshold=0.2 and dataset='classical model'
```

- 字符串用**'...'**圈起来

