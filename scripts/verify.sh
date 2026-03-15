#!/usr/bin/env bash
# Verifies the full agent-os environment is operational
set -euo pipefail

PASS=0
FAIL=0

check() {
  local label="$1"
  local cmd="$2"
  if eval "$cmd" &>/dev/null; then
    echo "  ✓ $label"
    ((PASS++))
  else
    echo "  ✗ $label"
    ((FAIL++))
  fi
}

echo ""
echo "agent-os environment check"
echo "══════════════════════════"
echo ""

echo "Core tools:"
check "Claude Code installed"   "command -v claude"
check "Ollama installed"        "command -v ollama"
check "git installed"           "command -v git"
check "git identity set"        "git config --global user.email"

echo ""
echo "Brain files:"
check "about-you.md exists"      "[[ -f brain/about-you.md ]]"
check "ai-behavior.md exists"    "[[ -f brain/ai-behavior.md ]]"
check "coding-standards.md exists" "[[ -f brain/coding-standards.md ]]"

echo ""
echo "Ollama model:"
check "qwen2.5-coder:7b pulled"  "ollama list | grep qwen2.5-coder"

echo ""
echo "──────────────────────────────"
echo "Passed: $PASS  Failed: $FAIL"
echo ""
if [[ $FAIL -gt 0 ]]; then
  echo "Run scripts/setup.sh to fix missing items."
fi
