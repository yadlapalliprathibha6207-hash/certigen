from PIL import Image, ImageDraw, ImageFont
# Load certificate image
image = Image.open("certificate.png")
# Create drawing object
draw = ImageDraw.Draw(image)
# Load font
font = ImageFont.truetype("fonts/TIMES.TTF", 45)
# ---------------------------
# INPUT
# ---------------------------
name = "Prathibha Yadlapalli"
gender = "female"   # male / female
# ---------------------------
# NAME POSITION (ONLY NAME)
# ---------------------------
x = 1010
y = 535
draw.text((x, y), name, fill="black", font=font)
# ---------------------------
# STRIKE LOGIC
# ---------------------------
if gender.lower() == "male":
    # Strike "Ms."
    strike_x = 933   # adjust
    strike_y = 560
else:
    # Strike "Mr."
    strike_x = 833   # adjust
    strike_y = 560
line_length = 60
draw.line(
    (strike_x, strike_y, strike_x + line_length, strike_y),
    fill="black",
    width=3
)

# ---------------------------
# SAVE
# ---------------------------
image.save("output.png")
print("✅ Certificate generated!")