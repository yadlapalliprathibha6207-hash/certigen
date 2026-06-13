from flask import Flask, render_template, request, send_file
import os
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

    # Save files inside uploads folder
    certificate.save(os.path.join(UPLOAD_FOLDER, "certificate.png"))
    excel.save(os.path.join(UPLOAD_FOLDER, "Students.xlsx"))

    # Run certificate generation script
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

@app.route("/test")
def test():
    return "TEST ROUTE WORKING"

# ----------------------------
# Run Application
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)