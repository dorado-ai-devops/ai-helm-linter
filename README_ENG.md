# 🧠 ai-helm-linter

> Smart microservice for auditing Helm Charts using LLMs (Ollama or OpenAI), detecting errors, inconsistencies, or bad practices through specialized prompts.  

Built with Python + Flask, with CLI integration and deployable via Helm + ArgoCD.

---

## 🚀 Features

- ✅ Audits syntax, conventions, and structural consistency in Helm Charts  
- 🔐 Analyzes `Chart.yaml`, `values.yaml`, `templates/*`, `*.tpl`, `*.json`, etc.  
- 🤖 Supports local models (Ollama) or remote (GPT-4 via OpenAI)  
- 🔄 Automatic fallback to OpenAI if Ollama fails  
- 🧩 Full CLI and REST API  
- 🐳 Dockerized and deployable via Helm + ArgoCD  
- 📁 Compatible with GitOps environments and CI/CD pipelines  
- ✍️ Modular and editable prompt (`helm_linting.prompt`)  
- 📦 Supports folders or packaged `.tgz` Helm Charts  

---

## 📦 Project Structure

```
ai-helm-linter/
├── app.py                 # Flask microservice entrypoint
├── cli/                   # CLI interface
├── lib/                   # Core logic and AI clients
├── prompts/               # Prompt templates
├── routes/                # Flask API routes
├── Dockerfile             # Container image
├── Makefile               # Build and deploy automation
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## 🧩 Components

### `cli/lint.py`

CLI for analyzing Helm Charts from the terminal:

```bash
python3 cli/lint.py --mode ollama --chart_path charts/example
```

- `--mode`: `ollama` or `openai`  
- `--chart_path`: folder or `.tgz` file  
- `--ruleset`: ruleset to apply (default: `"default"`)

### `app.py` + `routes/lint_chart.py`

Flask microservice exposing `/lint-chart` endpoint for uploading Charts and returning the AI analysis.

- Expected input:
  - `multipart/form-data` with `.tgz` file
  - fields `mode` (`ollama|openai`) and `ruleset` (optional)
- Output: AI-generated analysis in JSON

---

## 🧠 Internal Logic

### `lib/linter.py`

- Loads the base prompt (`helm_linting.prompt`)  
- Injects chart contents and selected rules  
- Calls `query_ollama()` or `query_openai()`  
- Falls back to OpenAI if Ollama fails

### `lib/utils.py`

- Loads Charts from folder or `.tgz`
- Scans `*.yaml`, `*.tpl`, `*.json`, etc. and includes relative paths
- Loads prompt templates as plain text

### `lib/ollama_client.py` & `lib/openai_client.py`

- Send HTTP requests to local Ollama or OpenAI's GPT-4  
- Configurable via `OLLAMA_BASE_URL` and `OPENAI_API_KEY`  

---

## 🔁 Jenkins Integration

```groovy
def jsonPayload = '''
{
  "chart_path": "./charts/mychart.tgz",
  "mode": "ollama"
}
'''

sh """
curl -X POST http://helm-linter.devops-ai.svc.cluster.local:5000/lint-chart \
  -F 'chart=@./charts/mychart.tgz' \
  -F 'mode=ollama' \
  -F 'ruleset=default'
"""
```

---

## 🛠️ Getting Started (Local)

```bash
git clone https://github.com/dorado-ai-devops/ai-helm-linter.git
cd ai-helm-linter
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run CLI

```bash
python3 cli/lint.py --mode ollama --chart_path charts/example
```

### Run Flask microservice

```bash
python3 app.py
```

---

## 💡 Sample Output

```
[ERROR] Chart.yaml is missing the "version" field.
[SUGGESTION] Add a "version: 1.0.0" key to comply with standards.
[REVIEW] deployment.yaml hardcodes port 80.
```

---

## 👨‍💻 Author

- **Dani** – [@dorado-ai-devops](https://github.com/dorado-ai-devops)

---

## 🧠 Inspired by

- [Helm Chart Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Ollama](https://ollama.com)
- [OpenAI API](https://platform.openai.com/docs)

---

## 🛡 License

GNU General Public License v3.0
