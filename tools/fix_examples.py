#!/usr/bin/env python3
"""استعادة مثالَين من الشيفرة نُقلا إلى جداول في التحويل من PDF."""
import os

CH = "/home/hmh/Videos/DDIA/chunks/ar"

CYPHER = """CREATE
  (NAmerica:Location {name:'North America', type:'continent'}),
  (USA:Location      {name:'United States', type:'country'  }),
  (Idaho:Location    {name:'Idaho',         type:'state'    }),
  (Lucy:Person       {name:'Lucy' }),
  (Idaho) -[:WITHIN]->  (USA)  -[:WITHIN]-> (NAmerica),
  (Lucy)  -[:BORN_IN]-> (Idaho)""".split("\n")

SQL = """WITH RECURSIVE
  -- in_usa is the set of vertex IDs of all locations within the United States
  in_usa(vertex_id) AS (
      SELECT vertex_id FROM vertices WHERE properties->>'name' = 'United States'
    UNION
      SELECT edges.tail_vertex FROM edges
        JOIN in_usa ON edges.head_vertex = in_usa.vertex_id
        WHERE edges.label = 'within'
  ),
  -- in_europe is the set of vertex IDs of all locations within Europe
  in_europe(vertex_id) AS (
      SELECT vertex_id FROM vertices WHERE properties->>'name' = 'Europe'
    UNION
      SELECT edges.tail_vertex FROM edges
        JOIN in_europe ON edges.head_vertex = in_europe.vertex_id
        WHERE edges.label = 'within'
  ),
  -- born_in_usa is the set of vertex IDs of all people born in the US
  born_in_usa(vertex_id) AS (
    SELECT edges.tail_vertex FROM edges
      JOIN in_usa ON edges.head_vertex = in_usa.vertex_id
      WHERE edges.label = 'born_in'
  ),
  -- lives_in_europe is the set of vertex IDs of all people living in Europe
  lives_in_europe(vertex_id) AS (
    SELECT edges.tail_vertex FROM edges
      JOIN in_europe ON edges.head_vertex = in_europe.vertex_id
      WHERE edges.label = 'lives_in'
  )
SELECT vertices.properties->>'name'
FROM vertices
-- join to find those people who were both born in the US *and* live in Europe
JOIN born_in_usa     ON vertices.vertex_id = born_in_usa.vertex_id
JOIN lives_in_europe ON vertices.vertex_id = lives_in_europe.vertex_id;""".split("\n")


def replace_table_containing(fname, marker, payload):
    """يستبدل كتلة <table>...</table> التي تحتوي المؤشّر بنصّ الشيفرة."""
    path = os.path.join(CH, fname)
    lines = open(path, encoding="utf-8").read().split("\n")
    for a in range(len(lines)):
        if lines[a].strip() != "<table>":
            continue
        b = a
        while b < len(lines) and lines[b].strip() != "</table>":
            b += 1
        if b >= len(lines):
            break
        block = "\n".join(lines[a:b + 1])
        if marker in block:
            lines[a:b + 1] = payload
            open(path, "w", encoding="utf-8").write("\n".join(lines))
            print("  patched %s lines %d-%d" % (fname, a + 1, b + 1))
            return True
    print("  ! table with %r not found in %s" % (marker, fname))
    return False


def replace_range(fname, start_mark, end_mark, payload):
    """يستبدل كل الأسطر بين علامتَي بداية ونهاية (شاملًا) بنصّ الشيفرة."""
    path = os.path.join(CH, fname)
    lines = open(path, encoding="utf-8").read().split("\n")
    a = None
    for i, l in enumerate(lines):
        if start_mark in l:
            a = i
            break
    if a is None:
        print("  ! start %r not found in %s" % (start_mark, fname))
        return False
    b = a
    while b < len(lines) and end_mark not in lines[b]:
        b += 1
    if b >= len(lines):
        print("  ! end %r not found in %s" % (end_mark, fname))
        return False
    lines[a:b + 1] = payload
    open(path, "w", encoding="utf-8").write("\n".join(lines))
    print("  patched %s lines %d-%d" % (fname, a + 1, b + 1))
    return True


print("restoring code examples from the PDF:")
replace_table_containing("chunk_0022.md", "Idaho:Location", CYPHER)
replace_range("chunk_0023.md", "<table>", "JOIN lives_in_europe ON vertices.vertex_id", SQL)
