#!/bin/bash

# Skills · 一键安装脚本
# 支持选择安装单个或全部技能

REPO="Aolinkun/Skills"
BASE_URL="https://raw.githubusercontent.com/$REPO/main"
SKILLS_DIR="$HOME/.claude/skills"

install_skill() {
  local SKILL="$1"
  local INSTALL_DIR="$SKILLS_DIR/$SKILL"

  echo ""
  echo "📦 安装 $SKILL ..."
  mkdir -p "$INSTALL_DIR/references"

  curl -fsSL "$BASE_URL/$SKILL/SKILL.md" -o "$INSTALL_DIR/SKILL.md" || { echo "❌ 下载 $SKILL/SKILL.md 失败，请稍后重试"; return 1; }
  curl -fsSL "$BASE_URL/$SKILL/references/theory.md" -o "$INSTALL_DIR/references/theory.md" 2>/dev/null || true
  curl -fsSL "$BASE_URL/$SKILL/references/difficulty-levels.md" -o "$INSTALL_DIR/references/difficulty-levels.md" 2>/dev/null || true
  curl -fsSL "$BASE_URL/$SKILL/references/mbo.md" -o "$INSTALL_DIR/references/mbo.md" 2>/dev/null || true
  curl -fsSL "$BASE_URL/$SKILL/references/examples.md" -o "$INSTALL_DIR/references/examples.md" 2>/dev/null || true

  VERSION=$(grep "^# Version" "$INSTALL_DIR/SKILL.md" 2>/dev/null || echo "# Version: 未知")
  echo "✅ $SKILL 安装完成！$VERSION"
}

echo "🚀 Skills 安装程序"
echo ""
echo "请选择要安装的技能："
echo "  1) ai-tutor    — 苏格拉底学习导师"
echo "  2) team-flow   — 多角色任务协作系统"
echo "  3) 全部安装（默认）"
echo ""

read -p "输入选项 [1/2/3]，直接回车默认全部安装：" choice < /dev/tty
choice=${choice:-3}

case "$choice" in
  1) install_skill "ai-tutor" ;;
  2) install_skill "team-flow" ;;
  3)
    install_skill "ai-tutor"
    install_skill "team-flow"
    ;;
  *)
    echo "❌ 无效选项，请输入 1、2 或 3"
    exit 1
    ;;
esac

echo ""
echo "验证已安装版本："
grep "^# Version" "$SKILLS_DIR/ai-tutor/SKILL.md" 2>/dev/null && echo "  路径：$SKILLS_DIR/ai-tutor"
grep "^# Version" "$SKILLS_DIR/team-flow/SKILL.md" 2>/dev/null && echo "  路径：$SKILLS_DIR/team-flow"
