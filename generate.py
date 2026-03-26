from PIL import Image, ImageDraw, ImageFont
import pandas as pd
# Load Excel file
data = pd.read_excel("students.xlsx")
# Loop through each row
for index, row in data.iterrows():
    name = row["Name"]
    gender = row["Gender"]
    # Load certificate image
    image = Image.open("certificate.png")
    # Create drawing object
    draw = ImageDraw.Draw(image)
    # Load font
    font = ImageFont.truetype("fonts/TIMES.TTF", 45)
    # ---------------------------
    # NAME POSITION (ONLY NAME)
    # ---------------------------
    x = 1030
    y = 535
    draw.text((x, y), name, fill="black", font=font)
    # ---------------------------
    # STRIKE LOGIC
    # ---------------------------
    if gender.lower() == "male":
        # Strike "Ms."
        strike_x = 933
        strike_y = 560
    else:
        # Strike "Mr."
        strike_x = 833
        strike_y = 560
    line_length = 60
    draw.line(
        (strike_x, strike_y, strike_x + line_length, strike_y),
        fill="black",
        width=3
    )
    # ---------------------------
    # SAVE (unique file for each)
    # ---------------------------
    filename = name.replace(" ", "_") + ".png"
    image.save(filename)
    print(f"Generated: {filename}")
print("✅ ALL CERTIFICATES GENERATED!")