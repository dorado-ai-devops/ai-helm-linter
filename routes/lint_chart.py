from flask import Blueprint, request, jsonify
from lib.linter import run_lint

lint_chart_route = Blueprint('lint_chart', __name__)

@lint_chart_route.route("/lint-chart", methods=["POST"])
def lint_chart():
    data = request.get_json()
    result = run_lint(chart_path=data["chart_path"], ruleset=data.get("ruleset", "default"), mode=data.get("mode", "ollama"))
    return jsonify({"result": result})
