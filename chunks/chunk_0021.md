The filter to consider only shark species can be specified declaratively (this is a MongoDB-specific extension to MapReduce). The JavaScript function map is called once for every document that matches query, with this set to the document object. The map function emits a key (a string consisting of year and month, such as "2013-12" or "2014-1") and a value (the number of animals in that observation). The key-value pairs emitted by map are grouped by key. For all key-value pairs with the same key (i.e., the same month and year), the reduce function is called once. The reduce function adds up the number of animals from all observations in a particular month. The final output is written to the collection monthlySharkReport. For example, say the observations collection contains these two documents: { } { } observationTimestamp: Date.parse("Mon, 25 Dec 1995 12:34:56 GMT"), family: "Sharks", species: "Carcharodon carcharias", numAnimals: 3 observationTimestamp: Date.parse("Tue, 12 Dec 1995 16:17:18 GMT"), family: species: "Sharks", "Carcharias taurus", numAnimals: 4

<!-- page 70 -->

The map function would be called once for each document, resulting in emit("1995-12", 3) and emit("1995-12", 4). Subsequently, the reduce function would be called with reduce("1995-12", [3, 4]), returning 7.

The map and reduce functions are somewhat restricted in what they are allowed to do. They must be pure functions, which means they only use the data that is passed to them as input, they cannot perform additional database queries, and they must not have any side effects. These restrictions allow the database to run the functions any‐ where, in any order, and rerun them on failure. However, they are nevertheless pow‐ erful: they can parse strings, call library functions, perform calculations, and more.

MapReduce is a fairly low-level programming model for distributed execution on a cluster of machines. Higher-level query languages like SQL can be implemented as a pipeline of MapReduce operations (see Chapter 10), but there are also many dis‐ tributed implementations of SQL that don’t use MapReduce. Note there is nothing in SQL that constrains it to running on a single machine, and MapReduce doesn’t have a monopoly on distributed query execution.

Being able to use JavaScript code in the middle of a query is a great feature for advanced queries, but it’s not limited to MapReduce—some SQL databases can be extended with JavaScript functions too [34].

A usability problem with MapReduce is that you have to write two carefully coordi‐ nated JavaScript functions, which is often harder than writing a single query. More‐ over, a declarative query language offers more opportunities for a query optimizer to improve the performance of a query. For these reasons, MongoDB 2.2 added support for a declarative query language called the aggregation pipeline [9]. In this language, the same shark-counting query looks like this:

db.observations.aggregate([ { $match: { family: "Sharks" } }, { $group: { _id: { year: { $year: "$observationTimestamp" }, month: { $month: "$observationTimestamp" } }, totalAnimals: { $sum: "$numAnimals" } } } ]);

The aggregation pipeline language is similar in expressiveness to a subset of SQL, but it uses a JSON-based syntax rather than SQL’s English-sentence-style syntax; the dif‐ ference is perhaps a matter of taste. The moral of the story is that a NoSQL system may find itself accidentally reinventing SQL, albeit in disguise.

<!-- page 71 -->

## Graph-Like Data Models

We saw earlier that many-to-many relationships are an important distinguishing fea‐ ture between different data models. If your application has mostly one-to-many rela‐ tionships (tree-structured data) or no relationships between records, the document model is appropriate.

But what if many-to-many relationships are very common in your data? The rela‐ tional model can handle simple cases of many-to-many relationships, but as the con‐ nections within your data become more complex, it becomes more natural to start modeling your data as a graph.

A graph consists of two kinds of objects: vertices (also known as nodes or entities) and edges (also known as relationships or arcs). Many kinds of data can be modeled as a graph. Typical examples include:

## Social graphs

Vertices are people, and edges indicate which people know each other.

## The web graph

Vertices are web pages, and edges indicate HTML links to other pages.

## Road or rail networks

Vertices are junctions, and edges represent the roads or railway lines between them.

Well-known algorithms can operate on these graphs: for example, car navigation sys‐ tems search for the shortest path between two points in a road network, and PageRank can be used on the web graph to determine the popularity of a web page and thus its ranking in search results.

In the examples just given, all the vertices in a graph represent the same kind of thing (people, web pages, or road junctions, respectively). However, graphs are not limited to such homogeneous data: an equally powerful use of graphs is to provide a consis‐ tent way of storing completely different types of objects in a single datastore. For example, Facebook maintains a single graph with many different types of vertices and edges: vertices represent people, locations, events, checkins, and comments made by users; edges indicate which people are friends with each other, which checkin hap‐ pened in which location, who commented on which post, who attended which event, and so on [35].

In this section we will use the example shown in Figure 2-5. It could be taken from a social network or a genealogical database: it shows two people, Lucy from Idaho and Alain from Beaune, France. They are married and living in London.

<!-- page 72 -->

<table>
<tr><th>type: continent</th><th></th><th>type: continent</th></tr>
<tr><td>America</td><td></td><td></td></tr>
<tr><td>type: cou</td><td>type: country</td><td></td></tr>
<tr><td>name: United ta</td><td>name: United</td><td></td></tr>
<tr><td></td><td>type: count</td><td></td></tr>
<tr><td>d</td><td>name: England</td><td>fr: Bo</td></tr>
<tr><td></td><td></td><td>ne_en: Burgu</td></tr>
<tr><td></td><td></td><td>ne: Côte-</td></tr>
</table>

Figure 2-5. Example of graph-structured data (boxes represent vertices, arrows repre‐ sent edges).

There are several different, but related, ways of structuring and querying data in graphs. In this section we will discuss the property graph model (implemented by Neo4j, Titan, and InfiniteGraph) and the triple-store model (implemented by Datomic, AllegroGraph, and others). We will look at three declarative query lan‐ guages for graphs: Cypher, SPARQL, and Datalog. Besides these, there are also imperative graph query languages such as Gremlin [36] and graph processing frame‐ works like Pregel (see Chapter 10).

## Property Graphs

In the property graph model, each vertex consists of:

• A unique identifier
• A set of outgoing edges
• A set of incoming edges
• A collection of properties (key-value pairs)

Each edge consists of:

• A unique identifier
• The vertex at which the edge starts (the tail vertex)

<!-- page 73 -->

