from flask import Flask, render_template, request, send_file, jsonify, url_for, send_from_directory
import os
import shutil
import json
import subprocess
import sys
import time
from pathlib import Path
from generate import generate_certificates

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
                    "italic": True,
                    "align": "center"
                }
            ],
            "genderLogic": True
        }
        with LAYOUT_FILE.open("w", encoding="utf-8") as handle:
            json.dump(default_layout, handle, indent=2)


def normalize_layout(layout):
    now = int(time.time() * 1000)
    normalized_fields = []
    for index, field in enumerate(layout.get("fields", []) if isinstance(layout, dict) else []):
        field_data = dict(field or {})
        if not field_data.get("id"):
            field_data["id"] = f"field-{now}-{index}"
        if "fontSize" not in field_data and "size" in field_data:
            field_data["fontSize"] = field_data["size"]
        field_data["fontSize"] = int(field_data.get("fontSize", field_data.get("size", 42)) or 42)
        field_data.pop("size", None)
        field_data["x"] = int(field_data.get("x", 0) or 0)
        field_data["y"] = int(field_data.get("y", 0) or 0)
        field_data["name"] = str(field_data.get("name", "Field"))
        field_data["fontFamily"] = str(field_data.get("fontFamily", "Times New Roman"))
        field_data["color"] = str(field_data.get("color", "#000000"))
        field_data["bold"] = bool(field_data.get("bold", False))
        field_data["italic"] = bool(field_data.get("italic", False))
        field_data["align"] = str(field_data.get("align", "center"))
        normalized_fields.append(field_data)
    return {
        "fields": normalized_fields,
        "genderLogic": bool(layout.get("genderLogic", True)) if isinstance(layout, dict) else True
    }


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
        layout = json.load(handle)
    normalized = normalize_layout(layout)
    return jsonify(normalized)


@app.route("/save_layout", methods=["POST"])
def save_layout():
    payload = request.get_json(silent=True) or {}
    layout = {
        "fields": payload.get("fields", []),
        "genderLogic": payload.get("genderLogic", True)
    }
    normalized = normalize_layout(layout)
    with LAYOUT_FILE.open("w", encoding="utf-8") as handle:
        json.dump(normalized, handle, indent=2)
    return jsonify({"message": "Layout saved successfully."})


@app.route("/generate")
def generate():
    try:
        generate_certificates()
        return render_template("success.html")
    except Exception as e:
        return f"""
        <h2>❌ Certificate generation failed</h2>
        <p>{str(e)}</p>
        <a href=\"/designer\">← Back to Designer</a>
        """


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