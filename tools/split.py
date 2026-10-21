#!/usr/bin/env python3
"""Split the DDIA markdown into translation chunks (structure-preserving)."""
import os
import re
import sys
import json

SRC = "/home/hmh/Videos/DDIA/Designing Data-Intensive Applications - Martin Kleppmann.md"
OUT = "/home/hmh/Videos/DDIA/chunks"
TARGET_WORDS = int(os.environ.get("TARGET_WORDS", "1100"))
MAX_WORDS = int(os.environ.get("MAX_WORDS", "1600"))

PAGE_RE = re.compile(r"^<!--\s*page\s+\d+\s*-->$")


def blocks(text):
    """Split markdown into atomic blocks: (kind, text)."""
    lines = text.split("\n")
    out = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        if PAGE_RE.match(s):
            out.append(("page", s))
            i += 1
            continue
        if s.startswith("<table>"):
            buf = []
            while i < n:
                buf.append(lines[i])
                if lines[i].strip().endswith("</table>"):
                    i += 1
                    break
                i += 1
            out.append(("table", "\n".join(buf)))
            continue
        if s.startswith("#"):
            out.append(("heading", line))
            i += 1
            continue
        if s.startswith("•"):
            buf = []
            while i < n and lines[i].strip().startswith("•"):
                buf.append(lines[i])
                i += 1
            out.append(("bullets", "\n".join(buf)))
            continue
        if re.match(r"^\d+\.\s", s):
            buf = []
            while i < n and re.match(r"^\d+\.\s", lines[i].strip()):
                buf.append(lines[i])
                i += 1
            out.append(("ordered", "\n".join(buf)))
            continue
        # paragraph: gather until blank line / structural marker
        buf = []
        while i < n:
            cur = lines[i]
            cs = cur.strip()
            if not cs:
                break
            if PAGE_RE.match(cs) or cs.startswith("<table>") or cs.startswith("#") \
               or cs.startswith("•") or re.match(r"^\d+\.\s", cs):
                break
            buf.append(cur)
            i += 1
        out.append(("para", "\n".join(buf)))
    return out


def words(t):
    return len(t.split())


def main():
    text = open(SRC, encoding="utf-8").read()
    bl = blocks(text)
    os.makedirs(OUT, exist_ok=True)
    chunks = []
    cur = []
    cur_w = 0
    for kind, b in bl:
        bw = words(b)
        if cur and (cur_w + bw > TARGET_WORDS or cur_w >= MAX_WORDS):
            chunks.append(cur)
            cur = []
            cur_w = 0
        cur.append((kind, b))
        cur_w += bw
    if cur:
        chunks.append(cur)

    manifest = []
    for idx, ch in enumerate(chunks, 1):
        cid = "chunk_%04d" % idx
        path = os.path.join(OUT, cid + ".md")
        with open(path, "w", encoding="utf-8") as f:
            for kind, b in ch:
                if kind == "page":
                    f.write(b + "\n\n")
                else:
                    f.write(b + "\n\n")
        manifest.append({
            "id": cid,
            "file": cid + ".md",
            "words": sum(words(b) for _, b in ch),
            "blocks": len(ch),
            "kinds": [k for k, _ in ch],
        })

    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)

    total = sum(m["words"] for m in manifest)
    print("chunks: %d  words: %d" % (len(manifest), total))
    print("min/median/max words:", min(m["words"] for m in manifest),
          sorted(m["words"] for m in manifest)[len(manifest)//2],
          max(m["words"] for m in manifest))


if __name__ == "__main__":
    main()
