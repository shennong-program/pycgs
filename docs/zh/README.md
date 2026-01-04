# 共指图搜索（Coreference Graph Search, CGS）

## 基础 CGS（Foundational CGS）

为阐明 CGS 的流程，我们用一个简单案例进行说明。

### 示例

考虑如下节点集合：

- $A, B, C, D, E, F$

共指关系如下：

- $A \to B$
- $B \to \mathbf{C}$
- $D \to B$
- $E \to \mathbf{F}$

其中，$\mathbf{C}$ 和 $\mathbf{F}$ 被人工指定为**主词（Primary Terms）**。

![CPTG](../images/cptg.png)

### CPTG 的要求

可由上述节点与有向边构建“共指主词图（Coreference Primary Term Graph, CPTG）”。该 CPTG 需满足：

1. 图必须是**有向无环图（Directed Acyclic Graph, DAG）**。
2. 图中任意**主词（Primary Term）**的**出度（out-degree）**必须为 **0**。
3. 图中任意节点的**出度**必须满足 **≤ 1**，即不存在**分叉节点（branching nodes）**。

### 预计算字典

一旦 CPTG 构建完成，即可进行预先的图计算以优化查询，从而确定任意术语节点所对应的**最终主词（ultimate Primary Term）**。

这些预计算结果会存入一个新建字典 $D$。需要特别指出的是，$D$ 也包含主词的**自映射关系**（例如 $\mathbf{C}\to\mathbf{C}$），从而使被查询的术语本身能够被识别为主词。

字典映射示例如下：

- $A \to \mathbf{C}$
- $B \to \mathbf{C}$
- $D \to \mathbf{C}$
- $E \to \mathbf{F}$
- $\mathbf{C} \to \mathbf{C}$
- $\mathbf{F} \to \mathbf{F}$

因此，在查询时，只需检索该字典即可快速判断任意给定术语（包括主词本身）是否存在对应的主词；若存在，则其对应值即为该术语关联的主词。

### 算法 1：基础 CGS

```text
Algorithm 1: Foundational CGS
Input:  Set of nodes N, coreference relationships R
Output: Dictionary D storing the ultimate Primary Terms

1.  Initialize dictionary D
2.  Construct the Coreference Primary Term Graph (CPTG) G from N and R
3.  for each node n in G do
4.      if n is not a Primary Term then
5.          Find the ultimate Primary Term p for n
6.          if p exists then
7.              Add mapping n → p to D
8.          end if
9.      else
10.         Add self-referencing mapping n → n to D
11.     end if
12. end for

For searching:
13. Given any term t, query D to ascertain whether a corresponding Primary Term exists
14. if t exists in D then
15.     Retrieve the corresponding Primary Term p from D
16. end if
```

## 加权 CGS（Weighted CGS）

在构建 CPTG 时，有向边通常由数据库自动抽取得到，因此往往无法满足基础 CGS CPTG 的第三条要求（即**不允许分叉节点**）。在这种情况下，我们可为每条有向边分配一个**权重（weight）**，并进行**加权图搜索**。

### 示例

考虑如下节点集合：

- $A, B, C, D, E$

共指关系如下（每条边带有权重）：

- $A \xrightarrow{w_{AB}=1} B$
- $B \xrightarrow{w_{BC}=2} \mathbf{C}$
- $D \xrightarrow{w_{DB}=1} B$
- $B \xrightarrow{w_{BE}=1} \mathbf{E}$

其中，$\mathbf{C}$ 和 $\mathbf{E}$ 被人工指定为**主词（Primary Terms）**。

该 CPTG 满足前两条要求（DAG；主词出度为 0），但不满足第三条要求，因为节点 $B$ 同时指向 $\mathbf{C}$ 与 $\mathbf{E}$，形成分叉。

![Weighted CPTG](../images/cptg-weighted.png)

### 加权图搜索规则

在为某个节点计算其最终主词时：

1. 获取该节点所有下游（outgoing）有向边。
2. **选择权重最大的那条出边**所指向的下游节点作为“下一跳”。
3. 重复上述过程，直到到达某个**主词**为止。

**以节点 $A$ 为例：**

- 从 $A$ 出发，其唯一的下游节点为 $B$。
- 从 $B$ 出发，有两条候选边：$B \to \mathbf{C}$（权重 2）与 $B \to \mathbf{E}$（权重 1）。
- 因为 $2 > 1$，选择 $B \to \mathbf{C}$。
- 到达 $\mathbf{C}$ 后停止，因为 $\mathbf{C}$ 是主词。

因此，$A$ 的最终主词为 $\mathbf{C}$，对应路径为：

- $A \to B \to \mathbf{C}$
  而不是：
- $A \to B \to \mathbf{E}$。

### 结果字典

按上述规则，我们仍可得到与基础版 CGS 一致形式的字典：

- $A \to \mathbf{C}$
- $B \to \mathbf{C}$
- $D \to \mathbf{C}$
- $\mathbf{C} \to \mathbf{C}$
- $\mathbf{E} \to \mathbf{E}$

### 算法 2：加权 CGS

```text
Algorithm 2: Weighted CGS Algorithm
Input:  Set of nodes N, coreference relationships R, weights W of directed edges
Output: Dictionary D storing the ultimate Primary Terms

1.  Initialize dictionary D
2.  Construct the Coreference Primary Term Graph (CPTG) G from N, R, and W
3.  for each node n in G do
4.      if n is not a Primary Term then
5.          Find the ultimate Primary Term p for n using weighted graph search
6.          if p exists then
7.              Add mapping n → p to D
8.          end if
9.      else
10.         Add self-referencing mapping n → n to D
11.     end if
12. end for

For searching:
13. Given any term t, query D to ascertain whether a corresponding Primary Term exists
14. if t exists in D then
15.     Retrieve the corresponding Primary Term p from D
16. end if
```

## 主词提取器（Primary Term Extractor）

当我们获得一个将术语映射到其主词的字典 $D$ 后，如何在任意给定字符串 $S$ 中**高效识别**所有可能出现的术语就成为一个关键挑战——尤其当 $D$ 中包含大量**高度相似或互相重叠**的术语时更为明显。

### 动机（术语重叠）

例如，考虑以下两个术语：

- “Ma-huang”（NMM ID：`NMM-0006`）
- “Ma-huang-duan”（NMM ID：`NMM-000A`）

它们均为**神农知识库**中记录的 NMM 通用名，并被纳入我们的主词字典。

假设用户提供两条字符串：

- **字符串 1：** `What is the NMM ID of Ma-huang?`
- **字符串 2：** `What is the NMM ID of Ma-huang-duan?`

若采用简单字符串匹配方法，在处理**字符串 2** 时可能同时匹配到 “Ma-huang” 与 “Ma-huang-duan”，产生重叠，从而干扰后续知识抽取并引入歧义。

### Trie + 最长匹配策略

为解决该问题，我们在 CGS 框架中引入**主词提取器（Primary Term Extractor）**算法。该算法使用：

- **Trie（前缀树）**数据结构
- **最长匹配（longest-match）**策略

从而在任意字符串 $S$ 中高效且准确地抽取所有出现在 $D$ 中的候选术语，并避免冲突或重叠。

### 算法 3：主词提取器

```text
Algorithm 3: Primary Term Extractor
Input:  Dictionary D mapping terms to their primary terms; text string S
Output: Mapping M from terms found in S to their primary terms

1.  Build a Trie T from the keys of D
2.  Initialize an empty mapping M
3.  Let n ← length of S
4.  Let index i ← 0
5.  while i < n do
6.      Candidates ← all prefixes of S[i:] that are in Trie T
7.      if Candidates is not empty then
8.          longest_match ← the longest string in Candidates
9.          primary_term ← D[longest_match]
10.         Add mapping longest_match → primary_term to M
11.         i ← i + length(longest_match)
12.     else
13.         i ← i + 1
14.     end if
15. end while
```
