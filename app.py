from flask import Flask, render_template, request, send_file, jsonify
import os
from flask import send_from_directory
import subprocess
import shutil

# Create Flask application
app = Flask(__name__)

# Folder where uploaded files will be stored
UPLOAD_FOLDER = "uploads"

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ----------------------------
# Home Page
# ----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# ----------------------------
# Upload and Generate
# ----------------------------
@app.route("/upload", methods=["POST"])
def upload():

    # Get uploaded files
    certificate = request.files["certificate"]
    excel = request.files["excel"]

    # Save uploaded files
    certificate.save(os.path.join(UPLOAD_FOLDER, "certificate.png"))
    excel.save(os.path.join(UPLOAD_FOLDER, "Students.xlsx"))

    # If settings.txt does not exist, create default values
    if not os.path.exists("settings.txt"):
        with open("settings.txt", "w") as f:
            f.write("45\n")
            f.write("1030\n")
            f.write("535\n")

    # Run certificate generation
    subprocess.run(["python", "generate.py"])

    return render_template("success.html")

@app.route("/download")
def download():

    zip_path = "certificates"

    shutil.make_archive(zip_path, "zip", "outputs")

    return send_file(
        "certificates.zip",
        as_attachment=True
    )

@app.route("/editor")
def editor():

    return render_template("editor.html")

@app.route("/save_position", methods=["POST"])
def save_position():

    data = request.get_json()

    x = data["x"]
    y = data["y"]

    # Save coordinates
    with open("settings.txt", "w") as f:
        f.write("45\n")
        f.write(str(x) + "\n")
        f.write(str(y) + "\n")

    return "✅ Layout Saved Successfully!"

@app.route("/test")
def test():
    return "TEST ROUTE WORKING"

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)

# ----------------------------
# Run Application
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)