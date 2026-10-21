The facilities for maintaining state as streams and replaying messages are also the basis for the techniques that enable stream joins and fault tolerance in various stream processing frameworks. We discussed several purposes of stream processing, includ‐ ing searching for event patterns (complex event processing), computing windowed aggregations (stream analytics), and keeping derived data systems up to date (materi‐ alized views).

We then discussed the difficulties of reasoning about time in a stream processor, including the distinction between processing time and event timestamps, and the problem of dealing with straggler events that arrive after you thought your window was complete.

We distinguished three types of joins that may appear in stream processes:

## Stream-stream joins

Both input streams consist of activity events, and the join operator searches for related events that occur within some window of time. For example, it may match two actions taken by the same user within 30 minutes of each other. The

<!-- page 503 -->

two join inputs may in fact be the same stream (a self-join) if you want to find related events within that one stream.

## Stream-table joins

One input stream consists of activity events, while the other is a database change‐ log. The changelog keeps a local copy of the database up to date. For each activity event, the join operator queries the database and outputs an enriched activity event.

## Table-table joins

Both input streams are database changelogs. In this case, every change on one side is joined with the latest state of the other side. The result is a stream of changes to the materialized view of the join between the two tables.

Finally, we discussed techniques for achieving fault tolerance and exactly-once semantics in a stream processor. As with batch processing, we need to discard the partial output of any failed tasks. However, since a stream process is long-running and produces output continuously, we can’t simply discard all output. Instead, a finer-grained recovery mechanism can be used, based on microbatching, checkpoint‐ ing, transactions, or idempotent writes.

## References

[1] Tyler Akidau, Robert Bradshaw, Craig Chambers, et al.: “The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing,” Proceedings of the VLDB Endowment, volume 8, number 12, pages 1792–1803, August 2015. doi:10.14778/2824032.2824076 [2] Harold Abelson, Gerald Jay Sussman, and Julie Sussman: Structure and Interpre‐ tation of Computer Programs, 2nd edition. MIT Press, 1996. ISBN: 978-0-262-51087-5, available online at mitpress.mit.edu

[3] Patrick Th. Eugster, Pascal A. Felber, Rachid Guerraoui, and Anne-Marie Ker‐ marrec: “The Many Faces of Publish/Subscribe,” ACM Computing Surveys, volume 35, number 2, pages 114–131, June 2003. doi:10.1145/857076.857078

[4] Joseph M. Hellerstein and Michael Stonebraker: Readings in Database Systems, 4th edition. MIT Press, 2005. ISBN: 978-0-262-69314-1, available online at red‐ book.cs.berkeley.edu

[5] Don Carney, Uğur Çetintemel, Mitch Cherniack, et al.: “Monitoring Streams – A New Class of Data Management Applications,” at 28th International Conference on Very Large Data Bases (VLDB), August 2002.

[6] Matthew Sackman: “Pushing Back,” lshift.net, May 5, 2016.

<!-- page 504 -->

[7] Vicent Martí: “Brubeck, a statsd-Compatible Metrics Aggregator,” githubengin‐ eering.com, June 15, 2015. [8] Seth Lowenberger: “MoldUDP64 Protocol Specification V 1.00,” nasdaq‐ trader.com, July 2009. [9] Pieter Hintjens: ZeroMQ – The Guide. O’Reilly Media, 2013. ISBN: 978-1-449-33404-8 [10] Ian Malpass: “Measure Anything, Measure Everything,” codeascraft.com, Febru‐ ary 15, 2011. [11] Dieter Plaetinck: “25 Graphite, Grafana and statsd Gotchas,” blog.raintank.io, March 3, 2016. [12] Jeff Lindsay: “Web Hooks to Revolutionize the Web,” progrium.com, May 3, 2007. [13] Jim N. Gray: “Queues Are Databases,” Microsoft Research Technical Report MSR-TR-95-56, December 1995. [14] Mark Hapner, Rich Burridge, Rahul Sharma, et al.: “JSR-343 Java Message Ser‐ vice (JMS) 2.0 Specification,” jms-spec.java.net, March 2013. [15] Sanjay Aiyagari, Matthew Arrott, Mark Atwell, et al.: “AMQP: Advanced Mes‐ sage Queuing Protocol Specification,” Version 0-9-1, November 2008. [16] “Google Cloud Pub/Sub: A Google-Scale Messaging Service,” cloud.google.com, 2016. [17] “Apache Kafka 0.9 Documentation,” kafka.apache.org, November 2015. [18] Jay Kreps, Neha Narkhede, and Jun Rao: “Kafka: A Distributed Messaging Sys‐ tem for Log Processing,” at 6th International Workshop on Networking Meets Data‐ bases (NetDB), June 2011. [19] “Amazon Kinesis Streams Developer Guide,” docs.aws.amazon.com, April 2016. [20] Leigh Stewart and Sijie Guo: “Building DistributedLog: Twitter’s High- Performance Replicated Log Service,” blog.twitter.com, September 16, 2015. [21] “DistributedLog Documentation,” Twitter, Inc., distributedlog.io, May 2016. [22] Jay Kreps: “Benchmarking Apache Kafka: 2 Million Writes Per Second (On Three Cheap Machines),” engineering.linkedin.com, April 27, 2014. [23] Kartik Paramasivam: “How We’re Improving and Advancing Kafka at LinkedIn,” engineering.linkedin.com, September 2, 2015. [24] Jay Kreps: “The Log: What Every Software Engineer Should Know About Real- Time Data’s Unifying Abstraction,” engineering.linkedin.com, December 16, 2013.

<!-- page 505 -->

[25] Shirshanka Das, Chavdar Botev, Kapil Surlaker, et al.: “All Aboard the Data‐ bus!,” at 3rd ACM Symposium on Cloud Computing (SoCC), October 2012. [26] Yogeshwer Sharma, Philippe Ajoux, Petchean Ang, et al.: “Wormhole: Reliable Pub-Sub to Support Geo-Replicated Internet Services,” at 12th USENIX Symposium on Networked Systems Design and Implementation (NSDI), May 2015. [27] P. P. S. Narayan: “Sherpa Update,” developer.yahoo.com, June 8, . [28] Martin Kleppmann: “Bottled Water: Real-Time Integration of PostgreSQL and Kafka,” martin.kleppmann.com, April 23, 2015. [29] Ben Osheroff: “Introducing Maxwell, a mysql-to-kafka Binlog Processor,” devel‐ oper.zendesk.com, August 20, 2015. [30] Randall Hauch: “Debezium 0.2.1 Released,” debezium.io, June 10, 2016. [31] Prem Santosh Udaya Shankar: “Streaming MySQL Tables in Real-Time to Kafka,” engineeringblog.yelp.com, August 1, 2016. [32] “Mongoriver,” Stripe, Inc., github.com, September 2014. [33] Dan Harvey: “Change Data Capture with Mongo + Kafka,” at Hadoop Users Group UK, August 2015. [34] “Oracle GoldenGate 12c: Real-Time Access to Real-Time Information,” Oracle White Paper, March 2015. [35] “Oracle GoldenGate Fundamentals: How Oracle GoldenGate Works,” Oracle Corporation, youtube.com, November 2012. [36] Slava Akhmechet: “Advancing the Realtime Web,” rethinkdb.com, January 27, 2015. [37] “Firebase Realtime Database Documentation,” Google, Inc., firebase.google.com, May 2016. [38] “Apache CouchDB 1.6 Documentation,” docs.couchdb.org, 2014. [39] Matt DeBergalis: “Meteor 0.7.0: Scalable Database Queries Using MongoDB Oplog Instead of Poll-and-Diff,” info.meteor.com, December 17, 2013. [40] “Chapter 15. Importing and Exporting Live Data,” VoltDB 6.4 User Manual, docs.voltdb.com, June 2016. [41] Neha Narkhede: “Announcing Kafka Connect: Building Large-Scale Low- Latency Data Pipelines,” confluent.io, February 18, 2016. [42] Greg Young: “CQRS and Event Sourcing,” at Code on the Beach, August 2014. [43] Martin Fowler: “Event Sourcing,” martinfowler.com, December 12, 2005.

<!-- page 506 -->

[44] Vaughn Vernon: Implementing Domain-Driven Design. Addison-Wesley Profes‐ sional, 2013. ISBN: 978-0-321-83457-7

