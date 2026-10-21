#!/usr/bin/env python3
"""توليد أيقونة القارئ من صورة غلاف الكتاب (مستخرَجة من PDF)."""
import os
import pymupdf
from PIL import Image

PDF = "/home/hmh/Downloads/Designing Data-Intensive Applications - Martin Kleppmann.pdf"
OUT = "/home/hmh/Videos/DDIA/assets/cover.png"
SCALE = 4

doc = pymupdf.open(PDF)
page = doc[0]

# ارسم الصفحة بدقة عالية
pix = page.get_pixmap(matrix=pymupdf.Matrix(SCALE, SCALE))
img = Image.open(__import__("io").BytesIO(pix.tobytes("png"))).convert("RGB")
W, H = img.size

# كتلة العنوان (النصّ الأبيض) داخل الشارة الحمراء
# x: 42..465 من 504 ، y: 78..272 من 661
x0, y0 = int(42 * SCALE), int(78 * SCALE)
x1, y1 = int(465 * SCALE), int(272 * SCALE)
block = img.crop((x0, y0, x1, y1))

# عيّنة اللون الأحمر من الشارة نفسها (من هامش فوق النصّ)
red = block.getpixel((6, 6))

# مربّع: العنوان في الوسط على خلفية بلون الشارة
side = 512
canvas = Image.new("RGB", (side, side), red)
band = block.resize((int(side * 0.9), int(block.height * (side * 0.9) / block.width)), Image.LANCZOS)
canvas.paste(band, ((side - band.width) // 2, (side - band.height) // 2))

# تقريب الحواف ليبدو أيقونة
canvas = canvas.resize((512, 512), Image.LANCZOS)
canvas.save(OUT, "PNG", optimize=True)
print("cover icon written:", OUT, os.path.getsize(OUT), "bytes", canvas.size)
