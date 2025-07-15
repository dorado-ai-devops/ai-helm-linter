from flask import Blueprint, request, jsonify
from lib.linter import run_lint
import tempfile
import os
import json
from datetime import datetime

lint_chart_route = Blueprint('lint_chart', __name__)

@lint_chart_route.route("/lint-chart", methods=["POST"])
def lint_chart():
    mode = request.form.get("mode", "ollama")
    ruleset = request.form.get("ruleset", "default")
    chart_name = request.form.get("chart_name", "unknown")

    if "chart" not in request.files:
        return jsonify({"error": "No chart file uploaded"}), 400

    chart_file = request.files["chart"]

    # Guardar el archivo .tgz en un temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix=".tgz") as tmp:
        chart_file.save(tmp.name)
        chart_path = tmp.name


    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    info_path = f"/mnt/data/gateway/charts/chart_{timestamp}.path.json"

    os.makedirs(os.path.dirname(info_path), exist_ok=True)
    with open(info_path, "w") as f:
        json.dump({
            "chart_name": chart_name,
            "chart_temp_path": chart_path
        }, f, indent=2)


    result = run_lint(chart_path=chart_path, ruleset=ruleset, mode=mode)
    return jsonify({"result": result})
