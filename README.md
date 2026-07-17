# Skills · 跨平台 Agent Skills 技能库

> 由 [@Aolinkun](https://github.com/Aolinkun) 维护 · 持续更新

一套来自真实工作与学习场景的 Agent Skills，支持 Claude Code、Codex 和 Grok。每个技能以 `SKILL.md` 为入口，并可携带 references、assets、scripts、tests 和 agents 等支持资源。

## 一键安装

```bash
curl -fsSL https://raw.githubusercontent.com/Aolinkun/Skills/main/install.sh | bash
```

按提示选择：

1. 安装目标：Claude Code / Codex / Grok / 全部；
2. 要安装的技能或全部技能。

安装器会下载完整仓库快照并复制完整技能目录，不会只安装 `SKILL.md`。如果宿主已经运行，安装后请重启应用或重新加载技能列表。

### 非交互安装

适合脚本和自动化环境：

```bash
# 安装 AI Tutor 到 Codex
curl -fsSL https://raw.githubusercontent.com/Aolinkun/Skills/main/install.sh \
  | SKILLS_TARGET=2 SKILLS_CHOICE=1 bash

# 安装 AI Tutor 到 Grok
curl -fsSL https://raw.githubusercontent.com/Aolinkun/Skills/main/install.sh \
  | SKILLS_TARGET=3 SKILLS_CHOICE=1 bash

# 把全部技能安装到三个宿主
curl -fsSL https://raw.githubusercontent.com/Aolinkun/Skills/main/install.sh \
  | SKILLS_TARGET=4 SKILLS_CHOICE=6 bash
```

`SKILLS_TARGET`：`1` Claude Code、`2` Codex、`3` Grok、`4` 全部。

`SKILLS_CHOICE`：`1` AI Tutor、`2` Team Flow、`3` Non-Consensus、`4` Skill Updater、`5` Fastlane、`6` 全部。

### 手动安装

```bash
git clone https://github.com/Aolinkun/Skills.git

# Claude Code
mkdir -p ~/.claude/skills/ai-tutor
cp -R Skills/ai-tutor/. ~/.claude/skills/ai-tutor/

# Codex
mkdir -p ~/.codex/skills/ai-tutor
cp -R Skills/ai-tutor/. ~/.codex/skills/ai-tutor/
```

Grok 要求技能入口包含 `user_invocable: true`。请优先使用一键安装器；它会在写入 `~/.grok/skills/` 时自动生成 Grok 专用入口，同时保持仓库中的跨平台源文件不变。

## 技能列表

### 🎓 AI Tutor · 自适应掌握学习导师

`v4.0.0` · 适合：系统学习、概念解释、练习检测、间隔复习和跨会话续学

**解决什么问题**：只阅读 AI 的讲解很容易产生“听懂了”的错觉。AI Tutor 通过起点诊断、主动加工、证据评估、纠错、间隔复习和迁移任务，帮助学习者形成能保持、能应用的能力。

**五种模式**：

- `course`：系统课程与长期学习；
- `quick-explain`：直接解释概念，默认不建档；
- `practice`：出题并根据回答评估；
- `review`：读取进度、追踪应用、做延迟复习；
- `diagnosis`：明确调用已学概念分析现实问题。

**v4 核心能力**：

- 只在 `check` 阶段强制等待，不为流程扣留用户明确需要的答案；
- 从学习者回答中的假设和破绽生成苏格拉底追问；
- 按准确性、推理、迁移和独立性给出证据评估；
- 区分 `assisted`、`provisional`、`retained`、`transferred` 和 `mastered`；
- 续学时先追踪上次应用意图和到期复习；
- 按课程复杂度分级建档，小问题不创建一整套文件；
- 使用 `state.json`、模板和校验脚本提高跨会话一致性。

**使用示例**：

```text
我想系统学习经济学，最终能看懂公司的商业模式
给我讲一下机会成本
考考我供需关系
继续学统计学基础
用我们学过的供需框架分析这个现实问题
```

---

### 🔀 Team Flow · 多角色任务协作系统

`v1.1.0` · 适合：用多个 AI 和真人协作管理任务

- 统一任务看板；
- 人类和 AI 可以相互调用；
- 创建任务前明确验收标准；
- 根据已完成任务更新成员能力。

```text
新建任务
完成任务
更新团队能力
查看任务
```

---

### ✍️ Non-Consensus · 正确的非共识内容生成

`v1.2.0` · 适合：需要生产反常识但可靠内容的创作者

- 识别领域中的刻板印象；
- 用反例检验，而不是为了反常识而反常识；
- 形成新框架并定义关键词；
- 适配小红书、抖音和视频号。

```text
帮我生成非共识内容
我是做知识服务的，给我 10 个选题
帮我判断这个观点是不是好的非共识
```

---

### 🔧 Skill Updater · 完整技能包更新器

`v2.0.0` · 适合：检查并升级本仓库技能

- 比较 Claude Code、Codex、Grok 的本地与远程版本；
- 只更新有新版本的技能；
- 经用户确认后调用安装器更新完整目录；
- 不遗漏 references、assets、scripts、tests 或 agents；
- 不触碰工作目录中的学习记录和业务数据。

```text
检查技能更新
更新技能
技能有没有新版本
```

---

### 🚀 Fastlane · 快车道业务评估

`v1.1.0` · 适合：评估业务潜力、瓶颈与升级路径

- 用 NECST 五维度评估业务；
- 判断当前位于人行道、慢车道或快车道；
- 找到最致命瓶颈；
- 给出换车道路径及代价。

```text
评估我的业务
我在哪条车道
这个生意能不能换快车道
```

## 验证安装

```bash
# 查看版本
grep '^# Version' ~/.claude/skills/ai-tutor/SKILL.md
grep '^# Version' ~/.codex/skills/ai-tutor/SKILL.md
grep '^# Version' ~/.grok/skills/ai-tutor/SKILL.md

# Grok 入口必须可调用
grep '^user_invocable: true' ~/.grok/skills/ai-tutor/SKILL.md

# 校验 AI Tutor v4 完整包
python3 ~/.codex/skills/ai-tutor/scripts/validate-package.py \
  ~/.codex/skills/ai-tutor

# 校验 Grok 专用入口
python3 ~/.grok/skills/ai-tutor/scripts/validate-package.py \
  --allow-grok-frontmatter ~/.grok/skills/ai-tutor
```

校验成功时会包含：

```text
OK: valid AI Tutor v4 package
```

## 仓库结构

```text
Skills/
├── ai-tutor/
│   ├── SKILL.md
│   ├── agents/
│   ├── assets/templates/
│   ├── references/
│   ├── scripts/
│   └── tests/
├── team-flow/
├── non-consensus/
├── skill-updater/
├── fastlane/
└── install.sh
```

## 卸载

删除对应宿主下的技能目录：

```bash
rm -rf ~/.claude/skills/ai-tutor
rm -rf ~/.codex/skills/ai-tutor
rm -rf ~/.grok/skills/ai-tutor
```

卸载技能不会删除工作目录中的学习课程和进度文件。

## 隐私与数据边界

- 仓库只包含通用技能规则、模板、参考资料、脚本和测试用例，不包含个人课程、学习记录、用户画像或客户资料；
- 安装器只下载本仓库并写入所选宿主的技能目录，不上传本地文件，也不收集遥测数据；
- 本机路径、密钥、令牌、邮箱、电话和系统元数据不应提交到仓库；发布包只从版本控制中的文件生成；
- 示例中的姓名、日期、数量和业务场景均为虚构或通用占位。

## 版本记录

### AI Tutor

| 版本 | 更新内容 |
|---|---|
| v4.0.0 | 将路由扩展为五种模式，引入显式教学状态、四维证据评估、长期掌握分层，以及结构化状态、模板与校验机制 |
| v3.0.0 | 明确触发边界与等待锚点，加入回答驱动追问、合并冷启动、动态学习风格画像、心流校准、元评估及暂停/切换/退出机制 |
| v2.2.0 | 修复续学时读取单元文件、user-profile 创建时机 |
| v2.1.0 | 明确每个单元必须存成独立文件 |
| v2.0.0 | 完整重构：消除重复规则，结构清晰，优先级明确 |
| v1.9.0 | 强制等待规则 |
| v1.8.0 | 学以致用追踪和问题反向诊断 |
| v1.7.0 | 用户画像机制 |
| v1.6.0 | 技能型主题实战任务 |
| v1.5.0 | 严格评估规则 |
| v1.4.0 | 角色、优先级和知识边界 |
| v1.3.0 | 主题澄清 |
| v1.2.0 | 提示、纠错、情绪感知和上下文压缩 |
| v1.1.0 | 续学、间隔复习和结课判断 |
| v1.0.0 | 初始版本 |

### Skill Updater

| 版本 | 更新内容 |
|---|---|
| v2.0.0 | 改为更新完整技能目录，支持 v4 的 agents、assets、scripts 和 tests，增加冲突与数据保护 |
| v1.1.0 | 网络失败容错、版本对比逻辑完善 |
| v1.0.0 | 初始版本 |

### 其他技能

| 技能 | 版本 | 更新内容 |
|---|---|---|
| Team Flow | v1.1.0 | 文件异常时提供明确引导 |
| Non-Consensus | v1.2.0 | 批量生产节流，先打分再展开 |
| Fastlane | v1.1.0 | 追问、双层评分、迭代评估与代价透明 |

## License

MIT
