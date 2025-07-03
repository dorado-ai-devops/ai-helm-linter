# 🧠 ai-helm-linter

> Microservicio inteligente para auditar Helm Charts usando LLMs (Ollama o OpenAI), detectando errores, inconsistencias o malas prácticas mediante prompts especializados.  

Desarrollado en Python + Flask, con CLI integrada y despliegue vía Helm + ArgoCD.

---

## 🚀 Características

- ✅ Audita sintaxis, convenciones y coherencia estructural en Charts Helm  
- 🔐 Analiza `Chart.yaml`, `values.yaml`, `templates/*`, `*.tpl`, `*.json`, etc.  
- 🤖 Compatible con modelos locales (Ollama) o remotos (GPT-4 vía OpenAI)  
- 🔄 Fallback automático a OpenAI si Ollama falla  
- 🧩 CLI y API REST completas  
- 🐳 Dockerizado y desplegable con Helm + ArgoCD  
- 📁 Compatible con entornos GitOps y pipelines CI/CD  
- ✍️ Prompt modular y editable (`helm_linting.prompt`)  
- 📦 Soporta Charts en carpeta o empaquetados `.tgz`  

---

## 📦 Estructura del Proyecto

```
ai-helm-linter/
├── app.py                 # Entrada Flask del microservicio
├── cli/                   # CLI para ejecución directa
├── lib/                   # Lógica de negocio y clientes IA
├── prompts/               # Plantillas de prompt
├── routes/                # Rutas API (Blueprint Flask)
├── Dockerfile             # Imagen contenedor
├── Makefile               # Build y despliegue automatizado
├── requirements.txt       # Dependencias Python
└── README.md              # Documentación del proyecto
```

---

## 🧩 Componentes

### `cli/lint.py`

CLI directa para analizar Charts desde terminal:

```bash
python3 cli/lint.py --mode ollama --chart_path charts/example
```

- `--mode`: `ollama` o `openai`  
- `--chart_path`: ruta a carpeta o `.tgz`  
- `--ruleset`: nombre del ruleset a aplicar (por defecto: `"default"`)

### `app.py` + `routes/lint_chart.py`

Microservicio Flask que expone el endpoint `/lint-chart` para recibir Charts y retornar el análisis IA.

- Entrada esperada:
  - `multipart/form-data` con archivo `.tgz`
  - campos `mode` (`ollama|openai`) y `ruleset` (opcional)
- Salida: JSON con resultado IA interpretado

---

## 🧠 Lógica Interna

### `lib/linter.py`

- Carga el prompt base (`helm_linting.prompt`)  
- Inserta el contenido del Chart y las reglas  
- Llama a `query_ollama()` o `query_openai()`  
- Si Ollama falla, hace fallback automático a OpenAI

### `lib/utils.py`

- Carga Charts desde carpeta o `.tgz`
- Recorre `*.yaml`, `*.tpl`, `*.json`, etc., inyectándolos con su path relativo
- Carga plantillas de prompt como texto plano

### `lib/ollama_client.py` y `lib/openai_client.py`

- Realizan peticiones HTTP a Ollama local o GPT-4 remoto  
- Configurables vía `OLLAMA_BASE_URL` y `OPENAI_API_KEY`  

---

## 🔁 Integración Jenkins

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

## 🛠️ Primeros pasos (Local)

```bash
git clone https://github.com/dorado-ai-devops/ai-helm-linter.git
cd ai-helm-linter
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Ejecutar CLI

```bash
python3 cli/lint.py --mode ollama --chart_path charts/example
```

### Ejecutar microservicio Flask

```bash
python3 app.py
```

---

## 💡 Ejemplo de salida

```
[ERROR] Chart.yaml no contiene el campo "version".
[SUGERENCIA] Añade una clave "version: 1.0.0" para cumplir con el estándar.
[REVISIÓN] La plantilla deployment.yaml fija el puerto 80 de forma rígida.
```

---

## 🔮 Próximos pasos

- [ ] Validaciones de seguridad (runAsNonRoot, seccomp, capabilities)
- [ ] Integrar validadores externos (kubeval, kube-score)
- [ ] Exportar JSON estructurado para dashboards Streamlit

---

## 👨‍💻 Autor

- **Dani** – [@dorado-ai-devops](https://github.com/dorado-ai-devops)

---

## 🧠 Inspirado en

- [Buenas prácticas Helm](https://helm.sh/docs/chart_best_practices/)
- [Ollama](https://ollama.com)
- [OpenAI API](https://platform.openai.com/docs)

---

## 🛡 Licencia

Licencia Pública General GNU v3.0
