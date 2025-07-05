from lib.ollama_client import query_ollama
from lib.openai_client import query_openai
from lib.utils import load_prompt, extract_chart_data

def run_lint(chart_path, ruleset, mode):
    chart_data = extract_chart_data(chart_path)
    prompt_template = load_prompt("helm_linting.prompt")
    prompt = prompt_template.replace("{{CHART_CONTENT}}", chart_data).replace("{{RULESET}}", ruleset)

    if mode == "ollama":
        try:
            return query_ollama(prompt)
        except:
            return query_openai(prompt)
    else:
        return query_openai(prompt)
