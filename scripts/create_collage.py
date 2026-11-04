from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from datetime import datetime

OUTPUT = Path("public/weather/marine-forecast.jpg")

WIDTH = 1080
HEIGHT = 1350

canvas = Image.new("RGB", (WIDTH, HEIGHT), (239, 244, 249))
draw = ImageDraw.Draw(canvas)

HEADER_H = 140
FOOTER_H = 80

GRID_TOP = HEADER_H + 10
GRID_HEIGHT = 850

try:
    title_font = ImageFont.truetype(
        "DejaVuSans-Bold.ttf",
        50
    )

    label_font = ImageFont.truetype(
        "DejaVuSans-Bold.ttf",
        24
    )

    footer_font = ImageFont.truetype(
        "DejaVuSans.ttf",
        22
    )

except:
    title_font = ImageFont.load_default()
    label_font = ImageFont.load_default()
    footer_font = ImageFont.load_default()

# Background
draw.rectangle(
    [(0, 0), (WIDTH, HEIGHT)],
    fill=(245, 248, 252)
)

# Header
draw.rectangle(
    [(0, 0), (WIDTH, HEADER_H)],
    fill=(0, 55, 110)
)

draw.text(
    (30, 38),
    "RabirubiaWeather Marine Forecast",
    fill="white",
    font=title_font
)

# Logo
logo_path = "assets/rabirubiaweather-logo.png"

try:
    logo = Image.open(logo_path).convert("RGBA")
    logo.thumbnail((180, 90))

    canvas.paste(
        logo,
        (870, 25),
        logo
    )
except:
    print("Logo not found. Continuing.")

images = [
    ("24 Hour Rainfall", "downloads/24hr.png"),
    ("48 Hour Rainfall", "downloads/48hr.png"),
    ("72 Hour Rainfall", "downloads/72hr.png"),
    ("Virtual Buoys", "downloads/buoys.png"),
]

positions = [
    (20, GRID_TOP),
    (550, GRID_TOP),
    (20, GRID_TOP + 370),
    (550, GRID_TOP + 370),
]

BOX_W = 510
BOX_H = 340

for (label, path), (x, y) in zip(images, positions):

    draw.rounded_rectangle(
        [x, y, x + BOX_W, y + BOX_H],
        radius=18,
        fill="white",
        outline=(210, 215, 220),
        width=2
    )

    draw.text(
        (x + 15, y + 10),
        label,
        fill=(0, 55, 110),
        font=label_font
    )

    img = Image.open(path).convert("RGB")

    img.thumbnail(
        (BOX_W - 20, BOX_H - 60),
        Image.Resampling.LANCZOS
    )

    px = x + (BOX_W - img.width) // 2
    py = y + 45

    canvas.paste(img, (px, py))

# Footer
footer_y = HEIGHT - FOOTER_H

draw.rectangle(
    [(0, footer_y), (WIDTH, HEIGHT)],
    fill=(0, 55, 110)
)

timestamp = datetime.utcnow().strftime(
    "Generated %Y-%m-%d %H:%M UTC"
)

draw.text(
    (20, footer_y + 25),
    timestamp,
    fill="white",
    font=footer_font
)

draw.text(
    (700, footer_y + 25),
    "www.rabirubiaweather.com",
    fill="white",
    font=footer_font
)

canvas.save(
    OUTPUT,
    quality=95,
    optimize=True
)

print(f"Saved {OUTPUT}")
