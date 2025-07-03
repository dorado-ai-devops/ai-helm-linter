# 🧠 ai-helm-linter

> Microservice to audit Helm Charts using LLMs (OpenAI or Ollama), detecting errors, inconsistencies, or bad practices via specialized prompts.

---

## 🚀 Features

- ✅ Audits syntax, conventions, and coherence in Helm Charts
- 📚 Analyzes `Chart.yaml`, `values.yaml`, and templates under `templates/`
- 🤖 Supports Ollama local models or GPT-4o via OpenAI
- 🧩 Includes CLI and REST API via Flask
- 🐳 Docker-ready and deployable with Helm + ArgoCD
- 🔁 Automatic fallback to OpenAI if Ollama fails
- 📁 GitOps and CI/CD friendly
- ✍️ Editable prompts to match your organization's policies

---

## 📦 Project Structure

```
ai-helm-linter/
├── app.py                 # Flask microservice (API /lint)
├── cli/                   # CLI scripts like lint.py
├── lib/                   # OpenAI/Ollama clients and logic
├── charts/                # Example charts for testing
├── prompts/               # Dynamic .prompt templates
├── requirements.txt       # Python dependencies
├── Dockerfile             # Flask container
├── Makefile               # Build & deployment automation
└── README.md              # Project documentation
```

---

## 🧩 Component Overview

### `app.py`

Deployable Flask microservice:
- Endpoint `/lint`
- Accepts JSON: `{ "chart": "./charts/example", "mode": "openai|ollama" }`
- Loads the chart contents
- Calls `lint.py` and returns structured analysis

### `cli/lint.py`

Main script for AI-powered linting:
- Args: `--mode`, `--chart`
- Loads `Chart.yaml`, `values.yaml`, and templates
- Injects into dynamic prompt
- Returns technical audit with explanation

### `lib/`

- `input_loader.py`: loads and organizes chart files
- `utils.py`: loads `.prompt` templates
- `ollama_client.py`: HTTP client for Ollama
- `openai_client.py`: client for OpenAI GPT-4o
- `docgen.py`: core function to produce output

### `prompts/`

- Includes prompts like `helm_lint.prompt`
- Extendable with custom rules for your organization

### `Dockerfile`

Flask container. Exposes port 5000.

```bash
docker build -t helm-linter:dev .
docker run -p 5000:5000 helm-linter:dev
```

### `Makefile`

Automates tasks like:

```bash
make build             # Local image build
make load              # Load into KIND
make sync              # Sync with ArgoCD
make release VERSION=v0.1.0
```

---

## 🔁 Jenkins Integration

You can invoke the microservice from a Jenkins declarative pipeline:

```groovy
def jsonPayload = '''
{
  "chart": "./charts/mychart",
  "mode": "ollama"
}
'''

sh '''
curl -X POST http://helm-linter.devops-ai.svc.cluster.local:5000/lint   -H "Content-Type: application/json"   -d '${jsonPayload}'
'''
```

---

## 🛠️ Getting Started

```bash
git clone https://github.com/dorado-ai-devops/ai-helm-linter.git
cd ai-helm-linter
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### ⚙️ Run CLI

```bash
python3 cli/lint.py --mode ollama --chart charts/example
```

### ⚙️ Run microservice

```bash
python3 app.py
```

---

## 💡 Example Output

```
[ERROR] Chart.yaml is missing the "version" field.
[SUGGESTION] Add a "version: 1.0.0" key to comply with standards.
[REVIEW] The deployment.yaml template hardcodes port 80.
```

---

## 🔮 Next Steps

- Add security rule validation (capabilities, runAsUser, etc)
- Integrate YAML validators like kubeval
- Export structured JSON for dashboards

---

## 👨‍💻 Author

- **Dani** – [@dorado-ai-devops](https://github.com/dorado-ai-devops)

---

## 🧠 Inspired by

- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Ollama](https://ollama.com)
- [OpenAI API](https://platform.openai.com/docs)

---

## 🛡 License

GNU General Public License v3.0
