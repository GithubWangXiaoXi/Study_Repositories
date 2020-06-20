## Leetcode刷题记录(同步记录)

### 一、前期必备

#### 1、数据结构

**一维：**

- 基础：数组 array (string), 链表 linked list
- 高级：栈 stack, 队列 queue, 双端队列 deque, 集合 set, 映射 map (hash or map), etc

**二维：**

- 基础：树 tree, 图 graph
- 高级：二叉搜索树 binary search tree (red-black tree, AVL), 堆 heap, 并查集 disjoint set, 字典树 Trie, etc

**特殊：**

- 位运算 Bitwise, 布隆过滤器 BloomFilter
- LRU Cache

#### 2、算法

- If-else, switch —> branch
- for, while loop —> Iteration
- 递归 Recursion (Divide & Conquer, Backtrace)
- **搜索 Search:** 深度优先搜索 Depth fifirst search, 广度优先搜索 Breadth fifirst search, A*, etc
- **动态规划** Dynamic Programming
- **二分查找** Binary Search
- **贪心** Greedy
- **数学** Math , 几何 Geometry

注意：在头脑中回忆上面**每种算法的思想**和**代码模板。** 大部分的求解思路离不开最近重复值问题，即**局部最优解**和**非局部最优解**。

#### 3、刻意练习

- **工欲善其事，必先利其器**。**基本功**是区别业余和职业选手的根本。
- 基础动作的**分解训练**和**反复练习**，例如乒乓球，台球，滑雪运动员。
- 算法学习的最大误区是一道题只刷一遍。
- 刻意练习 — **过遍数**（五毒神掌）
  - 练习缺陷、弱点地方
  - 不舒服、不爽、枯燥

#### 4、反馈

**1）即时反馈**

**2）主动型反馈（自己去找）**

- 高手代码 (GitHub, LeetCode, etc.)
- 第一视角直播

**3）被动式反馈（高手给你指点）**

- code review
- 教练看你打，给你反馈

#### 5、刷题要求

**1）刷题第一遍**

- 5分钟：读题 + 思考
- 如果会，别纠结算法优劣，先用最笨的方法求解
- 如果不会，直接看解法：注意！多解法，**比较解法优劣**
- 背诵、默写好的解法
- 记住：不要纠结、不需要抢救

**2）刷题第二遍**

- 马上自己写 —> LeetCode 提交
- 多种解法比较、体会 —> 优化！

**3）刷题第三遍**

- 过了一天后，再重复做题
- 不同解法的熟练程度 —> **专项练习**

**4）刷题第四遍**

- 过了一周：反复回来练习相同题目

### 二、按题型整理

#### 1、数学，几何

| 7. 整数反转      | https://leetcode-cn.com/problems/reverse-integer/ | easy |
| ------------ | ---------------------------------------- | ---- |
| 9.回文数        | https://leetcode-cn.com/problems/palindrome-number/ | easy |
| 13.罗马数字转整数   | https://leetcode-cn.com/problems/roman-to-integer/ | easy |
| 84.柱状图中最大的矩形 | https://leetcode-cn.com/problems/largest-rectangle-in-histogram/ | hard |
| 42. 接雨水      | https://leetcode-cn.com/problems/trapping-rain-water/ | hard |
| 441. 排列硬币    | https://leetcode-cn.com/problems/arranging-coins/ | easy |
| 836. 矩形重叠    | https://leetcode-cn.com/problems/rectangle-overlap/ | easy |
| 892.三维形体的表面积 | https://leetcode-cn.com/problems/surface-area-of-3d-shapes | easy |
|              |                                          |      |

#### 2、线性表：数组与链表

| 1.两数之和         | https://leetcode-cn.com/problems/two-sum/ | easy   |
| -------------- | ---------------------------------------- | ------ |
| 26.删除排序数组中的重复项 | https://leetcode-cn.com/problems/remove-duplicates-from-sorted-array/ | easy   |
| 189.旋转数组       | https://leetcode-cn.com/problems/rotate-array/ | easy   |
| 21.合并两个有序链表    | https://leetcode-cn.com/problems/merge-two-sorted-lists/ | easy   |
| 24.两两交换链表中的节点  | https://leetcode-cn.com/problems/swap-nodes-in-pairs/ | medium |
| 15.三数之和        | https://leetcode-cn.com/problems/3sum/   | medium |
| 4.寻找两个有序数组的中位数 | https://leetcode-cn.com/problems/median-of-two-sorted-arrays/ | hard   |
| 16.最接近的三数之和    | https://leetcode-cn.com/problems/3sum-closest/ | medium |
| 18.四数之和        | https://leetcode-cn.com/problems/4sum/   | medium |
| 27.移除元素        | https://leetcode-cn.com/problems/remove-element/ | easy   |

| 53. 最大子序和 | https://leetcode-cn.com/problems/maximum-subarray/ | easy |
| --------- | ---------------------------------------- | ---- |
|           |                                          |      |
|           |                                          |      |
|           |                                          |      |



#### 3、字符串

| 242. 有效的字母异位词       | https://leetcode-cn.com/problems/valid-anagram/ | easy   |
| ------------------- | ---------------------------------------- | ------ |
| 49.字母异位词分组          | https://leetcode-cn.com/problems/group-anagrams/ | medium |
| 14.最长公共前缀           | https://leetcode-cn.com/problems/longest-common-prefix/ | easy   |
| 28. 实现 strStr()     | https://leetcode-cn.com/problems/implement-strstr/ | easy   |
| 1047.删除字符串中的所有相邻重复项 | https://leetcode-cn.com/problems/remove-all-adjacent-duplicates-in-string/ | easy   |
| 面试题 01.06. 字符串压缩    | https://leetcode-cn.com/problems/compress-string-lcci/ | easy   |
| 1160.拼写单词           | https://leetcode-cn.com/problems/find-words-that-can-be-formed-by-characters/ | easy   |
|                     |                                          |        |

#### 4、栈与队列

| 20.有效的括号            | https://leetcode-cn.com/problems/valid-parentheses | easy |
| ------------------- | ---------------------------------------- | ---- |
| 1047.删除字符串中的所有相邻重复项 | https://leetcode-cn.com/problems/remove-all-adjacent-duplicates-in-string/ | easy |
| 1021. 删除最外层的括号      | https://leetcode-cn.com/problems/remove-outermost-parentheses/ | easy |
| 84.柱状图中最大的矩形        | https://leetcode-cn.com/problems/largest-rectangle-in-histogram/ | hard |
|                     |                                          |      |
|                     |                                          |      |
|                     |                                          |      |
|                     |                                          |      |

#### 5、树

| 111. 二叉树的最小深度    | https://leetcode-cn.com/problems/minimum-depth-of-binary-tree/ | easy   |
| ---------------- | ---------------------------------------- | ------ |
| 236. 二叉树的最近公共祖先  | https://leetcode-cn.com/problems/lowest-common-ancestor-of-a-binary-tree/ | medium |
| 101. 对称二叉树       | https://leetcode-cn.com/problems/symmetric-tree/ | easy   |
| 104. 二叉树的最大深度    | https://leetcode-cn.com/problems/maximum-depth-of-binary-tree/ | easy   |
| 662. 二叉树最大宽度     | https://leetcode-cn.com/problems/maximum-width-of-binary-tree/ | medium |
| 783. 二叉搜索树节点最小距离 | https://leetcode-cn.com/problems/minimum-distance-between-bst-nodes/ | easy   |
| 257. 二叉树的所有路径    | https://leetcode-cn.com/problems/binary-tree-paths/ | easy   |
| 938. 二叉搜索树的范围和   | https://leetcode-cn.com/problems/range-sum-of-bst/ | easy   |

#### 6、图

| 200. 岛屿数量   | https://leetcode-cn.com/problems/number-of-islands/ | medium |
| ----------- | ---------------------------------------- | ------ |
| 695.岛屿的最大面积 | https://leetcode-cn.com/problems/max-area-of-island/ | medium |
| 365. 水壶问题   | https://leetcode-cn.com/problems/water-and-jug-problem/ | medium |
|             |                                          |        |
|             |                                          |        |



#### 7、搜索

| 35. 搜索插入位置 | https://leetcode-cn.com/problems/search-insert-position/ | easy |
| ---------- | ---------------------------------------- | ---- |
|            |                                          |      |
|            |                                          |      |
|            |                                          |      |
|            |                                          |      |
|            |                                          |      |
|            |                                          |      |
|            |                                          |      |

#### 8、动态规划

| 300. 最长上升子序列  | https://leetcode-cn.com/problems/longest-increasing-subsequence/ | medium |
| ------------- | ---------------------------------------- | ------ |
| 53. 最大子序和     | https://leetcode-cn.com/problems/maximum-subarray/ | easy   |
| 1143. 最长公共子序列 | https://leetcode-cn.com/problems/longest-common-subsequence/ | medium |
| 5. 最长回文子串     | https://leetcode-cn.com/problems/longest-palindromic-substring/ | medium |
|               |                                          |        |
|               |                                          |        |
|               |                                          |        |
|               |                                          |        |

#### 9、贪心

| 53. 最大子序和 | https://leetcode-cn.com/problems/maximum-subarray/ | easy |
| --------- | ---------------------------------------- | ---- |
|           |                                          |      |
|           |                                          |      |
|           |                                          |      |



### 三、按日期整理

#### 2019-12

**2019.12.28**  

1，两数之和（用hashmap需要保证输出结果{i，j} ,I < j）
2，删除排序数组中的重复项（注意数组是有序的，比较相邻两个数即可）
3，旋转数组（用链表最好有头节点）
4，合并两个有序链表（最好有头节点和尾指针）

**2019.12.30**
1，两两交换链表中的节点（增加一个头指针，设置pre，p，r三指针进行调整）
2，三数之和（先排序，再二分查找，勉强通过；注意多种剪枝优化（当前最大最小值，排序后i的值是否大于0）；最好的方法是结合快排的思想，以0为界，前后移动left,right双指针，注意对i，left的去重）

-----------------------------------------------------------------------------------------------------------------

#### 2020-1

**2020.1.1**
1，寻找两个有序数组的中位数（要求的时间复杂度为O(log(m+n)），不是O(m+n)。。。）
2，最接近的三数之和（同三数之和，双指针，多一层判断）
3，四数之和（同三数之和，用当前max，min与target比较，进行剪枝）
4，移除元素
5，有效的字母异位词（用一个26位计数器表，比较时，s增，t减，O(n）即可）

**2020.1.2**
1、字母异位词分组

**2020.1.5**
1、整数反转（负数%10是负数，注意溢出判断）
2、回文数（回文数和整数反转不同不会溢出，注意剪枝）
3、罗马数字转整数（IV与VI的区别）
4、最长公共前缀
5、有效的括号
6、实现strStr(双指针）

**2020.1.6**
1、搜索插入位置（有序数组，考虑二分查找）
2、删除字符串中的所有相邻重复项（两个栈）
3、删除最外层的括号（注意if的判断顺序）
4、柱状图中最大的矩形（单调栈）
5、接雨水（testCase: [5,2,4,2,3],  [2,1,0,2],  [4,2,0,3,2,5],  [0,1,0,2,1,0,1,3,2,1,2,1]

**2020.1.7**
1、排列硬币（注意返回值，边界值检验）
2、二叉树的最小深度（找重复值问题）
3、二叉树的最近公共祖先

**2020.1.8**
1、对称二叉树
2、二叉树的最大深度
3、二叉树最大宽度

**2020.1.9**
1、二叉搜索树结点最小距离（中序遍历）
2、二叉树的所有路径
3、二叉搜索树范围和（不用递归的中序遍历，利用二叉搜索树二分查找）

-----------------------------------------------------------------------------------------------------------------

#### 2020-3

**2020.3.14**
1、300. 最长上升子序列        动态规划：若0 < j < i, 则若nums[j] < nums[i]，则上升子序列状态会发生变化，dp[i] = max（dp[i] ,dp[j] + 1）

**2020.3.15**
1、200.岛屿数量： 第一次到岛上， 便把这片岛屿沉下去
2、695.岛屿的最大面积：同上，


2020.3.16
1、面试题01.06    字符串压缩

2020.3.17
1、1160 拼写单词       注意保证chars中的每个字母只能使用一次

2020.3.21
1、365 水壶问题   BFS/DFS  题目理解错了，但是还不会做

-----------------------------------------------------------------------------------------------------------------

#### 2020-5

2020.5.4

53 最大子序和

2020.5.7

1143 最长公共子序列

2020.5.8

5 最长回文子串