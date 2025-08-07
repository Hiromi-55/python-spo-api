from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def handle_request():
    data = request.get_json()
    target_url = data.get("target_url")

    # Placeholder logic for PDF parsing and management number extraction
    management_number = "仮の管理番号"

    return jsonify({"management_number": management_number})
