#!/usr/bin/env python3
"""استبدال جداول الأشكال المشوّهة بصور الأشكال الأصلية من PDF.

حوّل ملف PDF إلى Markdown عملية تحويل رديئة: الأشكال البيانية الكبيرة صارت
جداول صفوفها مبعثرة. هنا نُصدّر الصور الكاملة من PDF ونستبدل تلك الجداول
(ومعها شظايا الشكل المحيطة بها) بصورة الشكل الأصلية.
"""
import io
import os
import re
import pymupdf
from PIL import Image

PDF = "/home/hmh/Downloads/Designing Data-Intensive Applications - Martin Kleppmann.pdf"
BASE = "/home/hmh/Videos/DDIA"
FIGDIR = os.path.join(BASE, "assets", "figures")
MAXW = 1400

doc = pymupdf.open(PDF)
os.makedirs(FIGDIR, exist_ok=True)


# ---------- 1) تصدير الصور الكبيرة ----------
def export(pno, xref):
    name = "page-%d.png" % pno
    path = os.path.join(FIGDIR, name)
    if os.path.exists(path):
        return name
    try:
        info = doc.extract_image(xref)
        img = Image.open(io.BytesIO(info["image"]))
        if img.mode in ("RGBA", "LA", "P"):
            img = img.convert("RGBA")
            bg = Image.new("RGB", img.size, (255, 255, 255))
            bg.paste(img, mask=img.split()[-1])
            img = bg
        else:
            img = img.convert("RGB")
    except Exception as e:
        print("  skip page", pno, "-", e)
        return None
    if img.width > MAXW:
        img = img.resize((MAXW, int(img.height * MAXW / img.width)), Image.LANCZOS)
    img.quantize(colors=64, method=Image.MEDIANCUT, dither=Image.NONE).save(
        path, "PNG", optimize=True)
    return name


# خريطة: رقم صفحة PDF -> (اسم الصورة، هل تغطّي الصفحة كلها)
figures = {}
for pno in range(doc.page_count):
    page = doc[pno]
    best = None
    for im in page.get_images(full=True):
        xref, w, h = im[0], im[2], im[3]
        if w < 1200 or h < 1200:
            continue
        for r in page.get_image_rects(xref):
            area = r.width * r.height
            if best is None or area > best[1]:
                best = (xref, area, r)
    if not best:
        continue
    xref, area, rect = best
    full = area >= 0.8 * page.rect.get_area()
    name = export(pno + 1, xref)
    if name:
        figures[pno + 1] = (name, full)

print("exported figures:", len(figures))


# ---------- 2) حفظ الخريطة ----------
import json
json.dump({str(k): {"file": v[0], "full": v[1]} for k, v in figures.items()},
          open(os.path.join(BASE, "assets", "figure_pages.json"), "w"), indent=0)
print("figure map written:", len(figures))
