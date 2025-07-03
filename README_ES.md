# 🧠 ai-helm-linter

> Microservicio para auditar Helm Charts con LLMs (OpenAI u Ollama), detectando errores, incoherencias o malas prácticas mediante prompts especializados.

---

## 🚀 Funcionalidades

- ✅ Audita sintaxis, convenciones y coherencia de Helm Charts
- 📚 Analiza `Chart.yaml`, `values.yaml` y plantillas en `templates/`
- 🤖 Usa modelos locales con Ollama o GPT-4o vía OpenAI
- 🧩 CLI y API REST con Flask integrados
- 🐳 Preparado para Docker y despliegue con Helm + ArgoCD
- 🔁 Fallback automático a OpenAI si Ollama falla
- 📁 Compatible con flujos GitOps y pipelines CI/CD
- ✍️ Prompts editables para adaptarse a políticas personalizadas

---

## 📦 Estructura del Proyecto

```
ai-helm-linter/
├── app.py                 # Microservicio Flask (API /lint)
├── cli/                   # Scripts CLI como lint.py
├── lib/                   # Clientes OpenAI/Ollama y lógica común
├── charts/                # Charts de ejemplo para pruebas
├── prompts/               # Plantillas .prompt dinámicas
├── requirements.txt       # Dependencias Python
├── Dockerfile             # Contenedor Flask
├── Makefile               # Build y despliegue automatizado
└── README.md              # Documentación del proyecto
```

---

## 🧩 Descripción Detallada de Componentes

### `app.py`

Microservicio Flask desplegable en K8s:
- Endpoint `/lint`
- Acepta JSON: `{ "chart": "./charts/example", "mode": "openai|ollama" }`
- Carga el contenido del chart
- Llama a `lint.py` y devuelve análisis estructurado

### `cli/lint.py`

Script principal para linting con IA:
- Argumentos: `--mode`, `--chart`
- Carga `Chart.yaml`, `values.yaml`, y plantillas
- Inyecta en prompt dinámico
- Devuelve auditoría técnica con explicación

### `lib/`

- `input_loader.py`: lee y organiza los archivos del chart
- `utils.py`: carga plantillas .prompt
- `ollama_client.py`: cliente HTTP para Ollama
- `openai_client.py`: cliente para OpenAI GPT-4o
- `docgen.py`: función core que unifica el análisis

### `prompts/`

- Contiene prompts como `helm_lint.prompt` que pueden modificarse.
- Admite templates para reglas específicas de tu organización.

### `Dockerfile`

Contenedor Flask. Expone puerto 5000.

```bash
docker build -t helm-linter:dev .
docker run -p 5000:5000 helm-linter:dev
```

### `Makefile`

Automatiza tareas como:

```bash
make build             # Build de imagen local
make load              # Carga en KIND
make sync              # Sincroniza con ArgoCD
make release VERSION=v0.1.0
```

---

## 🔁 Jenkins Integration

Puedes invocar este microservicio desde un pipeline declarativo:

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

## 🛠️ Primeros pasos

```bash
git clone https://github.com/dorado-ai-devops/ai-helm-linter.git
cd ai-helm-linter
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### ⚙️ Ejecutar CLI

```bash
python3 cli/lint.py --mode ollama --chart charts/example
```

### ⚙️ Ejecutar microservicio

```bash
python3 app.py
```

---

## 💡 Ejemplo de salida

```
[ERROR] El archivo Chart.yaml no contiene campo version.
[SUGERENCIA] Añade una clave "version: 1.0.0" para cumplir el estándar.
[REVISIÓN] El template deployment.yaml tiene hardcodeado el puerto 80.
```

---

## 🔮 Próximos pasos

- Añadir reglas de seguridad (capabilities, runAsUser, etc)
- Integración con validadores YAML y kubeval
- Exportación a JSON estructurado para dashboards

---

## 👨‍💻 Autor

- **Dani** – [@dorado-ai-devops](https://github.com/dorado-ai-devops)

---

## 🧠 Inspirado por

- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Ollama](https://ollama.com)
- [OpenAI API](https://platform.openai.com/docs)

---

## 🛡 Licencia

Licencia Pública General GNU v3.0