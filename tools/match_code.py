#!/usr/bin/env python3
"""مطابقة مقاطع الكود في PDF مع مواضعها في Markdown المُترجَم."""
import os
import re
import json
import glob
import pymupdf

PDF = "/home/hmh/Downloads/Designing Data-Intensive Applications - Martin Kleppmann.pdf"
BASE = "/home/hmh/Videos/DDIA"
MONO = ("UbuntuMono", "Courier", "Typewriter", "NimbusMono", "DejaVuSansMono")

doc = pymupdf.open(PDF)

# ---------- 1) مقاطع الكود من PDF ----------
blocks = []   # dict(page, lines=[...], y0, y1)
for pno in range(doc.page_count):
    page = doc[pno]
    lines = []
    for b in page.get_text("dict")["blocks"]:
        if b["type"] != 0:
            continue
        for l in b["lines"]:
            fonts = [s["font"] for s in l["spans"]]
            txt = "".join(s["text"] for s in l["spans"])
            if any(any(m in f for m in MONO) for f in fonts):
                lines.append((l["bbox"][1], txt.rstrip()))
    lines.sort()
    cur = []
    for y, t in lines:
        if cur and (y - cur[-1][0] > 18 or abs(l2x := 0) == 99):
            if cur:
                blocks.append({"page": pno, "lines": [x[1] for x in cur], "y0": cur[0][0], "y1": cur[-1][0]})
            cur = []
        cur.append((y, t))
    if cur:
        blocks.append({"page": pno, "lines": [x[1] for x in cur], "y0": cur[0][0], "y1": cur[-1][0]})

# ---------- 2) مناطق الصفحات في Markdown ----------
md_files = sorted(glob.glob(os.path.join(BASE, "chunks", "ar", "chunk_*.md")))
md_text = "\n".join(open(p, encoding="utf-8").read() for p in md_files)
md_lines = md_text.split("\n")
page_ranges = {}
cur_page = None
start = 0
for i, l in enumerate(md_lines):
    m = re.match(r"^<!--\s*page\s+(\d+)\s*-->$", l.strip())
    if m:
        if cur_page is not None:
            page_ranges.setdefault(cur_page, []).append((start, i))
        cur_page = int(m.group(1))
        start = i + 1
if cur_page is not None:
    page_ranges.setdefault(cur_page, []).append((start, len(md_lines)))


def region(pno):
    """أسطر الـMarkdown الموافقة لصفحة PDF (1-indexed)."""
    out = []
    for a, b in page_ranges.get(pno + 1, []):
        out.extend(md_lines[a:b])
    return out


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


# ---------- 3) مطابقة ----------
stats = {"exact": 0, "partial": 0, "none": 0}
results = []
for blk in blocks:
    reg = region(blk["page"])
    plines = [l for l in blk["lines"] if norm(l)]
    if not plines:
        continue
    key = max(plines, key=len)
    nk = norm(key)
    hit = None
    for i, l in enumerate(reg):
        if nk and nk in norm(l):
            hit = i
            break
    if hit is not None:
        stats["exact"] += 1
        results.append({"page": blk["page"], "status": "exact", "key": nk[:90],
                        "pdf_lines": len(plines)})
    else:
        # مطابقة جزئية: أكثر من نصف سطور الكود موجودة
        found = sum(1 for l in plines if len(norm(l)) > 6 and any(norm(l) in norm(r) for r in reg))
        ratio = found / len(plines)
        stats["partial" if ratio >= 0.5 else "none"] += 1
        results.append({"page": blk["page"], "status": "partial" if ratio >= 0.5 else "none",
                        "key": nk[:90], "pdf_lines": len(plines), "ratio": round(ratio, 2)})

print("code blocks in PDF:", len(blocks))
print("match:", stats)
json.dump(results, open("/tmp/opencode/code_match.json", "w"), ensure_ascii=False, indent=1)
for r in results[:12]:
    print("  p%-4d %-8s %s" % (r["page"] + 1, r["status"], r["key"]))
miss = [r for r in results if r["status"] == "none"]
print("\nunmatched:", len(miss))
for r in miss[:12]:
    print("  p%-4d %s" % (r["page"] + 1, r["key"]))
