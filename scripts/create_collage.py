from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from datetime import datetime

WIDTH = 1080
HEIGHT = 1350

HEADER_HEIGHT = 130
FOOTER_HEIGHT = 70

OUTPUT = "public/weather/marine-forecast.jpg"

canvas = Image.new(
    "RGB",
    (WIDTH, HEIGHT),
    (241, 246, 250)
)

draw = ImageDraw.Draw(canvas)

# --------------------------------------------------
# Fonts
# --------------------------------------------------

try:
    title_font = ImageFont.truetype(
        "DejaVuSans-Bold.ttf",
        42
    )

    section_font = ImageFont.truetype(
        "DejaVuSans-Bold.ttf",
        22
    )

    footer_font = ImageFont.truetype(
        "DejaVuSans.ttf",
        18
    )

except:
    title_font = ImageFont.load_default()
    section_font = ImageFont.load_default()
    footer_font = ImageFont.load_default()

# --------------------------------------------------
# Header
# --------------------------------------------------

draw.rectangle(
    [(0, 0), (WIDTH, HEADER_HEIGHT)],
    fill=(0, 45, 90)
)

draw.text(
    (28, 28),
    "RabirubiaWeather Rain Virtual Forecast",
    fill="white",
    font=title_font
)

# --------------------------------------------------
# Logo
# --------------------------------------------------

try:
    logo = Image.open(
        "assets/rabirubiaweather-logo.png"
    ).convert("RGBA")

    logo.thumbnail((220, 90))

    canvas.paste(
        logo,
        (840, 15),
        logo
    )

except:
    pass

# --------------------------------------------------
# Top Row
# --------------------------------------------------

def add_panel(label, image_path, x, y, w, h):

    draw.rounded_rectangle(
        [x, y, x + w, y + h],
        radius=20,
        fill="white",
        outline=(210, 210, 210),
        width=2
    )

    draw.text(
        (x + 15, y + 10),
        label,
        fill=(0, 45, 90),
        font=section_font
    )

    img = Image.open(image_path)

    img.thumbnail(
        (w - 30, h - 60),
        Image.Resampling.LANCZOS
    )

    px = x + (w - img.width) // 2
    py = y + 45

    canvas.paste(img, (px, py))

# 24h / 48h

add_panel(
    "24 Hour Rainfall",
    "downloads/24.png",
    20,
    150,
    510,
    320
)

add_panel(
    "48 Hour Rainfall",
    "downloads/48.png",
    550,
    150,
    510,
    320
)

# --------------------------------------------------
# 72 Hour Large Panel
# --------------------------------------------------

add_panel(
    "72 Hour Rainfall",
    "downloads/72.png",
    20,
    490,
    1040,
    330
)

# --------------------------------------------------
# Virtual Buoys
# --------------------------------------------------

add_panel(
    "Virtual Buoys",
    "downloads/buoys.png",
    20,
    845,
    1040,
    370
)

# --------------------------------------------------
# Footer
# --------------------------------------------------

draw.rectangle(
    [
        (0, HEIGHT - FOOTER_HEIGHT),
        (WIDTH, HEIGHT)
    ],
    fill=(0, 45, 90)
)

ast_time = datetime.utcnow().strftime(
    "%Y-%m-%d %H:%M UTC"
)

draw.text(
    (20, HEIGHT - 45),
    ast_time,
    fill="white",
    font=footer_font
)

draw.text(
    (760, HEIGHT - 45),
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
