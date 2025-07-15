from flask import Flask, request, jsonify
import subprocess
import tempfile
import os
import tarfile

app = Flask(__name__)

@app.route("/lint-chart", methods=["POST"])
def lint_chart():
    mode = request.form.get("mode", "openai")
    file = request.files.get("chart")

    if not file:
        return jsonify({"error": "No chart file uploaded"}), 400

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            chart_path = os.path.join(tmpdir, "chart.tgz")
            file.save(chart_path)

            with tarfile.open(chart_path) as tar:
                tar.extractall(path=tmpdir)

            extracted_dir = next(
                (os.path.join(tmpdir, name) for name in os.listdir(tmpdir)
                 if os.path.isdir(os.path.join(tmpdir, name))),
                None
            )

            if not extracted_dir:
                return jsonify({"error": "Failed to extract chart archive"}), 500

            result = subprocess.run(
                ["python3", "cli/lint.py", "--mode", mode, "--chart_path", extracted_dir],
                capture_output=True,
                text=True,
                env={**os.environ, "PYTHONPATH": "."}
            )

            if result.returncode != 0:
                return jsonify({"error": result.stderr.strip()}), 500

            return jsonify({"result": result.stdout.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
