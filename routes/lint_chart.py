from flask import Blueprint, request, jsonify
from lib.linter import run_lint
import tempfile

lint_chart_route = Blueprint('lint_chart', __name__)

@lint_chart_route.route("/lint-chart", methods=["POST"])
def lint_chart():
    mode = request.form.get("mode", "ollama")
    ruleset = request.form.get("ruleset", "default")
    
    if "chart" not in request.files:
        return jsonify({"error": "No chart file uploaded"}), 400
    
    chart_file = request.files["chart"]

    # Guardar el archivo .tgz en un temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".tgz") as tmp:
        chart_file.save(tmp.name)
        chart_path = tmp.name

    result = run_lint(chart_path=chart_path, ruleset=ruleset, mode=mode)
    return jsonify({"result": result})
