from flask import Flask, request, jsonify
from routes.lint_chart import lint_chart_route

app = Flask(__name__)
app.register_blueprint(lint_chart_route)

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)
