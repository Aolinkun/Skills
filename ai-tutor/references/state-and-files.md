# 状态与文件规范

## 1. 原则

- 让文件复杂度匹配课程复杂度。
- 把 `state.json` 作为唯一机器状态来源。
- 把 `progress.md` 作为人类可读摘要，不反向覆盖机器状态。
- 分离教材、会话和评估证据。
- 写入前读取，保留未知字段和用户手工内容。
- 追加式记录优先；不虚构写入成功。

## 2. 分级结构

### 短期课程

```text
learning/<topic-slug>/
├── state.json
├── progress.md
└── sessions/
    └── YYYY-MM-DD-HHMM.md
```

### 多单元课程按需增加

```text
├── curriculum.md
├── units/
│   └── unit-01-<slug>.md
├── assessments.jsonl
└── summary.md
```

不要预先创建空目录和永远不会使用的文件。

## 3. 文件职责

- `state.json`：版本、目标、模式、状态机位置、掌握状态、薄弱点、复习队列、应用队列和下一动作。
- `progress.md`：当前有效结论、最近表现、薄弱点、应用意图和续学入口。
- `sessions/`：每次会话的输入、教学动作、回答、评估、决策和下一步。
- `curriculum.md`：可观察成果、范围、先备知识和单元地图。
- `units/`：稳定教材与任务定义，不写入反复变化的聊天记录。
- `assessments.jsonl`：每行一个评估证据对象，只追加。
- `summary.md`：只在结课或阶段总结时生成。

从 `assets/templates/` 复制需要的模板。

## 4. 初始化

1. 检查主题目录是否存在；已有时先读取，不覆盖。
2. 使用稳定、简短的英文或拼音小写连字符作为 `topic-slug`。
3. 创建 `state.json`、`progress.md` 和第一次 session。
4. 写入真实已知信息；未知值使用 `null`、空数组或 `unknown`。
5. 使用 `scripts/validate-state.py` 校验状态。

## 5. 一次交互的更新顺序

1. 完成本次 session 记录。
2. 发生正式评估时，向 `assessments.jsonl` 追加合法 JSON。
3. 更新 `state.json` 的状态、证据、队列、下一动作和时间戳。
4. 运行 `scripts/validate-state.py`。
5. 校验通过后更新 `progress.md` 摘要。
6. 课程结构变化时再更新 `curriculum.md`。

关键步骤失败时，说明哪个文件未更新，并保留可复制的状态内容。

## 6. 续学读取顺序

1. `state.json`；
2. `progress.md`；
3. 最近一个 session；
4. 当前单元；
5. 与本次有关的评估记录。

先处理 `application_queue` 中未闭环的应用，再检测到期复习。不要默认扫描所有历史文件。

## 7. 冲突与恢复

### 状态不合法

- 不直接覆盖；
- 备份原状态；
- 从最近 session、评估证据和 progress 重建；
- 标记 `recovered: true` 和不确定项。

### 多窗口更新

写入前比较 `updated_at`。发现读取后被其他会话更新时重新读取并合并追加内容；无法安全合并时停止写入并报告冲突。

### 信息冲突

优先级：有效 `state.json` > 最新 assessment/session 证据 > `progress.md` > unit 文本。若状态明显陈旧，按证据修正并在 session 记录原因。

## 8. v3 迁移

旧版通常只有 `progress.md`、`user-profile.md` 和写入回答的 `unit-*.md`。

1. 保留全部原文件。
2. 运行 `scripts/migrate-v3.py <旧主题目录>` 生成独立预览目录。
3. 核对主题、下一步、薄弱点和单元状态。
4. 用户确认后再采用新目录；不自动删除或覆盖旧版。
5. 把旧单元视为历史教材和证据，不伪造未发生的评分。

## 9. 画像与隐私

`learning/learner-profile.md` 为可选文件。只记录用户同意长期保存、且会持续改善教学的信息。不要主动持久化敏感身份、健康、政治或财务信息。

## 10. 无文件系统

在对话中维护最小状态；用户需要跨窗口续学时输出可复制的 JSON 或 Markdown。不要声称已经创建、读取或更新本地文件。
