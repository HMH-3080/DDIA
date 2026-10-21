An algorithm for achieving serializable isolation that works by a transaction acquiring a lock on all data it reads or writes, and holding the lock until the end of the transaction. See “Two-Phase Lock‐ ing (2PL)” on page 257.

## unbounded

Not having any known upper limit or size.

The opposite of bounded.

<!-- page 581 -->

## A

aborts (transactions), 222, 224 in two-phase commit, 356 performance of optimistic concurrency con‐ trol, 266 retrying aborted transactions, 231 abstraction, 21, 27, 222, 266, 321 access path (in network model), 37, 60 accidental complexity, removing, 21 accountability, 535 ACID properties (transactions), 90, 223 atomicity, 223, 228 consistency, 224, 529 durability, 226 isolation, 225, 228 acknowledgements (messaging), 445 active/active replication (see multi-leader repli‐ cation) active/passive replication (see leader-based rep‐ lication) ActiveMQ (messaging), 137, 444 distributed transaction support, 361 ActiveRecord (object-relational mapper), 30, 232 actor model, 138 (see also message-passing) comparison to Pregel model, 425 comparison to stream processing, 468 Advanced Message Queuing Protocol (see AMQP) aerospace systems, 6, 10, 305, 372 aggregation data cubes and materialized views, 101 in batch processes, 406

in stream processes, 466 aggregation pipeline query language, 48 Agile, 22 minimizing irreversibility, 414, 497 moving faster with confidence, 532 Unix philosophy, 394 agreement, 365 (see also consensus) Airflow (workflow scheduler), 402 Ajax, 131 Akka (actor framework), 139 algorithms algorithm correctness, 308 B-trees, 79-83 for distributed systems, 306 hash indexes, 72-75 mergesort, 76, 402, 405 red-black trees, 78 SSTables and LSM-trees, 76-79 all-to-all replication topologies, 175 AllegroGraph (database), 50 ALTER TABLE statement (SQL), 40, 111 Amazon Dynamo (database), 177 Amazon Web Services (AWS), 8 Kinesis Streams (messaging), 448 network reliability, 279 postmortems, 9 RedShift (database), 93 S3 (object storage), 398 checking data integrity, 530 amplification of bias, 534 of failures, 364, 495

<!-- page 582 -->

<table>
<tr><th>of tail latency, 16, 207</th><th>Apache Storm (see Storm)</th></tr>
<tr><td>write amplification, 84</td><td>Apache Tajo (see Tajo)</td></tr>
<tr><td>AMQP (Advanced Message Queuing Protocol),</td><td>Apache Tez (see Tez)</td></tr>
<tr><td>444</td><td>Apache Thrift (see Thrift)</td></tr>
<tr><td>(see also messaging systems)</td><td>Apache ZooKeeper (see ZooKeeper)</td></tr>
<tr><td>comparison to log-based messaging, 448,</td><td>Apama (stream analytics), 466</td></tr>
<tr><td>451</td><td>append-only B-trees, 82, 242</td></tr>
<tr><td>message ordering, 446</td><td>append-only files (see logs)</td></tr>
<tr><td>analytics, 90</td><td>Application Programming Interfaces (APIs), 5,</td></tr>
<tr><td>comparison to transaction processing, 91</td><td>27</td></tr>
<tr><td>data warehousing (see data warehousing)</td><td>for batch processing, 403</td></tr>
<tr><td>parallel query execution in MPP databases,</td><td>for change streams, 456</td></tr>
<tr><td>415</td><td>for distributed transactions, 361</td></tr>
<tr><td>predictive (see predictive analytics)</td><td>for graph processing, 425</td></tr>
<tr><td>relation to batch processing, 411</td><td>for services, 131-136</td></tr>
<tr><td>schemas for, 93-95</td><td>(see also services)</td></tr>
<tr><td>snapshot isolation for queries, 238</td><td>evolvability, 136</td></tr>
<tr><td>stream analytics, 466</td><td>RESTful, 133</td></tr>
<tr><td>using MapReduce, analysis of user activity</td><td>SOAP, 133</td></tr>
<tr><td>events (example), 404</td><td>application state (see state)</td></tr>
<tr><td>anti-caching (in-memory databases), 89</td><td>approximate search (see similarity search)</td></tr>
<tr><td>anti-entropy, 178</td><td>archival storage, data from databases, 131</td></tr>
<tr><td>Apache ActiveMQ (see ActiveMQ)</td><td>arcs (see edges)</td></tr>
<tr><td>Apache Avro (see Avro)</td><td>arithmetic mean, 14</td></tr>
<tr><td>Apache Beam (see Beam)</td><td>ASCII text, 119, 395</td></tr>
<tr><td>Apache BookKeeper (see BookKeeper)</td><td>ASN.1 (schema language), 127</td></tr>
<tr><td>Apache Cassandra (see Cassandra)</td><td>asynchronous networks, 278, 553</td></tr>
<tr><td>Apache CouchDB (see CouchDB)</td><td>comparison to synchronous networks, 284</td></tr>
<tr><td>Apache Curator (see Curator)</td><td>formal model, 307</td></tr>
<tr><td>Apache Drill (see Drill)</td><td>asynchronous replication, 154, 553</td></tr>
<tr><td>Apache Flink (see Flink)</td><td>conflict detection, 172</td></tr>
<tr><td>Apache Giraph (see Giraph)</td><td>data loss on failover, 157</td></tr>
<tr><td>Apache Hadoop (see Hadoop)</td><td>reads from asynchronous follower, 162</td></tr>
<tr><td>Apache HAWQ (see HAWQ)</td><td>Asynchronous Transfer Mode (ATM), 285</td></tr>
<tr><td>Apache HBase (see HBase)</td><td>atomic broadcast (see total order broadcast)</td></tr>
<tr><td>Apache Helix (see Helix)</td><td>atomic clocks (caesium clocks), 294, 295</td></tr>
<tr><td>Apache Hive (see Hive)</td><td>(see also clocks)</td></tr>
<tr><td>Apache Impala (see Impala)</td><td>atomicity (concurrency), 553</td></tr>
<tr><td>Apache Jena (see Jena)</td><td>atomic increment-and-get, 351</td></tr>
<tr><td>Apache Kafka (see Kafka)</td><td>compare-and-set, 245, 327</td></tr>
<tr><td>Apache Lucene (see Lucene)</td><td>(see also compare-and-set operations)</td></tr>
<tr><td>Apache MADlib (see MADlib)</td><td>replicated operations, 246</td></tr>
<tr><td>Apache Mahout (see Mahout)</td><td>write operations, 243</td></tr>
<tr><td>Apache Oozie (see Oozie)</td><td>atomicity (transactions), 223, 228, 553</td></tr>
<tr><td>Apache Parquet (see Parquet)</td><td>atomic commit, 353</td></tr>
<tr><td>Apache Qpid (see Qpid)</td><td>avoiding, 523, 528</td></tr>
<tr><td>Apache Samza (see Samza)</td><td>blocking and nonblocking, 359</td></tr>
<tr><td>Apache Solr (see Solr)</td><td>in stream processing, 360, 477</td></tr>
<tr><td>Apache Spark (see Spark)</td><td>maintaining derived data, 453</td></tr>
</table>

<!-- page 583 -->

for multi-object transactions, 229 for single-object writes, 230 auditability, 528-533 designing for, 531 self-auditing systems, 530 through immutability, 460 tools for auditable data systems, 532 availability, 8 (see also fault tolerance) in CAP theorem, 337 in service level agreements (SLAs), 15 Avro (data format), 122-127 code generation, 127 dynamically generated schemas, 126 object container files, 125, 131, 414 reader determining writer’s schema, 125 schema evolution, 123 use in Hadoop, 414 awk (Unix tool), 391 AWS (see Amazon Web Services) Azure (see Microsoft)

B B-trees (indexes), 79-83 append-only/copy-on-write variants, 82, 242 branching factor, 81 comparison to LSM-trees, 83-85 crash recovery, 82 growing by splitting a page, 81 optimizations, 82 similarity to dynamic partitioning, 212 backpressure, 441, 553 in TCP, 282 backups database snapshot for replication, 156 integrity of, 530 snapshot isolation for, 238 use for ETL processes, 405 backward compatibility, 112 BASE, contrast to ACID, 223 bash shell (Unix), 70, 395, 503 batch processing, 28, 389-431, 553 combining with stream processing lambda architecture, 497 unifying technologies, 498 comparison to MPP databases, 414-418 comparison to stream processing, 464 comparison to Unix, 413-414

dataflow engines, 421-423 fault tolerance, 406, 414, 422, 442 for data integration, 494-498 graphs and iterative processing, 424-426 high-level APIs and languages, 403, 426-429 log-based messaging and, 451 maintaining derived state, 495 MapReduce and distributed filesystems, 397-413 (see also MapReduce) measuring performance, 13, 390 outputs, 411-413 key-value stores, 412 search indexes, 411 using Unix tools (example), 391-394 Bayou (database), 522 Beam (dataflow library), 498 bias, 534 big ball of mud, 20 Bigtable data model, 41, 99 binary data encodings, 115-128 Avro, 122-127 MessagePack, 116-117 Thrift and Protocol Buffers, 117-121 binary encoding based on schemas, 127 by network drivers, 128 binary strings, lack of support in JSON and XML, 114 BinaryProtocol encoding (Thrift), 118 Bitcask (storage engine), 72 crash recovery, 74 Bitcoin (cryptocurrency), 532 Byzantine fault tolerance, 305 concurrency bugs in exchanges, 233 bitmap indexes, 97 blockchains, 532 Byzantine fault tolerance, 305 blocking atomic commit, 359 Bloom (programming language), 504 Bloom filter (algorithm), 79, 466 BookKeeper (replicated log), 372 Bottled Water (change data capture), 455 bounded datasets, 430, 439, 553 (see also batch processing) bounded delays, 553 in networks, 285 process pauses, 298 broadcast hash joins, 409

<!-- page 584 -->

brokerless messaging, 442 Brubeck (metrics aggregator), 442 BTM (transaction coordinator), 356 bulk synchronous parallel (BSP) model, 425 bursty network traffic patterns, 285 business data processing, 28, 90, 390 byte sequence, encoding data in, 112 Byzantine faults, 304-306, 307, 553 Byzantine fault-tolerant systems, 305, 532 Byzantine Generals Problem, 304 consensus algorithms and, 366

## C

