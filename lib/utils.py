import os

def extract_chart_data(chart_path):
    content = ""
    for root, _, files in os.walk(chart_path):
        for file in files:
            path = os.path.join(root, file)
            with open(path, "r") as f:
                content += f"\n---\n# {path}\n" + f.read()
    return content

def load_prompt(filename):
    with open(f"prompts/{filename}", "r") as f:
        return f.read()
