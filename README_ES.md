# 🧠 ai-helm-linter

> Microservicio para auditar Helm Charts usando LLMs (OpenAI u Ollama), detectando errores, inconsistencias o malas prácticas mediante prompts especializados.

---

## 🚀 Características

- ✅ Audita sintaxis, convenciones y coherencia en Helm Charts  
- 📚 Analiza `Chart.yaml`, `values.yaml` y las plantillas en `templates/`  
- 🤖 Compatible con modelos locales de Ollama o GPT-4o vía OpenAI  
- 🧩 CLI y API REST vía Flask  
- 🐳 Preparado para Docker y desplegable con Helm + ArgoCD  
- 🔁 Fallback automático a OpenAI si Ollama falla  
- 📁 Compatible con GitOps y CI/CD  
- ✍️ Prompts editables para alinearse con políticas internas  

---

## 📦 Estructura del Proyecto

```
ai-helm-linter/
├── app.py                 # Entrada del microservicio Flask
├── cli/                   # Interfaz CLI (lint.py)
├── lib/                   # Lógica central y clientes LLM
├── prompts/               # Plantillas de prompts
├── routes/                # Rutas de Flask
├── requirements.txt       # Dependencias de Python
├── Dockerfile             # Configuración de contenedor
├── Makefile               # Automatización de build y despliegue
└── README.md              # Documentación del proyecto
```

---

## 🧩 Componentes

### `app.py`

Servidor Flask que inicia el endpoint `/lint-chart`, recibe JSON e invoca el linter.

### `routes/lint_chart.py`

- Endpoint: `/lint-chart`
- JSON de entrada:  
  ```json
  {
    "chart_path": "./charts/example",
    "mode": "ollama",
    "ruleset": "default"
  }
  ```
- Salida: Informe de lint generado por IA

### `cli/lint.py`

Herramienta CLI para ejecutar el linter desde terminal.

```bash
python3 cli/lint.py --mode ollama --chart charts/example
```

### `lib/`

- `linter.py`: Núcleo del análisis con LLM  
- `utils.py`: Carga prompts y contenido del chart  
- `ollama_client.py`: Cliente HTTP para Ollama  
- `openai_client.py`: Cliente para OpenAI

### `prompts/`

- `helm_linting.prompt`: Plantilla base de prompt
- Fácilmente extensible con reglas personalizadas

---

## 🔁 Integración Jenkins

Puedes invocar el microservicio desde un pipeline declarativo en Jenkins:

```groovy
def jsonPayload = '''
{
  "chart_path": "./charts/mychart",
  "mode": "ollama"
}
'''

sh '''
curl -X POST http://helm-linter.devops-ai.svc.cluster.local:5000/lint-chart   -H "Content-Type: application/json"   -d '${jsonPayload}'
'''
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

---

### Ejecutar CLI

```bash
python3 cli/lint.py --mode ollama --chart charts/example
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

- [ ] Validaciones de seguridad (runAsNonRoot, capabilities)
- [ ] Integrar kubeval u otros validadores YAML
- [ ] Exportar JSON estructurado para dashboards externos

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