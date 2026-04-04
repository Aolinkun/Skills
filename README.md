# Skills · Claude Code 技能库

适用于 Claude Code 的技能集合，一键安装，开箱即用。

---

## 一键安装

```bash
curl -fsSL https://raw.githubusercontent.com/Aolinkun/Skills/main/install.sh | bash
```

运行后选择安装哪个技能，或直接回车全部安装。

---

## 技能列表

### 🎓 AI Tutor · 苏格拉底学习导师
> 版本：v1.6.0

基于 Bloom Two Sigma 掌握学习法，Claude 主动提问而非被动讲解，根据你的回答实时调整难度。技能型主题额外布置实战任务。

**使用**：在 Claude Code 中说「我想学 XXX」

---

### 🔀 Team Flow · 多角色任务协作系统
> 版本：v1.0.0

基于德鲁克目标管理（MBO），让人类和 AI 作为平等角色协作。任务统一管理，任何角色都可以调用任何角色。

**使用**：在 Claude Code 中说「新建任务」「完成任务」「更新团队能力」

---

## 验证安装版本

```bash
grep "^# Version" ~/.claude/skills/ai-tutor/SKILL.md
grep "^# Version" ~/.claude/skills/team-flow/SKILL.md
```

---

## 卸载

```bash
rm -rf ~/.claude/skills/ai-tutor
rm -rf ~/.claude/skills/team-flow
```

---

## License

MIT
