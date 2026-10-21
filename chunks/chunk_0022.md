• The vertex at which the edge ends (the head vertex)
• A label to describe the kind of relationship between the two vertices
• A collection of properties (key-value pairs)

You can think of a graph store as consisting of two relational tables, one for vertices and one for edges, as shown in Example 2-2 (this schema uses the PostgreSQL json datatype to store the properties of each vertex or edge). The head and tail vertex are stored for each edge; if you want the set of incoming or outgoing edges for a vertex, you can query the edges table by head_vertex or tail_vertex, respectively.

Example 2-2. Representing a property graph using a relational schema

CREATE TABLE vertices ( vertex_id integer PRIMARY KEY, properties json ); CREATE TABLE edges ( edge_id integer PRIMARY KEY, tail_vertex integer REFERENCES vertices (vertex_id), head_vertex integer REFERENCES vertices (vertex_id), label text, properties json );

CREATE INDEX edges_tails ON edges (tail_vertex);

CREATE INDEX edges_heads ON edges (head_vertex);

Some important aspects of this model are:

1. Any vertex can have an edge connecting it with any other vertex. There is no schema that restricts which kinds of things can or cannot be associated.
2. Given any vertex, you can efficiently find both its incoming and its outgoing edges, and thus traverse the graph—i.e., follow a path through a chain of vertices —both forward and backward. (That’s why Example 2-2 has indexes on both the tail_vertex and head_vertex columns.)
3. By using different labels for different kinds of relationships, you can store several different kinds of information in a single graph, while still maintaining a clean data model.

Those features give graphs a great deal of flexibility for data modeling, as illustrated in Figure 2-5. The figure shows a few things that would be difficult to express in a traditional relational schema, such as different kinds of regional structures in differ‐ ent countries (France has départements and régions, whereas the US has counties and states), quirks of history such as a country within a country (ignoring for now the

<!-- page 74 -->

intricacies of sovereign states and nations), and varying granularity of data (Lucy’s current residence is specified as a city, whereas her place of birth is specified only at the level of a state).

You could imagine extending the graph to also include many other facts about Lucy and Alain, or other people. For instance, you could use it to indicate any food aller‐ gies they have (by introducing a vertex for each allergen, and an edge between a per‐ son and an allergen to indicate an allergy), and link the allergens with a set of vertices that show which foods contain which substances. Then you could write a query to find out what is safe for each person to eat. Graphs are good for evolvability: as you add features to your application, a graph can easily be extended to accommodate changes in your application’s data structures.

## The Cypher Query Language

Cypher is a declarative query language for property graphs, created for the Neo4j graph database [37]. (It is named after a character in the movie The Matrix and is not related to ciphers in cryptography [38].)

Example 2-3 shows the Cypher query to insert the lefthand portion of Figure 2-5 into a graph database. The rest of the graph can be added similarly and is omitted for readability. Each vertex is given a symbolic name like USA or Idaho, and other parts of the query can use those names to create edges between the vertices, using an arrow notation: (Idaho) -[:WITHIN]-> (USA) creates an edge labeled WITHIN, with Idaho as the tail node and USA as the head node.

Example 2-3. A subset of the data in Figure 2-5, represented as a Cypher query

## CREATE

(NAmerica:Location {name:'North America', type:'continent'}),

<table>
<tr><th>(USA:Location</th><th colspan="3">{name:'United States', type:'country' }),</th></tr>
<tr><td>(Idaho:Location</td><td>{name:'Idaho',</td><td>type:'state'</td><td>}),</td></tr>
<tr><td>(Lucy:Person</td><td>{name:'Lucy' }),</td><td></td><td></td></tr>
<tr><td colspan="3">(Idaho) -[:WITHIN]-&gt; (USA) -[:WITHIN]-&gt; (NAmerica),</td><td></td></tr>
<tr><td colspan="2">(Lucy) -[:BORN_IN]-&gt; (Idaho)</td><td></td><td></td></tr>
</table>

When all the vertices and edges of Figure 2-5 are added to the database, we can start asking interesting questions: for example, find the names of all the people who emigra‐ ted from the United States to Europe. To be more precise, here we want to find all the vertices that have a BORN_IN edge to a location within the US, and also a LIVING_IN edge to a location within Europe, and return the name property of each of those verti‐ ces.

Example 2-4 shows how to express that query in Cypher. The same arrow notation is used in a MATCH clause to find patterns in the graph: (person) -[:BORN_IN]-> ()

<!-- page 75 -->

matches any two vertices that are related by an edge labeled BORN_IN. The tail vertex of that edge is bound to the variable person, and the head vertex is left unnamed.

## Example 2-4. Cypher query to find people who emigrated from the US to Europe

## MATCH

(person) -[:BORN_IN]-> () -[:WITHIN*0..]-> (us:Location {name:'United States'}), (person) -[:LIVES_IN]-> () -[:WITHIN*0..]-> (eu:Location {name:'Europe'}) RETURN person.name

The query can be read as follows:

Find any vertex (call it person) that meets both of the following conditions:

1. person has an outgoing BORN_IN edge to some vertex. From that vertex, you can follow a chain of outgoing WITHIN edges until eventually you reach a vertex of type Location, whose name property is equal to "United States".
2. That same person vertex also has an outgoing LIVES_IN edge. Following that edge, and then a chain of outgoing WITHIN edges, you eventually reach a vertex of type Location, whose name property is equal to "Europe".

For each such person vertex, return the name property.

There are several possible ways of executing the query. The description given here suggests that you start by scanning all the people in the database, examine each per‐ son’s birthplace and residence, and return only those people who meet the criteria.

But equivalently, you could start with the two Location vertices and work backward. If there is an index on the name property, you can probably efficiently find the two vertices representing the US and Europe. Then you can proceed to find all locations (states, regions, cities, etc.) in the US and Europe respectively by following all incom‐ ing WITHIN edges. Finally, you can look for people who can be found through an incoming BORN_IN or LIVES_IN edge at one of the location vertices.

