#!/usr/bin/env python3
"""تصحيح الفقرات التي بقيت بالإنجليزية أو تلفت، بالرجوع إلى نصّ PDF الأصلي."""
import os
import re

CH = "/home/hmh/Videos/DDIA/chunks/ar"

# (ملف, رقم السطر 1-based, نوع الإجراء, النص البديل)
FIXES = [
    # شظايا إنجليزية مكرّرة (ترجمتها موجودة في ما سبقها)
    ("chunk_0023.md", 26, "delete", None),
    ("chunk_0023.md", 27, "delete", None),
    ("chunk_0023.md", 28, "delete", None),
    ("chunk_0089.md", 41, "delete", None),
    ("chunk_0108.md", 35, "delete", None),
    ("chunk_0108.md", 36, "delete", None),
    ("chunk_0108.md", 37, "delete", None),
    # نصّ تالف (نتيجة OCR/ترجمة)
    ("chunk_0070.md", 22, "replace",
     "ولأنّ دمج siblings في كود التطبيق معقّد ومعرّض للخطأ، فإنّ هناك محاولات لتصميم بنى "
     "بيانات قادرة على إجراء هذا الدمج تلقائيًا، كما ناقشنا في «الحلّ التلقائي لتعارضات "
     "الكتابة» في صفحة 174. فمثلًا، يدعم Riak أنواع بياناته عبر عائلة من بنى البيانات "
     "تُدعى CRDTs [38, 39, 55]، وهي قادرة على دمج siblings تلقائيًا بطرق معقولة، "
     "بما في ذلك الحفاظ على عمليات الحذف."),
    # شرح لم يُترجَم
    ("chunk_0144.md", 52, "replace",
     "‏counts هو جدول تجزئة (hash table) يحتفظ بعدّاد لعدد المرات التي رأينا فيها كل "
     "عنوان URL. ويكون العدّاد صفرًا افتراضيًا."),
]


def main():
    byfile = {}
    for f, ln, action, text in FIXES:
        byfile.setdefault(f, []).append((ln, action, text))

    for f, items in byfile.items():
        path = os.path.join(CH, f)
        lines = open(path, encoding="utf-8").read().split("\n")
        for ln, action, text in sorted(items, reverse=True):
            idx = ln - 1
            if action == "delete":
                # احذف السطر و(إن كان فارغًا) السطر الذي يليه
                del lines[idx]
                if idx < len(lines) and not lines[idx].strip():
                    del lines[idx]
            else:
                lines[idx] = text
        open(path, "w", encoding="utf-8").write("\n".join(lines))
        print("patched %s (%d)" % (f, len(items)))


if __name__ == "__main__":
    main()
