from flask import Flask, request, jsonify
import requests
import tempfile
import pdfplumber

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def handle_request():
    if request.method == "GET":
        return "App is running!"

    data = request.get_json()
    target_url = data.get("target_url")

    if not target_url:
        return jsonify({"error": "No target_url provided"}), 400

    try:
        # Download the PDF
        response = requests.get(target_url)
        response.raise_for_status()

        # Save to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf.write(response.content)
            tmp_pdf_path = tmp_pdf.name

        management_numbers = []

        # Extract tables and get rightmost column values
        with pdfplumber.open(tmp_pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if row and len(row) > 0:
                            management_numbers.append(row[-1])

        return jsonify({"management_numbers": management_numbers})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
