#!/bin/bash

# Skills · 一键安装脚本
# 支持 Claude Code、Codex、Grok

set -u

REPO="Aolinkun/Skills"
ARCHIVE_URL="https://github.com/$REPO/archive/refs/heads/main.tar.gz"
TMP_DIR="$(mktemp -d 2>/dev/null || mktemp -d -t skills-install)"
SOURCE_ROOT=""
ACTIVE_INSTALL_DIR=""
ACTIVE_BACKUP_DIR=""
ACTIVE_TRANSACTION_ROOT=""
ACTIVE_HAD_EXISTING=0
ACTIVE_REPLACEMENT_ENABLED=0

clear_active_transaction() {
  ACTIVE_INSTALL_DIR=""
  ACTIVE_BACKUP_DIR=""
  ACTIVE_TRANSACTION_ROOT=""
  ACTIVE_HAD_EXISTING=0
  ACTIVE_REPLACEMENT_ENABLED=0
}

rollback_active_transaction() {
  if [ -z "$ACTIVE_INSTALL_DIR" ]; then
    return 0
  fi

  if [ "$ACTIVE_REPLACEMENT_ENABLED" -eq 1 ] && \
     { [ -e "$ACTIVE_INSTALL_DIR" ] || [ -L "$ACTIVE_INSTALL_DIR" ]; }; then
    rm -rf "$ACTIVE_INSTALL_DIR" 2>/dev/null || true
  fi
  if [ "$ACTIVE_HAD_EXISTING" -eq 1 ] && [ -d "$ACTIVE_BACKUP_DIR" ]; then
    if ! mv "$ACTIVE_BACKUP_DIR" "$ACTIVE_INSTALL_DIR" 2>/dev/null; then
      echo "  ⚠️  自动恢复失败，旧版本仍位于：$ACTIVE_BACKUP_DIR" >&2
    fi
  fi
  if [ -n "$ACTIVE_TRANSACTION_ROOT" ]; then
    rm -rf "$ACTIVE_TRANSACTION_ROOT" 2>/dev/null || true
  fi
  clear_active_transaction
}

cleanup() {
  local exit_code=$?
  trap - EXIT INT TERM
  rollback_active_transaction
  rm -rf "$TMP_DIR"
  exit "$exit_code"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

choose_target() {
  if [ -n "${SKILLS_TARGET:-}" ]; then
    target="$SKILLS_TARGET"
  else
    echo "🚀 Skills 安装程序"
    echo ""
    echo "请选择安装目标："
    echo "  1) Claude Code  (~/.claude/skills/)    [默认]"
    echo "  2) Codex        (~/.codex/skills/)"
    echo "  3) Grok         (~/.grok/skills/)"
    echo "  4) 全部安装"
    echo ""
    read -r -p "输入选项 [1/2/3/4]，直接回车默认 Claude Code：" target < /dev/tty
    target=${target:-1}
  fi

  case "$target" in
    1) TARGETS=("claude|$HOME/.claude/skills") ;;
    2) TARGETS=("codex|$HOME/.codex/skills") ;;
    3) TARGETS=("grok|$HOME/.grok/skills") ;;
    4) TARGETS=("claude|$HOME/.claude/skills" "codex|$HOME/.codex/skills" "grok|$HOME/.grok/skills") ;;
    *)
      echo "❌ 无效安装目标：$target（应为 1、2、3 或 4）"
      exit 1
      ;;
  esac
}

make_grok_invocable() {
  local skill_file="$1"
  local temp_file="$skill_file.grok-tmp"

  if ! awk '
    NR == 1 {
      if ($0 != "---") exit 2
      print
      next
    }
    !closed && /^user_invocable:[[:space:]]*/ {
      print "user_invocable: true"
      seen = 1
      next
    }
    !closed && $0 == "---" {
      if (!seen) print "user_invocable: true"
      closed = 1
      print
      next
    }
    { print }
    END {
      if (!closed) exit 3
    }
  ' "$skill_file" > "$temp_file"; then
    rm -f "$temp_file"
    return 1
  fi

  mv "$temp_file" "$skill_file"
}

validate_skill_package() {
  local package_dir="$1"
  local host="$2"
  local validator="$package_dir/scripts/validate-package.py"

  if [ ! -f "$validator" ]; then
    return 0
  fi
  if ! command -v python3 >/dev/null 2>&1; then
    echo "  ❌ $(basename "$package_dir") 需要 Python 3 执行包校验。"
    return 1
  fi
  if [ "$host" = "grok" ]; then
    python3 "$validator" --allow-grok-frontmatter "$package_dir" >/dev/null
  else
    python3 "$validator" "$package_dir" >/dev/null
  fi
}

choose_skill() {
  if [ -n "${SKILLS_CHOICE:-}" ]; then
    choice="$SKILLS_CHOICE"
  else
    echo ""
    echo "请选择要安装的技能："
    echo "  1) ai-tutor       — 自适应掌握学习导师"
    echo "  2) team-flow      — 多角色任务协作系统"
    echo "  3) non-consensus  — 正确的非共识内容生成"
    echo "  4) skill-updater  — 技能库版本管理工具"
    echo "  5) fastlane       — 快车道业务评估"
    echo "  6) 全部安装（默认）"
    echo ""
    read -r -p "输入选项 [1/2/3/4/5/6]，直接回车默认全部安装：" choice < /dev/tty
    choice=${choice:-6}
  fi

  case "$choice" in
    1) SELECTED_SKILLS=("ai-tutor") ;;
    2) SELECTED_SKILLS=("team-flow") ;;
    3) SELECTED_SKILLS=("non-consensus") ;;
    4) SELECTED_SKILLS=("skill-updater") ;;
    5) SELECTED_SKILLS=("fastlane") ;;
    6) SELECTED_SKILLS=("ai-tutor" "team-flow" "non-consensus" "skill-updater" "fastlane") ;;
    *)
      echo "❌ 无效技能选项：$choice（应为 1 到 6）"
      exit 1
      ;;
  esac
}

download_repository() {
  if [ -n "${SKILLS_SOURCE_DIR:-}" ]; then
    SOURCE_ROOT="$SKILLS_SOURCE_DIR"
    if [ ! -d "$SOURCE_ROOT" ]; then
      echo "❌ SKILLS_SOURCE_DIR 不是有效目录：$SOURCE_ROOT"
      exit 1
    fi
    echo ""
    echo "🧪 使用本地技能源：$SOURCE_ROOT"
    return
  fi

  echo ""
  echo "⬇️  正在下载完整技能包……"
  if ! curl -fL --retry 2 --connect-timeout 15 "$ARCHIVE_URL" -o "$TMP_DIR/repo.tar.gz"; then
    echo "❌ 下载仓库失败，请检查网络后重试。"
    exit 1
  fi
  if ! tar -xzf "$TMP_DIR/repo.tar.gz" -C "$TMP_DIR"; then
    echo "❌ 解压仓库失败，安装已停止。"
    exit 1
  fi
  SOURCE_ROOT="$(find "$TMP_DIR" -mindepth 1 -maxdepth 1 -type d -name 'Skills-*' | head -n 1)"
  if [ -z "$SOURCE_ROOT" ] || [ ! -d "$SOURCE_ROOT" ]; then
    echo "❌ 未找到解压后的技能仓库。"
    exit 1
  fi
}

install_skill() {
  local skill="$1"
  local destination_root="$2"
  local host="$3"
  local source_skill="$SOURCE_ROOT/$skill"
  local install_dir="$destination_root/$skill"
  local transaction_root="$destination_root/.skills-install-$skill-$$"
  local stage_dir="$transaction_root/$skill"
  local backup_dir="$destination_root/.skills-backup-$skill-$$"

  if [ ! -f "$source_skill/SKILL.md" ]; then
    echo "  ❌ 仓库中缺少 $skill/SKILL.md"
    return 1
  fi
  if [ "$skill" = "ai-tutor" ] && [ ! -f "$source_skill/scripts/validate-package.py" ]; then
    echo "  ❌ 仓库中的 ai-tutor 缺少完整包校验脚本。"
    return 1
  fi
  if ! validate_skill_package "$source_skill" "canonical"; then
    echo "  ❌ 仓库中的 $skill 包不完整，未开始安装。"
    return 1
  fi

  if ! mkdir -p "$destination_root"; then
    echo "  ❌ 无法创建安装根目录：$destination_root"
    return 1
  fi

  ACTIVE_INSTALL_DIR="$install_dir"
  ACTIVE_BACKUP_DIR="$backup_dir"
  ACTIVE_TRANSACTION_ROOT="$transaction_root"
  ACTIVE_HAD_EXISTING=0
  ACTIVE_REPLACEMENT_ENABLED=0

  if ! mkdir -p "$stage_dir"; then
    echo "  ❌ 无法创建暂存目录：$stage_dir"
    rollback_active_transaction
    return 1
  fi
  if [ -d "$install_dir" ] && ! cp -R "$install_dir/." "$stage_dir/"; then
    echo "  ❌ 无法把现有 $skill 复制到暂存目录。"
    rollback_active_transaction
    return 1
  fi
  if ! cp -R "$source_skill/." "$stage_dir/"; then
    echo "  ❌ 无法把新 $skill 复制到暂存目录。"
    rollback_active_transaction
    return 1
  fi
  if [ "$host" = "grok" ] && ! make_grok_invocable "$stage_dir/SKILL.md"; then
    echo "  ❌ 无法为 Grok 生成 user_invocable: true 元数据。"
    rollback_active_transaction
    return 1
  fi

  if [ "$skill" = "ai-tutor" ] && [ ! -f "$stage_dir/scripts/validate-package.py" ]; then
    echo "  ❌ ai-tutor 缺少完整包校验脚本，未写入安装目录。"
    rollback_active_transaction
    return 1
  fi
  if ! validate_skill_package "$stage_dir" "$host"; then
    echo "  ❌ $skill 包校验失败，未写入安装目录。"
    rollback_active_transaction
    return 1
  fi

  echo "  📦 安装 $skill 到 $destination_root …"
  if [ -d "$install_dir" ]; then
    ACTIVE_HAD_EXISTING=1
    if ! mv "$install_dir" "$backup_dir"; then
      echo "  ❌ 无法暂存现有安装目录，更新已取消。"
      rollback_active_transaction
      return 1
    fi
  fi
  if ! mv "$stage_dir" "$install_dir"; then
    echo "  ❌ 无法启用新安装，正在恢复旧版本。"
    rollback_active_transaction
    return 1
  fi
  ACTIVE_REPLACEMENT_ENABLED=1
  rm -rf "$transaction_root"
  if [ -d "$install_dir/scripts" ]; then
    chmod +x "$install_dir"/scripts/*.py 2>/dev/null || true
  fi

  if ! validate_skill_package "$install_dir" "$host"; then
    echo "  ❌ 安装后校验失败，正在恢复旧版本。"
    rollback_active_transaction
    return 1
  fi
  clear_active_transaction
  rm -rf "$backup_dir"

  local version
  version="$(grep '^# Version' "$install_dir/SKILL.md" 2>/dev/null || echo '版本未知')"
  echo "  ✅ $skill 安装完成：$version"
}

choose_target
choose_skill
download_repository

failures=0
for target_spec in "${TARGETS[@]}"; do
  host="${target_spec%%|*}"
  destination="${target_spec#*|}"
  echo ""
  echo "━━ 安装到 $destination"
  for skill in "${SELECTED_SKILLS[@]}"; do
    install_skill "$skill" "$destination" "$host" || failures=$((failures + 1))
  done
done

echo ""
echo "━━ 已安装版本"
for skill in ai-tutor team-flow non-consensus skill-updater fastlane; do
  for destination in "$HOME/.claude/skills" "$HOME/.codex/skills" "$HOME/.grok/skills"; do
    file="$destination/$skill/SKILL.md"
    if [ -f "$file" ]; then
      version="$(grep '^# Version' "$file" 2>/dev/null || echo '版本未知')"
      echo "  $skill ($destination): $version"
    fi
  done
done

if [ "$failures" -gt 0 ]; then
  echo ""
  echo "⚠️  有 $failures 个安装任务失败，请检查上方错误。"
  exit 1
fi

echo ""
echo "✅ 安装完成。若宿主应用已经运行，请重启应用或重新加载技能列表。"
