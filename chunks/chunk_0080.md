[1] David J. DeWitt and Jim N. Gray: “Parallel Database Systems: The Future of High Performance Database Systems,” Communications of the ACM, volume 35, number 6, pages 85–98, June 1992. doi:10.1145/129888.129894 [2] Lars George: “HBase vs. BigTable Comparison,” larsgeorge.com, November 2009. [3] “The Apache HBase Reference Guide,” Apache Software Foundation, hbase.apache.org, 2014. [4] MongoDB, Inc.: “New Hash-Based Sharding Feature in MongoDB 2.4,” blog.mon‐ godb.org, April 10, 2013. [5] Ikai Lan: “App Engine Datastore Tip: Monotonically Increasing Values Are Bad,” ikaisays.com, January 25, 2011. [6] Martin Kleppmann: “Java’s hashCode Is Not Safe for Distributed Systems,” mar‐ tin.kleppmann.com, June 18, 2012. [7] David Karger, Eric Lehman, Tom Leighton, et al.: “Consistent Hashing and Ran‐ dom Trees: Distributed Caching Protocols for Relieving Hot Spots on the World Wide Web,” at 29th Annual ACM Symposium on Theory of Computing (STOC), pages 654–663, 1997. doi:10.1145/258533.258660 [8] John Lamping and Eric Veach: “A Fast, Minimal Memory, Consistent Hash Algo‐ rithm,” arxiv.org, June 2014. [9] Eric Redmond: “A Little Riak Book,” Version 1.4.0, Basho Technologies, Septem‐ ber 2013. [10] “Couchbase 2.5 Administrator Guide,” Couchbase, Inc., 2014. [11] Avinash Lakshman and Prashant Malik: “Cassandra – A Decentralized Struc‐ tured Storage System,” at 3rd ACM SIGOPS International Workshop on Large Scale Distributed Systems and Middleware (LADIS), October 2009. [12] Jonathan Ellis: “Facebook’s Cassandra Paper, Annotated and Compared to Apache Cassandra 2.0,” datastax.com, September 12, 2013. [13] “Introduction to Cassandra Query Language,” DataStax, Inc., 2014. [14] Samuel Axon: “3% of Twitter’s Servers Dedicated to Justin Bieber,” masha‐ ble.com, September 7, 2010. [15] “Riak 1.4.8 Docs,” Basho Technologies, Inc., 2014.

<!-- page 241 -->

[16] Richard Low: “The Sweet Spot for Cassandra Secondary Indexing,” wentnet.com, October 21, 2013. [17] Zachary Tong: “Customizing Your Document Routing,” elasticsearch.org, June 3, 2013. [18] “Apache Solr Reference Guide,” Apache Software Foundation, 2014. [19] Andrew Pavlo: “H-Store Frequently Asked Questions,” hstore.cs.brown.edu, October 2013. [20] “Amazon DynamoDB Developer Guide,” Amazon Web Services, Inc., 2014. [21] Rusty Klophaus: “Difference Between 2I and Search,” email to riak-users mailing list, lists.basho.com, October 25, 2011. [22] Donald K. Burleson: “Object Partitioning in Oracle,” dba-oracle.com, November 8, 2000. [23] Eric Evans: “Rethinking Topology in Cassandra,” at ApacheCon Europe, Novem‐ ber 2012. [24] Rafał Kuć: “Reroute API Explained,” elasticsearchserverbook.com, September 30, 2013. [25] “Project Voldemort Documentation,” project-voldemort.com. [26] Enis Soztutar: “Apache HBase Region Splitting and Merging,” hortonworks.com, February 1, 2013. [27] Brandon Williams: “Virtual Nodes in Cassandra 1.2,” datastax.com, December 4, 2012. [28] Richard Jones: “libketama: Consistent Hashing Library for Memcached Clients,” metabrew.com, April 10, 2007. [29] Branimir Lambov: “New Token Allocation Algorithm in Cassandra 3.0,” data‐ stax.com, January 28, 2016. [30] Jason Wilder: “Open-Source Service Discovery,” jasonwilder.com, February 2014. [31] Kishore Gopalakrishna, Shi Lu, Zhen Zhang, et al.: “Untangling Cluster Manage‐ ment with Helix,” at ACM Symposium on Cloud Computing (SoCC), October 2012. doi:10.1145/2391229.2391248 [32] “Moxi 1.8 Manual,” Couchbase, Inc., 2014. [33] Shivnath Babu and Herodotos Herodotou: “Massively Parallel Databases and MapReduce Systems,” Foundations and Trends in Databases, volume 5, number 1, pages 1–104, November 2013. doi:10.1561/1900000036

<!-- page 242 -->

<table>
<tr><th>HANTOMS</th><th>Actual serial execution •</th></tr>
<tr><td>Two-phase</td><td></td></tr>
<tr><td>lock king</td><td></td></tr>
<tr><td></td><td></td></tr>
</table>

<table>
<tr><th>ërializable</th><th></th></tr>
<tr><td>No  snapshot</td><td>Write’Skew</td></tr>
<tr><td>solation</td><td>.</td></tr>
<tr><td>1 5'o L A T 1 0 N</td><td></td></tr>
<tr><td></td><td></td></tr>
</table>

<table>
<tr><th></th><th>MVCC</th><th></th><th></th></tr>
<tr><td></td><td>7</td><td></td><td></td></tr>
<tr><td>•</td><td>No Read'Skew</td><td>N</td><td>Lost Updates</td></tr>
<tr><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td>Row-level /</td><td></td><td></td></tr>
<tr><td></td><td>locking @</td><td></td><td></td></tr>
<tr><td></td><td>No</td><td></td><td></td></tr>
<tr><td></td><td>Dirty</td><td></td><td></td></tr>
<tr><td></td><td>TES</td><td></td><td></td></tr>
<tr><td>irty Reads</td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td>-</td></tr>
<tr><td></td><td></td><td colspan="2">Muiti-Object Atomicity</td></tr>
<tr><td></td><td></td><td></td><td>- - …</td></tr>
<tr><td></td><td></td><td></td><td></td></tr>
<tr><td></td><td></td><td></td><td>To Distributed</td></tr>
<tr><td></td><td></td><td></td><td>Transactions</td></tr>
<tr><td></td><td></td><td></td><td>– (Chapter 9)</td></tr>
</table>

<!-- page 243 -->

## CHAPTER 7 Transactions

Some authors have claimed that general two-phase commit is too expensive to support, because of the performance or availability problems that it brings. We believe it is better to have application programmers deal with performance problems due to overuse of transac‐ tions as bottlenecks arise, rather than always coding around the lack of transactions.

—James Corbett et al., Spanner: Google’s Globally-Distributed Database (2012)

In the harsh reality of data systems, many things can go wrong:

• The database software or hardware may fail at any time (including in the middle of a write operation).
• The application may crash at any time (including halfway through a series of operations).
• Interruptions in the network can unexpectedly cut off the application from the database, or one database node from another.
• Several clients may write to the database at the same time, overwriting each other’s changes.
• A client may read data that doesn’t make sense because it has only partially been updated.
• Race conditions between clients can cause surprising bugs.

In order to be reliable, a system has to deal with these faults and ensure that they don’t cause catastrophic failure of the entire system. However, implementing faulttolerance mechanisms is a lot of work. It requires a lot of careful thinking about all the things that can go wrong, and a lot of testing to ensure that the solution actually works.

<!-- page 244 -->

For decades, transactions have been the mechanism of choice for simplifying these issues. A transaction is a way for an application to group several reads and writes together into a logical unit. Conceptually, all the reads and writes in a transaction are executed as one operation: either the entire transaction succeeds (commit) or it fails (abort, rollback). If it fails, the application can safely retry. With transactions, error handling becomes much simpler for an application, because it doesn’t need to worry about partial failure—i.e., the case where some operations succeed and some fail (for whatever reason).

If you have spent years working with transactions, they may seem obvious, but we shouldn’t take them for granted. Transactions are not a law of nature; they were cre‐ ated with a purpose, namely to simplify the programming model for applications accessing a database. By using transactions, the application is free to ignore certain potential error scenarios and concurrency issues, because the database takes care of them instead (we call these safety guarantees).

Not every application needs transactions, and sometimes there are advantages to weakening transactional guarantees or abandoning them entirely (for example, to achieve higher performance or higher availability). Some safety properties can be achieved without transactions.

How do you figure out whether you need transactions? In order to answer that ques‐ tion, we first need to understand exactly what safety guarantees transactions can pro‐ vide, and what costs are associated with them. Although transactions seem straightforward at first glance, there are actually many subtle but important details that come into play.

