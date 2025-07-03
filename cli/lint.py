import argparse
from lib.linter import run_lint

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lint Helm Chart using LLM")
    parser.add_argument("--chart_path", required=True, help="Path to the Helm Chart")
    parser.add_argument("--ruleset", default="default", help="Ruleset to apply")
    parser.add_argument("--mode", default="ollama", choices=["ollama", "openai"], help="LLM to use")
    args = parser.parse_args()

    result = run_lint(chart_path=args.chart_path, ruleset=args.ruleset, mode=args.mode)
    print(result)
