• In CODASYL, a database had a schema that specified which record type could be nested within which other record type. In a graph database, there is no such restriction: any vertex can have an edge to any other vertex. This gives much greater flexibility for applications to adapt to changing requirements.
• In CODASYL, the only way to reach a particular record was to traverse one of the access paths to it. In a graph database, you can refer directly to any vertex by its unique ID, or you can use an index to find vertices with a particular value.
• In CODASYL, the children of a record were an ordered set, so the database had to maintain that ordering (which had consequences for the storage layout) and applications that inserted new records into the database had to worry about the positions of the new records in these sets. In a graph database, vertices and edges are not ordered (you can only sort the results when making a query).
• In CODASYL, all queries were imperative, difficult to write and easily broken by changes in the schema. In a graph database, you can write your traversal in imperative code if you want to, but most graph databases also support high-level, declarative query languages such as Cypher or SPARQL.

## The Foundation: Datalog

Datalog is a much older language than SPARQL or Cypher, having been studied extensively by academics in the 1980s [44, 45, 46]. It is less well known among soft‐ ware engineers, but it is nevertheless important, because it provides the foundation that later query languages build upon.

In practice, Datalog is used in a few data systems: for example, it is the query lan‐ guage of Datomic [40], and Cascalog [47] is a Datalog implementation for querying large datasets in Hadoop.viii

<!-- page 83 -->

Datalog’s data model is similar to the triple-store model, generalized a bit. Instead of writing a triple as (subject, predicate, object), we write it as predicate(subject, object). Example 2-10 shows how to write the data from our example in Datalog.

Example 2-10. A subset of the data in Figure 2-5, represented as Datalog facts

name(namerica, 'North America'). type(namerica, continent). name(usa, 'United States'). type(usa, country). within(usa, namerica). name(idaho, 'Idaho'). type(idaho, state). within(idaho, usa). name(lucy, 'Lucy'). born_in(lucy, idaho).

Now that we have defined the data, we can write the same query as before, as shown in Example 2-11. It looks a bit different from the equivalent in Cypher or SPARQL, but don’t let that put you off. Datalog is a subset of Prolog, which you might have seen before if you’ve studied computer science.

Example 2-11. The same query as Example 2-4, expressed in Datalog

within_recursive(Location, Name) :- name(Location, Name). /* Rule 1 */ within_recursive(Location, Name) :- within(Location, Via), /* Rule 2 */ within_recursive(Via, Name). migrated(Name, BornIn, LivingIn) :- name(Person, Name), /* Rule 3 */ born_in(Person, BornLoc), within_recursive(BornLoc, BornIn), lives_in(Person, LivingLoc), within_recursive(LivingLoc, LivingIn).

?- migrated(Who, 'United States', 'Europe'). /* Who = 'Lucy'. */

Cypher and SPARQL jump in right away with SELECT, but Datalog takes a small step at a time. We define rules that tell the database about new predicates: here, we define two new predicates, within_recursive and migrated. These predicates aren’t triples stored in the database, but instead they are derived from data or from other rules. Rules can refer to other rules, just like functions can call other functions or recur‐ sively call themselves. Like this, complex queries can be built up a small piece at a time.

<!-- page 84 -->

In rules, words that start with an uppercase letter are variables, and predicates are matched like in Cypher and SPARQL. For example, name(Location, Name) matches the triple name(namerica, 'North America') with variable bindings Location = namerica and Name = 'North America'.

A rule applies if the system can find a match for all predicates on the righthand side of the :- operator. When the rule applies, it’s as though the lefthand side of the :- was added to the database (with variables replaced by the values they matched).

One possible way of applying the rules is thus:

1. name(namerica, 'North America') exists in the database, so rule 1 applies. It generates within_recursive(namerica, 'North America').
2. within(usa, namerica) exists in the database and the previous step generated within_recursive(namerica, 'North America'), so rule 2 applies. It generates within_recursive(usa, 'North America').
3. within(idaho, usa) exists in the database and the previous step generated within_recursive(usa, 'North America'), so rule 2 applies. It generates within_recursive(idaho, 'North America').

By repeated application of rules 1 and 2, the within_recursive predicate can tell us all the locations in North America (or any other location name) contained in our database. This process is illustrated in Figure 2-6.

<table>
<tr><th>After ap</th><th>ng rule 1:</th><th colspan="2">After applying rule 2 onc</th><th colspan="2">After applying rule 2 twice:</th></tr>
<tr><td>within</td><td></td><td>within_recursiv</td><td></td><td>within_recursive</td><td></td></tr>
<tr><td></td><td></td><td>ocation</td><td>Na</td><td>Location</td><td>Name</td></tr>
<tr><td>namer</td><td>orth</td><td>america</td><td>North A</td><td>namerica</td><td>North America</td></tr>
<tr><td></td><td>nited States</td><td></td><td>North A</td><td>isa</td><td>North America</td></tr>
<tr><td></td><td>ho</td><td>sa</td><td>nited</td><td>daho</td><td>North America</td></tr>
<tr><td></td><td></td><td>dah</td><td></td><td></td><td>United States</td></tr>
<tr><td></td><td></td><td>daho</td><td>d</td><td>laho</td><td>United States</td></tr>
<tr><td></td><td></td><td></td><td></td><td>daho</td><td>Idaho</td></tr>
<tr><td></td><td></td><td></td><td>within(idaho, usa)</td><td></td><td></td></tr>
</table>

Figure 2-6. Determining that Idaho is in North America, using the Datalog rules from Example 2-11.

Now rule 3 can find people who were born in some location BornIn and live in some location LivingIn. By querying with BornIn = 'United States' and LivingIn = 'Europe', and leaving the person as a variable Who, we ask the Datalog system to find out which values can appear for the variable Who. So, finally we get the same answer as in the earlier Cypher and SPARQL queries.

<!-- page 85 -->

The Datalog approach requires a different kind of thinking to the other query lan‐ guages discussed in this chapter, but it’s a very powerful approach, because rules can be combined and reused in different queries. It’s less convenient for simple one-off queries, but it can cope better if your data is complex.

## Summary

Data models are a huge subject, and in this chapter we have taken a quick look at a broad variety of different models. We didn’t have space to go into all the details of each model, but hopefully the overview has been enough to whet your appetite to find out more about the model that best fits your application’s requirements.

Historically, data started out being represented as one big tree (the hierarchical model), but that wasn’t good for representing many-to-many relationships, so the relational model was invented to solve that problem. More recently, developers found that some applications don’t fit well in the relational model either. New nonrelational “NoSQL” datastores have diverged in two main directions:

