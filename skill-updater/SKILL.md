---
name: skill-updater
description: >
  技能库版本管理工具，检查本地已安装技能的版本，与 GitHub 最新版本对比，
  只更新有新版本的技能，已是最新版的跳过不动。
  当用户说「检查技能更新」、「更新技能」、「技能有没有新版本」、
  「升级技能」、「sync skills」时，必须触发此技能。
---

# Version: v1.1.0

# Skill Updater · 技能库版本管理

---

## 角色定义

检查本地技能版本，与 GitHub 对比，只更新有新版本的，已是最新的跳过。

---

## 技能库信息

```
GitHub：https://github.com/Aolinkun/Skills
原始文件：https://raw.githubusercontent.com/Aolinkun/Skills/main
本地目录：~/.claude/skills/ | ~/.openclaw/skills/ | ~/.codex/skills/
```

已知技能：ai-tutor、team-flow、non-consensus、skill-updater

---

## 执行流程

### 第一步：检测本地安装

检查以下目录哪些存在：
```bash
~/.claude/skills/
~/.openclaw/skills/
~/.codex/skills/
```

### 第二步：读取本地版本

对每个已安装技能：
```bash
grep "^# Version" ~/.claude/skills/[技能名]/SKILL.md
```

### 第三步：获取远程版本

```bash
curl -fsSL https://raw.githubusercontent.com/Aolinkun/Skills/main/[技能名]/SKILL.md | grep "^# Version"
```

网络失败时报告：「获取 [技能名] 远程版本失败，请检查网络后重试。」继续检查其他技能，不中断。

### 第四步：生成对比报告

```
📦 技能版本检查报告

✅ ai-tutor        本地 v2.0.0  =  远程 v2.0.0  已是最新
🔄 team-flow       本地 v1.0.0  →  远程 v1.1.0  有新版本
⚠️  non-consensus  本地版本高于远程，可能是开发版，跳过
❓  cover-maker    未安装

需要更新：1 个 ｜ 跳过：2 个
```

### 第五步：询问是否更新

有新版本时：
> 「以上 X 个技能有新版本，要现在更新吗？
> 1）全部更新
> 2）选择更新
> 3）取消」

### 第六步：执行更新

**只覆盖文件，不删除目录**（避免丢失用户学习数据）：

```bash
curl -fsSL [BASE_URL]/[技能名]/SKILL.md -o ~/.claude/skills/[技能名]/SKILL.md
# 同样处理 references/ 下的文件
```

更新完成后确认：
```
✅ team-flow 已更新 v1.0.0 → v1.1.0
```

---

## 版本号规则

| 情况 | 处理 |
|------|------|
| 本地 = 远程 | ✅ 跳过 |
| 本地 < 远程 | 🔄 提示更新 |
| 本地 > 远程 | ⚠️ 跳过，标注「可能是开发版」 |
| 网络失败 | ❓ 报告失败，继续其他技能 |
| 技能未安装 | ❓ 标注未安装，询问是否要安装 |

---

## 禁止行为

- ❌ 删除整个技能目录（会丢失用户数据）
- ❌ 版本相同还执行更新
- ❌ 不经确认就自动更新
- ❌ 网络失败时静默跳过不报告
