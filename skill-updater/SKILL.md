---
name: skill-updater
description: >
  技能库版本管理工具，检查 Claude Code、Codex 和 Grok 中已安装技能的版本，与 Aolinkun/Skills 的 GitHub 最新版本比较，并在用户确认后完整更新技能目录。当用户说“检查技能更新”“更新技能”“技能有没有新版本”“升级技能”或“sync skills”时使用。
---

# Version: v2.0.0

# Skill Updater · 完整技能包更新器

## 目标

比较本地与 GitHub 版本，只在用户确认后更新。更新必须包含 `SKILL.md`、references、assets、scripts、tests 和 agents 等完整技能包，不能只下载主文件。

## 仓库与安装位置

```text
GitHub: https://github.com/Aolinkun/Skills
安装脚本: https://raw.githubusercontent.com/Aolinkun/Skills/main/install.sh
Claude Code: ~/.claude/skills/
Codex: ~/.codex/skills/
Grok: ~/.grok/skills/
```

已知技能：`ai-tutor`、`team-flow`、`non-consensus`、`skill-updater`、`fastlane`。

## 检查流程

1. 检查三个宿主目录中实际存在的技能。
2. 从本地 `SKILL.md` 读取 `# Version:`。
3. 从 GitHub 对应 `SKILL.md` 获取远程版本。
4. 网络失败时逐项报告，继续检查其他技能。
5. 按语义版本比较并输出报告：

```text
✅ ai-tutor        本地 v4.0.0 = 远程 v4.0.0
🔄 team-flow       本地 v1.0.0 → 远程 v1.1.0
⚠️ non-consensus  本地高于远程，可能是开发版
❓ fastlane        未安装
```

不要把字符串字典序当作版本大小；逐段比较主版本、次版本和修订号。

## 更新前确认

列出宿主、技能、旧版本和新版本，然后让用户选择全部更新、选择更新或取消。没有确认不得写入。

## 完整更新

调用仓库安装脚本的非交互参数，避免自行维护文件清单：

```bash
curl -fsSL https://raw.githubusercontent.com/Aolinkun/Skills/main/install.sh \
  | SKILLS_TARGET=1 SKILLS_CHOICE=1 bash
```

`SKILLS_TARGET`：

- `1` Claude Code
- `2` Codex
- `3` Grok
- `4` 三端全部

`SKILLS_CHOICE`：

- `1` ai-tutor
- `2` team-flow
- `3` non-consensus
- `4` skill-updater
- `5` fastlane
- `6` 全部技能

多个技能分次调用时，每次都核对返回码。更新后重新读取版本并确认完整目录存在。

## 数据与冲突保护

- 只更新宿主的技能包目录，不触碰工作目录中的 `learning/`、课程进度或用户资料。
- 安装器会覆盖仓库管理的同名文件，并保留技能目录中的未知附加文件。
- 安装到 Grok 时，安装器会自动在入口 frontmatter 中生成 `user_invocable: true`。
- 本地版本高于远程时默认跳过，除非用户明确要求降级。
- 本地文件有用户自定义修改时先报告差异；不要静默覆盖。
- 下载或包校验失败时停止该技能更新，不报告成功。

## 完成报告

说明：

- 更新了哪些宿主和技能；
- 每项的旧版本与新版本；
- 哪些失败或跳过及原因；
- 是否需要重启宿主或重新加载技能列表。

## 禁止行为

- 不经确认自动更新。
- 版本相同仍重复更新。
- 只下载 `SKILL.md` 而漏掉支持文件。
- 删除工作目录中的学习数据。
- 网络或校验失败时静默跳过。
- 把本地开发版自动降级到远程旧版。
