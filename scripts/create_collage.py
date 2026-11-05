from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import pytz

WIDTH = 1080
HEIGHT = 1350

HEADER_H = 130
FOOTER_H = 70

OUTPUT = "public/weather/marine-forecast.jpg"

canvas = Image.new(
    "RGB",
    (WIDTH, HEIGHT),
    (241, 246, 250)
)

draw = ImageDraw.Draw(canvas)

try:
    title_font = ImageFont.truetype(
        "DejaVuSans-Bold.ttf",
        42
    )

    panel_font = ImageFont.truetype(
        "DejaVuSans-Bold.ttf",
        24
    )

    footer_font = ImageFont.truetype(
        "DejaVuSans.ttf",
        18
    )

except:
    title_font = ImageFont.load_default()
    panel_font = ImageFont.load_default()
    footer_font = ImageFont.load_default()

# ------------------------------------------------------
# HEADER
# ------------------------------------------------------

draw.rectangle(
    [(0, 0), (WIDTH, HEADER_H)],
    fill=(0, 53, 102)
)

draw.text(
    (25, 30),
    "RabirubiaWeather Virtual Rain Forecast (images by NWS)",
    fill="white",
    font=title_font
)

# ------------------------------------------------------
# LOGO
# ------------------------------------------------------

try:
    logo = Image.open(
        "assets/rabirubiaweather-logo.png"
    ).convert("RGBA")

    logo.thumbnail((230, 85))

    canvas.paste(
        logo,
        (830, 18),
        logo
    )

except Exception as e:
    print("Logo load failed:", e)

# ------------------------------------------------------
# PANEL HELPER
# ------------------------------------------------------

def panel(title, file, x, y, w, h):

    draw.rounded_rectangle(
        [x, y, x + w, y + h],
        radius=18,
        fill="white",
        outline=(205, 210, 215),
        width=2
    )

    draw.text(
        (x + 15, y + 12),
        title,
        fill=(0, 53, 102),
        font=panel_font
    )

    img = Image.open(file).convert("RGB")

    img.thumbnail(
        (w - 25, h - 60),
        Image.Resampling.LANCZOS
    )

    px = x + (w - img.width) // 2
    py = y + 50

    canvas.paste(img, (px, py))

# ------------------------------------------------------
# TOP ROW
# ------------------------------------------------------

panel(
    "24 Hour Rainfall",
    "downloads/24hr.png",
    20,
    150,
    510,
    320
)

panel(
    "48 Hour Rainfall",
    "downloads/48hr.png",
    550,
    150,
    510,
    320
)

# ------------------------------------------------------
# MIDDLE
# ------------------------------------------------------

panel(
    "72 Hour Rainfall",
    "downloads/72hr.png",
    20,
    490,
    1040,
    320
)

# ------------------------------------------------------
# BOTTOM
# ------------------------------------------------------

panel(
    "Virtual Buoys",
    "downloads/buoys.png",
    20,
    830,
    1040,
    440
)

# ------------------------------------------------------
# FOOTER
# ------------------------------------------------------

draw.rectangle(
    [(0, HEIGHT - FOOTER_H), (WIDTH, HEIGHT)],
    fill=(0, 53, 102)
)

pr_tz = pytz.timezone("America/Puerto_Rico")

pr_now = datetime.now(pr_tz)

timestamp = pr_now.strftime(
    "Generated: %b %d, %Y %I:%M %p AST"
)

draw.text(
    (20, HEIGHT - 42),
    timestamp,
    fill="white",
    font=footer_font
)

draw.text(
    (720, HEIGHT - 42),
    "www.rabirubiaweather.com",
    fill="white",
    font=footer_font
)

canvas.save(
    OUTPUT,
    quality=95,
    optimize=True
)

print(f"Created {OUTPUT}")
