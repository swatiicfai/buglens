from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs("samples", exist_ok=True)

# Generate a realistic terminal stacktrace image
img = Image.new("RGB", (900, 360), color="#1e1e1e")
draw = ImageDraw.Draw(img)

# Window top bar
draw.rectangle([(0, 0), (900, 35)], fill="#2d2d2d")
draw.ellipse([(15, 12), (25, 22)], fill="#ff5f56")
draw.ellipse([(35, 12), (45, 22)], fill="#ffbd2e")
draw.ellipse([(55, 12), (65, 22)], fill="#27c93f")
draw.text((80, 10), "Terminal - bash - 80x24", fill="#888888")

# Terminal text
terminal_text = [
    ("$ python -m app.main", "#00ff88"),
    ("Traceback (most recent call last):", "#ff5555"),
    ("  File \"/workspace/app/main.py\", line 42, in <module>", "#cccccc"),
    ("    user_data = parse_user_payload(request.json)", "#cccccc"),
    ("  File \"/workspace/app/main.py\", line 18, in parse_user_payload", "#cccccc"),
    ("    token_expiry = datetime.fromtimestamp(payload['exp'])", "#cccccc"),
    ("KeyError: 'exp' - User JWT payload missing required expiration claim", "#ff5555"),
    ("", "#ffffff"),
    ("[CRITICAL ERROR] Server failed to start due to unhandled KeyError.", "#ffb86c"),
    ("Suggested action: Check token validation middleware or add .get('exp', None)", "#8be9fd")
]

y = 50
for line, color in terminal_text:
    draw.text((20, y), line, fill=color)
    y += 28

img.save("samples/sample_stacktrace.png")
print("Sample generated at samples/sample_stacktrace.png")
