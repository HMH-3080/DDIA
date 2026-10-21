#!/usr/bin/env python3
"""Verify translated chunks against source: structure parity."""
import os
import re
import json
import sys

BASE = "/home/hmh/Videos/DDIA/chunks"
AR = os.path.join(BASE, "ar")
man = json.load(open(os.path.join(BASE, "manifest.json"), encoding="utf-8"))

PAGE_RE = re.compile(r"^<!--\s*page\s+\d+\s*-->$")


def sig(path):
    """Structural signature: sequence of block kinds."""
    if not os.path.exists(path):
        return None
    txt = open(path, encoding="utf-8").read()
    s = []
    lines = txt.split("\n")
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        st = line.strip()
        if not st:
            i += 1
            continue
        if PAGE_RE.match(st):
            s.append("page")
            i += 1
            continue
        if st.startswith("<table>"):
            rows = 0
            while i < n:
                if lines[i].strip().startswith("<tr>"):
                    rows += 1
                if lines[i].strip().endswith("</table>"):
                    i += 1
                    break
                i += 1
            s.append("table:%d" % rows)
            continue
        if st.startswith("#"):
            s.append("h")
            i += 1
            continue
        if st.startswith("•"):
            c = 0
            while i < n and lines[i].strip().startswith("•"):
                c += 1
                i += 1
            s.append("b:%d" % c)
            continue
        if re.match(r"^\d+\.\s", st):
            c = 0
            while i < n and re.match(r"^\d+\.\s", lines[i].strip()):
                c += 1
                i += 1
            s.append("o:%d" % c)
            continue
        c = 0
        while i < n:
            cs = lines[i].strip()
            if not cs or PAGE_RE.match(cs) or cs.startswith("<table>") or cs.startswith("#") \
               or cs.startswith("•") or re.match(r"^\d+\.\s", cs):
                break
            c += 1
            i += 1
        s.append("p:%d" % c)
    return s


# مقاطع أُصلحت شيفرتها من نصّ PDF الأصلي (comments أُعيدت إلى الإنجليزية
# وشُرِّيت الأسطر كما في الكتاب) — فبنية الكتل فيها تختلف عن PDF→MD عمدًا.
CODE_RESTORED = {"chunk_0018", "chunk_0022", "chunk_0023", "chunk_0089",
                 "chunk_0090", "chunk_0108", "chunk_0144"}


def main():
    missing, mismatch, ok, restored = [], [], 0, []
    for m in man:
        src = sig(os.path.join(BASE, m["file"]))
        dst = sig(os.path.join(AR, m["file"]))
        if dst is None:
            missing.append(m["id"])
        elif src != dst:
            if m["id"] in CODE_RESTORED:
                ok += 1
                restored.append(m["id"])
            else:
                mismatch.append((m["id"], src, dst))
        else:
            ok += 1
    print("total=%d  ok=%d  missing=%d  mismatch=%d" % (len(man), ok, len(missing), len(mismatch)))
    if restored:
        print("  (code restored from PDF in: %s)" % ", ".join(restored))
    if missing:
        print("MISSING:", " ".join(missing))
    for mid, s, d in mismatch:
        print("\nMISMATCH", mid)
        for a, b in zip(s, d):
            if a != b:
                print("   src=%-12s ar=%-12s" % (a, b))
        if len(s) != len(d):
            print("   length differs: src=%d ar=%d" % (len(s), len(d)))
    return 0 if not missing and not mismatch else 1


if __name__ == "__main__":
    sys.exit(main())
