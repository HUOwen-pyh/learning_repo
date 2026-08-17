# 第 26 晚：KMP、Z 函数与字符串边界结构

## 学习目标

- 用 border（真前后缀）理解 prefix function。
- 证明 KMP 匹配指针只做线性总工作。
- 在 prefix function 与 Z function 两种视角间转换问题。

## 前置回忆

模式 `ababaca` 的前缀和后缀有哪些重合？失配后为何不必回退文本指针？Z 数组的 `z[i]` 表示哪个比较区间？

## 精读正文

字符串前缀函数 `pi[i]` 是 `s[:i+1]` 的最长真前缀、同时也是后缀的长度。计算时维护候选 border 长度 `j`；字符失配就跳到更短 border `pi[j-1]`，匹配则扩展。KMP 在文本扫描中复用同样的 border 链：`j` 表示模式前 `j` 字符已匹配，失配只缩短 `j`，文本位置不后退。

线性界来自势能式观察：`j` 每次增长至多 1，总增长 (O(n))；while 中每次回退让 `j` 严格下降，因而总回退也 (O(n))。匹配时间 (O(|text|+|pattern|))，额外空间 (O(|pattern|))。空模式的 API 语义必须明确，脚本按 Python `str.find` 返回 0。

Z 函数 `z[i]` 是从 `i` 开始与整个串前缀相同的最长长度。维护最右匹配盒 `[l,r)`，盒内位置可复用已有 z 值，只有越过 `r` 才产生新字符比较。Z 适合模式匹配、周期、重复前缀；prefix function 更直接表达 border 自动机。陷阱：真前缀不能等于整串、重叠匹配、分隔符恰好出现在输入、Unicode 的代码点语义。

## 60 分钟安排

- 0–10 分钟：手算两个字符串的 pi 与 z。
- 10–28 分钟：写出 KMP 循环不变量和线性证明。
- 28–52 分钟：运行两种算法与 `str.find` 差分。
- 52–60 分钟：处理空模式、重复字符和重叠匹配。

## 代码任务

运行 `practice.py`；实现返回所有（含重叠）匹配位置。进阶从 prefix function 求字符串最短周期，并用重复构造验证。

## 验收标准

- 随机字符串上 KMP 与 `str.find` 一致。
- pi/z 的定义断言通过。
- 能不靠“每轮常数”错误论证，解释 while 总成本线性。

## 延伸/原始资料

- Knuth, Morris & Pratt, [Fast Pattern Matching in Strings](https://doi.org/10.1137/0206024)
- Gusfield, *Algorithms on Strings, Trees, and Sequences*（[出版社页](https://www.cambridge.org/core/books/algorithms-on-strings-trees-and-sequences/F0B095049C7E6EF5356F0A26686C20D3)）

