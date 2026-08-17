# 第 27 晚：证明复杂度：Resolution、宽度与 SAT

## 今晚目标

把不可满足性的证明当计算对象，实现 resolution 闭包与证书检查。

## 前置回忆（0–5 分钟）

CNF；逻辑蕴涵；SAT。 不看资料先写下相关定义；不会也先留下猜测，阅读后再用另一颜色修正。

## 精读（5–25 分钟）

Resolution 从 (A∨x) 与 (B∨¬x) 推出 (A∨B)。若从 CNF 推到空子句，就得到不可满足证书；每一步可快速检查，因此 proof length/width 是有意义的资源。某些公式需要指数长的受限证明，而一般 Frege/Extended Frege 的强下界仍是重大开放问题。CDCL 求解器学到的冲突子句与 resolution 密切相关。代码生成 resolution 闭包、记录父子和 pivot，再独立验证一条 refutation。

**今晚唯一要守住的不变量：** resolvent 删除且仅删除互补 pivot；重言式子句可安全丢弃；空子句代表矛盾。

**常见陷阱：** 从不可满足直接假定短证明；生成非法 resolvent；把某证明系统下界推广到所有系统。

## 代码实战（25–50 分钟）

运行：

```powershell
python practice.py
```

对 pigeonhole 小实例与随机 CNF 搜索 refutation；输出长度和最大宽度。 先读输出，再定位 `# 动手改造`；只改变一个因素并重新运行。不要删掉原有断言。

## 边界测试与复盘（50–60 分钟）

- 50–57 分钟：补一个最小正例、最小反例和一个边界输入。
- 57–60 分钟：闭卷写“定义 / 不变量 / 本例不能证明什么”各一句。
- 验收：证书验证器不重新求解 SAT；篡改一步会被拒绝。

## 延伸与原始资料

[Cook–Reckhow 1979 DOI](https://doi.org/10.1016/0022-0000(79)90050-5)；[Proof Complexity survey](https://www.cs.toronto.edu/~sacook/homepage/proofcomplexity.pdf)

延伸阅读不计入今晚 60 分钟。先完成代码和验收，再按问题需要阅读原文；链接可能更新，引用时记录访问日期。
