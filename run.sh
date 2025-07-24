#!/bin/bash


PROJECT_ROOT="/root/devops-ai/ai-helm-linter"


cd "$PROJECT_ROOT" || {
  echo " No se puede acceder a $PROJECT_ROOT"
  exit 1
}


export PYTHONPATH="$PROJECT_ROOT"


MODE=${1:-openai}


CHART_DIR="/root/devops-ai/chart"
CHART_PACKAGE_DEST="/root/devops-ai/chart_package"

CHART_TGZ=$(helm package "$CHART_DIR" --destination $CHART_PACKAGE_DEST  | awk '{print $NF}' | tr -d '\n')


if [ -f "../venv/bin/activate" ]; then
  source ../venv/bin/activate
fi


python3 cli/lint.py --mode "$MODE" --chart_path "$CHART_TGZ" && rm $CHART_TGZ


