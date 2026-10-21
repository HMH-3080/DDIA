As is typical for a declarative query language, you don’t need to specify such execu‐ tion details when writing the query: the query optimizer automatically chooses the strategy that is predicted to be the most efficient, so you can get on with writing the rest of your application.

## Graph Queries in SQL

Example 2-2 suggested that graph data can be represented in a relational database. But if we put graph data in a relational structure, can we also query it using SQL?

The answer is yes, but with some difficulty. In a relational database, you usually know in advance which joins you need in your query. In a graph query, you may need to

<!-- page 76 -->

traverse a variable number of edges before you find the vertex you’re looking for— that is, the number of joins is not fixed in advance.

In our example, that happens in the () -[:WITHIN*0..]-> () rule in the Cypher query. A person’s LIVES_IN edge may point at any kind of location: a street, a city, a district, a region, a state, etc. A city may be WITHIN a region, a region WITHIN a state, a state WITHIN a country, etc. The LIVES_IN edge may point directly at the location ver‐ tex you’re looking for, or it may be several levels removed in the location hierarchy.

In Cypher, :WITHIN*0.. expresses that fact very concisely: it means “follow a WITHIN edge, zero or more times.” It is like the * operator in a regular expression.

Since SQL:1999, this idea of variable-length traversal paths in a query can be expressed using something called recursive common table expressions (the WITH RECURSIVE syntax). Example 2-5 shows the same query—finding the names of people who emigrated from the US to Europe—expressed in SQL using this technique (sup‐ ported in PostgreSQL, IBM DB2, Oracle, and SQL Server). However, the syntax is very clumsy in comparison to Cypher.

Example 2-5. The same query as Example 2-4, expressed in SQL using recursive common table expressions

<table>
<tr><td>WITH</td><td>RECURSIVE</td></tr>
</table>

<table>
<tr><th>-- in_usa is the set of vertex IDs of all locations within the United States</th></tr>
<tr><td>in_usa(vertex_id) AS (</td></tr>
<tr><td>SELECT vertex_id FROM vertices WHERE properties-&gt;&gt;'name' = 'United States'</td></tr>
<tr><td>UNION</td></tr>
<tr><td>SELECT edges.tail_vertex FROM edges</td></tr>
<tr><td>JOIN in_usa ON edges.head_vertex = in_usa.vertex_id</td></tr>
<tr><td>WHERE edges.label = 'within'</td></tr>
<tr><td>),</td></tr>
<tr><td>-- in_europe is the set of vertex IDs of all locations within Europe</td></tr>
<tr><td>in_europe(vertex_id) AS (</td></tr>
<tr><td>SELECT vertex_id FROM vertices WHERE properties-&gt;&gt;'name' = 'Europe'</td></tr>
<tr><td>UNION</td></tr>
<tr><td>SELECT edges.tail_vertex FROM edges</td></tr>
<tr><td>JOIN in_europe ON edges.head_vertex = in_europe.vertex_id</td></tr>
<tr><td>WHERE edges.label = 'within'</td></tr>
<tr><td>),</td></tr>
<tr><td>-- born_in_usa is the set of vertex IDs of all people born in the US</td></tr>
<tr><td>born_in_usa(vertex_id) AS (</td></tr>
<tr><td>SELECT edges.tail_vertex FROM edges</td></tr>
<tr><td>JOIN in_usa ON edges.head_vertex = in_usa.vertex_id</td></tr>
<tr><td>WHERE edges.label = 'born_in'</td></tr>
<tr><td>),</td></tr>
</table>

<!-- page 77 -->

-- lives_in_europe is the set of vertex IDs of all people living in Europe lives_in_europe(vertex_id) AS ( SELECT edges.tail_vertex FROM edges JOIN in_europe ON edges.head_vertex = in_europe.vertex_id WHERE edges.label = 'lives_in' )

SELECT vertices.properties->>'name'

FROM vertices

-- join to find those people who were both born in the US *and* live in Europe JOIN born_in_usa ON vertices.vertex_id = born_in_usa.vertex_id JOIN lives_in_europe ON vertices.vertex_id = lives_in_europe.vertex_id;

First find the vertex whose name property has the value "United States", and make it the first element of the set of vertices in_usa. Follow all incoming within edges from vertices in the set in_usa, and add them to the same set, until all incoming within edges have been visited. Do the same starting with the vertex whose name property has the value "Europe", and build up the set of vertices in_europe. For each of the vertices in the set in_usa, follow incoming born_in edges to find people who were born in some place within the United States. Similarly, for each of the vertices in the set in_europe, follow incoming lives_in edges to find people who live in Europe. Finally, intersect the set of people born in the USA with the set of people living in Europe, by joining them.

If the same query can be written in 4 lines in one query language but requires 29 lines in another, that just shows that different data models are designed to satisfy different use cases. It’s important to pick a data model that is suitable for your application.

## Triple-Stores and SPARQL

The triple-store model is mostly equivalent to the property graph model, using differ‐ ent words to describe the same ideas. It is nevertheless worth discussing, because there are various tools and languages for triple-stores that can be valuable additions to your toolbox for building applications.

In a triple-store, all information is stored in the form of very simple three-part state‐ ments: (subject, predicate, object). For example, in the triple (Jim, likes, bananas), Jim is the subject, likes is the predicate (verb), and bananas is the object.

<!-- page 78 -->

The subject of a triple is equivalent to a vertex in a graph. The object is one of two things:

1. A value in a primitive datatype, such as a string or a number. In that case, the predicate and object of the triple are equivalent to the key and value of a property on the subject vertex. For example, (lucy, age, 33) is like a vertex lucy with prop‐ erties {"age":33}.
2. Another vertex in the graph. In that case, the predicate is an edge in the graph, the subject is the tail vertex, and the object is the head vertex. For example, in (lucy, marriedTo, alain) the subject and object lucy and alain are both vertices, and the predicate marriedTo is the label of the edge that connects them.

Example 2-6 shows the same data as in Example 2-3, written as triples in a format called Turtle, a subset of Notation3 (N3) [39].

Example 2-6. A subset of the data in Figure 2-5, represented as Turtle triples

@prefix : <urn:example:>. _:lucy _:lucy _:lucy a :Person. :name "Lucy". :bornIn _:idaho. _:idaho _:idaho _:idaho a :name :type :Location. "Idaho". "state". _:idaho :within _:usa. _:usa _:usa _:usa _:usa a :name :Location. "United States". :type "country". :within _:namerica. _:namerica a :Location. _:namerica :name _:namerica :type "North America". "continent".

In this example, vertices of the graph are written as _:someName. The name doesn’t mean anything outside of this file; it exists only because we otherwise wouldn’t know which triples refer to the same vertex. When the predicate represents an edge, the object is a vertex, as in _:idaho :within _:usa. When the predicate is a property, the object is a string literal, as in _:usa :name "United States".

