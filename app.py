from flask import Flask, render_template, request
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():

    certificate = request.files["certificate"]
    excel = request.files["excel"]

    certificate.save(os.path.join(UPLOAD_FOLDER, certificate.filename))
    excel.save(os.path.join(UPLOAD_FOLDER, excel.filename))

    subprocess.run(["python", "generate.py"])

    return "Certificates generated successfully!"

if __name__ == "__main__":
    app.run(debug=True)