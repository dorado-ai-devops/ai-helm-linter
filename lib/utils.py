import os
import tarfile
import tempfile
import shutil

def extract_chart_data(chart_path):
    temp_dir = None
    try:
        if chart_path.endswith(".tgz") and os.path.isfile(chart_path):
            temp_dir = tempfile.mkdtemp()
            with tarfile.open(chart_path, "r:gz") as tar:
                tar.extractall(path=temp_dir)
            root_dir = os.path.join(temp_dir, os.listdir(temp_dir)[0])
        else:
            root_dir = chart_path

        content = ""
        for root, _, files in os.walk(root_dir):
            for file in files:
                path = os.path.join(root, file)
                if file.endswith((".yaml", ".yml", ".tpl", ".json")):
                    with open(path, "r") as f:
                        rel_path = os.path.relpath(path, root_dir)
                        content += f"\n---\n# {rel_path}\n" + f.read()
        return content
    finally:
        if temp_dir:
            shutil.rmtree(temp_dir)

def load_prompt(filename):
    with open(f"prompts/{filename}", "r") as f:
        return f.read()
