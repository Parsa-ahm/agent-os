#!/usr/bin/env bash
# Creates the local Ollama model from your filled-in Modelfile
set -euo pipefail

MODELFILE="ollama/Modelfile"
MODEL_NAME="${1:-my-coder}"

if [[ ! -f "$MODELFILE" ]]; then
  echo "ollama/Modelfile not found."
  echo "Copy the template first: cp ollama/Modelfile.template ollama/Modelfile"
  echo "Then fill in your details and re-run."
  exit 1
fi

if grep -q "\[YOUR NAME" "$MODELFILE"; then
  echo "Modelfile still has placeholders. Fill in [YOUR NAME/HANDLE] and your stack first."
  exit 1
fi

echo "Building model '$MODEL_NAME' from $MODELFILE..."
ollama create "$MODEL_NAME" -f "$MODELFILE"
echo ""
echo "Done. Test it with: ollama run $MODEL_NAME"
