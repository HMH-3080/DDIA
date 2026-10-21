As computers became vastly more powerful and networked, they started being used for increasingly diverse purposes. And remarkably, relational databases turned out to generalize very well, beyond their original scope of business data processing, to a broad variety of use cases. Much of what you see on the web today is still powered by relational databases, be it online publishing, discussion, social networking, ecom‐ merce, games, software-as-a-service productivity applications, or much more.

## The Birth of NoSQL

Now, in the 2010s, NoSQL is the latest attempt to overthrow the relational model’s dominance. The name “NoSQL” is unfortunate, since it doesn’t actually refer to any particular technology—it was originally intended simply as a catchy Twitter hashtag for a meetup on open source, distributed, nonrelational databases in 2009 [3]. Never‐ theless, the term struck a nerve and quickly spread through the web startup commu‐ nity and beyond. A number of interesting database systems are now associated with the #NoSQL hashtag, and it has been retroactively reinterpreted as Not Only SQL [4].

There are several driving forces behind the adoption of NoSQL databases, including:

• A need for greater scalability than relational databases can easily achieve, includ‐ ing very large datasets or very high write throughput
• A widespread preference for free and open source software over commercial database products
• Specialized query operations that are not well supported by the relational model
• Frustration with the restrictiveness of relational schemas, and a desire for a more dynamic and expressive data model [5]

Different applications have different requirements, and the best choice of technology for one use case may well be different from the best choice for another use case. It therefore seems likely that in the foreseeable future, relational databases will continue to be used alongside a broad variety of nonrelational datastores—an idea that is sometimes called polyglot persistence [3].

## The Object-Relational Mismatch

Most application development today is done in object-oriented programming lan‐ guages, which leads to a common criticism of the SQL data model: if data is stored in relational tables, an awkward translation layer is required between the objects in the

<!-- page 52 -->

i. A term borrowed from electronics. Every electric circuit has a certain impedance (resistance to alternating current) on its inputs and outputs. When you connect one circuit’s output to another one’s input, the power transfer across the connection is maximized if the output and input impedances of the two circuits match. An impedance mismatch can lead to signal reflections and other troubles.

application code and the database model of tables, rows, and columns. The discon‐ nect between the models is sometimes called an impedance mismatch. i

Object-relational mapping (ORM) frameworks like ActiveRecord and Hibernate reduce the amount of boilerplate code required for this translation layer, but they can’t completely hide the differences between the two models.

For example, Figure 2-1 illustrates how a résumé (a LinkedIn profile) could be expressed in a relational schema. The profile as a whole can be identified by a unique identifier, user_id. Fields like first_name and last_name appear exactly once per user, so they can be modeled as columns on the users table. However, most people have had more than one job in their career (positions), and people may have varying numbers of periods of education and any number of pieces of contact information. There is a one-to-many relationship from the user to these items, which can be repre‐ sented in various ways:

• In the traditional SQL model (prior to SQL:1999), the most common normalized representation is to put positions, education, and contact information in separate tables, with a foreign key reference to the users table, as in Figure 2-1.
• Later versions of the SQL standard added support for structured datatypes and XML data; this allowed multi-valued data to be stored within a single row, with support for querying and indexing inside those documents. These features are supported to varying degrees by Oracle, IBM DB2, MS SQL Server, and Post‐ greSQL [6, 7]. A JSON datatype is also supported by several databases, including IBM DB2, MySQL, and PostgreSQL [8].
• A third option is to encode jobs, education, and contact info as a JSON or XML document, store it on a text column in the database, and let the application inter‐ pret its structure and content. In this setup, you typically cannot use the database to query for values inside that encoded column.

<!-- page 53 -->

<table>
<tr><th></th><th></th><th></th><th></th><th></th><th>users table</th></tr>
<tr><td>http://www.linkedin.com/in/williamhgates</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td>user_id</td><td>first_name</td><td>last_name</td><td></td><td>summary</td></tr>
<tr><td>Bill Gates</td><td>251</td><td>Bill</td><td>Gates</td><td></td><td>Co-chair of … blogger.</td></tr>
<tr><td>Greater Seattle Area | Philanthropy</td><td></td><td>region_id</td><td>industry_id</td><td></td><td>photo_id</td></tr>
<tr><td></td><td></td><td>• us:91</td><td>131 \phi</td><td></td><td>57817532</td></tr>
<tr><td>Summary</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Co-chair of the Bill &amp; Melinda Gates Foundation.</td><td></td><td></td><td>regions table</td><td></td><td>industries table</td></tr>
<tr><td>Chairman, Microsoft Corporation. Voracious reader. Avid traveler. Active blogger.</td><td>id</td><td colspan="2">/ region_name</td><td>id</td><td>industry_name</td></tr>
<tr><td></td><td>us:7</td><td colspan="2">Greater Boston Area</td><td>43</td><td>Financial Services</td></tr>
<tr><td>Experience</td><td>us:91</td><td colspan="2">Greater Seattle Area</td><td>48</td><td>Construction</td></tr>
<tr><td>Co-chair • Bill &amp; Melinda Gates Foundation</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>2000 – Present</td><td></td><td></td><td></td><td>131</td><td>Philanthropy</td></tr>
<tr><td>Co-founder, Chairman • Microsoft</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>1975 – Present</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td></td><td></td><td>positions table</td></tr>
<tr><td>Education</td><td>id</td><td>user_id</td><td>job_title</td><td></td><td>organization</td></tr>
<tr><td>Harvard University</td><td>458</td><td>• 251</td><td>Co-chair</td><td colspan="2">Bill &amp; Melinda Gates F..</td></tr>
<tr><td>1973 – 1975</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr><td>Lakeside School, Seattle</td><td>457</td><td>• 251</td><td>Co-founder, Chairman</td><td></td><td>Microsoft</td></tr>
<tr><td>Contact Info</td><td></td><td></td><td></td><td></td><td>education table</td></tr>
<tr><td>Blog: thegatesnotes.com Twitter: @BillGates</td><td>id</td><td>user_id</td><td>school_name</td><td></td><td>end start</td></tr>
<tr><td></td><td>807</td><td>• 251</td><td colspan="2">Harvard University</td><td>1975 1973</td></tr>
<tr><td></td><td>806</td><td>• 251</td><td></td><td>Lakeside School,</td><td>NULL NULL</td></tr>
<tr><td></td><td></td><td></td><td>Seattle</td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td></td><td></td><td>contact_info table</td></tr>
<tr><td></td><td>id</td><td>user_id</td><td>type</td><td></td><td>url</td></tr>
<tr><td></td><td>155</td><td>• 251</td><td>blog</td><td colspan="2">http://thegatesnotes.com</td></tr>
<tr><td></td><td>156</td><td>• 251</td><td>twitter</td><td colspan="2">http://twitter.com/BillGates</td></tr>
</table>

Figure 2-1. Representing a LinkedIn profile using a relational schema. Photo of Bill Gates courtesy of Wikimedia Commons, Ricardo Stuckert, Agência Brasil.

For a data structure like a résumé, which is mostly a self-contained document, a JSON representation can be quite appropriate: see Example 2-1. JSON has the appeal of being much simpler than XML. Document-oriented databases like MongoDB [9], RethinkDB [10], CouchDB [11], and Espresso [12] support this data model.

Example 2-1. Representing a LinkedIn profile as a JSON document

{ "user_id": 251, "first_name": "Bill" "last_name": "Gates", "summary": "Co-chair of the Bill & Melinda Gates... Active blogger.", "region_id": "us:91", "industry_id": 131, "photo_url": "/p/7/000/253/05b/308dd6e.jpg",

<!-- page 54 -->

} "positions": [ {"job_title": "Co-chair", "organization": "Bill & Melinda Gates Foundation"}, {"job_title": "Co-founder, Chairman", "organization": "Microsoft"} ], "education": [ {"school_name": "Harvard University", "start": 1973, "end": 1975}, {"school_name": "Lakeside School, Seattle", "start": null, "end": null} ], "contact_info": { "blog": "http://thegatesnotes.com", "twitter": "http://twitter.com/BillGates" }

Some developers feel that the JSON model reduces the impedance mismatch between the application code and the storage layer. However, as we shall see in Chapter 4, there are also problems with JSON as a data encoding format. The lack of a schema is often cited as an advantage; we will discuss this in “Schema flexibility in the docu‐ ment model” on page 39.

