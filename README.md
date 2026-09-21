# CertiGen

## Description

CertiGen is an automated certificate generation system built using Python and Flask. It generates personalized certificates from an Excel sheet and allows users to download all generated certificates as a ZIP file.

## Features

- Upload certificate template
- Upload Excel sheet
- Automatic certificate generation
- Gender-based Mr./Ms. strike logic
- Batch generation
- ZIP download
- Simple web interface

## Tech Stack

- Python
- Flask
- Pillow (PIL)
- Pandas
- HTML
- CSS

## Folder Structure

certigen/
│
├── app.py
├── generate.py
├── templates/
├── static/
├── uploads/
├── outputs/
├── fonts/

## Future Scope

- Email certificates automatically
- QR code verification
- PDF certificate generation
- Cloud deployment
- Admin dashboard

## Quick Start

- Create a virtual environment and activate it:

	- Windows: `python -m venv venv` then `venv\Scripts\activate`
	- macOS / Linux: `python -m venv venv` then `source venv/bin/activate`

- Install dependencies:

```
pip install -r requirements.txt
```

- Run the app (development):

```
python app.py
```

## Template Designer

A Template Designer UI was added on the `version-3-template-designer` branch. See the interactive designer and its assets:

- templates/designer.html
- static/designer.js

This lets you visually place text and images on a certificate template before generating certificates.

## Usage

- Upload a certificate template (image) and an Excel file with recipient data.
- Use the web UI to map fields and generate certificates in batch.
- Generated files are saved to the `outputs/` folder and can be downloaded as a ZIP.

## Dependencies & Python

- All Python dependencies are listed in `requirements.txt`.
- The project is developed for modern Python 3.x (3.8+ recommended).

## Contributing

- Fork the repo, create a branch, make changes, and open a PR against `main`.
- If you're sharing this repo with a friend, consider adding a short CONTRIBUTING.md and a license.
