# 第154晚：约束解码周验收

## 目标与前置

- 目标：组合查询约束、PDA mask 与终值 schema，区分 soundness、completeness 与性能。
- 前置：第148–153晚。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 8 | [LMQL paper](https://arxiv.org/pdf/2212.06094v3) | v3 | §6.4 Discussion（PDF pp.21–22），重点读 user-study 威胁效度段 | 论文明确承认哪类结论尚未被验证？ |
| 6 | [PICARD](https://aclanthology.org/2021.emnlp-main.779.pdf) | EMNLP 2021 | §3 Experiments 末段与 §4 Conclusion（PDF pp.5–6）；论文没有单列 Limitations | 增量语法有效是否等于任务语义正确？ |
| 6 | [XGrammar](https://proceedings.mlsys.org/paper_files/paper/2025/file/5c20ca4b0b20b0bd2f1d839dc605e70f-Paper-Conference.pdf) | MLSys 2025 | §4.4 Impact on Structured Generation 与 §6 Conclusion（PDF pp.10–11）；论文没有 §6 Discussion | 论文验证了格式正确性还是业务正确性？ |

## 阅读导引

建立三列表：前缀语法、终值结构、业务语义。每个失败案例只归入最早能发现它的一层，并写出漏报或误报风险。注意三篇论文都没有题为“Limitations”的统一章节；本晚必须从各自真实存在的讨论、实验边界与结论中提取限制，不能按想象中的目录跳读。

## 核心推导

令 G 为语法语言、S 为 schema 接受集、B 为业务谓词，则最终输出集合为 G∩S∩B。若每层过滤均 sound（不接受层外值），组合仍 sound；若任一层过度剪枝，则组合不 complete。

## 工业联系与事实标签

- [THEOREM] 集合交保持每个成员约束，因此多个 sound 验证器串联仍 sound。
- [EMPIRICAL] 三篇论文测量对象不同，不能直接横向比较吞吐数字。
- [INFERENCE] 生产系统应记录“哪一层拒绝、在哪个路径、哪个前缀”，支持回放。
- [OPEN] 自由文本与严格结构混合输出的统一低延迟约束仍活跃发展。

## 严格 60 分钟

- 0–5：画三层图；5–25：必读；25–50：完成综合练习；50–57：做一次故障注入；57–60：写周结论。

## 验收

全部断言通过；能给出一个语法合法但 schema 非法、以及 schema 合法但业务非法的例子。

## 可选延伸

将枚举解码换成 beam search，不计时。
