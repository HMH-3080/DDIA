#!/usr/bin/env python3
"""Pack book-ar.md into assets/book.js so the reader works offline from file://"""
import json
import os

BASE = "/home/hmh/Videos/DDIA"
src = os.path.join(BASE, "book-ar.md")
dst = os.path.join(BASE, "assets", "book.js")

text = open(src, encoding="utf-8").read()

# split into 64k pieces to keep the generated file friendly to parsers
CH = 65536
pieces = [text[i:i + CH] for i in range(0, len(text), CH)] or [""]

out = ["/* DDIA — النسخة العربية (مولّدة آليًا). لا تعدّل يدويًا. */\n",
       "window.__BOOK__ = (\n"]
for i, p in enumerate(pieces):
    out.append("  " + json.dumps(p, ensure_ascii=False) + ("" if i == len(pieces) - 1 else " +\n"))
out.append(");\n")

open(dst, "w", encoding="utf-8").write("".join(out))
print("wrote", dst, os.path.getsize(dst), "bytes,", len(pieces), "pieces")
