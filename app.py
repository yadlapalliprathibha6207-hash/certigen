from flask import Flask, render_template, request, send_file, jsonify, url_for, send_from_directory
import os
import shutil
import json
import subprocess
import sys
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
OUTPUT_FOLDER = BASE_DIR / "outputs"
LAYOUT_FILE = BASE_DIR / "layout.json"
SETTINGS_FILE = BASE_DIR / "settings.txt"

UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)


def ensure_layout_file():
    if not LAYOUT_FILE.exists():
        default_layout = {
            "fields": [
                {
                    "id": "field-name",
                    "name": "Name",
                    "x": 460,
                    "y": 320,
                    "fontSize": 42,
                    "fontFamily": "Times New Roman",
                    "color": "#000000",
                    "bold": False,
                    "italic": False,
                    "align": "center"
                }
            ],
            "genderLogic": True
        }
        with LAYOUT_FILE.open("w", encoding="utf-8") as handle:
            json.dump(default_layout, handle, indent=2)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    certificate = request.files.get("certificate")
    excel = request.files.get("excel")

    if not certificate or not excel:
        return "Please upload both a certificate template and an Excel file.", 400

    certificate.save(UPLOAD_FOLDER / "certificate.png")
    excel.save(UPLOAD_FOLDER / "Students.xlsx")

    ensure_layout_file()

    if not SETTINGS_FILE.exists():
        SETTINGS_FILE.write_text("True\n", encoding="utf-8")

    subprocess.run([sys.executable, str(BASE_DIR / "generate.py")], check=False)

    output_count = len(list(OUTPUT_FOLDER.glob("*.png")))
    return render_template("success.html", output_count=output_count)


@app.route("/designer")
def designer():
    ensure_layout_file()
    template_image = ""
    if (UPLOAD_FOLDER / "certificate.png").exists():
        template_image = url_for("uploaded_file", filename="certificate.png")
    return render_template("designer.html", template_image=template_image)


@app.route("/get_layout")
def get_layout():
    ensure_layout_file()
    with LAYOUT_FILE.open("r", encoding="utf-8") as handle:
        return jsonify(json.load(handle))


@app.route("/save_layout", methods=["POST"])
def save_layout():
    payload = request.get_json(silent=True) or {}
    layout = {
        "fields": payload.get("fields", []),
        "genderLogic": payload.get("genderLogic", True)
    }
    with LAYOUT_FILE.open("w", encoding="utf-8") as handle:
        json.dump(layout, handle, indent=2)
    return jsonify({"message": "Layout saved successfully."})


@app.route("/download")
def download():
    archive_path = BASE_DIR / "certificates"
    shutil.make_archive(str(archive_path), "zip", OUTPUT_FOLDER)
    return send_file(
        BASE_DIR / "certificates.zip",
        as_attachment=True,
        download_name="certificates.zip"
    )


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)