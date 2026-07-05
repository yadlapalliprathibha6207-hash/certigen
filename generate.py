from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os

# Create outputs folder
os.makedirs("outputs", exist_ok=True)

# Read saved layout settings
with open("settings.txt", "r") as f:
    fontsize = int(f.readline())
    x = int(f.readline())
    y = int(f.readline())

# Load Excel file
data = pd.read_excel("uploads/Students.xlsx")

# Generate certificate for each student
for index, row in data.iterrows():

    name = row["Name"]
    gender = row["Gender"]

    # Load certificate template
    image = Image.open("uploads/certificate.png")

    # Create drawing object
    draw = ImageDraw.Draw(image)

    # Load font
    font = ImageFont.truetype(
        "fonts/TIMES.TTF",
        fontsize
    )

    # Draw student name
    draw.text(
        (x, y),
        name,
        fill="black",
        font=font
    )

    # Strike logic
    if gender.lower() == "male":
        strike_x = 933
        strike_y = 560
    else:
        strike_x = 833
        strike_y = 560

    draw.line(
        (
            strike_x,
            strike_y,
            strike_x + 60,
            strike_y
        ),
        fill="black",
        width=3
    )

    # Save certificate
    filename = "outputs/" + name.replace(" ", "_") + ".png"
    image.save(filename)

    print(f"Generated: {filename}")

print("✅ ALL CERTIFICATES GENERATED!")