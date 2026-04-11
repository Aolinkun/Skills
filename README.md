# Skills · Claude Code 技能库

> 由 [@Aolinkun](https://github.com/Aolinkun) 维护 · 持续更新

一套用于 Claude Code / OpenClaw / Codex 的实用技能集合，来自真实业务场景中的沉淀。每个技能都经过真实使用验证，开箱即用。

---

## 一键安装

```bash
curl -fsSL https://raw.githubusercontent.com/Aolinkun/Skills/main/install.sh | bash
```

运行后选择安装目标（Claude Code / OpenClaw / Codex / 全部），再选择安装哪个技能。

> **Codex 用户注意**：需要用 `codex --enable skills` 启动才能使用技能。

---

## 技能列表

### 🎓 AI Tutor · 苏格拉底学习导师
`v1.9.0` · 适合：想高效学习新知识的人

**解决什么问题**：大多数人用 AI 学习的方式是错的——问 AI 问题，AI 给你讲解。但真正高效的学习是反过来的：导师主动提问，你来回答。Bloom 1984 年的研究证明，这种方式可以让学生超越 98% 的同龄人。

**这个技能做什么**：
- Claude 主动出题，而不是被动讲解
- 遇到问题时反向诊断，推荐相关知识框架
- 每个单元结束后追踪「学以致用」，下次续学先问效果
- 答对了才进入下一阶段，答错了退回巩固
- 技能型主题（短视频、写作、编程）额外布置实战任务
- 学习进度存成文件，换了对话也能继续
- 连续答错时自动降难度，不机械推进

**使用**：
```
我想学维特根斯坦的逻辑哲学论
我想学短视频文案创作
继续学经济学
```

---

### 🔀 Team Flow · 多角色任务协作系统
`v1.0.0` · 适合：用 Claude Code / OpenClaw 管理团队任务的人

**解决什么问题**：一个人同时用多个 AI 和真人协作时，任务散落在各处——AI 做到一半发现缺资料又来找人，没有一个地方让所有角色都知道现在在做什么。

**这个技能做什么**：
- 统一任务看板，人类和 AI 都能看到
- 任何角色都可以调用任何角色（人调 AI、AI 调人、AI 调 AI）
- 任务必须有验收标准才能创建，防止模糊任务
- 已完成任务自动推断每个成员擅长什么，下次分配更精准

**使用**：
```
新建任务
完成任务
更新团队能力
查看任务
```

---

### ✍️ Non-Consensus · 正确的非共识内容生成
`v1.0.0` · 适合：做自媒体内容的人

**解决什么问题**：大多数人知道「反常识」内容容易爆，但不知道怎么批量生产。盲目反常识又容易传播错误认知。这个技能帮你系统性地找到真正正确的非共识，而不是为了反而反。

**这个技能做什么**：
- 批量挖掘你所在领域的刻板印象（简化因果关系）
- 按「识别刻板印象 → 反例 → 新框架 → 定义关键词」四步生成完整内容
- 自动适配小红书、抖音、视频号、公众号的不同风格
- 结合你的真实业务场景，生产有说服力的具体反例

**使用**：
```
帮我生成非共识内容
我是做写字楼租赁的，给我10个选题
帮我看看这个观点是好的非共识吗：[你的观点]
```

---

### 💡 Non-Consensus · 正确的非共识内容生成器
`v1.0.0` · 适合：自媒体博主、内容创作者

**解决什么问题**：很多创作者知道要「讲认知」，但不知道怎么批量产出有深度的内容。这个技能基于李普曼《公众舆论》的刻板印象理论，帮你系统化地找到领域内的刻板印象并击破它。

**这个技能做什么**：
- 给定领域，批量挖掘 8-12 个刻板印象
- 对每个刻板印象生成完整的「识别→反例→新框架→定义」四步结构
- 结合你的真实经历生成内容，不为反而反
- 将所有框架存入内容库，随时取用

**使用**：
```
帮我找写字楼租赁行业的刻板印象
我有个观点想做成内容
帮我批量生产非共识内容
```


---

### 🖼️ Cover Maker · 社交媒体封面生成器
`v1.4.0` · 适合：做自媒体内容的人

**解决什么问题**：每次发内容都要花时间做封面，设计工具又复杂。这个技能让你直接说内容和平台，自动生成符合平台尺寸、排版专业的 HTML 封面文件，浏览器打开截图就能用。

**这个技能做什么**：
- 自动按平台规格生成封面（小红书、抖音、视频号、B站等）
- 大字冲击、杂志感、色块撞色等多种风格
- 平台尺寸更新时自动搜索最新规格
- 账号风格记忆，下次生成只需提供标题内容
- 系列封面保持视觉一致性
- 安全区标注，重要内容不被平台 UI 遮挡
- 支持 puppeteer 自动截图，省去手动截图

**使用**：
```
帮我做一个小红书封面
标题是「涨粉越快越不赚钱」，黑白极简风格
帮我做抖音封面，内容是...
```

---

### 🔧 Skill Updater · 技能库版本管理
`v1.0.0` · 适合：所有安装了技能库的用户

**解决什么问题**：技能库更新后，不知道本地哪些技能需要更新，也不想全部删了重装。这个技能帮你检查每个技能的版本，只更新有新版本的，已是最新的跳过不动。

**使用**：
```
检查技能更新
更新技能
```

---

## 验证安装版本

```bash
# Claude Code
grep "^# Version" ~/.claude/skills/ai-tutor/SKILL.md
grep "^# Version" ~/.claude/skills/team-flow/SKILL.md
grep "^# Version" ~/.claude/skills/non-consensus/SKILL.md

# OpenClaw
grep "^# Version" ~/.openclaw/skills/ai-tutor/SKILL.md
grep "^# Version" ~/.openclaw/skills/team-flow/SKILL.md
grep "^# Version" ~/.openclaw/skills/non-consensus/SKILL.md

# Codex
grep "^# Version" ~/.codex/skills/ai-tutor/SKILL.md
grep "^# Version" ~/.codex/skills/team-flow/SKILL.md
grep "^# Version" ~/.codex/skills/non-consensus/SKILL.md
grep "^# Version" ~/.codex/skills/non-consensus/SKILL.md
```

---

## 卸载

```bash
# Claude Code
rm -rf ~/.claude/skills/ai-tutor
rm -rf ~/.claude/skills/team-flow
rm -rf ~/.claude/skills/non-consensus

# OpenClaw
rm -rf ~/.openclaw/skills/ai-tutor
rm -rf ~/.openclaw/skills/team-flow
rm -rf ~/.openclaw/skills/non-consensus

# Codex
rm -rf ~/.codex/skills/ai-tutor
rm -rf ~/.codex/skills/team-flow
rm -rf ~/.codex/skills/non-consensus
```

---

## 版本记录

### AI Tutor
| 版本 | 更新内容 |
|------|---------|
| v1.8.0 | 学以致用追踪 + 问题反向诊断：遇到问题可反向推荐知识，每单元追踪应用结果 |
| v1.9.0 | 强制等待规则：发出单元后必须等用户回答再继续，不能跳过检测 |
| v1.9.0 | 强制等待规则提至最高优先级，修复讲完直接跳下一单元的问题 |
| v1.8.0 | 问题反向诊断：遇到问题来问，激活已学知识或推荐新概念 |
| v1.7.0 | 用户画像 + 学以致用追踪：了解背景、追踪应用效果 |
| v1.6.0 | 实战任务：技能型主题自动布置实战，两者都通过才推进 |
| v1.5.0 | 严格评估：关键词检查 + 模糊语言降级 |
| v1.4.0 | 角色定义、核心原则优先级、知识边界、行为边界 |
| v1.3.0 | 主题澄清步骤 |
| v1.2.0 | 三级提示、纠错方式、情绪感知、上下文压缩、跨主题关联 |
| v1.1.0 | 续学机制、间隔复习、结课判断 |
| v1.0.0 | 初始版本 |

### Team Flow
| 版本 | 更新内容 |
|------|---------|
| v1.0.0 | 初始版本 |

---

## License

MIT


### Non-Consensus
| 版本 | 更新内容 |
|------|----------|
| v1.0.0 | 初始版本 |
