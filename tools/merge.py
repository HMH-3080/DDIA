#!/usr/bin/env python3
"""دمج مقاطع الترجمة في الكتاب النهائي.

مستويات العناوين تُستعاد من بنية الكتاب الأصلية: المصدر الإنجليزي والترجمة العربية
لهما بنية كتل متطابقة تمامًا (يتحقق منها tools/verify.py)، لذا العنوان رقم N في
الترجمة يقابل العنوان رقم N في المصدر.

أض��نًا: الأشكال (Figure N-M) تُستخرج صورًا أصلية من ملف PDF وتُدرج مكان
الشظايا المشوّهة التي تركها التحويل من PDF.
"""
import os
import re
import glob

BASE = "/home/hmh/Videos/DDIA"
CH = os.path.join(BASE, "chunks", "ar")
EN = os.path.join(BASE, "Designing Data-Intensive Applications - Martin Kleppmann.md")
FIGDIR = os.path.join(BASE, "assets", "figures")
OUT_MD = os.path.join(BASE, "book-ar.md")

# ---------------------------------------------------------------- levels
L1 = [
    12, 45, 109, 113, 121, 139, 166, 293,                       # front matter + parts
    340, 799, 1660, 2507, 3173, 3293, 4293, 4767, 5868, 6627,     # chapters
    7730, 7792, 8706, 9606,
    10911, 10980, 11009, 11042, 11056, 11085, 10997, 11115,       # index letters
    11162, 11166, 11246, 11266,
    11271, 11277,
]
L1 = [x for x in L1 if x != 10997] + [10997]

L2 = [
    196, 214, 227, 239, 243, 252, 272,               # front matter
    365, 421, 502, 676, 762, 781,                   # ch1
    825, 1124, 1236, 1572, 1599,                    # ch2
    1679, 2028, 2107, 2243, 2428, 2453,             # ch3
    2539, 2901, 2921, 3130, 3156,                   # ch4
    3263,                                           # part II references
    3316, 3347, 3391, 3407, 3443, 3509, 3675, 3889, 4196, 4257,   # ch5
    4318, 4340, 4426, 4515, 4618, 4684, 4692, 4722,               # ch6
    4797, 4808, 4901, 5011, 5242, 5330, 5469, 5793, 5847,         # ch7
    5887, 5946, 6121, 6276, 6348, 6563, 6593,                     # ch8
    6652, 6676, 6996, 7249, 7281, 7397, 7477, 7580, 7639, 7694,   # ch9
    7828, 7957, 8362, 8538, 8582,                                 # ch10
    8727, 8852, 8945, 8960, 9183, 9268, 9355, 9429, 9486, 9530,   # ch11
    9619, 9773, 9869, 9955, 10061, 10185, 10330, 10413, 10472,
    10585, 10609,                                                 # ch12
]

L3 = [
    407, 411, 415, 443, 460, 479, 494, 513, 577, 589, 625, 653,
    687, 691, 695, 701, 730, 749,                                # ch1
    842, 855, 931, 994, 1044, 1065, 1099, 1109, 1156, 1195, 1278,
    1320, 1368, 1427, 1466, 1480, 1505, 1516,                    # ch2
    1709, 1818, 1907, 1992, 2139, 2169, 2179, 2343, 2349, 2371, 2381,   # ch3
    2561, 2576, 2648, 2770, 2934, 2992, 3081,                   # ch4
    3385, 3413, 3447, 3464, 3480, 3499, 3528, 3572, 3607, 3662, 3683,
    3687, 3706, 3710, 3714, 3725, 3737, 3748, 3761, 3767, 3775, 3793,
    3808, 3831, 3897, 3930, 3939, 3949, 3983, 4008, 4021, 4045, 4053,
    4080, 4094, 4107, 4115, 4166, 4181,                         # ch5
    4353, 4370, 4396, 4411, 4436, 4494, 4532, 4536, 4546, 4578,
    4592, 4605,                                                  # ch6
    4818, 4833, 4853, 4872, 4881, 4962, 4977, 4991, 5030, 5039, 5059,
    5087, 5100, 5134, 5149, 5200, 5221, 5232, 5259, 5274, 5301, 5309,
    5374, 5403, 5407, 5431, 5436, 5440, 5444, 5459, 5491, 5505, 5543,
    5557, 5572, 5584, 5601, 5615, 5630, 5651, 5671, 5679, 5696, 5712,
    5746, 5780,                                                  # ch7
    5906, 5935, 5978, 5995, 6015, 6030, 6055, 6072, 6102, 6145, 6149,
    6157, 6170, 6192, 6202, 6240, 6255, 6316, 6337, 6360, 6375, 6408,
    6435, 6443, 6466, 6474, 6485, 6489, 6493, 6499, 6503, 6507, 6514,
    6520, 6524, 6528, 6534, 6550,                                # ch8
    6706, 6794, 6813, 6865, 6925, 6954, 6968, 6983, 7008, 7061, 7074,
    7163, 7257, 7287, 7310, 7345, 7365, 7388, 7405, 7409, 7415, 7428,
    7441, 7452, 7462, 7488, 7492, 7500, 7519, 7537, 7550, 7590, 7594,
    7599, 7603, 7609, 7622, 7630,                                # ch9
    7840, 7867, 7884, 7897, 7917, 7932, 7945, 7981, 8046, 8065, 8138,
    8180, 8229, 8276, 8291, 8302, 8319, 8336, 8374, 8396, 8449, 8497,
    8510, 8527,                                                  # ch10
    8748, 8769, 8785, 8793, 8807, 8811, 8816, 8832, 8865, 8893, 8907,
    8926, 8937, 8994, 9011, 9024, 9033, 9047, 9058, 9078, 9092, 9104,
    9127, 9140, 9155, 9168, 9202, 9213, 9224, 9239, 9247, 9256, 9283,
    9304, 9318, 9335, 9339, 9343, 9347, 9351, 9364, 9374, 9389, 9412,
    9438, 9448, 9459, 9471,                                      # ch11
    9631, 9642, 9655, 9670, 9681, 9701, 9714, 9727, 9733, 9746, 9762,
    9787, 9802, 9810, 9819, 9825, 9831, 9847, 9860, 9893, 9915, 9935,
    9976, 9993, 10006, 10016, 10031, 10050, 10080, 10088, 10099, 10105,
    10126, 10155, 10172, 10193, 10204, 10218, 10254, 10260, 10273, 10293,
    10314, 10345, 10358, 10368, 10377, 10387, 10398, 10425, 10434, 10447,
    10464, 10487, 10502, 10517, 10536, 10555, 10570,              # ch12
]

L4 = [
    305, 313,                                                     # garbled cover art
    519, 523,
    958, 962, 973, 1008, 1025, 1038, 1244, 1248, 1252, 1328, 1347,
    1349, 1452, 1471, 1486,
    1683, 1781, 1785, 1789, 1796, 1800, 1873, 1888, 1899, 1964, 1976,
    1999, 2013, 2039, 2052, 2071, 2081, 2194, 2204, 2206, 2215, 2265,
    2279, 2296, 2303, 2307, 2311, 2335,
    2527, 2531, 2555, 2593, 2618, 2697, 2748, 2761, 2789, 2838, 2855,
    2861, 2865, 2872, 2878, 2891, 2971, 2984, 3007, 3035, 3054, 3067,
    3100, 3113,
    3183, 3187, 3191, 3200, 3210, 3223, 3227, 3231,
    3611, 3624, 3628, 3797, 3801, 3943,
    4445, 4472, 4474,
    4905, 4909, 4915, 4928, 5130, 5588, 5723, 5803, 5807, 5811, 5816,
    5820, 5824, 5830, 5834, 5838,
    6798, 6802, 6817, 6825, 6838, 6876, 6882, 6886, 6890, 6899, 7026,
    7034, 7038, 7049, 7089, 7108, 7142, 7175, 7179, 7188, 7205, 7230,
    7264, 7268, 7323, 7486, 7650, 7654, 7658, 7662, 7666, 7670,
    7739, 7743, 7747, 7760, 7804, 7809, 7813,
    7994, 7999, 8005, 8076, 8101, 8105, 8146, 8163, 8191, 8203, 8214,
    8220, 8237, 8252, 8425, 8440, 8468, 8478, 8487, 8546, 8552, 8559,
    8563, 8567, 8607,
    9117, 9294, 9492, 9497, 9513, 9520, 9524,
    9573,
    10993, 11024, 11111, 11135, 11217, 11221, 11250, 11258,
] + list(range(10637, 10911))

LEVELS = {}
for i in L1:
    LEVELS[i] = 1
for i in L2:
    LEVELS.setdefault(i, 2)
for i in L3:
    LEVELS.setdefault(i, 3)
for i in L4:
    LEVELS.setdefault(i, 4)

# أرقام أسطر العناوين في المصدر الإنجليزي: الفصول والأجزاء
EN_CHAPTERS = [340, 799, 1660, 2507, 3293, 4293, 4767, 5868, 6627, 7792, 8706, 9606]
EN_PARTS = [113, 121, 139, 3173, 7730]

# ---------------------------------------------------------------- helpers
FIGSPECIAL = ("FIGTXT|", "RUNFOOT|", "FIGCAP|", "FIGIMG|", "EPIATTR|")
FIGAR = re.compile("[؀-ۿ]")
FIGLA = re.compile("[A-Za-z]")


FIGWORD = re.compile(r"[A-Za-z]+")


def is_fig_shard(t):
    """هل هذا السطر شظيّة نصّ مشوّهة ناتجة عن رسم في PDF؟"""
    if t.startswith(("#", "•", "<")) or re.match(r"^\d+\.\s", t):
        return False
    if t.startswith(FIGSPECIAL):
        return False
    if len(t) > 130:
        return False
    ar = len(FIGAR.findall(t))
    if ar == 0:
        return True                      # بلا عربي: تسمية شكل، كود، أو تسلسل hex
    if t[0] in "=|+*~«»()[]{}\u201c\u201d'\"":
        return True                      # أسطر تبدأ برموز (شظايا رسم)
    if re.match(r"^[A-Za-z]{1,2}\s*=", t):
        return True                      # تسمية متغيّر: w = ... / n = ...
    if ar / float(len(t)) < 0.35:
        return True                      # نصّ مشوّهة مختلط
    if len(t) < 45 and t[-1] not in ".؟!":
        return True                      # شظايا قصيرة (لا تنتهي بجملة)
    return False


def is_prose_line(line):
    t = line.strip()
    if not t or t.startswith(("<", "#", "|", "\u2022", "FIG", "LBL4", "RUNFOOT",
                              "EPIATTR", "COVER", "PART", "CHAPTER")):
        return False
    if re.match(r"^\d+\.\s", t):
        return False
    return len(t) > 90 and len(re.findall(r"[\u0600-\u06FF]", t)) > 40


def build_en_levels():
    lines = open(EN, encoding="utf-8").read().split("\n")
    lv = []
    ordinal = {}
    o = 0
    for idx, l in enumerate(lines):
        if l.strip().startswith("#") and l.strip().strip("# ").strip():
            lv.append(LEVELS.get(idx, 4))
            ordinal[idx] = o
            o += 1
    return lv, ordinal


def build_ar_lines():
    parts = []
    for p in sorted(glob.glob(os.path.join(CH, "chunk_*.md"))):
        parts.append(open(p, encoding="utf-8").read())
    return "\n".join(parts).split("\n")


en_levels, en_ord = build_en_levels()
ar_lines = build_ar_lines()
ar_head_lines = [i for i, l in enumerate(ar_lines)
                 if l.strip().startswith("#") and l.strip().strip("# ").strip()]

if len(ar_head_lines) != len(en_levels):
    raise SystemExit("heading count mismatch: EN=%d AR=%d" % (len(en_levels), len(ar_head_lines)))

level_by_line = {ln: en_levels[o] for o, ln in enumerate(ar_head_lines)}
ord_of = {ln: o for o, ln in enumerate(ar_head_lines)}
CHAPTER_ORD = set(en_ord[i] for i in EN_CHAPTERS if i in en_ord)
PART_ORD = set(en_ord[i] for i in EN_PARTS if i in en_ord)
CH_NUM = {}
for _n, _i in enumerate(EN_CHAPTERS, 1):
    if _i in en_ord:
        CH_NUM[en_ord[_i]] = _n

# ---------------------------------------------------------------- walk
RUNFOOT = re.compile(r"^\d+\s*\|\s")
FIGCAP = re.compile(r"^(الشكل|Figure|شكل)\s*[\d–\-]+")
EPI_ATTR = re.compile(r"^—\s*\S")
FIGNUM = re.compile(r"^الشكل\s+([\d–\-]+)")

out = []
stats = {}
prev_nonempty = ""
i = 0
n = len(ar_lines)
figs_used = 0
skip_title = None



# غلاف الكتاب: نُنظّفه من شوائب OCR ونحوّله إلى كتلة غلاف منسّقة
if len(out) == 0 and n > 10:
    head = [l.strip() for l in ar_lines[:12]]
    if head[:1] == ["<!-- page 1 -->"] and "O'REI" in head:
        title = subtitle = author = ""
        for l in ar_lines[:14]:
            s2 = l.strip()
            if s2 in ("O'REI", "ILLY", "L", "L "):
                continue
            if not s2 or s2.startswith("<!--"):
                continue
            if not title and ("تصميم" in s2 or "تطبيقات" in s2):
                title = s2.lstrip("L ").strip()
            elif not subtitle and ("الأفكار" in s2 or "الأنظمة" in s2):
                subtitle = s2
            elif not author and re.match(r"^[A-Z][A-Za-z.'\- ]+$", s2):
                author = s2
        if title:
            out.append("COVER|" + title)
            if subtitle:
                out.append("COVER|" + subtitle)
            if author:
                out.append("COVER|" + author)
            skip_title = title
            # تخطّي الأسطر القديمة للغلاف
            k = 0
            while k < len(ar_lines) and k < 16:
                t2 = ar_lines[k].strip()
                if t2.startswith("<!-- page 2 -->"):
                    k += 1
                    break
                k += 1
            i = k

_cur_page = [1]

# خريطة: رقم صفحة PDF -> رقم صفحة الكتاب (من tools/page_map.py)
try:
    import json
    page_book = {int(k): v for k, v in
                  json.load(open(os.path.join(BASE, "assets", "page_map.json"),
                                encoding="utf-8")).items()}
except Exception:
    page_book = {}

# خريطة صفحات الأشكال الكاملة (من tools/fix_figures.py)
try:
    import json
    _figmap = {int(k): v for k, v in
               json.load(open(os.path.join(BASE, "assets", "figure_pages.json"),
                             encoding="utf-8")).items()}
except Exception:
    _figmap = {}

while i < n:
    s = ar_lines[i].strip()

    if not s:
        out.append("")
        i += 1
        continue

    if s.startswith("<!--"):
        _pm = re.match(r"^<!--\s*page\s+(\d+)\s*-->$", s)
        if _pm:
            _cur_page[0] = int(_pm.group(1))
        out.append(s)
        i += 1
        continue

    if s.startswith("<table>"):
        # صفحة شكل كامل: نستبدل الصفحة كلها بالصورة الأصلية
        if _cur_page[0] in _figmap:
            _j = i
            while _j < n and not ar_lines[_j].strip().endswith("</table>"):
                _j += 1
            _k = _j + 1
            if not any(is_prose_line(x) for x in ar_lines[i:_k]):
                out.extend(["FIGIMG|" + _figmap[_cur_page[0]]["file"]])
                i = _k
                continue
        while i < n:
            out.append(ar_lines[i])
            if ar_lines[i].strip().endswith("</table>"):
                break
            i += 1
        i += 1
        continue

    if s.startswith("#"):
        title = re.sub(r"^#+\s*", "", s).strip()
        if skip_title and title.strip() == skip_title.strip():
            skip_title = None
            i += 1
            continue
        lvl = level_by_line.get(i, 4)
        marker = ""
        if lvl == 1:
            title = re.sub(r"^(الفصل\s+\d+)\s*[-—:.]?\s*", "", title)
            o = ord_of.get(i)
            if o in CHAPTER_ORD:
                marker = "CHAPTER%d|" % CH_NUM.get(o, 0)
            elif o in PART_ORD:
                marker = "PART|"
        if lvl == 4:
            out.append("LBL4|" + title)
        else:
            out.append(marker + "#" * lvl + " " + title)
        # صفحة الفهرس التقليدية: نستبدلها بصفحة فهرس تفاعلية
        if title.strip() == "جدول المحتويات" and lvl == 1:
            _k = i + 1
            while _k < n:
                _t = ar_lines[_k].strip()
                if _t.startswith("#") and re.search(r"مقدمة|Preface", _t):
                    break
                _k += 1
            out.append("TOCPAGE|")
            i = _k
            continue
        if lvl <= 2 and _cur_page[0] in page_book:
            out.append("PAGENO|" + str(page_book[_cur_page[0]]))
        stats[lvl] = stats.get(lvl, 0) + 1
        prev_nonempty = s
        i += 1
        continue

    if RUNFOOT.match(s):
        out.append("RUNFOOT|" + s)
        i += 1
        continue

    if FIGCAP.match(s):
        mc = FIGNUM.match(s)
        if mc:
            num = mc.group(1).replace("–", "-")
            if os.path.exists(os.path.join(FIGDIR, "fig-%s.png" % num)):
                # احذف شظايا الشكل المشوّهة السابقة
                j = len(out) - 1
                while j >= 0:
                    t = out[j].strip()
                    if not t:
                        del out[j]
                        j -= 1
                        continue
                    if t.endswith("</table>"):
                        k = j
                        while k >= 0 and not out[k].strip().startswith("<table>"):
                            k -= 1
                        if k < 0:
                            break
                        del out[k:j + 1]
                        j = k - 1
                        continue
                    if t.startswith("LBL4|") and len(t) < 60:
                        del out[j]
                        j -= 1
                        continue
                    if is_fig_shard(t):
                        del out[j]
                        j -= 1
                        continue
                    break
                out.append("FIGIMG|fig-%s.png" % num)
                figs_used += 1
        out.append("FIGCAP|" + s)
        i += 1
        continue

    if s.startswith("FIGTXT|"):
        out.append("FIGTXT|" + s[7:])
        i += 1
        continue

    if s.startswith("EPIATTR|"):
        out.append("EPIATTR|" + s[8:])
        i += 1
        continue

    out.append(s)
    prev_nonempty = s
    i += 1

final = re.sub(r"\n{3,}", "\n\n", "\n".join(out))
open(OUT_MD, "w", encoding="utf-8").write(final)
print("levels:", dict(sorted(stats.items())), "| figures embedded:", figs_used)
print("bytes:", len(final.encode("utf-8")))
