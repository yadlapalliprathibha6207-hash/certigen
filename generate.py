import json
import os
from pathlib import Path

import pandas as pd
from PIL import Image, ImageDraw, ImageFont


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
OUTPUT_FOLDER = BASE_DIR / "outputs"
FONTS_FOLDER = BASE_DIR / "fonts"
LAYOUT_FILE = BASE_DIR / "layout.json"
EXCEL_FILE = UPLOAD_FOLDER / "Students.xlsx"
TEMPLATE_FILE = UPLOAD_FOLDER / "certificate.png"

OUTPUT_FOLDER.mkdir(exist_ok=True)
FONTS_FOLDER.mkdir(exist_ok=True)


def load_layout(layout_path=None, base_dir=None):
    base_dir = Path(base_dir or BASE_DIR)
    layout_path = Path(layout_path or base_dir / "layout.json")
    if not layout_path.exists():
        return {"fields": [], "genderLogic": True}
    with layout_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def get_font_path(font_family, base_dir=None):
    base_dir = Path(base_dir or BASE_DIR)
    font_family = (font_family or "Times New Roman").strip()
    candidates = []
    normalized_names = {
        font_family,
        font_family.replace(" ", ""),
        font_family.replace(" ", "_"),
        font_family.lower(),
        font_family.lower().replace(" ", ""),
        font_family.lower().replace(" ", "_"),
    }

    for name in normalized_names:
        candidates.append(name)
        candidates.append(f"{name}.ttf")
        candidates.append(f"{name}.TTF")

    for candidate in candidates:
        path = base_dir / "fonts" / candidate
        if path.exists():
            return path

    if font_family.lower() == "times new roman":
        fallback = base_dir / "fonts" / "TIMES.TTF"
        if fallback.exists():
            return fallback

    return None


def create_font(font_family, font_size, base_dir=None):
    font_path = get_font_path(font_family, base_dir)
    if font_path:
        try:
            return ImageFont.truetype(str(font_path), font_size)
        except Exception:
            pass
    return ImageFont.load_default()


def sanitize_filename(value):
    cleaned = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in str(value))
    return cleaned.strip("_") or "student"


def draw_field(draw, field, value, image_width, image_height):
    font_size = int(field.get("fontSize", 42))
    font_family = field.get("fontFamily", "Times New Roman")
    color = field.get("color", "#000000")
    align = field.get("align", "center")
    bold = bool(field.get("bold", False))
    italic = bool(field.get("italic", False))

    font = create_font(font_family, font_size, BASE_DIR)
    text = str(value if value is not None else "")

    if bold and italic:
        font = create_font(font_family, font_size, BASE_DIR)
    elif bold:
        font = create_font(font_family, font_size, BASE_DIR)
    elif italic:
        font = create_font(font_family, font_size, BASE_DIR)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = int(field.get("x", 0))
    y = int(field.get("y", 0))

    if align == "center":
        x = x - (text_width // 2)
    elif align == "right":
        x = x - text_width

    x = max(0, min(x, image_width - text_width))
    y = max(0, min(y, image_height - text_height))

    draw.text((x, y), text, fill=color, font=font)


def apply_gender_prefix(row, field_name, gender_logic):
    if not gender_logic or field_name != "Name":
        return None
    if "Gender" not in row:
        return None

    gender = str(row.get("Gender", "")).strip().lower()
    if gender.startswith("m"):
        return "Mr."
    if gender.startswith("f"):
        return "Ms."
    return None


def generate_certificates(layout_path=None):
    OUTPUT_FOLDER.mkdir(exist_ok=True)
    layout = load_layout(layout_path=layout_path)
    fields = layout.get("fields", [])
    gender_logic = bool(layout.get("genderLogic", True))

    if not TEMPLATE_FILE.exists():
        raise FileNotFoundError("Certificate template not found.")
    if not EXCEL_FILE.exists():
        raise FileNotFoundError("Excel file not found.")

    dataframe = pd.read_excel(EXCEL_FILE)
    image = Image.open(TEMPLATE_FILE)
    image_width, image_height = image.size

    for index, row in dataframe.iterrows():
        certificate = image.copy()
        draw = ImageDraw.Draw(certificate)

        for field in fields:
            field_name = field.get("name", "")
            if not field_name:
                continue

            raw_value = row.get(field_name)
            if pd.isna(raw_value):
                value = ""
            else:
                value = str(raw_value)

            prefix = apply_gender_prefix(row, field_name, gender_logic)
            if prefix and value:
                value = f"{prefix} {value}"

            draw_field(draw, field, value, image_width, image_height)

        student_name = sanitize_filename(row.get("Name") if "Name" in row else index)
        output_path = OUTPUT_FOLDER / f"{student_name}_{index + 1}.png"
        certificate.save(output_path)
        print(f"Generated: {output_path}")

    print("✅ ALL CERTIFICATES GENERATED!")


if __name__ == "__main__":
    generate_certificates()