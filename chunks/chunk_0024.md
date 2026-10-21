It’s quite repetitive to repeat the same subject over and over again, but fortunately you can use semicolons to say multiple things about the same subject. This makes the Turtle format quite nice and readable: see Example 2-7.

<!-- page 79 -->

vii. Technically, Datomic uses 5-tuples rather than triples; the two additional fields are metadata for version‐ ing.

## Example 2-7. A more concise way of writing the data in Example 2-6

@prefix : <urn:example:>. _:lucy a :Person; :name "Lucy"; :bornIn _:idaho. _:idaho a :Location; :name "Idaho"; :type "state"; :within _:usa. _:usa a :Location; :name "United States"; :type "country"; :within _:namerica. _:namerica a :Location; :name "North America"; :type "continent".

## The semantic web

If you read more about triple-stores, you may get sucked into a maelstrom of articles written about the semantic web. The triple-store data model is completely independ‐ ent of the semantic web—for example, Datomic [40] is a triple-store that does not claim to have anything to do with it.vii But since the two are so closely linked in many people’s minds, we should discuss them briefly.

The semantic web is fundamentally a simple and reasonable idea: websites already publish information as text and pictures for humans to read, so why don’t they also publish information as machine-readable data for computers to read? The Resource Description Framework (RDF) [41] was intended as a mechanism for different web‐ sites to publish data in a consistent format, allowing data from different websites to be automatically combined into a web of data—a kind of internet-wide “database of everything.”

Unfortunately, the semantic web was overhyped in the early 2000s but so far hasn’t shown any sign of being realized in practice, which has made many people cynical about it. It has also suffered from a dizzying plethora of acronyms, overly complex standards proposals, and hubris.

However, if you look past those failings, there is also a lot of good work that has come out of the semantic web project. Triples can be a good internal data model for appli‐ cations, even if you have no interest in publishing RDF data on the semantic web.

## The RDF data model

The Turtle language we used in Example 2-7 is a human-readable format for RDF data. Sometimes RDF is also written in an XML format, which does the same thing much more verbosely—see Example 2-8. Turtle/N3 is preferable as it is much easier on the eyes, and tools like Apache Jena [42] can automatically convert between differ‐ ent RDF formats if necessary.

<!-- page 80 -->

## Example 2-8. The data of Example 2-7, expressed using RDF/XML syntax

<rdf:RDF xmlns="urn:example:" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"> <Location rdf:nodeID="idaho"> <name>Idaho</name> <type>state</type> <within> <Location rdf:nodeID="usa"> <name>United States</name> <type>country</type> <within> <Location rdf:nodeID="namerica"> <name>North America</name> <type>continent</type> </Location> </within> </Location> </within> </Location> <Person rdf:nodeID="lucy"> <name>Lucy</name> <bornIn rdf:nodeID="idaho"/> </Person> </rdf:RDF>

RDF has a few quirks due to the fact that it is designed for internet-wide data exchange. The subject, predicate, and object of a triple are often URIs. For example, a predicate might be an URI such as <http://my-company.com/namespace#within> or <http://my-company.com/namespace#lives_in>, rather than just WITHIN or LIVES_IN. The reasoning behind this design is that you should be able to combine your data with someone else’s data, and if they attach a different meaning to the word within or lives_in, you won’t get a conflict because their predicates are actually <http://other.org/foo#within> and <http://other.org/foo#lives_in>.

The URL <http://my-company.com/namespace> doesn’t necessarily need to resolve to anything—from RDF’s point of view, it is simply a namespace. To avoid potential confusion with http:// URLs, the examples in this section use non-resolvable URIs such as urn:example:within. Fortunately, you can just specify this prefix once at the top of the file, and then forget about it.

<!-- page 81 -->

## The SPARQL query language

SPARQL is a query language for triple-stores using the RDF data model [43]. (It is an acronym for SPARQL Protocol and RDF Query Language, pronounced “sparkle.”) It predates Cypher, and since Cypher’s pattern matching is borrowed from SPARQL, they look quite similar [37].

The same query as before—finding people who have moved from the US to Europe— is even more concise in SPARQL than it is in Cypher (see Example 2-9).

## Example 2-9. The same query as Example 2-4, expressed in SPARQL

PREFIX : <urn:example:>

SELECT ?personName WHERE { ?person :name ?personName. ?person :bornIn / :within* / :name "United States". ?person :livesIn / :within* / :name "Europe". }

The structure is very similar. The following two expressions are equivalent (variables start with a question mark in SPARQL):

(person) -[:BORN_IN]-> () -[:WITHIN*0..]-> (location) # Cypher ?person :bornIn / :within* ?location. # SPARQL

Because RDF doesn’t distinguish between properties and edges but just uses predi‐ cates for both, you can use the same syntax for matching properties. In the following expression, the variable usa is bound to any vertex that has a name property whose value is the string "United States":

(usa {name:'United States'}) # Cypher ?usa :name "United States". # SPARQL

SPARQL is a nice query language—even if the semantic web never happens, it can be a powerful tool for applications to use internally.

<!-- page 82 -->

viii. Datomic and Cascalog use a Clojure S-expression syntax for Datalog. In the following examples we use a Prolog syntax, which is a little easier to read, but this makes no functional difference.

## Graph Databases Compared to the Network Model

In “Are Document Databases Repeating History?” on page 36 we discussed how CODASYL and the relational model competed to solve the problem of many-tomany relationships in IMS. At first glance, CODASYL’s network model looks similar to the graph model. Are graph databases the second coming of CODASYL in disguise?

No. They differ in several important ways:

