from flask import Flask, render_template, request, send_file
import os, json
from pdf_utils import auto_clean_pdf

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("pdf")
        if not file:
            return "No file uploaded."

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        output_path = os.path.join(UPLOAD_FOLDER, f"cleaned_{file.filename}")

        # Parse JSON-style rotation and bookmarks from frontend
        try:
            rotate_pages = json.loads(request.form.get("rotate_pages", "{}"))
            bookmarks = json.loads(request.form.get("bookmarks", "{}"))
        except json.JSONDecodeError:
            return "Invalid JSON format in rotate_pages or bookmarks."

        try:
            auto_clean_pdf(input_path, output_path, rotate_pages, bookmarks)
            return send_file(output_path, as_attachment=True)
        except ValueError as e:
            return f"❌ Error: {str(e)}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
