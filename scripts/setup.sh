#!/usr/bin/env bash
# agent-os setup script
# Installs Claude Code, ECC, and verifies Ollama
set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

ok()   { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}!${NC} $1"; }
fail() { echo -e "${RED}✗${NC} $1"; exit 1; }

echo ""
echo "agent-os setup"
echo "═══════════════════════════════"
echo ""

# ── Claude Code ──────────────────────────────────────────
echo "Checking Claude Code..."
if command -v claude &>/dev/null; then
  ok "Claude Code found: $(claude --version 2>/dev/null || echo 'installed')"
else
  warn "Claude Code not found."
  echo "  Install it: https://claude.ai/download"
  echo "  Then re-run this script."
  exit 1
fi

# ── ECC plugin ───────────────────────────────────────────
echo ""
echo "Checking ECC plugin..."
if claude plugins list 2>/dev/null | grep -q "everything-claude-code"; then
  ok "ECC plugin installed"
else
  warn "ECC not detected. Installing..."
  claude plugins install everything-claude-code 2>/dev/null && ok "ECC installed" || warn "ECC install failed — install manually: /install in Claude Code"
fi

# ── Ollama ───────────────────────────────────────────────
echo ""
echo "Checking Ollama..."
if command -v ollama &>/dev/null; then
  ok "Ollama found"
  if ollama list 2>/dev/null | grep -q "qwen2.5-coder"; then
    ok "qwen2.5-coder model present"
  else
    warn "qwen2.5-coder not pulled yet."
    echo "  Run: ollama pull qwen2.5-coder:7b"
  fi
else
  warn "Ollama not installed. Get it at https://ollama.ai"
fi

# ── Brain files ──────────────────────────────────────────
echo ""
echo "Checking brain files..."
BRAIN_FILES=("brain/about-you.md" "brain/active-projects.md" "brain/decisions.md")
ALL_BRAIN_FILLED=true
for f in "${BRAIN_FILES[@]}"; do
  if grep -q "\[" "$f" 2>/dev/null; then
    warn "$f still has placeholders — fill it in before using"
    ALL_BRAIN_FILLED=false
  fi
done
if $ALL_BRAIN_FILLED; then
  ok "Brain files look filled in"
fi

# ── Git ──────────────────────────────────────────────────
echo ""
echo "Checking git config..."
if git config --global user.email &>/dev/null; then
  ok "Git identity configured"
else
  warn "Git identity not set. Run:"
  echo "  git config --global user.name 'Your Name'"
  echo "  git config --global user.email 'you@example.com'"
fi

# ── Summary ──────────────────────────────────────────────
echo ""
echo "═══════════════════════════════"
echo "Next steps:"
echo "  1. Fill in brain/about-you.md and brain/active-projects.md"
echo "  2. Copy ollama/Modelfile.template → ollama/Modelfile and fill in your stack"
echo "  3. Run scripts/create-model.sh to build your local model"
echo "  4. Read docs/ — start with 01-why-this-exists.md"
echo ""
