from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route("/lint-chart", methods=["POST"])
def lint_chart():
    data = request.get_json()
    chart_path = data.get("chart_path", "")
    mode = data.get("mode", "openai")

    if not chart_path:
        return jsonify({"error": "Missing 'chart_path' in request"}), 400

    try:
        result = subprocess.run(
            ["python3", "cli/lint.py", "--mode", mode, "--chart_path", chart_path],
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": "."}
        )

        if result.returncode != 0:
            return jsonify({"error": result.stderr.strip()}), 500

        return jsonify({"result": result.stdout.strip()}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
