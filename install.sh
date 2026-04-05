#!/bin/bash

# Skills · 一键安装脚本
# 支持 Claude Code、OpenClaw、Codex

REPO="Aolinkun/Skills"
BASE_URL="https://raw.githubusercontent.com/$REPO/main"

echo "🚀 Skills 安装程序"
echo ""
echo "请选择安装目标："
echo "  1) Claude Code  (~/.claude/skills/)    [默认]"
echo "  2) OpenClaw     (~/.openclaw/skills/)"
echo "  3) Codex        (~/.codex/skills/)"
echo "  4) 全部安装"
echo ""

read -p "输入选项 [1/2/3/4]，直接回车默认 Claude Code：" target < /dev/tty
target=${target:-1}

case "$target" in
  1) DIRS=("$HOME/.claude/skills") ;;
  2) DIRS=("$HOME/.openclaw/skills") ;;
  3) DIRS=("$HOME/.codex/skills") ;;
  4) DIRS=("$HOME/.claude/skills" "$HOME/.openclaw/skills" "$HOME/.codex/skills") ;;
  *)
    echo "❌ 无效选项，请输入 1、2、3 或 4"
    exit 1
    ;;
esac

echo ""
echo "请选择要安装的技能："
echo "  1) ai-tutor       — 苏格拉底学习导师"
echo "  2) team-flow      — 多角色任务协作系统"
echo "  3) non-consensus  — 正确的非共识内容生成"
echo "  4) 全部安装（默认）"
echo ""

read -p "输入选项 [1/2/3/4]，直接回车默认全部安装：" choice < /dev/tty
choice=${choice:-4}

install_skill() {
  local SKILL="$1"
  local DIR="$2"
  local INSTALL_DIR="$DIR/$SKILL"

  echo "  📦 安装 $SKILL 到 $DIR ..."
  mkdir -p "$INSTALL_DIR/references"

  curl -fsSL "$BASE_URL/$SKILL/SKILL.md" -o "$INSTALL_DIR/SKILL.md" || { echo "  ❌ 下载失败，请稍后重试"; return 1; }
  curl -fsSL "$BASE_URL/$SKILL/references/theory.md" -o "$INSTALL_DIR/references/theory.md" 2>/dev/null || true
  curl -fsSL "$BASE_URL/$SKILL/references/difficulty-levels.md" -o "$INSTALL_DIR/references/difficulty-levels.md" 2>/dev/null || true
  curl -fsSL "$BASE_URL/$SKILL/references/mbo.md" -o "$INSTALL_DIR/references/mbo.md" 2>/dev/null || true
  curl -fsSL "$BASE_URL/$SKILL/references/examples.md" -o "$INSTALL_DIR/references/examples.md" 2>/dev/null || true
  curl -fsSL "$BASE_URL/$SKILL/references/lippmann.md" -o "$INSTALL_DIR/references/lippmann.md" 2>/dev/null || true

  VERSION=$(grep "^# Version" "$INSTALL_DIR/SKILL.md" 2>/dev/null || echo "版本未知")
  echo "  ✅ $SKILL 安装完成！$VERSION"
}

for DIR in "${DIRS[@]}"; do
  echo ""
  echo "━━ 安装到 $DIR"
  case "$choice" in
    1) install_skill "ai-tutor" "$DIR" ;;
    2) install_skill "team-flow" "$DIR" ;;
    3) install_skill "non-consensus" "$DIR" ;;
    4)
      install_skill "ai-tutor" "$DIR"
      install_skill "team-flow" "$DIR"
      install_skill "non-consensus" "$DIR"
      ;;
  esac
done

echo ""
echo "━━ 已安装版本"
for skill in ai-tutor team-flow non-consensus; do
  for dir in "$HOME/.claude/skills" "$HOME/.openclaw/skills" "$HOME/.codex/skills"; do
    FILE="$dir/$skill/SKILL.md"
    if [ -f "$FILE" ]; then
      VERSION=$(grep "^# Version" "$FILE" 2>/dev/null || echo "版本未知")
      echo "  $skill ($dir): $VERSION"
    fi
  done
done

echo ""
echo "注意：Codex 需要用 --enable skills 参数启动才能使用技能"
echo "  codex --enable skills"
