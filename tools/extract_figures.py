#!/usr/bin/env python3
"""استخراج أشكال الكتاب (Figure N-M) من ملف PDF وحفظها في assets/figures/."""
import os
import re
import sys
import pymupdf
from PIL import Image

PDF = "/home/hmh/Downloads/Designing Data-Intensive Applications - Martin Kleppmann.pdf"
OUT = "/home/hmh/Videos/DDIA/assets/figures"
MAXW = 1500

CAP = re.compile(r'^(Figure|Example)\s+(\d+)-(\d+)\s*[.:]?\s*(.*)$')

os.makedirs(OUT, exist_ok=True)
doc = pymupdf.open(PDF)

# 1) اجمع التسميات ومواضعها
captions = []   # (page, kind, num, text, bbox)
for pno in range(doc.page_count):
    page = doc[pno]
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            txt = "".join(s["text"] for s in l["spans"]).strip()
            m = CAP.match(txt)
            if m:
                captions.append((pno, m.group(1), "%s-%s" % (m.group(2), m.group(3)),
                                 m.group(4).strip(), tuple(l["bbox"])))

# 2) اجمع مواضع الصور لكل صفحة
placements = {}   # page -> list of (xref, rect)
for pno in range(doc.page_count):
    page = doc[pno]
    lst = []
    for im in page.get_images(full=True):
        xref = im[0]
        for r in page.get_image_rects(xref):
            lst.append((xref, r, im[2], im[3]))
    placements[pno] = lst

# 3) اربط كل تسمية بأقرب صورة/مجموعة صور فوقها
used = set()
manifest = []
unmatched = []

for pno, kind, num, ctext, cbbox in captions:
    lst = placements.get(pno, [])
    # الصور التي تنتهي فوق أعلى التسمية
    cands = [(x, r, w, h) for (x, r, w, h) in lst if r.y1 <= cbbox[1] + 2 and (x, r) not in used]
    if not cands:
        unmatched.append((pno, kind, num, ctext[:50]))
        continue
    # الأقرب: أكبر y1
    cands.sort(key=lambda t: -t[1].y1)
    # اجمع كل الصور المتلاصقة (فجوة < 12 نقطة) فوق التسمية
    chosen = [cands[0]]
    limit = cands[0][1].y0
    for c in cands[1:]:
        if c[1].y1 >= limit - 14:
            chosen.append(c)
            limit = min(limit, c[1].y0)
    for c in chosen:
        used.add((c[0], c[1]))

    #領域: من أعلى عنصر مختار إلى أسفله
    x0 = min(c[1].x0 for c in chosen)
    y0 = min(c[1].y0 for c in chosen)
    x1 = max(c[1].x1 for c in chosen)
    y1 = max(c[1].y1 for c in chosen)

    # احفظ الصورة (أو المركّب عدة صور)
    if len(chosen) == 1:
        xref = chosen[0][0]
        pix = pymupdf.Pixmap(doc, xref)
        if pix.n - pix.alpha >= 4:
            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    else:
        imgs = []
        for c in sorted(chosen, key=lambda t: t[1].y0):
            pix = pymupdf.Pixmap(doc, c[0])
            if pix.n - pix.alpha >= 4:
                pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
            imgs.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
        W = max(i.width for i in imgs)
        H = sum(i.height for i in imgs)
        img = Image.new("RGB", (W, H), "white")
        yy = 0
        for i in imgs:
            img.paste(i, (0, yy))
            yy += i.height

    if img.width > MAXW:
        h = int(img.height * MAXW / img.width)
        img = img.resize((MAXW, h), Image.LANCZOS)
    name = "fig-%s.png" % num if kind == "Figure" else "ex-%s.png" % num
    path = os.path.join(OUT, name)
    # الأشكال مسطّحة الألوان → لوحة ألوان صغيرة (حجم أصغر بكثير بلا فرق مرئي)
    q = img.quantize(colors=64, method=Image.MEDIANCUT, dither=Image.NONE)
    q.save(path, "PNG", optimize=True)
    # نصوص الشكل الداخلية (الشظايا المشوّهة التي تُحذف من الـMarkdown)
    shards = []
    for b in doc[pno].get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        bx = b["bbox"]
        cx, cy = (bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2
        if y0 - 2 <= cy <= y1 + 2 and x0 - 2 <= cx <= x1 + 2:
            for l in b["lines"]:
                for sp in l["spans"]:
                    shards.append(sp["text"])
    toks = set()
    for t in shards:
        for w in re.findall(r"[\w\u0600-\u06FF]+", t.lower()):
            if len(w) >= 2:
                toks.add(w)
    manifest.append({"num": num, "kind": kind, "page": pno, "file": name,
                      "caption": ctext, "w": img.width, "h": img.height,
                      "shard_tokens": sorted(toks)[:400]})

# 4) صور لم تُربط بتسمية (قد تكون أشكالًا بلا تسمية، أو نصوصًا مصوّرة)
leftover = []
for pno, lst in placements.items():
    for (x, r, w, h) in lst:
        if (x, r) not in used:
            leftover.append((pno, x, round(r.y0, 1), round(r.y1, 1)))

import json
with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=1)

print("extracted:", len(manifest))
print("unmatched captions:", len(unmatched))
for u in unmatched[:20]:
    print("   ", u)
print("leftover images:", len(leftover))
for l in leftover[:20]:
    print("   ", l)
tot = sum(os.path.getsize(os.path.join(OUT, m["file"])) for m in manifest)
print("total size: %.1f MB" % (tot / 1048576))
