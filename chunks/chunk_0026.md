1. Document databases target use cases where data comes in self-contained docu‐ ments and relationships between one document and another are rare.
2. Graph databases go in the opposite direction, targeting use cases where anything is potentially related to everything.

All three models (document, relational, and graph) are widely used today, and each is good in its respective domain. One model can be emulated in terms of another model —for example, graph data can be represented in a relational database—but the result is often awkward. That’s why we have different systems for different purposes, not a single one-size-fits-all solution.

One thing that document and graph databases have in common is that they typically don’t enforce a schema for the data they store, which can make it easier to adapt applications to changing requirements. However, your application most likely still assumes that data has a certain structure; it’s just a question of whether the schema is explicit (enforced on write) or implicit (handled on read).

Each data model comes with its own query language or framework, and we discussed several examples: SQL, MapReduce, MongoDB’s aggregation pipeline, Cypher, SPARQL, and Datalog. We also touched on CSS and XSL/XPath, which aren’t data‐ base query languages but have interesting parallels.

Although we have covered a lot of ground, there are still many data models left unmentioned. To give just a few brief examples:

• Researchers working with genome data often need to perform sequencesimilarity searches, which means taking one very long string (representing a

<!-- page 86 -->

DNA molecule) and matching it against a large database of strings that are simi‐ lar, but not identical. None of the databases described here can handle this kind of usage, which is why researchers have written specialized genome database software like GenBank [48].

• Particle physicists have been doing Big Data–style large-scale data analysis for decades, and projects like the Large Hadron Collider (LHC) now work with hun‐ dreds of petabytes! At such a scale custom solutions are required to stop the hardware cost from spiraling out of control [49].
• Full-text search is arguably a kind of data model that is frequently used alongside databases. Information retrieval is a large specialist subject that we won’t cover in great detail in this book, but we’ll touch on search indexes in Chapter 3 and Part III.

We have to leave it there for now. In the next chapter we will discuss some of the trade-offs that come into play when implementing the data models described in this chapter.

## References

[1] Edgar F. Codd: “A Relational Model of Data for Large Shared Data Banks,” Com‐ munications of the ACM, volume 13, number 6, pages 377–387, June 1970. doi: 10.1145/362384.362685 [2] Michael Stonebraker and Joseph M. Hellerstein: “What Goes Around Comes Around,” in Readings in Database Systems, 4th edition, MIT Press, pages 2–41, 2005. ISBN: 978-0-262-69314-1 [3] Pramod J. Sadalage and Martin Fowler: NoSQL Distilled. Addison-Wesley, August 2012. ISBN: 978-0-321-82662-6 [4] Eric Evans: “NoSQL: What’s in a Name?,” blog.sym-link.com, October 30, 2009. [5] James Phillips: “Surprises in Our NoSQL Adoption Survey,” blog.couchbase.com, February 8, 2012. [6] Michael Wagner: SQL/XML:2006 – Evaluierung der Standardkonformität ausge‐ wählter Datenbanksysteme. Diplomica Verlag, Hamburg, 2010. ISBN: 978-3-836-64609-3 [7] “XML Data in SQL Server,” SQL Server 2012 documentation, technet.micro‐ soft.com, 2013. [8] “PostgreSQL 9.3.1 Documentation,” The PostgreSQL Global Development Group, 2013. [9] “The MongoDB 2.4 Manual,” MongoDB, Inc., 2013.

<!-- page 87 -->

[10] “RethinkDB 1.11 Documentation,” rethinkdb.com, 2013. [11] “Apache CouchDB 1.6 Documentation,” docs.couchdb.org, 2014. [12] Lin Qiao, Kapil Surlaker, Shirshanka Das, et al.: “On Brewing Fresh Espresso: LinkedIn’s Distributed Data Serving Platform,” at ACM International Conference on Management of Data (SIGMOD), June 2013. [13] Rick Long, Mark Harrington, Robert Hain, and Geoff Nicholls: IMS Primer. IBM Redbook SG24-5352-00, IBM International Technical Support Organization, January 2000. [14] Stephen D. Bartlett: “IBM’s IMS—Myths, Realities, and Opportunities,” The Clipper Group Navigator, TCG2013015LI, July 2013. [15] Sarah Mei: “Why You Should Never Use MongoDB,” sarahmei.com, November 11, 2013. [16] J. S. Knowles and D. M. R. Bell: “The CODASYL Model,” in Databases—Role and Structure: An Advanced Course, edited by P. M. Stocker, P. M. D. Gray, and M. P. Atkinson, pages 19–56, Cambridge University Press, 1984. ISBN: 978-0-521-25430-4 [17] Charles W. Bachman: “The Programmer as Navigator,” Communications of the ACM, volume 16, number 11, pages 653–658, November 1973. doi: 10.1145/355611.362534 [18] Joseph M. Hellerstein, Michael Stonebraker, and James Hamilton: “Architecture of a Database System,” Foundations and Trends in Databases, volume 1, number 2, pages 141–259, November 2007. doi:10.1561/1900000002 [19] Sandeep Parikh and Kelly Stirman: “Schema Design for Time Series Data in MongoDB,” blog.mongodb.org, October 30, 2013. [20] Martin Fowler: “Schemaless Data Structures,” martinfowler.com, January 7, 2013. [21] Amr Awadallah: “Schema-on-Read vs. Schema-on-Write,” at Berkeley EECS RAD Lab Retreat, Santa Cruz, CA, May 2009. [22] Martin Odersky: “The Trouble with Types,” at Strange Loop, September 2013. [23] Conrad Irwin: “MongoDB—Confessions of a PostgreSQL Lover,” at HTML5DevConf, October 2013. [24] “Percona Toolkit Documentation: pt-online-schema-change,” Percona Ireland Ltd., 2013. [25] Rany Keddo, Tobias Bielohlawek, and Tobias Schmidt: “Large Hadron Migra‐ tor,” SoundCloud, 2013.

<!-- page 88 -->

[26] Shlomi Noach: “gh-ost: GitHub’s Online Schema Migration Tool for MySQL,” githubengineering.com, August 1, 2016.

