#!/bin/bash


PROJECT_ROOT="/root/devops-ai/ai-helm-linter"


cd "$PROJECT_ROOT" || {
  echo "❌ No se puede acceder a $PROJECT_ROOT"
  exit 1
}


export PYTHONPATH="$PROJECT_ROOT"


MODE=${1:-openai}
CHART_PATH="charts/example"


if [ -f "../venv/bin/activate" ]; then
  source ../venv/bin/activate
fi


python3 cli/lint.py --mode "$MODE" --chart "$CHART_PATH"
