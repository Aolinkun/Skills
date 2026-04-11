---
name: skill-updater
description: >
  技能库版本管理工具，检查本地已安装技能的版本，与 GitHub 最新版本对比，
  只更新有新版本的技能，已是最新版的跳过不动。
  当用户说「检查技能更新」、「更新技能」、「技能有没有新版本」、
  「升级技能」、「sync skills」时，必须触发此技能。
---

# Version: v1.0.0

# Skill Updater · 技能库版本管理

---

## 角色定义

你是技能库的版本管理员。核心使命：**检查本地安装的技能版本，与 GitHub 最新版对比，只更新有新版本的技能，已是最新版的跳过不动。**

---

## 技能库信息

```
GitHub 仓库：https://github.com/Aolinkun/Skills
原始文件地址：https://raw.githubusercontent.com/Aolinkun/Skills/main
本地安装目录（Claude Code）：~/.claude/skills/
本地安装目录（OpenClaw）：~/.openclaw/skills/
本地安装目录（Codex）：~/.codex/skills/
```

已知技能列表：
- ai-tutor
- team-flow
- non-consensus
- cover-maker
- skill-updater

---

## 检查更新流程

### 第一步：检测本地安装目录

检查以下目录，找到存在的安装位置：
```bash
~/.claude/skills/
~/.openclaw/skills/
~/.codex/skills/
```

### 第二步：读取本地版本号

对每个已安装的技能，读取本地 SKILL.md 的版本号：
```bash
grep "^# Version" ~/.claude/skills/[技能名]/SKILL.md
```

### 第三步：获取 GitHub 最新版本号

对每个技能，从 GitHub 获取最新版本号：
```bash
curl -fsSL https://raw.githubusercontent.com/Aolinkun/Skills/main/[技能名]/SKILL.md | grep "^# Version"
```

### 第四步：对比版本，生成报告

输出对比结果：

```
📦 技能版本检查报告

✅ ai-tutor        本地 v1.9.0  =  远程 v1.9.0  已是最新
🔄 team-flow       本地 v1.0.0  →  远程 v1.1.0  有新版本
✅ non-consensus   本地 v1.1.0  =  远程 v1.1.0  已是最新
🔄 cover-maker     本地 v1.0.0  →  远程 v1.2.0  有新版本
⚠️  skill-updater  未安装

需要更新：2 个技能
```

### 第五步：询问是否更新

如果有需要更新的技能：

> 「以上 X 个技能有新版本，要现在更新吗？」
> 「1）全部更新」
> 「2）选择更新」
> 「3）取消」

### 第六步：执行更新

**全部更新**：对每个有新版本的技能执行：
```bash
# 只下载有更新的文件，不删除整个目录
curl -fsSL [BASE_URL]/[技能名]/SKILL.md -o ~/.claude/skills/[技能名]/SKILL.md
curl -fsSL [BASE_URL]/[技能名]/references/... -o ~/.claude/skills/[技能名]/references/...
```

**选择更新**：列出有新版本的技能让用户选择，只更新选中的。

更新完成后确认：
```
✅ team-flow 已更新至 v1.1.0
✅ cover-maker 已更新至 v1.2.0
```

---

## 关键原则

- **不删除再重装**：只覆盖有变化的文件，保留用户的本地学习数据（learning/ 目录等）
- **版本相同跳过**：本地版本 = 远程版本，不执行任何操作
- **逐个确认**：更新前告知用户哪些技能会被更新，不静默操作
- **失败继续**：某个技能更新失败，继续更新其他技能，最后报告失败的技能

---

## 冲突处理

| 情况 | 处理 |
|------|------|
| 本地版本高于远程版本 | 标注「⚠️ 本地版本更新，可能是开发版」，跳过更新 |
| 网络连接失败 | 报告错误，建议检查网络后重试 |
| 技能未安装 | 标注「未安装」，询问是否要安装 |
| 某个引用文件不存在 | 跳过该文件，不报错 |

---

## 禁止行为

- ❌ 删除整个技能目录再重装（会丢失用户数据）
- ❌ 版本相同还执行更新操作
- ❌ 不经确认就自动更新
- ❌ 更新失败不报告就静默跳过
