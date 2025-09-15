from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

# Canvas setup
W, H = 800, 1600  # portrait layout
bg_color = (7, 24, 48)  # dark navy background
img = Image.new('RGB', (W, H), bg_color)
draw = ImageDraw.Draw(img)

# Center point for emblem
cx, cy = W//2, H//2 - 120
emblem_r = 220

# Orange crescent (outer circle)
outer_color = (255, 140, 0)  # orange
draw.ellipse((cx-emblem_r, cy-emblem_r, cx+emblem_r, cy+emblem_r), fill=outer_color)

# Cutout inner circle to form crescent
inner_r = int(emblem_r * 0.7)
shift_x, shift_y = int(emblem_r * 0.28), -int(emblem_r * 0.05)
mask = Image.new('L', (W, H), 0)
mask_draw = ImageDraw.Draw(mask)
mask_draw.ellipse((cx-inner_r+shift_x, cy-inner_r+shift_y,
                   cx+inner_r+shift_x, cy+inner_r+shift_y), fill=255)
img.paste(bg_color, mask=mask)

# Water inside crescent (blue semicircle)
water_color = (30, 144, 255)  # dodger blue
water_r = int(emblem_r * 0.7)
water_bbox = (cx-water_r, cy-water_r//4, cx+water_r, cy+water_r//4 + 2*water_r)
draw.pieslice(water_bbox, start=180, end=360, fill=water_color)

# White wave lines
wave_y = cy + int(water_r*0.45)
for k in range(3):
    offset = k * 18
    points = []
    for x in range(cx-water_r+10, cx+water_r-10, 6):
        y = wave_y + math.sin((x+offset)/20.0) * 8 + (k*4)
        points.append((x, y))
    draw.line(points, fill=(255, 255, 255), width=3)

# Islands / pyramids
island_color = (255, 200, 0)
p1 = [(cx-80, cy-20), (cx-30, cy-110), (cx+20, cy-20)]
p2 = [(cx+40, cy+10), (cx+90, cy-60), (cx+140, cy+10)]
draw.polygon(p1, fill=island_color)
draw.polygon(p2, fill=island_color)

# Palm trees
trunk_color, leaf_color = (80, 42, 42), (34, 139, 34)
draw.line([(cx+60, cy-90), (cx+40, cy-30)], fill=trunk_color, width=8)
draw.line([(cx+100, cy-60), (cx+90, cy+10)], fill=trunk_color, width=6)

def palm_leaves(x, y, scale=1.0):
    for angle in [-140, -110, -80, -50, -20]:
        rad = math.radians(angle)
        x2 = x + math.cos(rad) * int(60*scale)
        y2 = y + math.sin(rad) * int(60*scale)
        draw.line([(x,y),(x2,y2)], fill=leaf_color, width=int(6*scale))
        draw.line([(x2,y2),(x2+math.cos(rad-0.2)*12,
                            y2+math.sin(rad-0.2)*12)], fill=leaf_color, width=int(3*scale))

palm_leaves(cx+40, cy-110, scale=1.0)
palm_leaves(cx+90, cy-80, scale=0.7)

# Glow effect
glow = img.filter(ImageFilter.GaussianBlur(radius=6))
img = Image.blend(glow, img, alpha=0.6)
draw = ImageDraw.Draw(img)

# Text
try:
    title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 34)
    tag_font = ImageFont.truetype("DejaVuSans.ttf", 14)
except:
    title_font = ImageFont.load_default()
    tag_font = ImageFont.load_default()

title = "SAFARNAMA"
tag = "YOUR JOURNEY, YOUR MATE"
w_title, h_title = draw.textsize(title, font=title_font)
w_tag, h_tag = draw.textsize(tag, font=tag_font)

draw.text((cx - w_title/2, cy + emblem_r + 40), title, font=title_font, fill=(255,255,255))
draw.text((cx - w_tag/2, cy + emblem_r + 40 + h_title + 6), tag, font=tag_font, fill=(180,200,220))

# Save
img.save("safarnama_logo.png")
print("✅ Logo saved as safarnama_logo.png")
