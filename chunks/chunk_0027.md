[27] James C. Corbett, Jeffrey Dean, Michael Epstein, et al.: “Spanner: Google’s Globally-Distributed Database,” at 10th USENIX Symposium on Operating System Design and Implementation (OSDI), October 2012. [28] Donald K. Burleson: “Reduce I/O with Oracle Cluster Tables,” dba-oracle.com. [29] Fay Chang, Jeffrey Dean, Sanjay Ghemawat, et al.: “Bigtable: A Distributed Stor‐ age System for Structured Data,” at 7th USENIX Symposium on Operating System Design and Implementation (OSDI), November 2006. [30] Bobbie J. Cochrane and Kathy A. McKnight: “DB2 JSON Capabilities, Part 1: Introduction to DB2 JSON,” IBM developerWorks, June 20, 2013. [31] Herb Sutter: “The Free Lunch Is Over: A Fundamental Turn Toward Concur‐ rency in Software,” Dr. Dobb’s Journal, volume 30, number 3, pages 202-210, March 2005. [32] Joseph M. Hellerstein: “The Declarative Imperative: Experiences and Conjec‐ tures in Distributed Logic,” Electrical Engineering and Computer Sciences, Univer‐ sity of California at Berkeley, Tech report UCB/EECS-2010-90, June 2010. [33] Jeffrey Dean and Sanjay Ghemawat: “MapReduce: Simplified Data Processing on Large Clusters,” at 6th USENIX Symposium on Operating System Design and Imple‐ mentation (OSDI), December 2004. [34] Craig Kerstiens: “JavaScript in Your Postgres,” blog.heroku.com, June 5, 2013. [35] Nathan Bronson, Zach Amsden, George Cabrera, et al.: “TAO: Facebook’s Dis‐ tributed Data Store for the Social Graph,” at USENIX Annual Technical Conference (USENIX ATC), June 2013. [36] “Apache TinkerPop3.2.3 Documentation,” tinkerpop.apache.org, October 2016. [37] “The Neo4j Manual v2.0.0,” Neo Technology, 2013. [38] Emil Eifrem: Twitter correspondence, January 3, 2014. [39] David Beckett and Tim Berners-Lee: “Turtle – Terse RDF Triple Language,” W3C Team Submission, March 28, 2011. [40] “Datomic Development Resources,” Metadata Partners, LLC, 2013. [41] W3C RDF Working Group: “Resource Description Framework (RDF),” w3.org, 10 February 2004.

[42] “Apache Jena,” Apache Software Foundation.

<!-- page 89 -->

[43] Steve Harris, Andy Seaborne, and Eric Prud’hommeaux: “SPARQL 1.1 Query Language,” W3C Recommendation, March 2013.

[44] Todd J. Green, Shan Shan Huang, Boon Thau Loo, and Wenchao Zhou: “Data‐ log and Recursive Query Processing,” Foundations and Trends in Databases, volume 5, number 2, pages 105–195, November 2013. doi:10.1561/1900000017

[45] Stefano Ceri, Georg Gottlob, and Letizia Tanca: “What You Always Wanted to Know About Datalog (And Never Dared to Ask),” IEEE Transactions on Knowledge and Data Engineering, volume 1, number 1, pages 146–166, March 1989. doi: 10.1109/69.43410 [46] Serge Abiteboul, Richard Hull, and Victor Vianu: Foundations of Databases. Addison-Wesley, 1995. ISBN: 978-0-201-53771-0, available online at web‐ dam.inria.fr/Alice [47] Nathan Marz: “Cascalog,” cascalog.org.

[48] Dennis A. Benson, Ilene Karsch-Mizrachi, David J. Lipman, et al.: “GenBank,” Nucleic Acids Research, volume 36, Database issue, pages D25–D30, December 2007. doi:10.1093/nar/gkm929 [49] Fons Rademakers: “ROOT for Big Data Analysis,” at Workshop on the Future of Big Data Management, London, UK, June 2013.

<!-- page 90 -->

Q Q AQ V Q o Z <

<table>
<tr><th></th><th></th></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td>c</td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td>O</td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td>=</td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td>2)</td></tr>
<tr><td></td><td>u</td></tr>
<tr><td></td><td>&lt;</td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td>O</td></tr>
<tr><td>৩</td><td></td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td>V</td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td>o</td></tr>
<tr><td></td><td></td></tr>
<tr><td></td><td>7</td></tr>
<tr><td></td><td></td></tr>
<tr><td>4</td><td></td></tr>
<tr><td></td><td>V</td></tr>
<tr><td></td><td></td></tr>
</table>

=

<!-- page 91 -->

## Storage and Retrieval

Wer Ordnung hält, ist nur zu faul zum Suchen.

(If you keep things tidily ordered, you’re just too lazy to go searching.) —German proverb

On the most fundamental level, a database needs to do two things: when you give it some data, it should store the data, and when you ask it again later, it should give the data back to you.

In Chapter 2 we discussed data models and query languages—i.e., the format in which you (the application developer) give the database your data, and the mecha‐ nism by which you can ask for it again later. In this chapter we discuss the same from the database’s point of view: how we can store the data that we’re given, and how we can find it again when we’re asked for it.

Why should you, as an application developer, care how the database handles storage and retrieval internally? You’re probably not going to implement your own storage engine from scratch, but you do need to select a storage engine that is appropriate for your application, from the many that are available. In order to tune a storage engine to perform well on your kind of workload, you need to have a rough idea of what the storage engine is doing under the hood.

In particular, there is a big difference between storage engines that are optimized for transactional workloads and those that are optimized for analytics. We will explore that distinction later in “Transaction Processing or Analytics?” on page 90, and in “Column-Oriented Storage” on page 95 we’ll discuss a family of storage engines that is optimized for analytics.

However, first we’ll start this chapter by talking about storage engines that are used in the kinds of databases that you’re probably familiar with: traditional relational data‐ bases, and also most so-called NoSQL databases. We will examine two families of

<!-- page 92 -->

storage engines: log-structured storage engines, and page-oriented storage engines such as B-trees.

## Data Structures That Power Your Database

Consider the world’s simplest database, implemented as two Bash functions:

#!/bin/bash db_set () { echo "$1,$2" >> database } db_get () { grep "^$1," database | sed -e "s/^$1,//" | tail -n 1 }

These two functions implement a key-value store. You can call db_set key value, which will store key and value in the database. The key and value can be (almost) anything you like—for example, the value could be a JSON document. You can then call db_get key, which looks up the most recent value associated with that particular key and returns it.

And it works:

$ db_set 123456 '{"name":"London","attractions":["Big Ben","London Eye"]}' $ db_set 42 '{"name":"San Francisco","attractions":["Golden Gate Bridge"]}' $ db_get 42 {"name":"San Francisco","attractions":["Golden Gate Bridge"]}

The underlying storage format is very simple: a text file where each line contains a key-value pair, separated by a comma (roughly like a CSV file, ignoring escaping issues). Every call to db_set appends to the end of the file, so if you update a key sev‐ eral times, the old versions of the value are not overwritten—you need to look at the last occurrence of a key in a file to find the latest value (hence the tail -n 1 in db_get):

$ db_set 42 '{"name":"San Francisco","attractions":["Exploratorium"]}' $ db_get 42 {"name":"San Francisco","attractions":["Exploratorium"]} $ cat database 123456,{"name":"London","attractions":["Big Ben","London Eye"]} 42,{"name":"San Francisco","attractions":["Golden Gate Bridge"]} 42,{"name":"San Francisco","attractions":["Exploratorium"]}

<!-- page 93 -->

