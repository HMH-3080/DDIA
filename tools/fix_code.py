#!/usr/bin/env python3
"""إصلاح أمثلة الكود العربية بنصّها الإنجليزي الأصلي من ملف PDF.

المبدأ: الخط أحادي المسافة (UbuntuMono) في PDF هو المرجع الرسمي.
نأخذ أسطر الشيفرة من PDF مرتّبة، ونأخذ أسطر الشيفرة من Markdown مرتّبة،
ثم نُحاذي السلسلتين (SequenceMatcher). ما يطابق يُستبدل بنصّ PDF الأصلي،
وما لا يطابق (تعليق مُترجَم مثلًا) يُملأ من أسطر PDF غير المطابقة بالترتيب.
"""
import os
import re
import glob
import difflib
import pymupdf

PDF = "/home/hmh/Downloads/Designing Data-Intensive Applications - Martin Kleppmann.pdf"
BASE = "/home/hmh/Videos/DDIA"
CH = os.path.join(BASE, "chunks", "ar")
MONO = ("UbuntuMono", "Courier", "Typewriter", "NimbusMono")
FIGAR = re.compile("[؀-ۿ]")

doc = pymupdf.open(PDF)

# ---------- 1) أسطر الشيفرة من PDF لكل صفحة ----------
pdf_lines = {}       # page(0-based) -> [(y, x, text)]
pdf_groups = {}      # page(0-based) -> [(i, j), ...] مجموعات أسطر متجاورة
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
    pdf_lines[pno] = ls
    groups = []
    i = 0
    while i < len(ls):
        j = i
        while j + 1 < len(ls) and (ls[j + 1][0] - ls[j][0] <= 16) and abs(ls[j + 1][1] - ls[i][1]) <= 40:
            j += 1
        groups.append((i, j))
        i = j + 1
    pdf_groups[pno] = groups

# ---------- 2) خرائط الصفحات في Markdown ----------
files = sorted(glob.glob(os.path.join(CH, "chunk_*.md")))
contents = [open(p, encoding="utf-8").read() for p in files]
page_index = []      # (file_idx, line_idx, page1)
page = 1
for fi, txt in enumerate(contents):
    for li, l in enumerate(txt.split("\n")):
        m = re.match(r"^<!--\s*page\s+(\d+)\s*-->$", l.strip())
        if m:
            page = int(m.group(1))
        page_index.append((fi, li, page))

CODEISH = re.compile(r"(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|WITH\b|function|var\s|let\s|const\s|def\s|class\s|for\s*\(|while\s*\(|if\s*\(|return|--|//|#\{|=>|::|\{|\}|\$|\|\||&&|==|!=|>=|<=|\w+\s*=\s*[^=])")


def is_code_line(s):
    if not s or s.startswith(("<", "|", ">", "[", "(")):
        return False
    if "http" in s:
        return False
    ar = len(FIGAR.findall(s))
    la = len(re.findall(r"[A-Za-z]", s))
    if ar == 0:
        return False
    is_comment = re.match(r"^(--|//|#\s|\*\s|/\*)", s) is not None
    if la < 16 and not is_comment:
        return False
    if not (is_comment or CODEISH.search(s)):
        return False
    if ar / float(len(s)) > 0.30 and not is_comment:
        return False
    if len(re.findall(r"[^\w\s؀-ۿ]", s)) < 2 and not is_comment:
        return False
    return True


def nz(s):
    return re.sub(r"\s+", "", s)


def key(s):
    """مفتاح مقارنة متسامح: يهمّ الحروف والأرقام والرموز الأساسية."""
    s = s.lower()
    s = re.sub(r"//.*", "", s)
    s = re.sub(r"--.*", "", s)
    s = re.sub(r"[^a-z0-9_{}()\[\];:,.<>=!+*/&|%$#@\"'\- ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


# ---------- 2b) جداول هي في الحقيقة قوائم شيفرة → استبدلها بشيفرة PDF ----------
TABLE_RE = re.compile(r"^<table>(?:.*?)</table>$", re.S)
CODEWORDS = re.compile(r"\b(AS|SELECT|JOIN|FROM|WHERE|UNION|VALUES|INSERT|UPDATE|DELETE|CREATE|PRIMARY\s+KEY|AND|OR)\b")

table_fix = {}
for fi, txt in enumerate(contents):
    lines = txt.split("\n")
    i = 0
    while i < len(lines):
        if lines[i].strip() == "<table>":
            j = i
            while j < len(lines) and lines[j].strip() != "</table>":
                j += 1
            block = "\n".join(lines[i:j + 1])
            cells = " ".join(re.findall(r"<td[^>]*>(.*?)</td>", block, re.S))
            if CODEWORDS.search(cells) and re.search(r"[;()=<>]", cells):
                # صفحة الـPDF لهذه الخانة
                pg = 1
                for l2 in lines[:i]:
                    m2 = re.match(r"^<!--\s*page\s+(\d+)\s*-->$", l2.strip())
                    if m2:
                        pg = int(m2.group(1))
                # ابحث عن قائمة PDFZyklon Hilda孤儿 في الصفحة نفسها
                pl = pdf_lines.get(pg - 1, [])
                cand = []
                for k in range(len(pl)):
                    grp = [pl[k][2]]
                    for k2 in range(k + 1, len(pl)):
                        if pl[k2][0] - pl[k2 - 1][0] <= 16 and abs(pl[k2][1] - pl[k][1]) <= 40:
                            grp.append(pl[k2][2])
                        else:
                            break
                    if len(grp) >= 3:
                        cand.append(grp)
                if cand:
                    best = max(cand, key=lambda g: sum(len(x) for x in g))
                    table_fix[(fi, i, j)] = best
            i = j + 1
        else:
            i += 1

# ---------- 3) لكل صفحة: محاذاة سلسلتين ----------
patches = {}         # (fi, li) -> [new lines]
report = []

by_page = {}
for fi, li, page in page_index:
    by_page.setdefault(page, []).append((fi, li))

for page1, entries in sorted(by_page.items()):
    pl = pdf_lines.get(page1 - 1, [])
    if not pl:
        continue
    # أسطر الـMarkdown المرشّحة للشيفرة (مرتّبة)
    cand = []
    for fi, li in entries:
        s = contents[fi].split("\n")[li].strip()
        if is_code_line(s):
            cand.append((fi, li, s))
    if not cand:
        continue
    pkeys = [key(t) for _, _, t in pl]
    mkeys = [key(s) for _, _, s in cand]
    sm = difflib.SequenceMatcher(None, mkeys, pkeys, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            # أسطر متطابقة بنيويًا: إن كان نصّ Markdown مُترجَمًا
            # (تعليق عربي) نستبدله بنصّ PDF الأصلي الإنجليزي
            groups = pdf_groups.get(page1 - 1, [])
            for k in range(i2 - i1):
                fi, li, mtext = cand[i1 + k]
                ptext = pl[j1 + k][2]
                if FIGAR.search(mtext) and re.search(r"[A-Za-z]", ptext):
                    # استبدل بقائمة PDF كاملة المحيطة بهذا السطر
                    gi = j1 + k
                    span = [t for (a, b) in groups if a <= gi <= b for t in [pl[x][2] for x in range(a, b + 1)]]
                    if not span:
                        span = [ptext]
                    patches[(fi, li)] = span
                    report.append(("untrans", fi, li, span[0]))
            continue
        mseg = cand[i1:i2]
        pseg = [t for _, _, t in pl[j1:j2]]
        if not pseg:
            continue
        if tag == "insert":
            # أسطر PDF زائدة: تُدرج قبل سطر Markdown التالي
            if mseg:
                fi, li, _ = mseg[0]
                patches.setdefault((fi, li), []).extend(pseg)
            continue
        # replace: استبدل مقطع Markdown بمقطع PDF
        if len(mseg) == len(pseg):
            for (fi, li, _), nl in zip(mseg, pseg):
                patches[(fi, li)] = [nl]
                report.append(("one2one", fi, li, nl))
        else:
            fi, li, _ = mseg[0]
            patches[(fi, li)] = pseg
            report.append(("block", fi, li, pseg[0]))
            for extra in mseg[1:]:
                patches[(extra[0], extra[1])] = []      # احذفها
                report.append(("drop", extra[0], extra[1], ""))

# ---------- 4) التطبيق ----------
if os.environ.get("APPLY") == "1":
    byfile = {}
    for (fi, li), lines in patches.items():
        byfile.setdefault(fi, []).append((li, li, lines))
    for (fi, a, b), lines in table_fix.items():
        byfile.setdefault(fi, []).append((a, b, lines))
    for fi, items in byfile.items():
        src = contents[fi].split("\n")
        for a, b, lines in sorted(items, reverse=True, key=lambda t: t[0]):
            if b > a:                      # استبدال كتلة جدول
                src[a:b + 1] = lines
                print("  table->code in %s:%d" % (files[fi].split("/")[-1], a + 1))
                continue
            if not lines:                 # حذف سطر
                del src[a]
                continue
            joined = nz(" ".join(lines))
            j = a + 1
            while j < len(src):
                t = src[j].strip()
                if not t:
                    j += 1
                    continue
                nt = nz(t)
                if nt and len(nt) > 3 and nt in joined:
                    del src[j]
                    continue
                break
            src[a:a + 1] = lines
        open(files[fi], "w", encoding="utf-8").write("\n".join(src))
    print("patched", len(patches), "positions in", len(byfile), "files")

print("changes:", len(report))
for r in report[:40]:
    print("  %-7s %s:%s  %s" % (r[0], files[r[1]].split("/")[-1], r[2] + 1, str(r[3])[:95]))
