#!/usr/bin/env python3
"""خريطة: رقم صفحة PDF -> رقم صفحة الكتاب (من تذييل الصفحة)."""
import json
import os
import re
import pymupdf

PDF = "/home/hmh/Downloads/Designing Data-Intensive Applications - Martin Kleppmann.pdf"
OUT = "/home/hmh/Videos/DDIA/assets/page_map.json"

doc = pymupdf.open(PDF)
m = {}
for pno in range(doc.page_count):
    page = doc[pno]
    best = None
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            if l["bbox"][1] < page.rect.height - 60:
                continue
            txt = "".join(s["text"] for s in l["spans"]).strip()
            nums = re.findall(r"\d{1,3}", txt)
            if nums:
                v = int(nums[-1])
                if best is None or v > best:
                    best = v
    if best is not None:
        m[pno + 1] = best

# ملء الفجوات (صفحات الأشكال التي لا تذييل لها) بالاستيفاء
keys = sorted(m)
for a, b in zip(keys, keys[1:]):
    if b - a <= 1:
        continue
    va, vb = m[a], m[b]
    for k in range(a + 1, b):
        m[k] = round(va + (vb - va) * (k - a) / float(b - a))
# الصفحات قبل أول تذييل
if keys and keys[0] > 1:
    for k in range(1, keys[0]):
        m[k] = m[keys[0]] - (keys[0] - k)
for k in range(keys[-1] + 1, doc.page_count + 1):
    m[k] = m[keys[-1]] + (k - keys[-1])

json.dump(m, open(OUT, "w"), indent=0)
print("pages mapped:", len(m), "of", doc.page_count)
print("sample:", dict(list(sorted(m.items()))[:8]))
