#!/usr/bin/env python3
"""تأكيد أمثلة الشيفرة: كل قائمة شيفرة مُعلَّمة «Example N-M» في PDF
يجب أن ترد بنصّها في الكتاب العربي."""
import os
import re
import pymupdf

PDF = "/home/hmh/Downloads/Designing Data-Intensive Applications - Martin Kleppmann.pdf"
BASE = "/home/hmh/Videos/DDIA"
MONO = ("UbuntuMono", "Courier", "Typewriter", "NimbusMono")

doc = pymupdf.open(PDF)

# ---------- 1) تسميات Example في PDF ----------
example_at = {}     # page -> [(y, "Example N-M")]
for pno in range(doc.page_count):
    page = doc[pno]
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            txt = "".join(sp["text"] for sp in l["spans"]).strip()
            m = re.match(r"^Example\s+(\d+)-(\d+)", txt)
            if m:
                example_at.setdefault(pno, []).append((l["bbox"][1], m.group(0)))

# ---------- 2) قوائم الشيفرة في PDF ----------
listings = []
for pno in range(doc.page_count):
    page = doc[pno]
    ls = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            fonts = [s["font"] for s in l["spans"]]
            if any(any(m in f for m in MONO) for f in fonts):
                ls.append((round(l["bbox"][1], 1), round(l["bbox"][0], 1),
                           "".join(s["text"] for s in l["spans"]).rstrip()))
    ls.sort()
    groups, cur = [], []
    for y, x, t in ls:
        if cur and (y - cur[-1][0] > 16 or abs(x - cur[0][1]) > 40):
            groups.append(cur)
            cur = []
        cur.append((y, x, t))
    if cur:
        groups.append(cur)

    for g in groups:
        lines = [c[2] for c in g]
        if len(lines) < 2:
            continue
        # يجب أن تسبق القائمة تسمية Example (وإلا فهي شيفرة داخل نص)
        caps = [c for c in example_at.get(pno, []) if c[0] > g[-1][0]]
        prevs = [c for c in example_at.get(pno, []) if c[0] < g[0][0]]
        near = [c for c in caps + prevs if abs(c[0] - g[-1][0]) < 300 or abs(c[0] - g[0][0]) < 300]
        if not near:
            continue
        syms = sum(len(re.findall(r"[{}()\[\];=<>|&]|->|::", l)) for l in lines)
        if syms / len(lines) < 0.9:
            continue
        listings.append((pno, lines, near[0][1]))

# ---------- 3) نص الكتاب ----------
md = open(os.path.join(BASE, "book-ar.md"), encoding="utf-8").read()
page = 1
page_text = {}
for l in md.split("\n"):
    m = re.match(r"^<!--\s*page\s+(\d+)\s*-->$", l.strip())
    if m:
        page = int(m.group(1))
    page_text.setdefault(page, []).append(l)


def nz(s):
    return re.sub(r"\s+", "", s)


ok, bad = 0, []
for pno, lines, label in listings:
    reg = "\n".join(page_text.get(pno + 1, []))
    rn = nz(reg)
    codes = [nz(l) for l in lines if len(nz(l)) >= 6]
    found = sum(1 for c in codes if c in rn)
    ratio = found / max(1, len(codes))
    if ratio >= 0.8:
        ok += 1
    else:
        bad.append((pno + 1, label, round(ratio, 2), lines[0][:60]))

print("PDF code listings with 'Example N-M':", len(listings))
print("confirmed in the Arabic book:", ok)
print("need review:", len(bad))
for b in bad[:20]:
    print("   p%-4d %-14s %.2f  %s" % b)
